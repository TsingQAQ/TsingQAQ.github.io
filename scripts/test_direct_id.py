#!/usr/bin/env python3
from scholarly import scholarly
import json

SCHOLAR_ID = "mE9l0sQAAAAJ"

def test_direct_fetch():
    print(f"Testing direct fetch with Scholar ID: {SCHOLAR_ID}")
    
    try:
        # Try direct ID method
        print("Method 1: Using search_author_id...")
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author)
        
        print(f"SUCCESS! Found: {author.get('name', 'Unknown')}")
        print(f"Affiliation: {author.get('affiliation', 'Unknown')}")
        print(f"Publications: {len(author.get('publications', []))}")
        print(f"Citations: {author.get('citedby', 0)}")
        
        # Test getting first publication
        pubs = author.get('publications', [])
        if pubs:
            first_pub = pubs[0]
            print(f"First publication: {first_pub.get('bib', {}).get('title', 'Unknown')}")
            
        return True
        
    except Exception as e:
        print(f"Direct ID failed: {e}")
        
    # Try alternative approach
    try:
        print("Method 2: Using search with known publication...")
        search_query = scholarly.search_pubs("Parallel Feasible Pareto Frontier Entropy Search Jixiang Qing")
        pubs = list(search_query)
        
        if pubs:
            print(f"Found {len(pubs)} publications via publication search")
            for pub in pubs[:2]:
                title = pub.get('bib', {}).get('title', 'Unknown')
                authors = pub.get('bib', {}).get('author', 'Unknown')
                print(f"  - {title}")
                print(f"    Authors: {authors}")
                
                if 'qing' in authors.lower():
                    print("    >>> This looks like a match!")
        
        return True
        
    except Exception as e:
        print(f"Publication search failed: {e}")
        
    return False

if __name__ == '__main__':
    test_direct_fetch()