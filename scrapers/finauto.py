#!/usr/bin/env python3
"""
Finauto Scraper - Catalogo de autos desde finauto.com.cu
"""

SOURCE_ID = "finauto"
SOURCE_LABEL = "Finauto"

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re

BASE_URL = "https://finauto.com.cu"
SEARCH_PATHS = ["/inventario", "/autos-electricos", "/catalogo"]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
}


def _fetch(url: str) -> Optional[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        return None


def _parse_price(text: str) -> Optional[float]:
    m = re.search(r'([\d,.]+)\s*(USD|CUP|EUR|\$|CUC)', text)
    if m:
        try:
            return float(m.group(1).replace(',', ''))
        except ValueError:
            pass
    return None


def get_finauto_ads(max_results: int = 20) -> List[Dict]:
    ads = []

    for path in SEARCH_PATHS:
        if len(ads) >= max_results:
            break
        html = _fetch(BASE_URL + path)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.select('.product, .item, .vehicle, [class*=product], [class*=car], article, .card')[:max_results]:
            try:
                title_el = item.select_one('h2, h3, h4, .title, [class*=title], .nombre')
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if not title:
                    continue

                link = title_el if title_el.name == 'a' else item.select_one('a[href]')
                url = link.get('href', '') if link else ''
                if url and not url.startswith('http'):
                    url = BASE_URL + url

                price_el = item.select_one('.price, [class*=price], .precio, .amount')
                price_text = price_el.get_text(strip=True) if price_el else ''
                price = _parse_price(price_text)

                img_el = item.select_one('img')
                images = [img_el.get('src', '')] if img_el and img_el.get('src') else []

                desc_el = item.select_one('.description, [class*=desc], .info, p')
                description = desc_el.get_text(strip=True)[:2000] if desc_el else ''

                ads.append({
                    'id': f"finauto_{re.sub(r'[^a-z0-9]', '', title.lower())[:20]}",
                    'title': title,
                    'price': price or 0,
                    'currency': 'USD',
                    'url': url,
                    'description': description,
                    'specs': None,
                    'images': images[:3],
                    'source': 'finauto',
                    'source_label': 'Finauto',
                    'contact_phone': '',
                    'contact_whatsapp': '',
                    'contact_name': '',
                    'province': '',
                    'municipality': '',
                })
            except Exception:
                continue

    return ads


if __name__ == '__main__':
    ads = get_finauto_ads(3)
    for ad in ads:
        print(f"\n--- {ad['title']} ---")
        print(f"Precio: {ad['price']} {ad['currency']}")
        print(f"URL: {ad['url']}")
