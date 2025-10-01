#!/usr/bin/env python3
"""
Test script to find the correct Google Scholar search parameters
"""

from scholarly import scholarly
import time

def test_search_queries():
    """Test different search queries to find the author profile"""
    search_queries = [
        "Jixiang Qing",
        "Jixiang Qing Ghent University",
        "Jixiang Qing Bayesian optimization",
        "Jixiang Qing SUMO lab",
        "J Qing Ghent",
        "Qing Jixiang",
        "Qing Jixiang Ghent University",
        "Qing Bayesian optimization Ghent",
    ]
    
    for query in search_queries:
        print(f"\n🔍 Testing search query: '{query}'")
        try:
            search_query = scholarly.search_author(query)
            authors = list(search_query)
            
            if authors:
                print(f"✅ Found {len(authors)} author(s)")
                for i, author in enumerate(authors[:3]):  # Show first 3 results
                    print(f"  {i+1}. Name: {author.get('name', 'Unknown')}")
                    print(f"     Affiliation: {author.get('affiliation', 'Unknown')}")
                    print(f"     Citations: {author.get('citedby', 'Unknown')}")
                    print(f"     Email: {author.get('email_domain', 'Unknown')}")
                    
                    # Check if this might be our author
                    name = author.get('name', '').lower()
                    affiliation = author.get('affiliation', '').lower()
                    if ('jixiang' in name or 'qing' in name) and ('ghent' in affiliation or 'sumo' in affiliation):
                        print(f"     🎯 This looks like a match!")
                        return author
            else:
                print("❌ No authors found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Rate limiting
        time.sleep(2)
    
    return None

def test_publication_search():
    """Test searching by publication titles"""
    print("\n🔍 Testing publication-based search...")
    
    publication_titles = [
        "Parallel Feasible Pareto Frontier Entropy Search Multi-Objective Bayesian Optimization",
        "Spectral Representation Robustness Measures Optimization Input Uncertainty",
        "Kriging Assisted Integrated Rotor-Duct Optimization Ducted Fan Hover"
    ]
    
    for title in publication_titles:
        print(f"\n📄 Searching for publication: '{title[:50]}...'")
        try:
            search_query = scholarly.search_pubs(title)
            pubs = list(search_query)
            
            if pubs:
                print(f"✅ Found {len(pubs)} publication(s)")
                for i, pub in enumerate(pubs[:2]):
                    print(f"  {i+1}. {pub.get('bib', {}).get('title', 'Unknown title')}")
                    authors = pub.get('bib', {}).get('author', 'Unknown authors')
                    print(f"     Authors: {authors}")
                    
                    # If we find a publication, try to get the author
                    if 'qing' in authors.lower():
                        print(f"     🎯 Found publication by Qing!")
                        return pub
            else:
                print("❌ No publications found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)
    
    return None

if __name__ == '__main__':
    print("🚀 Testing Google Scholar search parameters for Jixiang Qing")
    print("=" * 60)
    
    # Test author searches
    author = test_search_queries()
    
    if not author:
        # Test publication searches
        pub = test_publication_search()
        
        if pub:
            print(f"\n📚 Found via publication search! Now trying to get author profile...")
        else:
            print(f"\n❌ Could not find author profile through any method")
            print("This might be due to:")
            print("- Google Scholar rate limiting")
            print("- Profile privacy settings")
            print("- Different name formatting")
            print("- Network restrictions")
    
    print("\n✅ Search test completed!")