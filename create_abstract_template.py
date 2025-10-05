#!/usr/bin/env python3
"""Create manual_abstracts.json template with all papers missing abstracts"""
import json

# Load publications
with open('publications.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find papers without abstracts
papers_without_abstracts = []
for pub in data['publications']:
    if not pub.get('abstract'):
        papers_without_abstracts.append(pub['title'])

# Create template
template = {
    "manual_abstracts": {}
}

# Add all papers as empty strings with helpful comments
for title in papers_without_abstracts:
    template["manual_abstracts"][title] = ""

# Save template
with open('manual_abstracts.json', 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print(f"Created manual_abstracts.json template with {len(papers_without_abstracts)} papers")
print("\nPapers needing abstracts:")
for i, title in enumerate(papers_without_abstracts, 1):
    print(f"{i}. {title}")
