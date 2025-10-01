#!/usr/bin/env python3
from scholarly import scholarly
import json
import time
from datetime import datetime

SCHOLAR_ID = "mE9l0sQAAAAJ"

def generate_pub_id(title, year):
    import re
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    words = clean_title.split()[:4]
    return f"{'_'.join(words)}_{year}"

def load_manual_enhancements():
    manual_file = '../publications_manual.json'
    try:
        with open(manual_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {k: v for k, v in data.items() if not k.startswith('_')}
    except:
        return {}

def main():
    print("Generating REAL publications.json from Google Scholar...")
    
    # Fetch author
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author)
    
    print(f"Author: {author.get('name')}")
    print(f"Affiliation: {author.get('affiliation')}")
    print(f"Processing {len(author.get('publications', []))} publications...")
    
    publications = []
    
    for i, pub in enumerate(author.get('publications', [])):
        try:
            print(f"Processing {i+1}: {pub.get('bib', {}).get('title', 'Unknown')[:50]}...")
            
            # Fill publication details
            pub_filled = scholarly.fill(pub)
            bib = pub_filled.get('bib', {})
            
            pub_data = {
                'id': generate_pub_id(bib.get('title', ''), bib.get('pub_year', '')),
                'title': bib.get('title', ''),
                'authors': bib.get('author', ''),
                'year': bib.get('pub_year', ''),
                'venue': bib.get('venue', ''),
                'abstract': bib.get('abstract', ''),
                'url': pub_filled.get('pub_url', ''),
                'citations': pub_filled.get('num_citations', 0),
                'filled_manually': False,
                'media': None,
                'custom_description': None,
                'links': [],
                'tags': [],
                'featured': False
            }
            
            publications.append(pub_data)
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error processing publication {i+1}: {e}")
            continue
    
    # Load manual enhancements
    manual_enhancements = load_manual_enhancements()
    print(f"Loaded {len(manual_enhancements)} manual enhancements")
    
    # Apply manual enhancements
    for pub in publications:
        pub_id = pub['id']
        title_lower = pub['title'].lower()
        
        # Try exact match first
        if pub_id in manual_enhancements:
            manual_data = manual_enhancements[pub_id]
        # Try fuzzy matching
        elif any(key in title_lower for key in ['pf2es', 'parallel feasible']):
            manual_data = manual_enhancements.get('pf2es_parallel_feasible_2023', {})
        elif any(key in title_lower for key in ['spectral', 'robustness']):
            manual_data = manual_enhancements.get('spectral_representation_robustness_2022', {})
        elif any(key in title_lower for key in ['adaptive sampling']):
            manual_data = manual_enhancements.get('adaptive_sampling_automatic_2021', {})
        else:
            manual_data = {}
        
        if manual_data:
            print(f"Enhancing: {pub['title'][:50]}...")
            pub.update({
                'filled_manually': True,
                'media': manual_data.get('media'),
                'custom_description': manual_data.get('custom_description'),
                'links': manual_data.get('links', []),
                'tags': manual_data.get('tags', []),
                'featured': manual_data.get('featured', False)
            })
    
    # Categorize by year
    by_year = {}
    featured = []
    recent = []
    current_year = datetime.now().year
    
    for pub in publications:
        year = str(pub.get('year', 'Unknown'))
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(pub)
        
        if pub.get('featured'):
            featured.append(pub)
        
        if year.isdigit() and int(year) >= current_year - 4:
            recent.append(pub)
    
    # Sort by citations within each year
    for year in by_year:
        by_year[year].sort(key=lambda x: x.get('citations', 0), reverse=True)
    
    # Final data structure
    final_data = {
        'last_updated': datetime.now().isoformat(),
        'total_publications': len(publications),
        'author_info': {
            'name': author.get('name', 'Jixiang Qing'),
            'affiliation': author.get('affiliation', ''),
            'total_citations': author.get('citedby', 0),
            'h_index': author.get('hindex', 0),
            'i10_index': author.get('i10index', 0),
            'scholar_id': SCHOLAR_ID
        },
        'publications': publications,
        'categorized': {
            'by_year': by_year,
            'featured': featured,
            'recent': recent
        }
    }
    
    # Save
    with open('../publications.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"SUCCESS! Generated publications.json with {len(publications)} publications")
    print(f"Citations: {final_data['author_info']['total_citations']}")
    print(f"H-index: {final_data['author_info']['h_index']}")
    print(f"Featured: {len(featured)}")

if __name__ == '__main__':
    main()