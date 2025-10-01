#!/usr/bin/env python3

from scholarly import scholarly
import time

def test_search():
    print("Testing Google Scholar search for Jixiang Qing...")
    
    queries = [
        "Jixiang Qing",
        "Qing Jixiang", 
        "Jixiang Qing Ghent",
        "J Qing Bayesian optimization"
    ]
    
    for query in queries:
        print(f"Trying: {query}")
        try:
            search_query = scholarly.search_author(query)
            authors = list(search_query)
            
            print(f"Found {len(authors)} authors")
            for i, author in enumerate(authors[:2]):
                print(f"  {i+1}. {author.get('name', 'Unknown')}")
                print(f"     {author.get('affiliation', 'Unknown')}")
                if 'qing' in author.get('name', '').lower():
                    print(f"     >>> POTENTIAL MATCH <<<")
                    
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(3)
        print("---")

if __name__ == '__main__':
    test_search()