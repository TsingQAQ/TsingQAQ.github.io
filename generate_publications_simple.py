#!/usr/bin/env python3
"""
Enhanced publication script with:
- scholarly library for reliable Google Scholar scraping
- Automatic arXiv/DOI URL extraction from publication metadata
- Abstract extraction using scholarly library (anti-blocking)
- Hierarchical TL;DR generation via Gemini API:
  1. Full PDF text (arXiv, OpenReview, etc.) → Best quality TL;DR
  2. Abstract from Google Scholar → Good quality TL;DR
  3. Empty if neither available
- PDF extraction from open access sources (arXiv, OpenReview, JMLR, etc.)
- Safety validations to prevent data loss (minimum 15 publications)
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import os
import sys
import io

# Try to import required libraries
try:
    from scholarly import scholarly
    SCHOLARLY_AVAILABLE = True
except ImportError:
    SCHOLARLY_AVAILABLE = False
    print("WARNING: scholarly library not installed. Abstract fetching will be limited.")
    print("         Install with: pip install scholarly")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("INFO: google-generativeai not installed. TL;DR generation disabled.")
    print("      Install with: pip install google-generativeai")

try:
    import PyPDF2
    PDF_EXTRACTION_AVAILABLE = True
except ImportError:
    PDF_EXTRACTION_AVAILABLE = False
    print("INFO: PyPDF2 not installed. Full paper PDF extraction disabled.")
    print("      Install with: pip install PyPDF2")

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def fetch_abstract_from_arxiv(arxiv_id):
    """Fetch abstract from arXiv API given an arXiv ID"""
    try:
        # arXiv API endpoint
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        # Parse XML response
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)

        # Find abstract in the response
        # arXiv API returns Atom XML format
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', namespace)
        if entry is not None:
            summary = entry.find('atom:summary', namespace)
            if summary is not None and summary.text:
                abstract = clean_text(summary.text)
                safe_print(f"  [OK] Fetched abstract from arXiv API ({len(abstract)} chars)")
                return abstract

        return ""
    except Exception as e:
        print(f"  Warning: Could not fetch from arXiv API: {e}")
        return ""

def extract_paper_url_from_publication_info(pub_info, title):
    """Extract direct paper URL from publication info (arXiv ID, DOI, etc.)"""
    if not pub_info:
        return ""

    # Check for arXiv ID
    arxiv_match = re.search(r'arXiv[:\s]+(\d+\.\d+)', pub_info, re.IGNORECASE)
    if arxiv_match:
        arxiv_id = arxiv_match.group(1)
        return f"https://arxiv.org/abs/{arxiv_id}"

    # Check for proceedings.mlr.press
    if 'proceedings.mlr.press' in pub_info.lower() or 'pmlr' in pub_info.lower():
        # Try to find volume and paper ID
        mlr_match = re.search(r'v(\d+)[^\d]*(\d+)', pub_info)
        if mlr_match:
            volume = mlr_match.group(1)
            # Create likely URL pattern
            return f"https://proceedings.mlr.press/v{volume}/"

    # Check for DOI
    doi_match = re.search(r'10\.\d{4,}/[^\s,]+', pub_info)
    if doi_match:
        doi = doi_match.group(0)
        return f"https://doi.org/{doi}"

    return ""

def safe_print(text):
    """Safely print text, replacing problematic Unicode characters for Windows console"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace special characters with ASCII equivalents
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

def extract_pdf_text(url, max_pages=10):
    """Extract text from PDF URL (works for arXiv, OpenReview, and other open access papers)"""
    if not PDF_EXTRACTION_AVAILABLE:
        return None

    try:
        print(f"  Downloading PDF from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Create PDF reader from bytes
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        pages_to_read = min(len(pdf_reader.pages), max_pages)

        for i in range(pages_to_read):
            page = pdf_reader.pages[i]
            text += page.extract_text() + "\n"

        # Clean up the text
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)

        print(f"  Extracted {len(text)} characters from PDF")
        return text[:15000]  # Limit to ~15k chars for Gemini API

    except Exception as e:
        print(f"  Warning: Could not extract PDF text: {e}")
        return None

def get_full_text_if_available(url, title):
    """Try to get full text from paper URL, prioritizing arXiv, OpenReview, and open access sources"""
    if not url:
        return None, False

    # Check if it's arXiv
    if 'arxiv.org' in url:
        # Convert to PDF URL if needed
        if '/abs/' in url:
            pdf_url = url.replace('/abs/', '/pdf/') + '.pdf'
        elif url.endswith('.pdf'):
            pdf_url = url
        else:
            pdf_url = url + '.pdf'

        text = extract_pdf_text(pdf_url)
        if text:
            return text, True

    # Check if it's OpenReview (https://openreview.net/forum?id=FFnRLvWefK)
    if 'openreview.net' in url:
        # OpenReview URLs: https://openreview.net/forum?id=XXX or /pdf?id=XXX
        if '/forum?id=' in url:
            paper_id = url.split('id=')[-1]
            pdf_url = f"https://openreview.net/pdf?id={paper_id}"
        elif '/pdf?id=' in url:
            pdf_url = url
        else:
            pdf_url = url  # Try as-is

        text = extract_pdf_text(pdf_url)
        if text:
            return text, True

    # Check other open access sources
    open_access_domains = [
        'proceedings.mlr.press',
        'jmlr.org',
        'biorxiv.org',
        'medrxiv.org'
    ]

    for domain in open_access_domains:
        if domain in url:
            if url.endswith('.pdf'):
                text = extract_pdf_text(url)
                if text:
                    return text, True
            # Try adding .pdf
            try:
                text = extract_pdf_text(url + '.pdf')
                if text:
                    return text, True
            except:
                continue

    return None, False

def generate_tldr_with_gemini(title, text, gemini_model=None, is_full_paper=False):
    """Generate TL;DR using Gemini API"""
    if not gemini_model or not text:
        return ""

    try:
        if is_full_paper:
            prompt = f"""Please create a concise TL;DR (strictly less than 100 words, ideally 50-80 words) for this research paper.
Focus on the main contribution, method, and key findings. Be specific and technical.
Keep it brief and to the point.

Title: {title}

Paper content (first ~15k characters): {text}

TL;DR:"""
        else:
            prompt = f"""Please create a concise TL;DR (strictly less than 100 words, ideally 50-80 words) for this research paper.
Focus on the main contribution and key findings. Be specific and technical.
Keep it brief and to the point.

Title: {title}

Abstract: {text}

TL;DR:"""

        response = gemini_model.generate_content(prompt)
        tldr = response.text.strip()

        # Remove common prefixes if Gemini adds them
        tldr = re.sub(r'^(TL;?DR:?\s*|Summary:?\s*)', '', tldr, flags=re.IGNORECASE)

        return tldr

    except Exception as e:
        print(f"  Warning: Gemini TL;DR generation failed: {e}")
        return ""

def fetch_abstract_and_url(title_link_href, headers):
    """Fetch abstract and paper URL from Google Scholar detail page"""
    pub_url = ""
    abstract = ""

    if not title_link_href:
        return pub_url, abstract

    try:
        detail_url = f"https://scholar.google.com{title_link_href}"
        time.sleep(3)  # Be polite to Google
        detail_response = requests.get(detail_url, headers=headers, timeout=30)
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

        # Extract URL to actual paper
        url_links = detail_soup.find_all('a', href=True)
        for link in url_links:
            href = link.get('href', '')
            if any(domain in href for domain in ['arxiv.org', 'sciencedirect.com', 'springer.com',
                                               'ieee.org', 'acm.org', 'proceedings.mlr.press',
                                               'arc.aiaa.org', 'nature.com', 'science.org']):
                pub_url = href
                break

        # Extract abstract if available
        abstract_div = detail_soup.find('div', class_='gsh_small')
        if abstract_div:
            abstract = clean_text(abstract_div.text)

    except Exception as e:
        print(f"  Warning: Could not fetch details: {e}")

    return pub_url, abstract

def extract_publications_scholarly(scholar_id="mE9l0sQAAAAJ", gemini_model=None):
    """Extract publications using scholarly library (anti-blocking) with optional TL;DR generation"""
    if not SCHOLARLY_AVAILABLE:
        print("scholarly library not available, skipping")
        return None

    publications = []

    try:
        print("Fetching publications via scholarly library...")

        # Search for author by ID
        author = scholarly.search_author_id(scholar_id)
        author_filled = scholarly.fill(author, sections=['basics', 'publications'])

        pubs = author_filled.get('publications', [])
        print(f"Found {len(pubs)} publications via scholarly")

        if gemini_model:
            print("TL;DR generation enabled via Gemini API")

        for idx, pub in enumerate(pubs, 1):
            try:
                # Fill publication details (includes abstract!)
                print(f"  [{idx}/{len(pubs)}] Fetching details for: {pub.get('bib', {}).get('title', 'Unknown')}")
                pub_filled = scholarly.fill(pub)
                bib = pub_filled.get('bib', {})

                title = bib.get('title', '')
                authors = bib.get('author', '')
                year = bib.get('pub_year', None)
                if year:
                    try:
                        year = int(year)
                    except:
                        year = None

                # Get venue info
                venue = bib.get('venue', '')
                if not venue and bib.get('journal'):
                    venue = bib.get('journal')
                elif not venue and bib.get('conference'):
                    venue = bib.get('conference')

                # Get abstract and URL
                abstract = bib.get('abstract', '')
                pub_url = pub_filled.get('pub_url', '') or pub_filled.get('eprint_url', '')

                # Try to get arXiv abstract if scholarly didn't get one
                if not abstract:
                    arxiv_match = re.search(r'arXiv[:\s]+(\d+\.\d+)', venue, re.IGNORECASE)
                    if arxiv_match:
                        arxiv_id = arxiv_match.group(1)
                        time.sleep(0.3)
                        abstract = fetch_abstract_from_arxiv(arxiv_id)
                        if not pub_url:
                            pub_url = f"https://arxiv.org/abs/{arxiv_id}"

                # If still no URL, try to extract from publication info
                if not pub_url:
                    pub_url = extract_paper_url_from_publication_info(venue, title)

                # Get citations
                citations = pub_filled.get('num_citations', 0)

                # Hierarchical TL;DR generation: 1) Full PDF, 2) Abstract, 3) Empty
                tldr = ""
                tldr_source = ""
                if gemini_model:
                    # Try to get full PDF text first
                    full_text, is_full_paper = get_full_text_if_available(pub_url, title)
                    if full_text:
                        print(f"  [{idx}/{len(pubs)}] Generating TL;DR from full paper PDF")
                        tldr = generate_tldr_with_gemini(title, full_text, gemini_model, is_full_paper=True)
                        tldr_source = "full_paper"
                        time.sleep(0.5)
                    elif abstract:
                        print(f"  [{idx}/{len(pubs)}] Generating TL;DR from abstract")
                        tldr = generate_tldr_with_gemini(title, abstract, gemini_model, is_full_paper=False)
                        tldr_source = "abstract"
                        time.sleep(0.5)

                has_abstract = 'Yes' if abstract else 'No'
                has_url = 'Yes' if pub_url else 'No'
                has_tldr = 'Yes' if tldr else 'No'
                source_info = f" (from {tldr_source})" if tldr_source else ""
                safe_print(f"[{idx}/{len(pubs)}] {title} ({year}) - Abstract: {has_abstract}, URL: {has_url}, TL;DR: {has_tldr}{source_info}")

                # Create publication object
                pub_id = re.sub(r'[^a-z0-9_]', '_', title.lower().replace(' ', '_'))[:50]
                if year:
                    pub_id += f"_{year}"

                publication = {
                    "id": pub_id,
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "venue": venue,
                    "tldr": tldr,
                    "abstract": abstract,
                    "url": pub_url,
                    "citations": citations,
                    "filled_manually": False,
                    "media": None,
                    "custom_description": None,
                    "links": [],
                    "tags": [],
                    "featured": False
                }

                publications.append(publication)

                # Rate limiting to be polite (reduced when not generating TL;DRs)
                if gemini_model:
                    time.sleep(1)  # Shorter delay since Gemini calls have delays
                else:
                    time.sleep(0.5)  # Very short delay when just fetching abstracts

            except Exception as e:
                print(f"  Error processing publication: {e}")
                continue

        # Don't sort here - we'll preserve Google Scholar's order
        # (will be sorted by pubdate in the main function)
        print(f"Fetched {len(publications)} publications")

        return publications

    except Exception as e:
        print(f"Error fetching from scholarly: {e}")
        return None

def extract_publications_serpapi(scholar_id="mE9l0sQAAAAJ", api_key=None, gemini_model=None):
    """Extract publications using SerpAPI with optional TL;DR generation"""
    if not api_key:
        print("No SerpAPI key provided, skipping SerpAPI method")
        return None

    publications = []

    try:
        print("Fetching publications via SerpAPI...")
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_scholar_author",
            "author_id": scholar_id,
            "api_key": api_key,
            "num": 100,
            "sort": "pubdate"  # Sort by publication date, not citations
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        print(f"Found {len(articles)} publications via SerpAPI")

        if gemini_model:
            print("TL;DR generation enabled via Gemini API")

        # Set up headers for detail fetching
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        for idx, article in enumerate(articles, 1):
            # Extract year from publication info (use LAST occurrence to avoid page ranges)
            year = None
            pub_info = article.get("publication", "")
            year_matches = re.findall(r'\b(?:19|20)\d{2}\b', pub_info)
            if year_matches:
                # Use the last year found (publication year is typically at the end)
                year = int(year_matches[-1])

            title = article.get("title", "")

            # Try to extract arXiv ID from publication info for abstract fetching
            abstract = ""
            arxiv_match = re.search(r'arXiv[:\s]+(\d+\.\d+)', pub_info, re.IGNORECASE)
            if arxiv_match:
                arxiv_id = arxiv_match.group(1)
                # Fetch abstract from arXiv API (reliable!)
                time.sleep(0.3)  # Be polite to arXiv
                abstract = fetch_abstract_from_arxiv(arxiv_id)

            # Extract direct paper URL from publication info (arXiv, DOI, etc.)
            pub_url = extract_paper_url_from_publication_info(pub_info, title)

            # Hierarchical TL;DR generation: 1) Full PDF, 2) Abstract, 3) Empty
            tldr = ""
            tldr_source = ""
            if gemini_model:
                # Try to get full PDF text first
                full_text, is_full_paper = get_full_text_if_available(pub_url, title)
                if full_text:
                    print(f"  [{idx}/{len(articles)}] Generating TL;DR from full paper PDF")
                    tldr = generate_tldr_with_gemini(title, full_text, gemini_model, is_full_paper=True)
                    tldr_source = "full_paper"
                    time.sleep(0.5)
                elif abstract:
                    print(f"  [{idx}/{len(articles)}] Generating TL;DR from abstract")
                    tldr = generate_tldr_with_gemini(title, abstract, gemini_model, is_full_paper=False)
                    tldr_source = "abstract"
                    time.sleep(0.5)

            has_abstract = 'Yes' if abstract else 'No'
            has_url = 'Yes' if pub_url else 'No'
            has_tldr = 'Yes' if tldr else 'No'
            source_info = f" (from {tldr_source})" if tldr_source else ""
            safe_print(f"[{idx}/{len(articles)}] {title} ({year}) - Abstract: {has_abstract}, URL: {has_url}, TL;DR: {has_tldr}{source_info}")

            # Create publication object
            pub_id = re.sub(r'[^a-z0-9_]', '_', title.lower().replace(' ', '_'))[:50]
            if year:
                pub_id += f"_{year}"

            publication = {
                "id": pub_id,
                "title": title,
                "authors": article.get("authors", ""),
                "year": year,
                "venue": pub_info,
                "tldr": tldr,
                "abstract": abstract,
                "url": pub_url,
                "citations": article.get("cited_by", {}).get("value", 0),
                "filled_manually": False,
                "media": None,
                "custom_description": None,
                "links": [],
                "tags": [],
                "featured": False
            }

            publications.append(publication)

        return publications

    except Exception as e:
        print(f"Error fetching from SerpAPI: {e}")
        return None

def extract_publications_simple(scholar_id="mE9l0sQAAAAJ", fetch_details=True, gemini_model=None):
    """Extract publications from Google Scholar with optional TL;DR generation"""
    publications = []
    base_url = "https://scholar.google.com/citations"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = f"{base_url}?user={scholar_id}&cstart=0&pagesize=100&sortby=pubdate"
    print(f"Fetching: {url}")

    if gemini_model:
        print("TL;DR generation enabled via Gemini API")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        pub_rows = soup.find_all('tr', class_='gsc_a_tr')
        print(f"Found {len(pub_rows)} publications")

        if len(pub_rows) == 0:
            print("WARNING: No publications found - possible blocking or rate limiting")
            return None

        for idx, row in enumerate(pub_rows, 1):
            try:
                # Extract title
                title_cell = row.find('td', class_='gsc_a_t')
                if not title_cell:
                    continue

                title_link = title_cell.find('a')
                if not title_link:
                    continue

                title = clean_text(title_link.text)

                # Extract venue information
                author_divs = title_cell.find_all('div', class_='gs_gray')
                authors = ""
                venue = ""
                if len(author_divs) > 0:
                    authors = clean_text(author_divs[0].text)
                if len(author_divs) > 1:
                    venue = clean_text(author_divs[1].text)

                # Extract year
                year_cell = row.find('td', class_='gsc_a_y')
                year = None
                if year_cell and year_cell.text.strip():
                    try:
                        year = int(year_cell.text.strip())
                    except ValueError:
                        year = None

                # Extract citations
                cite_cell = row.find('td', class_='gsc_a_c')
                citations = 0
                if cite_cell:
                    cite_link = cite_cell.find('a')
                    if cite_link and cite_link.text.strip():
                        try:
                            citations = int(cite_link.text.strip())
                        except ValueError:
                            citations = 0

                # Get publication URL and abstract
                pub_url = ""
                abstract = ""

                if fetch_details:
                    # Try to extract arXiv ID from venue info
                    arxiv_match = re.search(r'arXiv[:\s]+(\d+\.\d+)', venue, re.IGNORECASE)
                    if arxiv_match:
                        arxiv_id = arxiv_match.group(1)
                        pub_url = f"https://arxiv.org/abs/{arxiv_id}"
                        # Fetch abstract from arXiv API (reliable!)
                        time.sleep(0.3)  # Be polite to arXiv
                        abstract = fetch_abstract_from_arxiv(arxiv_id)

                    # If no arXiv abstract, try extracting URL from publication info
                    if not pub_url:
                        pub_url = extract_paper_url_from_publication_info(venue, title)

                # Hierarchical TL;DR generation: 1) Full PDF, 2) Abstract, 3) Empty
                tldr = ""
                tldr_source = ""
                if gemini_model:
                    # Try to get full PDF text first
                    full_text, is_full_paper = get_full_text_if_available(pub_url, title)
                    if full_text:
                        print(f"  [{idx}/{len(pub_rows)}] Generating TL;DR from full paper PDF")
                        tldr = generate_tldr_with_gemini(title, full_text, gemini_model, is_full_paper=True)
                        tldr_source = "full_paper"
                        time.sleep(0.5)
                    elif abstract:
                        print(f"  [{idx}/{len(pub_rows)}] Generating TL;DR from abstract")
                        tldr = generate_tldr_with_gemini(title, abstract, gemini_model, is_full_paper=False)
                        tldr_source = "abstract"
                        time.sleep(0.5)

                has_abstract = 'Yes' if abstract else 'No'
                has_url = 'Yes' if pub_url else 'No'
                has_tldr = 'Yes' if tldr else 'No'
                source_info = f" (from {tldr_source})" if tldr_source else ""
                safe_print(f"[{idx}/{len(pub_rows)}] {title} ({year}) - Abstract: {has_abstract}, URL: {has_url}, TL;DR: {has_tldr}{source_info}")

                # Create publication object
                pub_id = re.sub(r'[^a-z0-9_]', '_', title.lower().replace(' ', '_'))[:50]
                if year:
                    pub_id += f"_{year}"

                publication = {
                    "id": pub_id,
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "venue": venue,
                    "tldr": tldr,
                    "abstract": abstract,
                    "url": pub_url,
                    "citations": citations,
                    "filled_manually": False,
                    "media": None,
                    "custom_description": None,
                    "links": [],
                    "tags": [],
                    "featured": False
                }

                publications.append(publication)

            except Exception as e:
                print(f"Error processing publication: {e}")
                continue

    except Exception as e:
        print(f"Error fetching publications: {e}")
        return None

    return publications if len(publications) > 0 else None

def generate_simple_publications():
    """Generate basic publications.json with safety checks"""
    print("Extracting basic publications from Google Scholar...")

    # Minimum threshold to prevent data loss
    MIN_PUBLICATIONS = 15

    # Check for existing publications.json for validation
    existing_count = 0
    if os.path.exists("publications.json"):
        try:
            with open("publications.json", 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_count = existing_data.get("total_publications", 0)
                print(f"Existing publications.json has {existing_count} publications")
        except Exception as e:
            print(f"Warning: Could not read existing publications.json: {e}")

    # Initialize Gemini API if available
    gemini_model = None
    gemini_key = os.environ.get("GEMINI_API_KEY")

    if gemini_key and GEMINI_AVAILABLE:
        try:
            genai.configure(api_key=gemini_key)
            gemini_model = genai.GenerativeModel('gemini-2.5-flash')
            print("Gemini API initialized for TL;DR generation")
        except Exception as e:
            print(f"Warning: Could not initialize Gemini API: {e}")
    elif gemini_key and not GEMINI_AVAILABLE:
        print("Warning: GEMINI_API_KEY set but google-generativeai not installed")
    else:
        print("No GEMINI_API_KEY found - skipping TL;DR generation")

    # Load manual URLs
    manual_urls = {}
    if os.path.exists("manual_urls.json"):
        try:
            with open("manual_urls.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                manual_urls = data.get("manual_urls", {})
                print(f"Loaded {len(manual_urls)} manual URLs")
        except Exception as e:
            print(f"Warning: Could not read manual_urls.json: {e}")

    # Load manual abstracts
    manual_abstracts = {}
    if os.path.exists("manual_abstracts.json"):
        try:
            with open("manual_abstracts.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                manual_abstracts = data.get("manual_abstracts", {})
                print(f"Loaded {len(manual_abstracts)} manual abstracts")
        except Exception as e:
            print(f"Warning: Could not read manual_abstracts.json: {e}")

    # Strategy: SerpAPI only (scholarly gets blocked by Google Scholar)
    # Abstracts come from: arXiv API + manual URLs (OpenReview, etc.)
    publications = None
    serpapi_key = os.environ.get("SERPAPI_KEY")

    if serpapi_key:
        print("Fetching publications from SerpAPI (correct order with sortby=pubdate)...")
        publications = extract_publications_serpapi(api_key=serpapi_key, gemini_model=gemini_model)

        # Apply manual URLs to get more abstracts/PDFs from OpenReview, etc.
        if publications and manual_urls:
            print("\nApplying manual URLs...")
            for pub in publications:
                if pub['title'] in manual_urls:
                    old_url = pub.get('url', '')
                    pub['url'] = manual_urls[pub['title']]
                    print(f"Applied manual URL for: {pub['title']}")

                    # Try to fetch abstract/PDF from the manual URL if we don't have it
                    if not pub.get('abstract') and gemini_model:
                        full_text, is_full_paper = get_full_text_if_available(pub['url'], pub['title'])
                        if full_text and not pub.get('tldr'):
                            # Re-generate TL;DR with the PDF from manual URL
                            print(f"  Re-generating TL;DR with PDF from manual URL...")
                            tldr = generate_tldr_with_gemini(pub['title'], full_text, gemini_model, is_full_paper=True)
                            pub['tldr'] = tldr
                            time.sleep(0.5)

        # Apply manual abstracts and generate TL;DRs
        if publications and manual_abstracts:
            print("\nApplying manual abstracts...")
            tldr_count = 0
            for pub in publications:
                if pub['title'] in manual_abstracts:
                    # Add abstract if not already present
                    if not pub.get('abstract'):
                        pub['abstract'] = manual_abstracts[pub['title']]
                        safe_print(f"Applied manual abstract for: {pub['title']}")

                        # Generate TL;DR from manual abstract if we don't have one
                        if gemini_model and not pub.get('tldr'):
                            print(f"  Generating TL;DR from manual abstract...")
                            tldr = generate_tldr_with_gemini(pub['title'], pub['abstract'], gemini_model, is_full_paper=False)
                            pub['tldr'] = tldr
                            tldr_count += 1
                            time.sleep(0.5)

            if tldr_count > 0:
                print(f"Generated {tldr_count} TL;DRs from manual abstracts")

    # Fallback to scholarly library if SerpAPI not available
    elif SCHOLARLY_AVAILABLE:
        print("Trying scholarly library (anti-blocking)...")
        publications = extract_publications_scholarly(gemini_model=gemini_model)

        # Apply manual URLs
        if publications and manual_urls:
            for pub in publications:
                if pub['title'] in manual_urls:
                    pub['url'] = manual_urls[pub['title']]
                    print(f"Applied manual URL for: {pub['title']}")

    # Last resort: try direct scraping (has sortby=pubdate)
    if publications is None:
        print("Trying direct Google Scholar scraping...")
        publications = extract_publications_simple(fetch_details=True, gemini_model=gemini_model)

    # Validation: ensure we got reasonable data
    if publications is None or len(publications) < MIN_PUBLICATIONS:
        print(f"\nERROR: Only {len(publications) if publications else 0} publications found (minimum: {MIN_PUBLICATIONS})")
        print("This likely means scraping failed or Google Scholar is blocking requests.")

        if existing_count > 0:
            print(f"Keeping existing publications.json with {existing_count} publications")
            print("Not overwriting to prevent data loss!")
            sys.exit(1)  # Exit with error to prevent commit
        else:
            print("No existing data to preserve. Creating file anyway.")
            publications = publications or []
    else:
        print(f"Successfully fetched {len(publications)} publications")

    # Calculate statistics
    total_citations = sum(pub.get('citations') or 0 for pub in publications)

    # Calculate h-index
    citations_sorted = sorted([pub.get('citations') or 0 for pub in publications], reverse=True)
    h_index = 0
    for i, cites in enumerate(citations_sorted):
        if cites >= i + 1:
            h_index = i + 1
        else:
            break

    # Calculate i10-index
    i10_index = sum(1 for pub in publications if (pub.get('citations') or 0) >= 10)

    # Categorize by year
    by_year = {}
    for pub in publications:
        year = pub['year'] or 'TBD'
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(pub)

    # Safety check: Ensure we have a reasonable number of publications
    MINIMUM_PUBLICATIONS = 15
    if len(publications) < MINIMUM_PUBLICATIONS:
        error_msg = f"ERROR: Only {len(publications)} publications found (minimum: {MINIMUM_PUBLICATIONS})"
        print(error_msg)
        print("This likely indicates an API error or scraping failure.")
        print("Aborting to prevent data loss. publications.json will not be updated.")
        sys.exit(1)

    # Safety check: Ensure we have abstracts for most publications
    MINIMUM_ABSTRACTS = 18
    publications_with_abstracts = sum(1 for pub in publications if pub.get('abstract'))
    if publications_with_abstracts < MINIMUM_ABSTRACTS:
        error_msg = f"ERROR: Only {publications_with_abstracts}/{len(publications)} publications have abstracts (minimum: {MINIMUM_ABSTRACTS})"
        print(error_msg)
        print("This likely indicates abstract fetching failure (arXiv API down, manual_abstracts.json missing, etc.).")
        print("Aborting to prevent data loss. publications.json will not be updated.")
        sys.exit(1)

    # Create result
    result = {
        "last_updated": datetime.now().isoformat(),
        "total_publications": len(publications),
        "author_info": {
            "name": "Jixiang Qing",
            "affiliation": "Lancaster University",
            "total_citations": total_citations,
            "h_index": h_index,
            "i10_index": i10_index,
            "scholar_id": "mE9l0sQAAAAJ"
        },
        "publications": publications,
        "categorized": {
            "by_year": by_year
        }
    }

    # Write to file
    with open("publications.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSafety checks passed:")
    print(f"   - Publications: {len(publications)}/{MINIMUM_PUBLICATIONS} minimum")
    print(f"   - Abstracts: {publications_with_abstracts}/{MINIMUM_ABSTRACTS} minimum")

    print(f"\nGenerated publications.json with {len(publications)} publications")
    print(f"Total citations: {total_citations}")
    print(f"h-index: {h_index}, i10-index: {i10_index}")

if __name__ == "__main__":
    generate_simple_publications()