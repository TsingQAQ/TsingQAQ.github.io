#!/usr/bin/env python3
"""
Enhanced script to extract publications from Google Scholar with Claude API integration
for generating high-quality TL;DRs from full papers or abstracts
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import urllib.parse
import PyPDF2
import io
import anthropic
from pathlib import Path
import os

# Claude API temporarily disabled - using fallback TL;DR generation
claude = None
print("INFO: Claude API disabled - using simple TL;DR fallback")

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def extract_pdf_text(url, max_pages=10):
    """
    Extract text from PDF URL (works for arXiv and other open access papers)
    """
    try:
        print(f"Downloading PDF from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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

        print(f"Extracted {len(text)} characters from PDF")
        return text[:15000]  # Limit to ~15k chars for Claude API

    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def generate_tldr_with_claude(text, title, is_full_paper=True):
    """
    Generate TL;DR using Claude API
    """
    try:
        # Using fallback TL;DR generation (Claude API disabled)
        if not claude:
            if text and len(text.strip()) > 0:
                # Extract meaningful first sentence(s) from abstract
                sentences = text.split('.')
                # Take first sentence, or first two if first is very short
                if len(sentences) > 0:
                    first_sentence = sentences[0].strip()
                    if len(first_sentence) < 50 and len(sentences) > 1:
                        return f"{first_sentence}. {sentences[1].strip()}."
                    else:
                        return first_sentence + '.'
                else:
                    return text[:200] + '...' if len(text) > 200 else text
            else:
                # No abstract available
                return f"Research contribution in the field of {title.lower().split(':')[0]}."

        if is_full_paper:
            prompt = f"""
            Please create a concise TL;DR (2-3 sentences) for this research paper titled "{title}".
            Focus on the main contribution, method, and key findings.

            Paper content: {text}

            TL;DR:
            """
        else:
            prompt = f"""
            Please create a concise TL;DR (2-3 sentences) for this research paper based on its abstract.
            Focus on the main contribution and key findings.

            Title: {title}
            Abstract: {text}

            TL;DR:
            """

        response = claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    except Exception as e:
        print(f"Error generating TL;DR with Claude: {e}")
        # Fallback to simple extraction
        sentences = text.split('.')
        return sentences[0].strip() + '.' if sentences else "Research contribution in the field."

def get_full_text_if_available(url, title):
    """
    Try to get full text from paper URL, prioritizing arXiv and open access sources
    """
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

    # Check other open access sources
    open_access_domains = [
        'proceedings.mlr.press',
        'jmlr.org',
        'openreview.net',
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

def extract_publications_from_scholar(scholar_id="mE9l0sQAAAAJ"):
    """
    Extract publications from Google Scholar profile with enhanced TL;DR generation
    """
    publications = []
    base_url = "https://scholar.google.com/citations"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    start = 0
    page_size = 100

    while True:
        url = f"{base_url}?user={scholar_id}&cstart={start}&pagesize={page_size}&sortby=pubdate"
        print(f"Fetching: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            pub_rows = soup.find_all('tr', class_='gsc_a_tr')

            if not pub_rows:
                print("No more publications found")
                break

            for row in pub_rows:
                try:
                    # Extract basic publication info (same as before)
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

                    # Get detailed publication info and paper URL
                    pub_link = title_link.get('href')
                    pub_url = ""
                    abstract = ""

                    if pub_link:
                        detail_url = f"https://scholar.google.com{pub_link}"
                        try:
                            time.sleep(1)
                            detail_response = requests.get(detail_url, headers=headers)
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

                            # Extract abstract
                            abstract_div = detail_soup.find('div', class_='gsh_small')
                            if abstract_div:
                                abstract = clean_text(abstract_div.text)

                        except Exception as e:
                            print(f"Error fetching details for {title}: {e}")

                    # Enhanced TL;DR generation
                    print(f"Processing: {title}")

                    # Try to get full text
                    full_text, is_full_paper = get_full_text_if_available(pub_url, title)

                    # Generate TL;DR
                    claude_tldr = ""
                    tldr_source = ""

                    if full_text:
                        print(f"  - Generating TL;DR from full paper")
                        claude_tldr = generate_tldr_with_claude(full_text, title, True)
                        tldr_source = "full_paper"
                    elif abstract:
                        print(f"  - Generating TL;DR from abstract")
                        claude_tldr = generate_tldr_with_claude(abstract, title, False)
                        tldr_source = "abstract"
                    else:
                        print(f"  - No text available for TL;DR")
                        claude_tldr = f"Research contribution related to {title.lower()}."
                        tldr_source = "generated"

                    # Create enhanced publication object
                    pub_id = re.sub(r'[^a-z0-9_]', '_', title.lower().replace(' ', '_'))[:50]
                    if year:
                        pub_id += f"_{year}"

                    publication = {
                        "id": pub_id,
                        "title": title,
                        "authors": authors,
                        "year": year,
                        "venue": venue,
                        "abstract": abstract,
                        "claude_tldr": claude_tldr,
                        "tldr_source": tldr_source,
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
                    print(f"  Generated TL;DR: {claude_tldr[:100]}...")

                except Exception as e:
                    print(f"Error processing publication row: {e}")
                    continue

            if len(pub_rows) < page_size:
                break

            start += page_size
            time.sleep(2)

        except Exception as e:
            print(f"Error fetching publications: {e}")
            break

    return publications

def generate_enhanced_publications_json():
    """Generate enhanced publications.json with Claude-generated TL;DRs"""

    print("=" * 60)
    print("ENHANCED PUBLICATIONS GENERATOR WITH CLAUDE API")
    print("=" * 60)

    # Check if Claude API key is available
    # if not os.getenv('CLAUDE_API_KEY') and 'CLAUDE_API_KEY' not in globals():
    #     print("⚠️  WARNING: No Claude API key found!")
    #     print("   Add your API key to CLAUDE_API_KEY variable")
    #     print("   For now, using fallback TL;DR generation")

    print("Extracting publications from Google Scholar...")
    publications = extract_publications_from_scholar()

    # Calculate statistics
    total_citations = sum(pub['citations'] for pub in publications)

    # Calculate h-index
    citations_sorted = sorted([pub['citations'] for pub in publications], reverse=True)
    h_index = 0
    for i, cites in enumerate(citations_sorted):
        if cites >= i + 1:
            h_index = i + 1
        else:
            break

    # Calculate i10-index
    i10_index = sum(1 for pub in publications if pub['citations'] >= 10)

    # Categorize publications by year
    by_year = {}
    for pub in publications:
        year = pub['year'] or 'Unknown'
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(pub)

    # Count TL;DR sources
    tldr_stats = {}
    for pub in publications:
        source = pub.get('tldr_source', 'unknown')
        tldr_stats[source] = tldr_stats.get(source, 0) + 1

    # Create final JSON structure
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
        "tldr_generation_stats": tldr_stats,
        "publications": publications,
        "categorized": {
            "by_year": by_year
        }
    }

    # Write to file
    output_file = "publications.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"Generated {output_file} with {len(publications)} publications")
    print(f"Total citations: {total_citations}")
    print(f"h-index: {h_index}, i10-index: {i10_index}")
    print("\nTL;DR Generation Stats:")
    for source, count in tldr_stats.items():
        print(f"   {source}: {count} publications")
    print("=" * 60)

    return result

if __name__ == "__main__":
    # Install required packages if needed
    try:
        import PyPDF2
        import anthropic
    except ImportError:
        print("Installing required packages...")
        os.system("pip install PyPDF2 anthropic")
        import PyPDF2
        import anthropic

    generate_enhanced_publications_json()