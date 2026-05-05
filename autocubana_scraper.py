#!/usr/bin/env python3
"""
AutoCubana Scraper - Extrae anuncios de autos electricos desde autocubana.com
Sitio de clasificados similar a Revolico (particulares e importadores).
"""

import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

AUTOCUBANA_BASE = "https://autocubana.com"
AUTOCUBANA_EV_URL = f"{AUTOCUBANA_BASE}/electric_cars?car_type=carros&ev_type=ev"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}


def fetch_ev_page() -> Optional[str]:
    try:
        response = requests.get(AUTOCUBANA_EV_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  [AutoCubana] Error fetching EV page: {e}")
        return None


def extract_listings(html: str) -> List[Dict]:
    """Extrae listado de autos electricos desde AutoCubana."""
    soup = BeautifulSoup(html, 'lxml')
    ads = []

    # AutoCubana uses listing cards, typically in article or div with specific patterns
    for card in soup.find_all(['article', 'div'], class_=re.compile(r'listing|ad-listing|card', re.I)):
        title_el = card.find(['h2', 'h3', 'a'])
        title = title_el.get_text(strip=True) if title_el else ""
        
        if not title:
            continue

        # URL
        link = card.find('a', href=True)
        url = link.get('href', '')
        if url and not url.startswith('http'):
            url = f"{AUTOCUBANA_BASE}{url}"
        
        # Price
        price_text = ""
        price_el = card.find(string=re.compile(r'[\d,]+', re.I))
        if price_el:
            price_text = price_el.strip()
        
        # Check for EV indicators
        text = card.get_text().lower()
        ev_keywords = ['electric', 'ev', 'electrico', 'electrica', 'tesla', 'nissan leaf', 'byd', 'bolt']
        if not any(kw in text for kw in ev_keywords) and 'electric' not in url.lower():
            continue

        ads.append({
            "title": title,
            "url": url,
            "price_text": price_text,
            "source": "autocubana",
        })

    # Deduplicate
    seen = set()
    unique = []
    for ad in ads:
        if ad["url"] not in seen and ad["url"]:
            seen.add(ad["url"])
            unique.append(ad)

    return unique


def get_autocubana_ads(max_results: int = 20) -> List[Dict]:
    """Obtiene anuncios de autos electricos de AutoCubana."""
    print("  [AutoCubana] Buscando EVs en clasificados...")

    html = fetch_ev_page()
    if not html:
        return []

    ads = extract_listings(html)
    print(f"  [AutoCubana] Encontrados {len(ads)} anuncios de EVs")

    return ads[:max_results]


if __name__ == "__main__":
    ads = get_autocubana_ads(10)
    print(f"\nEncontrados {len(ads)} anuncios en AutoCubana")
    for ad in ads:
        print(f"\n--- {ad['title']} ---")
        print(f"URL: {ad['url']}")
