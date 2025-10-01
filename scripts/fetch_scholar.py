#!/usr/bin/env python3
"""
Google Scholar Publication Fetcher for Jixiang Qing
Fetches publications and merges with manual enhancements
"""

import json
import os
from scholarly import scholarly
import time
from datetime import datetime

def search_author():
    """Search for author profile on Google Scholar"""
    try:
        # Search for your specific profile
        search_query = scholarly.search_author('Jixiang Qing Ghent University Bayesian optimization')
        authors = list(search_query)
        
        if not authors:
            print("No authors found, trying alternative search...")
            search_query = scholarly.search_author('Jixiang Qing SUMO')
            authors = list(search_query)
        
        if authors:
            # Get the most likely match (first result)
            author = scholarly.fill(authors[0])
            print(f"Found author: {author.get('name', 'Unknown')}")
            print(f"Affiliation: {author.get('affiliation', 'Unknown')}")
            print(f"Total publications: {len(author.get('publications', []))}")
            return author
        else:
            print("No matching author found")
            return None
    except Exception as e:
        print(f"Error searching for author: {e}")
        return None

def process_publication(pub):
    """Process a single publication and extract relevant data"""
    try:
        # Fill in additional details
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get('bib', {})
        
        # Extract publication data
        pub_data = {
            'title': bib.get('title', 'Unknown Title'),
            'authors': bib.get('author', ''),
            'year': bib.get('pub_year', ''),
            'venue': bib.get('venue', ''),
            'journal': bib.get('journal', ''),
            'conference': bib.get('conference', ''),
            'publisher': bib.get('publisher', ''),
            'abstract': bib.get('abstract', ''),
            'url': pub_filled.get('pub_url', ''),
            'scholar_url': pub_filled.get('author_pub_url', ''),
            'citations': pub_filled.get('num_citations', 0),
            'eprint_url': pub_filled.get('eprint_url', ''),
            'filled_manually': False,  # Flag for manual enhancements
            'media': None,  # Placeholder for GIFs/videos
            'custom_description': None,  # Custom description override
            'links': [],  # Additional custom links
            'tags': [],  # Research categories/tags
            'featured': False  # Whether to feature this publication
        }
        
        # Clean up venue information
        if not pub_data['venue'] and pub_data['journal']:
            pub_data['venue'] = pub_data['journal']
        elif not pub_data['venue'] and pub_data['conference']:
            pub_data['venue'] = pub_data['conference']
        
        # Generate a unique ID for manual enhancement matching
        pub_data['id'] = generate_pub_id(pub_data['title'], pub_data['year'])
        
        return pub_data
    except Exception as e:
        print(f"Error processing publication: {e}")
        return None

def generate_pub_id(title, year):
    """Generate a unique ID for publication matching"""
    # Simple ID generation based on first few words of title + year
    import re
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    words = clean_title.split()[:3]  # First 3 words
    return f"{'_'.join(words)}_{year}"

def load_manual_enhancements():
    """Load manual enhancements from JSON file"""
    manual_file = 'publications_manual.json'
    if os.path.exists(manual_file):
        try:
            with open(manual_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading manual enhancements: {e}")
    return {}

def merge_with_manual_enhancements(auto_pubs, manual_enhancements):
    """Merge auto-fetched publications with manual enhancements"""
    enhanced_pubs = []
    
    for pub in auto_pubs:
        pub_id = pub['id']
        
        # Check if we have manual enhancements for this publication
        if pub_id in manual_enhancements:
            manual_data = manual_enhancements[pub_id]
            
            # Merge manual enhancements
            pub.update({
                'filled_manually': True,
                'media': manual_data.get('media'),
                'custom_description': manual_data.get('custom_description'),
                'links': manual_data.get('links', []),
                'tags': manual_data.get('tags', []),
                'featured': manual_data.get('featured', False),
                'custom_venue': manual_data.get('custom_venue'),  # Override venue if needed
                'custom_authors': manual_data.get('custom_authors'),  # Override authors if needed
            })
            
            # Use custom venue/authors if provided
            if pub['custom_venue']:
                pub['venue'] = pub['custom_venue']
            if pub['custom_authors']:
                pub['authors'] = pub['custom_authors']
        
        enhanced_pubs.append(pub)
    
    # Add any completely manual publications
    for pub_id, manual_data in manual_enhancements.items():
        if manual_data.get('manual_only', False):
            enhanced_pubs.append(manual_data)
    
    return enhanced_pubs

def categorize_publications(publications):
    """Categorize publications by year and type"""
    categorized = {
        'by_year': {},
        'by_type': {
            'conference': [],
            'journal': [],
            'workshop': [],
            'other': []
        },
        'featured': [],
        'recent': []
    }
    
    current_year = datetime.now().year
    
    for pub in publications:
        year = pub.get('year', 'Unknown')
        
        # Categorize by year
        if year not in categorized['by_year']:
            categorized['by_year'][year] = []
        categorized['by_year'][year].append(pub)
        
        # Categorize by type (simple heuristic)
        venue = pub.get('venue', '').lower()
        if any(conf in venue for conf in ['conference', 'workshop', 'symposium', 'icml', 'neurips', 'iclr', 'aistats']):
            categorized['by_type']['conference'].append(pub)
        elif any(jour in venue for jour in ['journal', 'transactions', 'letters']):
            categorized['by_type']['journal'].append(pub)
        elif 'workshop' in venue:
            categorized['by_type']['workshop'].append(pub)
        else:
            categorized['by_type']['other'].append(pub)
        
        # Featured publications
        if pub.get('featured', False):
            categorized['featured'].append(pub)
        
        # Recent publications (last 3 years)
        if year and year.isdigit() and int(year) >= current_year - 3:
            categorized['recent'].append(pub)
    
    # Sort by year (descending)
    for year in categorized['by_year']:
        categorized['by_year'][year].sort(key=lambda x: x.get('citations', 0), reverse=True)
    
    return categorized

def create_sample_manual_file():
    """Create a sample manual enhancements file"""
    sample_manual = {
        "pf2es_parallel_feasible_2023": {
            "media": {
                "type": "video",
                "url": "images/pf2es_demo.mp4",
                "thumbnail": "images/pf2es_thumbnail.png",
                "description": "Demo of PF²ES algorithm in action"
            },
            "custom_description": "Our method for parallel multi-objective Bayesian optimization with constraints.",
            "links": [
                {"text": "Interactive Demo", "url": "https://your-demo-link.com"},
                {"text": "Supplementary", "url": "path/to/supplementary.pdf"}
            ],
            "tags": ["bayesian-optimization", "multi-objective", "constraints"],
            "featured": true
        },
        "spectral_representation_robustness_2022": {
            "media": {
                "type": "gif",
                "url": "images/spectral_method.gif",
                "description": "Visualization of spectral representation approach"
            },
            "featured": true,
            "tags": ["optimization", "uncertainty", "spectral-methods"]
        },
        "manual_only_example": {
            "manual_only": true,
            "title": "Example Manual Publication",
            "authors": "Your Name, Others",
            "year": "2024",
            "venue": "Special Conference",
            "url": "https://example.com",
            "media": {
                "type": "image",
                "url": "images/manual_pub.png"
            }
        }
    }
    
    with open('publications_manual.json', 'w', encoding='utf-8') as f:
        json.dump(sample_manual, f, indent=2, ensure_ascii=False)
    print("Created sample publications_manual.json file")

def main():
    """Main function to fetch and process publications"""
    print("Fetching publications from Google Scholar...")
    
    # Search for author
    author = search_author()
    if not author:
        print("Could not find author profile. Using fallback data.")
        return
    
    # Process publications
    publications = []
    for pub in author.get('publications', []):
        print(f"Processing: {pub.get('bib', {}).get('title', 'Unknown')}")
        processed_pub = process_publication(pub)
        if processed_pub:
            publications.append(processed_pub)
        
        # Rate limiting to be respectful to Google Scholar
        time.sleep(1)
    
    # Load manual enhancements
    manual_enhancements = load_manual_enhancements()
    
    # Merge with manual enhancements
    enhanced_publications = merge_with_manual_enhancements(publications, manual_enhancements)
    
    # Categorize publications
    categorized = categorize_publications(enhanced_publications)
    
    # Prepare final data structure
    final_data = {
        'last_updated': datetime.now().isoformat(),
        'total_publications': len(enhanced_publications),
        'author_info': {
            'name': author.get('name', 'Jixiang Qing'),
            'affiliation': author.get('affiliation', ''),
            'total_citations': author.get('citedby', 0),
            'h_index': author.get('hindex', 0),
            'i10_index': author.get('i10index', 0)
        },
        'publications': enhanced_publications,
        'categorized': categorized
    }
    
    # Save to JSON file
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    # Create sample manual file if it doesn't exist
    if not os.path.exists('publications_manual.json'):
        create_sample_manual_file()
    
    print(f"Successfully fetched {len(enhanced_publications)} publications")
    print("Publications data saved to publications.json")
    print("You can customize publications using publications_manual.json")

if __name__ == '__main__':
    main()