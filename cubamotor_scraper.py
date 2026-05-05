#!/usr/bin/env python3
"""
CubaMotor Scraper - Extrae autos electricos desde cubamotor.com
Sitio WordPress con filtro por tipo de combustible.
"""

import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

CUBAMOTOR_BASE = "https://www.cubamotor.com"
CUBAMOTOR_EV_URL = f"{CUBAMOTOR_BASE}/autos/"

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
        print(f"  [CubaMotor] Error: {e}")
        return None


def _extract_price(text: str) -> Optional[float]:
    m = re.search(r'\$([\d,]+)', text)
    if m:
        try:
            return float(m.group(1).replace(',', ''))
        except ValueError:
            pass
    return None


def get_cubamotor_ads(max_results: int = 20) -> List[Dict]:
    """Obtiene autos electricos de CubaMotor."""
    print("  [CubaMotor] Buscando autos electricos...")

    html = _fetch(CUBAMOTOR_EV_URL)
    if not html:
        return []

    soup = BeautifulSoup(html, 'lxml')
    ads = []
    seen = set()

    # Listings link to /listings/<slug>/
    for link in soup.find_all('a', href=re.compile(r'/listings/')):
        if len(ads) >= max_results:
            break
        href = link['href']
        if href in seen:
            continue
        seen.add(href)

        card = link.find_parent('article') or link.find_parent('div', class_=re.compile(r'listing|card'))
        if not card:
            continue

        card_text = card.get_text()

        # Filter: only electric
        if 'electrico' not in card_text.lower() and 'ev' not in card_text.lower():
            continue

        title = link.get_text(strip=True)
        if not title or len(title) < 3:
            continue

        price = _extract_price(card_text)
        img = card.find('img')
        thumb = img.get('src', '') if img else ''

        ads.append({
            'id': f"cubamotor_{re.sub(r'[^a-z0-9]', '', title.lower())[:20]}",
            'title': title,
            'price': price,
            'currency': 'USD',
            'url': href,
            'description': card_text[:1000],
            'specs': None,
            'images': [thumb] if thumb else [],
            'source': 'cubamotor',
            'source_label': 'CubaMotor',
            'contact_phone': '',
            'contact_whatsapp': '',
            'contact_name': '',
            'province': '',
            'municipality': '',
        })

    print(f"  [CubaMotor] {len(ads)} vehiculos electricos encontrados")
    return ads


if __name__ == '__main__':
    ads = get_cubamotor_ads(10)
    for ad in ads:
        print(f"\n--- {ad['title']} ---")
        print(f"Precio: {ad['price']} {ad['currency']}")
        print(f"URL: {ad['url']}")
