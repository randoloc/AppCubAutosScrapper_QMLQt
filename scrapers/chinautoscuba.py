#!/usr/bin/env python3
"""
ChinautosCuba Scraper - Extrae catalogo de autos electricos desde chinautoscuba.com
Sitio WordPress/WooCommerce con productos BYD y Changan.
"""

SOURCE_ID = "chinautoscuba"
SOURCE_LABEL = "ChinautosCuba"

import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

CHINAUTOS_BASE = "https://chinautoscuba.com"
CHINAUTOS_BYD_URL = f"{CHINAUTOS_BASE}/byd/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
}


def _fetch(url: str) -> Optional[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"  [ChinautosCuba] Error: {e}")
        return None


def get_chinautoscuba_ads(max_results: int = 20) -> List[Dict]:
    """Obtiene catalogo de autos electricos de ChinautosCuba (LXWY)."""
    print("  [ChinautosCuba] Obteniendo catalogo BYD EVs...")

    html = _fetch(CHINAUTOS_BYD_URL)
    if not html:
        return []

    soup = BeautifulSoup(html, 'lxml')
    ads = []
    seen = set()

    # Products link to /producto/<slug>/
    for link in soup.find_all('a', href=re.compile(r'/producto/')):
        if len(ads) >= max_results:
            break
        href = link['href']
        if href in seen:
            continue
        seen.add(href)

        title_el = link.find_next_sibling('h2') or link.parent.find(['h2', 'h3'])
        title = title_el.get_text(strip=True) if title_el else link.get_text(strip=True)
        if not title or len(title) < 3:
            continue

        # Thumbnail
        img = link.find('img')
        thumb = img.get('src', '') if img else ''

        # Fetch detail
        detail = _fetch(href)
        if not detail:
            continue

        dsoup = BeautifulSoup(detail, 'lxml')
        content = dsoup.find('div', class_='woocommerce-product-details__short-description') or dsoup.find('div', class_='entry-content')
        desc = content.get_text(separator=' ', strip=True)[:2000] if content else ''

        images = []
        if content:
            for img in content.find_all('img'):
                src = img.get('src', '') or img.get('data-src', '')
                if src and 'wp-content' in src:
                    images.append(src)

        ads.append({
            'id': f"chinautos_{re.sub(r'[^a-z0-9]', '', title.lower())[:20]}",
            'title': title,
            'price': None,
            'currency': 'USD',
            'url': href,
            'description': desc,
            'specs': None,
            'images': images[:3] or ([thumb] if thumb else []),
            'source': 'chinautoscuba',
            'source_label': 'LXWY (ChinautosCuba)',
            'contact_phone': '+53 53578277',
            'contact_whatsapp': '5353578277',
            'contact_name': 'LXWY Ventas',
            'province': 'La Habana',
            'municipality': 'Miramar',
        })

    print(f"  [ChinautosCuba] {len(ads)} vehiculos encontrados")
    return ads


if __name__ == '__main__':
    ads = get_chinautoscuba_ads(5)
    for ad in ads:
        print(f"\n--- {ad['title']} ---")
        print(f"URL: {ad['url']}")

get_ads = get_chinautoscuba_ads
