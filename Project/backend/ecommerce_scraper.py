"""
Web scraper for fetching phones from Indian e-commerce platforms
Amazon & Flipkart
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict

class EcommerceScraper:
    """Scrape phones from Amazon and Flipkart"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_flipkart(self, query: str, max_results: int = 10) -> List[Dict]:
        """Scrape phones from Flipkart"""
        try:
            url = f"https://www.flipkart.com/search?q={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            phones = []
            
            # Find product containers
            products = soup.find_all('div', {'class': '_1AtVbE'})
            
            for product in products[:max_results]:
                try:
                    name = product.find('a', {'class': 's1Q9rs'})
                    price = product.find('div', {'class': '_30jeq3'})
                    rating = product.find('div', {'class': '_3LWZlK'})
                    
                    if name and price:
                        phones.append({
                            'name': name.text.strip(),
                            'price': int(re.sub(r'[^\d]', '', price.text.split(',')[0])),
                            'platform': 'Flipkart',
                            'rating': float(rating.text) if rating else 4.0,
                            'url': 'flipkart.com'
                        })
                except:
                    continue
            
            return phones
        except Exception as e:
            print(f"⚠️  Flipkart scraping error: {e}")
            return []
    
    def scrape_amazon(self, query: str, max_results: int = 10) -> List[Dict]:
        """Scrape phones from Amazon India"""
        try:
            url = f"https://www.amazon.in/s?k={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            phones = []
            
            # Find product containers
            products = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for product in products[:max_results]:
                try:
                    name = product.find('h2', {'class': 's-line-clamp-2'})
                    price = product.find('span', {'class': 'a-price-whole'})
                    rating = product.find('span', {'class': 'a-icon-star-small'})
                    
                    if name and price:
                        phones.append({
                            'name': name.text.strip(),
                            'price': int(re.sub(r'[^\d]', '', price.text.split(',')[0])),
                            'platform': 'Amazon',
                            'rating': float(rating.text.split()[0]) if rating else 4.0,
                            'url': 'amazon.in'
                        })
                except:
                    continue
            
            return phones
        except Exception as e:
            print(f"⚠️  Amazon scraping error: {e}")
            return []
    
    def search_all(self, query: str = "smartphone", max_results: int = 5) -> Dict:
        """Search all platforms"""
        print(f"\n🔍 Searching for '{query}' on e-commerce platforms...")
        print("   (This may take a moment...)\n")
        
        results = {
            'flipkart': self.scrape_flipkart(query, max_results),
            'amazon': self.scrape_amazon(query, max_results)
        }
        
        return results

# Fallback: Sample data from Indian platforms (when scraping fails)
SAMPLE_ECOMMERCE_DATA = {
    'flipkart': [
        {
            'name': 'Redmi 12',
            'brand': 'Xiaomi',
            'price': 8999,
            'ram': 4,
            'storage': 64,
            'camera': 50,
            'battery': 5000,
            'rating': 3.9,
            'platform': 'Flipkart',
            'url': 'flipkart.com/redmi-12'
        },
        {
            'name': 'Realme C55',
            'brand': 'Realme',
            'price': 10999,
            'ram': 4,
            'storage': 128,
            'camera': 50,
            'battery': 5000,
            'rating': 4.0,
            'platform': 'Flipkart',
            'url': 'flipkart.com/realme-c55'
        },
        {
            'name': 'Infinix Note 30',
            'brand': 'Infinix',
            'price': 12499,
            'ram': 6,
            'storage': 128,
            'camera': 50,
            'battery': 5000,
            'rating': 4.1,
            'platform': 'Flipkart',
            'url': 'flipkart.com/infinix-note30'
        },
        {
            'name': 'POCO X5 Pro',
            'brand': 'POCO',
            'price': 15999,
            'ram': 6,
            'storage': 128,
            'camera': 108,
            'battery': 5000,
            'rating': 4.3,
            'platform': 'Flipkart',
            'url': 'flipkart.com/poco-x5'
        },
        {
            'name': 'Redmi Note 13',
            'brand': 'Xiaomi',
            'price': 18999,
            'ram': 6,
            'storage': 128,
            'camera': 108,
            'battery': 5000,
            'rating': 4.2,
            'platform': 'Flipkart',
            'url': 'flipkart.com/redmi-note-13'
        },
        {
            'name': 'Realme 12',
            'brand': 'Realme',
            'price': 21999,
            'ram': 6,
            'storage': 128,
            'camera': 50,
            'battery': 5000,
            'rating': 4.1,
            'platform': 'Flipkart',
            'url': 'flipkart.com/realme-12'
        },
        {
            'name': 'Tecno Spark 10',
            'brand': 'Tecno',
            'price': 9999,
            'ram': 4,
            'storage': 128,
            'camera': 50,
            'battery': 5000,
            'rating': 3.8,
            'platform': 'Flipkart',
            'url': 'flipkart.com/tecno-spark10'
        },
    ],
    'amazon': [
        {
            'name': 'Motorola G24',
            'brand': 'Motorola',
            'price': 11999,
            'ram': 4,
            'storage': 128,
            'camera': 50,
            'battery': 5000,
            'rating': 4.0,
            'platform': 'Amazon',
            'url': 'amazon.in/moto-g24'
        },
        {
            'name': 'Samsung Galaxy M14',
            'brand': 'Samsung',
            'price': 13999,
            'ram': 4,
            'storage': 128,
            'camera': 50,
            'battery': 5000,
            'rating': 4.1,
            'platform': 'Amazon',
            'url': 'amazon.in/samsung-m14'
        },
        {
            'name': 'Honor 90 Lite',
            'brand': 'Honor',
            'price': 17999,
            'ram': 6,
            'storage': 128,
            'camera': 50,
            'battery': 4500,
            'rating': 4.2,
            'platform': 'Amazon',
            'url': 'amazon.in/honor-90lite'
        },
        {
            'name': 'Samsung Galaxy A15',
            'brand': 'Samsung',
            'price': 28999,
            'ram': 8,
            'storage': 256,
            'camera': 50,
            'battery': 5000,
            'rating': 4.4,
            'platform': 'Amazon',
            'url': 'amazon.in/samsung-a15'
        },
        {
            'name': 'OnePlus Nord CE 4',
            'brand': 'OnePlus',
            'price': 39999,
            'ram': 8,
            'storage': 128,
            'camera': 50,
            'battery': 5500,
            'rating': 4.3,
            'platform': 'Amazon',
            'url': 'amazon.in/oneplus-nord'
        },
        {
            'name': 'iQOO Z9 5G',
            'brand': 'iQOO',
            'price': 29999,
            'ram': 8,
            'storage': 256,
            'camera': 50,
            'battery': 5000,
            'rating': 4.2,
            'platform': 'Amazon',
            'url': 'amazon.in/iqoo-z9'
        },
    ]
}

def get_ecommerce_phones():
    """Get phones from e-commerce platforms (with fallback)"""
    try:
        scraper = EcommerceScraper()
        results = scraper.search_all(query="smartphone", max_results=3)
        
        all_phones = []
        for platform_phones in results.values():
            all_phones.extend(platform_phones)
        
        if all_phones:
            return all_phones
    except Exception as e:
        print(f"⚠️  Web scraping failed: {e}")
    
    # Fallback to sample data
    print("✅ Using sample data from Indian platforms...\n")
    all_phones = SAMPLE_ECOMMERCE_DATA['flipkart'] + SAMPLE_ECOMMERCE_DATA['amazon']
    return all_phones
