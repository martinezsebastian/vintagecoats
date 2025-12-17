#!/usr/bin/env python3
"""
Test script to see what HTML structure we're actually getting from sites
"""
import requests
from bs4 import BeautifulSoup

def test_kleinanzeigen():
    print("=" * 60)
    print("TESTING KLEINANZEIGEN")
    print("=" * 60)

    search_term = "vintage herringbone coat"
    base_url = "https://www.kleinanzeigen.de/s-kleidung-damen/c153"
    search_url = f"{base_url}?keywords={search_term.replace(' ', '+')}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print(f"\nURL: {search_url}")

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Try multiple selector patterns
            print("\n--- Testing different selectors ---")

            selectors = [
                ('article.aditem', soup.find_all('article', class_='aditem')),
                ('article[class*="ad"]', soup.find_all('article', class_=lambda x: x and 'ad' in x)),
                ('div[class*="listing"]', soup.find_all('div', class_=lambda x: x and 'listing' in x)),
                ('li[class*="ad"]', soup.find_all('li', class_=lambda x: x and 'ad' in x)),
                ('article (any)', soup.find_all('article')[:5]),
            ]

            for selector_name, results in selectors:
                print(f"\n{selector_name}: Found {len(results)} elements")
                if results:
                    print(f"First element classes: {results[0].get('class', 'No class')}")
                    print(f"First element HTML (first 200 chars):\n{str(results[0])[:200]}...")

            # Check for any links that might be listings
            all_links = soup.find_all('a', href=True)
            listing_links = [a for a in all_links if '/s-anzeige/' in a.get('href', '')]
            print(f"\n--- Links with '/s-anzeige/' in href: {len(listing_links)} ---")
            if listing_links:
                print(f"Example link: {listing_links[0].get('href')}")

    except Exception as e:
        print(f"Error: {e}")


def test_ebay_de():
    print("\n" + "=" * 60)
    print("TESTING EBAY GERMANY")
    print("=" * 60)

    search_term = "vintage herringbone coat"
    search_url = f"https://www.ebay.de/sch/i.html?_nkw={search_term.replace(' ', '+')}&_sacat=11450"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    print(f"\nURL: {search_url}")

    try:
        response = requests.get(search_url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Try multiple selector patterns
            print("\n--- Testing different selectors ---")

            selectors = [
                ('div.s-item__wrapper', soup.find_all('div', class_='s-item__wrapper')),
                ('li.s-item', soup.find_all('li', class_='s-item')),
                ('div[class*="s-item"]', soup.find_all('div', class_=lambda x: x and 's-item' in str(x))),
                ('li[class*="item"]', soup.find_all('li', class_=lambda x: x and 'item' in str(x))[:5]),
                ('div.srp-results', soup.find_all('div', class_='srp-results')),
            ]

            for selector_name, results in selectors:
                print(f"\n{selector_name}: Found {len(results)} elements")
                if results:
                    print(f"First element classes: {results[0].get('class', 'No class')}")
                    print(f"First element HTML (first 200 chars):\n{str(results[0])[:200]}...")

            # Check for any listing container
            results_container = soup.find('ul', class_='srp-results')
            if results_container:
                print(f"\n--- Found results container! ---")
                items = results_container.find_all('li')
                print(f"Items in container: {len(items)}")

    except Exception as e:
        print(f"Error: {e}")


def test_ebay_uk():
    print("\n" + "=" * 60)
    print("TESTING EBAY UK")
    print("=" * 60)

    search_term = "vintage herringbone coat"
    search_url = f"https://www.ebay.co.uk/sch/i.html?_nkw={search_term.replace(' ', '+')}&_sacat=11450"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    print(f"\nURL: {search_url}")

    try:
        response = requests.get(search_url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Try multiple selector patterns
            print("\n--- Testing different selectors ---")

            selectors = [
                ('div.s-item__wrapper', soup.find_all('div', class_='s-item__wrapper')),
                ('li.s-item', soup.find_all('li', class_='s-item')),
                ('div[class*="s-item"]', soup.find_all('div', class_=lambda x: x and 's-item' in str(x))),
            ]

            for selector_name, results in selectors:
                print(f"\n{selector_name}: Found {len(results)} elements")
                if results:
                    print(f"First element classes: {results[0].get('class', 'No class')}")
                    print(f"First element HTML (first 200 chars):\n{str(results[0])[:200]}...")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    test_kleinanzeigen()
    test_ebay_de()
    test_ebay_uk()
    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
