#!/usr/bin/env python3
"""
Test eBay data extraction from actual listings
"""
import requests
from bs4 import BeautifulSoup

search_term = "CP Company coat"
search_url = f"https://www.ebay.de/sch/i.html?_nkw={search_term.replace(' ', '+')}&_sacat=11450"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
}

print("Testing eBay data extraction...")
print(f"URL: {search_url}\n")

response = requests.get(search_url, headers=headers, timeout=30)
soup = BeautifulSoup(response.content, 'html.parser')

results_container = soup.find('ul', class_='srp-results')
if results_container:
    listings = results_container.find_all('li', class_='s-card', recursive=False)
    print(f"Found {len(listings)} listings\n")

    for idx, listing in enumerate(listings[:3], 1):
        print(f"=== Listing {idx} ===")

        # Test title selectors
        title_selectors = [
            ('div.s-item__title', listing.find('div', class_='s-item__title')),
            ('h3.s-item__title', listing.find('h3', class_='s-item__title')),
            ('span[role="heading"]', listing.find('span', role='heading')),
            ('div[class*="title"]', listing.find('div', class_=lambda x: x and 'title' in str(x).lower())),
            ('h3', listing.find('h3')),
            ('any a with href', listing.find('a', href=True)),
        ]

        print("\nTitle attempts:")
        for name, elem in title_selectors:
            if elem:
                text = elem.get_text(strip=True)
                print(f"  ✓ {name}: {text[:80]}")
                break
        else:
            print("  ✗ No title found")

        # Test price selectors
        price_selectors = [
            ('span.s-item__price', listing.find('span', class_='s-item__price')),
            ('span[class*="price"]', listing.find('span', class_=lambda x: x and 'price' in str(x))),
            ('div[class*="price"]', listing.find('div', class_=lambda x: x and 'price' in str(x))),
        ]

        print("\nPrice attempts:")
        for name, elem in price_selectors:
            if elem:
                text = elem.get_text(strip=True)
                print(f"  ✓ {name}: {text}")
                break
        else:
            print("  ✗ No price found")

        # Test link selectors
        link_selectors = [
            ('a.s-item__link', listing.find('a', class_='s-item__link')),
            ('a[href*="/itm/"]', listing.find('a', href=lambda x: x and '/itm/' in str(x))),
            ('any a', listing.find('a', href=True)),
        ]

        print("\nLink attempts:")
        for name, elem in link_selectors:
            if elem:
                href = elem.get('href', '')
                print(f"  ✓ {name}: {href[:80]}...")
                break
        else:
            print("  ✗ No link found")

        print("\n" + "-" * 60 + "\n")
