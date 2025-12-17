#!/usr/bin/env python3
"""
Test Kleinanzeigen article structure in detail
"""
import requests
from bs4 import BeautifulSoup

search_term = "vintage herringbone"
base_url = "https://www.kleinanzeigen.de/s-kleidung-damen/c153"
search_url = f"{base_url}?keywords={search_term.replace(' ', '+')}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
}

print("Testing Kleinanzeigen article details...")
print(f"URL: {search_url}\n")

response = requests.get(search_url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

listings = soup.find_all('article', class_='aditem')
print(f"Found {len(listings)} articles\n")

if listings:
    for idx, listing in enumerate(listings[:2], 1):
        print(f"=== Article {idx} ===")
        print(f"data-href: {listing.get('data-href', 'N/A')}")

        # Try different title selectors
        title_selectors = [
            ('a.ellipsis', listing.find('a', class_='ellipsis')),
            ('a.aditem-main--middle--anchor', listing.find('a', class_='aditem-main--middle--anchor')),
            ('any a with text', listing.find('a', string=True)),
            ('h2', listing.find('h2')),
        ]

        for name, elem in title_selectors:
            if elem:
                print(f"\nTitle ({name}):")
                print(f"  Text: {elem.get_text(strip=True)[:80]}")
                print(f"  href: {elem.get('href', 'N/A')}")
                break

        # Try different price selectors
        price_selectors = [
            ('p.aditem-main--middle--price-shipping--price', listing.find('p', class_='aditem-main--middle--price-shipping--price')),
            ('p[class*="price"]', listing.find('p', class_=lambda x: x and 'price' in str(x))),
            ('span[class*="price"]', listing.find('span', class_=lambda x: x and 'price' in str(x))),
        ]

        for name, elem in price_selectors:
            if elem:
                print(f"\nPrice ({name}):")
                print(f"  Text: {elem.get_text(strip=True)}")
                break
        else:
            print("\nPrice: NOT FOUND")

        print("\n" + "-" * 50 + "\n")
