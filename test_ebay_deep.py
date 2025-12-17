#!/usr/bin/env python3
"""
Deep dive into eBay HTML structure
"""
import requests
from bs4 import BeautifulSoup

def test_ebay_structure():
    search_term = "vintage herringbone coat"
    search_url = f"https://www.ebay.de/sch/i.html?_nkw={search_term.replace(' ', '+')}&_sacat=11450"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    print("Testing eBay Germany structure...")
    print(f"URL: {search_url}\n")

    response = requests.get(search_url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the results container
    results_container = soup.find('ul', class_='srp-results')

    if results_container:
        print(f"✓ Found results container: ul.srp-results")
        items = results_container.find_all('li', recursive=False)
        print(f"✓ Found {len(items)} <li> elements in container\n")

        # Examine first few items
        for idx, item in enumerate(items[:3], 1):
            print(f"--- Item {idx} ---")
            print(f"Classes: {item.get('class', [])}")

            # Look for title
            title_selectors = [
                item.find('div', class_='s-item__title'),
                item.find('h3', class_='s-item__title'),
                item.find('span', role='heading'),
                item.find('div', class_=lambda x: x and 'title' in str(x).lower()),
            ]

            for selector in title_selectors:
                if selector:
                    print(f"Title found: {selector.get_text(strip=True)[:80]}")
                    break
            else:
                print("No title found")

            # Look for price
            price_elem = item.find('span', class_='s-item__price')
            if price_elem:
                print(f"Price: {price_elem.get_text(strip=True)}")

            # Look for link
            link_elem = item.find('a', class_='s-item__link')
            if link_elem:
                print(f"Link: {link_elem.get('href', '')[:80]}...")

            print()

    else:
        print("✗ No results container found")

        # Try to find any relevant divs
        print("\nSearching for alternative containers...")

        # Save a sample of the HTML
        print("\nFirst 2000 characters of body HTML:")
        body = soup.find('body')
        if body:
            print(body.prettify()[:2000])


if __name__ == '__main__':
    test_ebay_structure()
