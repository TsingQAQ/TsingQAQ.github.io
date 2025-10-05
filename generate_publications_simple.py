#!/usr/bin/env python3
"""
Enhanced publication script with:
- SerpAPI support for reliable scraping
- Automatic arXiv/DOI URL extraction from publication metadata
- Abstract and URL extraction from Google Scholar detail pages
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
            "num": 100
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
            # Extract year from publication info
            year = None
            pub_info = article.get("publication", "")
            year_match = re.search(r'\b(19|20)\d{2}\b', pub_info)
            if year_match:
                year = int(year_match.group())

            title = article.get("title", "")

            # Extract direct paper URL from publication info (arXiv, DOI, etc.)
            pub_url = extract_paper_url_from_publication_info(pub_info, title)

            # Try to get abstract from Google Scholar detail page
            abstract = ""
            citation_id = article.get("citation_id", "")
            if citation_id:
                detail_link = f"/citations?view_op=view_citation&citation_for_view={scholar_id}:{citation_id}"
                fetched_url, fetched_abstract = fetch_abstract_and_url(detail_link, headers)
                # Use fetched URL if we don't already have one
                if fetched_url and not pub_url:
                    pub_url = fetched_url
                if fetched_abstract:
                    abstract = fetched_abstract

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

                # Get publication link for detail fetching
                pub_url = ""
                abstract = ""

                if fetch_details and title_link:
                    pub_link = title_link.get('href')
                    if pub_link:
                        pub_url, abstract = fetch_abstract_and_url(pub_link, headers)

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

    # Try SerpAPI first (more reliable for automation)
    serpapi_key = os.environ.get("SERPAPI_KEY")
    publications = None

    if serpapi_key:
        print("Trying SerpAPI method...")
        publications = extract_publications_serpapi(api_key=serpapi_key, gemini_model=gemini_model)

    # Fallback to direct scraping if SerpAPI fails or not available
    if publications is None:
        print("Trying direct Google Scholar scraping...")
        publications = extract_publications_simple(gemini_model=gemini_model)

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

    print(f"\nGenerated publications.json with {len(publications)} publications")
    print(f"Total citations: {total_citations}")
    print(f"h-index: {h_index}, i10-index: {i10_index}")

if __name__ == "__main__":
    generate_simple_publications()