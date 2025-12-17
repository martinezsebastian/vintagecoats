#!/usr/bin/env python3
"""
Vintage Coat Finder Bot
Searches multiple sources for vintage coats and sends email notifications
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import re


class VintageCoatFinder:
    def __init__(self, config_path='config.json'):
        """Initialize the finder with configuration"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.db_path = 'seen_items.db'
        # Delete old database to start fresh each time
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Deleted old database to start fresh")
        self.setup_database()
        self.results = []

    def setup_database(self):
        """Create fresh database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seen_items (
                id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                price TEXT,
                source TEXT,
                found_date TEXT,
                image_url TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Failed to fetch {url} after {max_retries} attempts")
                    return None
    
    def generate_item_id(self, title: str, url: str) -> str:
        """Generate unique ID for an item"""
        unique_string = f"{title}_{url}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def save_item(self, item: Dict):
        """Save item to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO seen_items (id, title, url, price, source, found_date, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['id'],
            item['title'],
            item['url'],
            item.get('price', 'N/A'),
            item['source'],
            datetime.now().isoformat(),
            item.get('image_url', '')
        ))
        conn.commit()
        conn.close()
    
    def search_kleinanzeigen(self):
        """Search Kleinanzeigen (formerly eBay Kleinanzeigen)"""
        print("Searching Kleinanzeigen...")

        # Build search URL
        search_terms = '+'.join(self.config['search_terms'])
        base_url = "https://www.kleinanzeigen.de/s-kleidung-damen/c153"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        max_per_source = self.config.get('max_results_per_source', 10)
        items_found = 0

        try:
            # Search for each term combination
            for term in self.config['search_terms']:
                if items_found >= max_per_source:
                    print(f"  Reached limit of {max_per_source} items for Kleinanzeigen")
                    break
                search_url = f"{base_url}?keywords={term.replace(' ', '+')}"
                print(f"  Searching Kleinanzeigen for: {term}")
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Parse listings (adjust selectors based on actual site structure)
                    listings = soup.find_all('article', class_='aditem')
                    print(f"  Found {len(listings)} listings on Kleinanzeigen for '{term}'")

                    for listing in listings:
                        if items_found >= max_per_source:
                            break

                        try:
                            title_elem = listing.find('a', class_='ellipsis')
                            price_elem = listing.find('p', class_='aditem-main--middle--price-shipping--price')

                            # Find image
                            image_url = ''
                            img_elem = listing.find('img')
                            if img_elem:
                                image_url = img_elem.get('src', '') or img_elem.get('data-src', '')

                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                url = 'https://www.kleinanzeigen.de' + title_elem['href']
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'

                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'Kleinanzeigen',
                                    'image_url': image_url
                                }

                                self.results.append(item)
                                self.save_item(item)
                                items_found += 1
                                print(f"  ✓ Item found: {title[:50]}...")
                        except Exception as e:
                            print(f"  Error parsing listing: {e}")
                            continue

                time.sleep(2)  # Be polite, wait between requests

        except Exception as e:
            print(f"Error searching Kleinanzeigen: {e}")

    def search_ebay(self):
        """Search eBay Germany"""
        print("Searching eBay...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        max_per_source = self.config.get('max_results_per_source', 10)
        items_found = 0

        try:
            for term in self.config['search_terms']:
                if items_found >= max_per_source:
                    print(f"  Reached limit of {max_per_source} items for eBay Germany")
                    break
                # eBay Germany search URL
                search_url = f"https://www.ebay.de/sch/i.html?_nkw={term.replace(' ', '+')}&_sacat=11450"
                print(f"  Searching eBay Germany for: {term}")
                response = requests.get(search_url, headers=headers, timeout=30)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # eBay uses ul.srp-results container
                    results_container = soup.find('ul', class_='srp-results')
                    listings = []
                    if results_container:
                        listings = results_container.find_all('li', class_='s-card', recursive=False)

                    print(f"  Found {len(listings)} listings on eBay Germany for '{term}'")

                    for listing in listings:
                        if items_found >= max_per_source:
                            break

                        try:
                            # Find title - any div with "title" in class
                            title_elem = listing.find('div', class_=lambda x: x and 'title' in str(x).lower())

                            # Find link - any a with "/itm/" in href
                            link_elem = listing.find('a', href=lambda x: x and '/itm/' in str(x))

                            # Find price - any span with "price" in class
                            price_elem = listing.find('span', class_=lambda x: x and 'price' in str(x))

                            # Find image
                            image_url = ''
                            img_elem = listing.find('img')
                            if img_elem:
                                image_url = img_elem.get('src', '') or img_elem.get('data-src', '')

                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                # Skip eBay's "Shop on eBay" header item
                                if title.lower() in ['shop on ebay', 'ergebnisse']:
                                    continue

                                url = link_elem['href']
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'

                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'eBay',
                                    'image_url': image_url
                                }

                                self.results.append(item)
                                self.save_item(item)
                                items_found += 1
                                print(f"  ✓ Item found: {title[:50]}...")
                        except Exception as e:
                            print(f"Error parsing eBay listing: {e}")
                            continue

                time.sleep(2)

        except Exception as e:
            print(f"Error searching eBay: {e}")

    def search_ebay_uk(self):
        """Search eBay UK"""
        print("Searching eBay UK...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        max_per_source = self.config.get('max_results_per_source', 10)
        items_found = 0

        try:
            for term in self.config['search_terms']:
                if items_found >= max_per_source:
                    print(f"  Reached limit of {max_per_source} items for eBay UK")
                    break
                # eBay UK search URL
                search_url = f"https://www.ebay.co.uk/sch/i.html?_nkw={term.replace(' ', '+')}&_sacat=11450"
                print(f"  Searching eBay UK for: {term}")
                response = requests.get(search_url, headers=headers, timeout=30)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # eBay uses ul.srp-results container
                    results_container = soup.find('ul', class_='srp-results')
                    listings = []
                    if results_container:
                        listings = results_container.find_all('li', class_='s-card', recursive=False)

                    print(f"  Found {len(listings)} listings on eBay UK for '{term}'")

                    for listing in listings:
                        if items_found >= max_per_source:
                            break

                        try:
                            # Find title - any div with "title" in class
                            title_elem = listing.find('div', class_=lambda x: x and 'title' in str(x).lower())

                            # Find link - any a with "/itm/" in href
                            link_elem = listing.find('a', href=lambda x: x and '/itm/' in str(x))

                            # Find price - any span with "price" in class
                            price_elem = listing.find('span', class_=lambda x: x and 'price' in str(x))

                            # Find image
                            image_url = ''
                            img_elem = listing.find('img')
                            if img_elem:
                                image_url = img_elem.get('src', '') or img_elem.get('data-src', '')

                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                # Skip eBay's "Shop on eBay" header item
                                if title.lower() in ['shop on ebay', 'results']:
                                    continue

                                url = link_elem['href']
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'

                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'eBay UK',
                                    'image_url': image_url
                                }

                                self.results.append(item)
                                self.save_item(item)
                                items_found += 1
                                print(f"  ✓ Item found: {title[:50]}...")
                        except Exception as e:
                            print(f"Error parsing eBay UK listing: {e}")
                            continue

                time.sleep(2)

        except Exception as e:
            print(f"Error searching eBay UK: {e}")

    def search_vinted(self):
        """Search Vinted"""
        print("Searching Vinted...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            for term in self.config['search_terms']:
                search_url = f"https://www.vinted.de/vetements?search_text={term.replace(' ', '+')}"
                print(f"  Searching Vinted for: {term}")
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Vinted uses dynamic loading, so basic scraping might not get all items
                    # This is a simplified version - might need Selenium for full results
                    listings = soup.find_all('div', class_='feed-grid__item')
                    print(f"  Found {len(listings)} listings on Vinted for '{term}' (Note: Vinted uses JavaScript, may show 0)")

                    for listing in listings[:10]:
                        try:
                            title_elem = listing.find('h3')
                            link_elem = listing.find('a')
                            price_elem = listing.find('span', class_='price')
                            
                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                url = 'https://www.vinted.de' + link_elem['href']
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'
                                
                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'Vinted'
                                }
                                
                                if not self.is_item_seen(item['id']):
                                    self.results.append(item)
                                    self.mark_item_seen(item)
                        except Exception as e:
                            print(f"Error parsing Vinted listing: {e}")
                            continue
                
                time.sleep(2)
                
        except Exception as e:
            print(f"Error searching Vinted: {e}")
    
    def search_google_shopping(self):
        """Search Google Shopping via SerpAPI"""
        print("Searching Google Shopping (via SerpAPI)...")

        serpapi_key = os.environ.get('SERPAPI_KEY')
        print(f"  DEBUG: SERPAPI_KEY present: {bool(serpapi_key)}")
        if serpapi_key:
            print(f"  DEBUG: SERPAPI_KEY length: {len(serpapi_key)} chars")
            print(f"  DEBUG: SERPAPI_KEY starts with: {serpapi_key[:8]}...")
        if not serpapi_key:
            print("  ⚠ SERPAPI_KEY not found, skipping Google Shopping")
            return

        max_per_source = self.config.get('max_results_per_source', 10)
        items_found = 0

        try:
            for term in self.config['search_terms']:
                if items_found >= max_per_source:
                    print(f"  Reached limit of {max_per_source} items for Google Shopping")
                    break
                print(f"  Searching Google Shopping for: {term}")

                # SerpAPI request
                params = {
                    "api_key": serpapi_key,
                    "q": term,
                    "tbm": "shop",  # Shopping results
                    "location": "Germany",
                    "hl": "en",  # Language
                    "gl": "de",  # Country
                }

                response = requests.get("https://serpapi.com/search", params=params, timeout=15)

                if response.status_code == 200:
                    data = response.json()
                    shopping_results = data.get('shopping_results', [])

                    print(f"  Found {len(shopping_results)} products on Google Shopping for '{term}'")

                    for idx, result in enumerate(shopping_results):
                        if items_found >= max_per_source:
                            break

                        try:
                            title = result.get('title', 'No title')
                            price = result.get('price', 'N/A')
                            link = result.get('product_link', '')  # SerpAPI uses 'product_link', not 'link'
                            source = result.get('source', 'Unknown Store')
                            image_url = result.get('thumbnail', '')

                            if not link:
                                print(f"  DEBUG: Skipping item {idx} - no product_link")
                                continue

                            item = {
                                'id': self.generate_item_id(title, link),
                                'title': title,
                                'url': link,
                                'price': price,
                                'source': f'Google Shopping ({source})',
                                'image_url': image_url
                            }

                            self.results.append(item)
                            self.save_item(item)
                            items_found += 1
                            print(f"  ✓ Item found: {title[:50]}...")

                        except Exception as e:
                            print(f"  Error parsing Google Shopping result: {e}")
                            continue

                else:
                    print(f"  ⚠ SerpAPI returned status {response.status_code}")

                time.sleep(2)  # Be polite between requests

        except Exception as e:
            print(f"Error searching Google Shopping: {e}")

    def search_google(self):
        """Search via Google (for general web results)"""
        print("Searching Google...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            for term in self.config['search_terms']:
                # Add "vintage coat" and location to search
                query = f"{term} vintage coat berlin"
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=10"
                print(f"  Searching Google for: {query}")

                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Parse Google search results
                    search_results = soup.find_all('div', class_='g')
                    print(f"  Found {len(search_results)} results on Google for '{query}'")

                    for result in search_results[:5]:  # Top 5 results
                        try:
                            title_elem = result.find('h3')
                            link_elem = result.find('a')
                            
                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                url = link_elem['href']
                                
                                # Skip if not a relevant domain
                                if any(skip in url.lower() for skip in ['google.com', 'youtube.com']):
                                    continue
                                
                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': 'N/A',
                                    'source': 'Google Search'
                                }
                                
                                if not self.is_item_seen(item['id']):
                                    self.results.append(item)
                                    self.mark_item_seen(item)
                        except Exception as e:
                            print(f"Error parsing Google result: {e}")
                            continue
                
                time.sleep(3)  # Be extra polite with Google
                
        except Exception as e:
            print(f"Error searching Google: {e}")

    def search_vintage_threads(self):
        """Search Vintage Threads"""
        print("Searching Vintage Threads...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            for term in self.config['search_terms']:
                # Vintage Threads search URL structure
                search_url = f"https://vintage-threads.com/search?q={term.replace(' ', '+')}"
                print(f"  Searching Vintage Threads for: {term}")
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Common e-commerce patterns - adjust if needed
                    listings = soup.find_all('div', class_=['product-item', 'product', 'item'])
                    if not listings:
                        listings = soup.find_all('article')

                    print(f"  Found {len(listings)} listings on Vintage Threads for '{term}'")

                    for listing in listings[:10]:
                        try:
                            # Try common selector patterns
                            title_elem = listing.find(['h2', 'h3', 'h4'], class_=re.compile('product|title|name'))
                            if not title_elem:
                                title_elem = listing.find('a', class_=re.compile('product|title'))

                            link_elem = listing.find('a', href=True)
                            price_elem = listing.find(['span', 'div', 'p'], class_=re.compile('price'))

                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                url = link_elem['href']
                                if not url.startswith('http'):
                                    url = 'https://vintage-threads.com' + url
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'

                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'Vintage Threads'
                                }

                                if not self.is_item_seen(item['id']):
                                    self.results.append(item)
                                    self.mark_item_seen(item)
                        except Exception as e:
                            print(f"Error parsing Vintage Threads listing: {e}")
                            continue

                time.sleep(2)

        except Exception as e:
            print(f"Error searching Vintage Threads: {e}")

    def search_vilis_vintage(self):
        """Search Vilis Vintage"""
        print("Searching Vilis Vintage...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            for term in self.config['search_terms']:
                # Vilis Vintage search URL structure
                search_url = f"https://www.vilisvintage.com/search?q={term.replace(' ', '+')}"
                print(f"  Searching Vilis Vintage for: {term}")
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Common e-commerce patterns
                    listings = soup.find_all('div', class_=['product-item', 'product', 'item'])
                    if not listings:
                        listings = soup.find_all('article')

                    print(f"  Found {len(listings)} listings on Vilis Vintage for '{term}'")

                    for listing in listings[:10]:
                        try:
                            title_elem = listing.find(['h2', 'h3', 'h4'], class_=re.compile('product|title|name'))
                            if not title_elem:
                                title_elem = listing.find('a', class_=re.compile('product|title'))

                            link_elem = listing.find('a', href=True)
                            price_elem = listing.find(['span', 'div', 'p'], class_=re.compile('price'))

                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                url = link_elem['href']
                                if not url.startswith('http'):
                                    url = 'https://www.vilisvintage.com' + url
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'

                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'Vilis Vintage'
                                }

                                if not self.is_item_seen(item['id']):
                                    self.results.append(item)
                                    self.mark_item_seen(item)
                        except Exception as e:
                            print(f"Error parsing Vilis Vintage listing: {e}")
                            continue

                time.sleep(2)

        except Exception as e:
            print(f"Error searching Vilis Vintage: {e}")

    def search_etsy(self):
        """Search Etsy"""
        print("Searching Etsy...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            for term in self.config['search_terms']:
                # Etsy search URL structure
                search_url = f"https://www.etsy.com/search?q={term.replace(' ', '+')}"
                print(f"  Searching Etsy for: {term}")
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Etsy uses data-listing-id attributes
                    listings = soup.find_all('div', {'data-listing-id': True})
                    if not listings:
                        # Fallback to other common patterns
                        listings = soup.find_all('div', class_=re.compile('listing'))

                    print(f"  Found {len(listings)} listings on Etsy for '{term}' (Note: Etsy uses JavaScript, may show 0)")

                    for listing in listings[:10]:
                        try:
                            title_elem = listing.find('h3')
                            if not title_elem:
                                title_elem = listing.find('h2')

                            link_elem = listing.find('a', href=True)
                            price_elem = listing.find('span', class_=re.compile('price'))

                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                url = link_elem['href']
                                if not url.startswith('http'):
                                    url = 'https://www.etsy.com' + url
                                price = price_elem.get_text(strip=True) if price_elem else 'N/A'

                                item = {
                                    'id': self.generate_item_id(title, url),
                                    'title': title,
                                    'url': url,
                                    'price': price,
                                    'source': 'Etsy'
                                }

                                if not self.is_item_seen(item['id']):
                                    self.results.append(item)
                                    self.mark_item_seen(item)
                        except Exception as e:
                            print(f"Error parsing Etsy listing: {e}")
                            continue

                time.sleep(2)

        except Exception as e:
            print(f"Error searching Etsy: {e}")

    
    def run(self):
        """Run all searches and send results"""
        print(f"Starting vintage coat search at {datetime.now()}")
        print(f"Search terms: {self.config['search_terms']}")
        
        # Run searches based on config
        # Google Shopping first - most varied results from 50+ stores
        if self.config.get('search_google_shopping', True):
            self.search_google_shopping()

        if self.config.get('search_kleinanzeigen', True):
            self.search_kleinanzeigen()

        if self.config.get('search_ebay', True):
            self.search_ebay()

        if self.config.get('search_ebay_uk', True):
            self.search_ebay_uk()

        if self.config.get('search_vinted', True):
            self.search_vinted()

        if self.config.get('search_google', True):
            self.search_google()

        if self.config.get('search_vintage_threads', True):
            self.search_vintage_threads()

        if self.config.get('search_vilis_vintage', True):
            self.search_vilis_vintage()

        if self.config.get('search_etsy', True):
            self.search_etsy()

        print(f"\nSearch complete. Found {len(self.results)} items.")


if __name__ == '__main__':
    finder = VintageCoatFinder()
    finder.run()
