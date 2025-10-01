#!/usr/bin/env python3
"""
Simple script to extract basic publications from Google Scholar
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def extract_publications_simple(scholar_id="mE9l0sQAAAAJ"):
    """Extract basic publications from Google Scholar profile"""
    publications = []
    base_url = "https://scholar.google.com/citations"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = f"{base_url}?user={scholar_id}&cstart=0&pagesize=100&sortby=pubdate"
    print(f"Fetching: {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        pub_rows = soup.find_all('tr', class_='gsc_a_tr')
        print(f"Found {len(pub_rows)} publications")

        for row in pub_rows:
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

                # Create publication object with basic info only
                pub_id = re.sub(r'[^a-z0-9_]', '_', title.lower().replace(' ', '_'))[:50]
                if year:
                    pub_id += f"_{year}"

                publication = {
                    "id": pub_id,
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "venue": venue,
                    "abstract": "",  # Skip abstract for speed
                    "url": "",       # Skip URL for speed
                    "citations": citations,
                    "filled_manually": False,
                    "media": None,
                    "custom_description": None,
                    "links": [],
                    "tags": [],
                    "featured": False
                }

                publications.append(publication)
                print(f"Added: {title} ({year})")

            except Exception as e:
                print(f"Error processing publication: {e}")
                continue

    except Exception as e:
        print(f"Error fetching publications: {e}")

    return publications

def generate_simple_publications():
    """Generate basic publications.json"""
    print("Extracting basic publications from Google Scholar...")

    publications = extract_publications_simple()

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
        year = pub['year'] or 'Unknown'
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