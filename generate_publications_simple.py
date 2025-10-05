#!/usr/bin/env python3
"""
Simple script to extract basic publications from Google Scholar
with SerpAPI fallback and safety validations
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import os
import sys

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

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

def extract_publications_serpapi(scholar_id="mE9l0sQAAAAJ", api_key=None):
    """Extract publications using SerpAPI (more reliable for automation)"""
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

            # Get the citation link to fetch abstract/URL
            citation_id = article.get("citation_id", "")
            pub_url = article.get("link", "")
            abstract = ""

            # Try to get abstract and better URL from detail page
            if citation_id:
                detail_link = f"/citations?view_op=view_citation&citation_for_view={scholar_id}:{citation_id}"
                fetched_url, fetched_abstract = fetch_abstract_and_url(detail_link, headers)
                if fetched_url:
                    pub_url = fetched_url
                if fetched_abstract:
                    abstract = fetched_abstract

            has_abstract = 'Yes' if abstract else 'No'
            has_url = 'Yes' if pub_url else 'No'
            print(f"[{idx}/{len(articles)}] {title} ({year}) - Abstract: {has_abstract}, URL: {has_url}")

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

def extract_publications_simple(scholar_id="mE9l0sQAAAAJ", fetch_details=True):
    """Extract publications from Google Scholar profile with optional detail fetching"""
    publications = []
    base_url = "https://scholar.google.com/citations"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = f"{base_url}?user={scholar_id}&cstart=0&pagesize=100&sortby=pubdate"
    print(f"Fetching: {url}")

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

                has_abstract = 'Yes' if abstract else 'No'
                has_url = 'Yes' if pub_url else 'No'
                print(f"[{idx}/{len(pub_rows)}] {title} ({year}) - Abstract: {has_abstract}, URL: {has_url}")

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

    # Try SerpAPI first (more reliable for automation)
    serpapi_key = os.environ.get("SERPAPI_KEY")
    publications = None

    if serpapi_key:
        print("Trying SerpAPI method...")
        publications = extract_publications_serpapi(api_key=serpapi_key)

    # Fallback to direct scraping if SerpAPI fails or not available
    if publications is None:
        print("Trying direct Google Scholar scraping...")
        publications = extract_publications_simple()

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