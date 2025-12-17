#!/usr/bin/env python3
"""
Deep dive into Kleinanzeigen HTML structure
"""
import requests
from bs4 import BeautifulSoup

def test_kleinanzeigen():
    search_term = "vintage herringbone"  # Simpler search
    base_url = "https://www.kleinanzeigen.de/s-kleidung-damen/c153"
    search_url = f"{base_url}?keywords={search_term.replace(' ', '+')}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    print("Testing Kleinanzeigen structure...")
    print(f"URL: {search_url}\n")

    response = requests.get(search_url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.content)} bytes\n")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for common patterns
    print("--- Looking for listing patterns ---")

    patterns = [
        ('article', soup.find_all('article')[:3]),
        ('div[id*="srchrslt"]', soup.find_all('div', id=lambda x: x and 'srchrslt' in str(x))),
        ('ul[id*="srchrslt"]', soup.find_all('ul', id=lambda x: x and 'srchrslt' in str(x))),
        ('li[class*="ad"]', soup.find_all('li', class_=lambda x: x and 'ad' in str(x))[:3]),
    ]

    for name, elements in patterns:
        print(f"\n{name}: Found {len(elements)}")
        if elements:
            for idx, elem in enumerate(elements[:1], 1):
                print(f"  Element {idx} classes: {elem.get('class', 'No class')}")
                print(f"  Element {idx} id: {elem.get('id', 'No id')}")
                print(f"  Content (first 150 chars): {str(elem)[:150]}...")

    # Look for links
    all_links = soup.find_all('a', href=True)
    print(f"\n--- Total links found: {len(all_links)} ---")

    # Look for ad links
    ad_links = [a for a in all_links if '/s-anzeige/' in a.get('href', '') or '/anzeige/' in a.get('href', '')]
    print(f"Ad links (with '/s-anzeige/' or '/anzeige/'): {len(ad_links)}")
    if ad_links:
        for idx, link in enumerate(ad_links[:3], 1):
            print(f"  Link {idx}: {link.get('href', '')[:100]}")
            print(f"  Text: {link.get_text(strip=True)[:80]}")

    # Check for JavaScript indicators
    scripts = soup.find_all('script')
    print(f"\n--- Script tags found: {len(scripts)} ---")

    # Look for React/Next.js indicators
    has_nextjs = any('__NEXT_DATA__' in str(script) for script in scripts)
    has_react = soup.find(id='__next') or soup.find('div', id='root')

    print(f"Has Next.js indicator: {has_nextjs}")
    print(f"Has React root: {bool(has_react)}")

    # Save a sample of HTML
    print("\n--- Saving HTML sample to file ---")
    with open('kleinanzeigen_sample.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify()[:5000])
    print("Saved first 5000 chars to kleinanzeigen_sample.html")


if __name__ == '__main__':
    test_kleinanzeigen()
