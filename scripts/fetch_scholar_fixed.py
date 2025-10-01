#!/usr/bin/env python3
"""
Google Scholar Publication Fetcher - FIXED VERSION
Uses direct Scholar ID instead of search
"""

import json
import os
from scholarly import scholarly
import time
from datetime import datetime

# Your Google Scholar ID from _config.yml
SCHOLAR_ID = "mE9l0sQAAAAJ"

def fetch_author_by_id(scholar_id):
    """Fetch author profile directly by Scholar ID"""
    try:
        print(f"Fetching author profile with ID: {scholar_id}")
        
        # Method 1: Try direct ID approach
        author = scholarly.search_author_id(scholar_id)
        if author:
            author = scholarly.fill(author)
            print(f"✅ Found author via ID: {author.get('name', 'Unknown')}")
            print(f"✅ Affiliation: {author.get('affiliation', 'Unknown')}")
            print(f"✅ Total publications: {len(author.get('publications', []))}")
            print(f"✅ Citations: {author.get('citedby', 0)}")
            return author
        
    except Exception as e:
        print(f"❌ Direct ID fetch failed: {e}")
        
    # Method 2: Try search with known details
    print("Trying search method as fallback...")
    try:
        # Search with exact name from config
        search_query = scholarly.search_author('Jixiang Qing')
        authors = list(search_query)
        
        for author in authors:
            author_id = author.get('scholar_id', '')
            if scholar_id in str(author_id):
                print(f"✅ Found matching author via search!")
                return scholarly.fill(author)
        
        # If we have any results, take the first one and verify
        if authors:
            first_author = scholarly.fill(authors[0])
            print(f"⚠️  Taking first result: {first_author.get('name', 'Unknown')}")
            return first_author
            
    except Exception as e:
        print(f"❌ Search fallback failed: {e}")
    
    return None

def process_publication(pub):
    """Process a single publication from Scholar"""
    try:
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
            'filled_manually': False,
            'media': None,
            'custom_description': None,
            'links': [],
            'tags': [],
            'featured': False
        }
        
        # Clean up venue information
        if not pub_data['venue'] and pub_data['journal']:
            pub_data['venue'] = pub_data['journal']
        elif not pub_data['venue'] and pub_data['conference']:
            pub_data['venue'] = pub_data['conference']
        
        # Generate ID for manual enhancement matching
        pub_data['id'] = generate_pub_id(pub_data['title'], pub_data['year'])
        
        return pub_data
    except Exception as e:
        print(f"❌ Error processing publication: {e}")
        return None

def generate_pub_id(title, year):
    """Generate a unique ID for publication matching"""
    import re
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    words = clean_title.split()[:4]  # First 4 words for more uniqueness
    return f"{'_'.join(words)}_{year}"

def load_manual_enhancements():
    """Load manual enhancements from JSON file"""
    manual_file = 'publications_manual.json'
    if os.path.exists(manual_file):
        try:
            with open(manual_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Filter out template entries
                filtered_data = {k: v for k, v in data.items() 
                               if not k.startswith('_')}
                return filtered_data
        except Exception as e:
            print(f"❌ Error loading manual enhancements: {e}")
    return {}

def merge_with_manual_enhancements(auto_pubs, manual_enhancements):
    """Merge auto-fetched publications with manual enhancements"""
    enhanced_pubs = []
    
    print(f"📚 Merging {len(auto_pubs)} auto-fetched pubs with {len(manual_enhancements)} manual enhancements")
    
    for pub in auto_pubs:
        pub_id = pub['id']
        
        # Check if we have manual enhancements for this publication
        if pub_id in manual_enhancements:
            manual_data = manual_enhancements[pub_id]
            print(f"✨ Enhancing: {pub['title'][:50]}...")
            
            # Merge manual enhancements
            pub.update({
                'filled_manually': True,
                'media': manual_data.get('media'),
                'custom_description': manual_data.get('custom_description'),
                'links': manual_data.get('links', []),
                'tags': manual_data.get('tags', []),
                'featured': manual_data.get('featured', False),
                'custom_venue': manual_data.get('custom_venue'),
                'custom_authors': manual_data.get('custom_authors'),
            })
            
            # Use custom venue/authors if provided
            if pub.get('custom_venue'):
                pub['venue'] = pub['custom_venue']
            if pub.get('custom_authors'):
                pub['authors'] = pub['custom_authors']
        else:
            # Try fuzzy matching for IDs that might have changed
            title_lower = pub['title'].lower()
            for manual_id, manual_data in manual_enhancements.items():
                if ('pf2es' in title_lower and 'pf2es' in manual_id) or \
                   ('spectral' in title_lower and 'spectral' in manual_id) or \
                   ('adaptive' in title_lower and 'adaptive' in manual_id):
                    print(f"🔍 Fuzzy match found for: {pub['title'][:50]}...")
                    pub.update({
                        'filled_manually': True,
                        'media': manual_data.get('media'),
                        'custom_description': manual_data.get('custom_description'),
                        'links': manual_data.get('links', []),
                        'tags': manual_data.get('tags', []),
                        'featured': manual_data.get('featured', False),
                    })
                    break
        
        enhanced_pubs.append(pub)
    
    # Add any completely manual publications
    for pub_id, manual_data in manual_enhancements.items():
        if manual_data.get('manual_only', False):
            print(f"➕ Adding manual-only publication: {manual_data.get('title', 'Unknown')}")
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
        year = str(pub.get('year', 'Unknown'))
        
        # Categorize by year
        if year not in categorized['by_year']:
            categorized['by_year'][year] = []
        categorized['by_year'][year].append(pub)
        
        # Categorize by type
        venue = pub.get('venue', '').lower()
        if any(conf in venue for conf in ['conference', 'icml', 'neurips', 'iclr', 'aistats', 'wsc', 'eucap', 'aiaa']):
            categorized['by_type']['conference'].append(pub)
        elif any(jour in venue for jour in ['journal', 'optimization', 'computers']):
            categorized['by_type']['journal'].append(pub)
        elif 'workshop' in venue:
            categorized['by_type']['workshop'].append(pub)
        else:
            categorized['by_type']['other'].append(pub)
        
        # Featured publications
        if pub.get('featured', False):
            categorized['featured'].append(pub)
        
        # Recent publications (last 4 years)
        if year.isdigit() and int(year) >= current_year - 4:
            categorized['recent'].append(pub)
    
    # Sort by citations within each year
    for year in categorized['by_year']:
        categorized['by_year'][year].sort(key=lambda x: x.get('citations', 0), reverse=True)
    
    return categorized

def main():
    """Main function to fetch and process publications"""
    print("🚀 Fetching publications from Google Scholar (REAL VERSION)")
    print("=" * 60)
    
    # Fetch author using Scholar ID
    author = fetch_author_by_id(SCHOLAR_ID)
    if not author:
        print("❌ Could not find author profile with any method")
        print("📝 Note: This could be due to:")
        print("   - Google Scholar rate limiting")
        print("   - Network restrictions") 
        print("   - Temporary Scholar API issues")
        print("   - Profile privacy settings")
        return
    
    # Process publications
    publications = []
    scholar_pubs = author.get('publications', [])
    print(f"📚 Processing {len(scholar_pubs)} publications from Scholar...")
    
    for i, pub in enumerate(scholar_pubs):
        print(f"⏳ Processing {i+1}/{len(scholar_pubs)}: {pub.get('bib', {}).get('title', 'Unknown')[:50]}...")
        processed_pub = process_publication(pub)
        if processed_pub:
            publications.append(processed_pub)
        
        # Rate limiting to be respectful
        time.sleep(1)
    
    print(f"✅ Successfully processed {len(publications)} publications")
    
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
            'i10_index': author.get('i10index', 0),
            'scholar_id': SCHOLAR_ID
        },
        'publications': enhanced_publications,
        'categorized': categorized
    }
    
    # Save to JSON file
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"🎉 SUCCESS! Generated publications.json with {len(enhanced_publications)} publications")
    print(f"📊 Author stats: {final_data['author_info']['total_citations']} citations, h-index: {final_data['author_info']['h_index']}")
    print(f"⭐ Featured publications: {len(categorized['featured'])}")
    print(f"🕒 Last updated: {final_data['last_updated']}")

if __name__ == '__main__':
    main()