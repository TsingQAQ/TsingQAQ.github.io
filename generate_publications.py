#!/usr/bin/env python3
"""
Script to extract publications from Google Scholar with proper venue information
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import urllib.parse

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def extract_publications_from_scholar(scholar_id="mE9l0sQAAAAJ"):
    """
    Extract publications from Google Scholar profile
    """
    publications = []
    base_url = "https://scholar.google.com/citations"

    # Headers to mimic browser request - updated user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Start with first page
    start = 0
    page_size = 20  # Get fewer publications to avoid rate limiting

    while True:
        url = f"{base_url}?user={scholar_id}&cstart={start}&pagesize={page_size}&sortby=pubdate"
        print(f"Fetching: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find publication rows
            pub_rows = soup.find_all('tr', class_='gsc_a_tr')

            if not pub_rows:
                print("No more publications found")
                break

            for row in pub_rows:
                try:
                    # Extract title and link
                    title_cell = row.find('td', class_='gsc_a_t')
                    if not title_cell:
                        continue

                    title_link = title_cell.find('a')
                    if not title_link:
                        continue

                    title = clean_text(title_link.text)

                    # Extract venue information
                    venue_elem = title_cell.find('div', class_='gs_gray')
                    venue = ""
                    if venue_elem:
                        venue = clean_text(venue_elem.text)

                    # Extract authors (second gray div)
                    author_divs = title_cell.find_all('div', class_='gs_gray')
                    authors = ""
                    if len(author_divs) > 1:
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

                    # Get detailed publication info
                    pub_link = title_link.get('href')
                    pub_url = ""
                    abstract = ""

                    if pub_link:
                        # Get full publication details
                        detail_url = f"https://scholar.google.com{pub_link}"
                        try:
                            time.sleep(3)  # Be more polite to Google
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

                            # Extract abstract if available
                            abstract_div = detail_soup.find('div', class_='gsh_small')
                            if abstract_div:
                                abstract = clean_text(abstract_div.text)

                        except Exception as e:
                            print(f"Error fetching details for {title}: {e}")

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
                    print(f"Extracted: {title} ({year}) - {venue}")

                except Exception as e:
                    print(f"Error processing publication row: {e}")
                    continue

            # Check if there are more pages
            if len(pub_rows) < page_size:
                break

            start += page_size
            time.sleep(5)  # Be more polite to Google

        except Exception as e:
            print(f"Error fetching publications: {e}")
            break

    return publications

def generate_publications_json():
    """Generate the publications.json file"""
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

    # Calculate i10-index (papers with >= 10 citations)
    i10_index = sum(1 for pub in publications if pub['citations'] >= 10)

    # Categorize publications by year
    by_year = {}
    for pub in publications:
        year = pub['year'] or 'Unknown'
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(pub)

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
        "publications": publications,
        "categorized": {
            "by_year": by_year
        }
    }

    # Write to file
    output_file = "publications.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nGenerated {output_file} with {len(publications)} publications")
    print(f"Total citations: {total_citations}")
    print(f"h-index: {h_index}")
    print(f"i10-index: {i10_index}")

    return result

if __name__ == "__main__":
    generate_publications_json()