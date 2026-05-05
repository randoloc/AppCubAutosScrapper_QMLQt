#!/usr/bin/env python3
"""
Atrexport Scraper - Extrae catalogo de autos electricos desde atrexport.com

Sitio WordPress con portfolio de productos. Precios en EUR, todo incluido
hasta entrega en Mariel (compra, transporte, documentacion, nacionalizacion).
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re

ATREXPORT_BASE = "https://atrexport.com"
ATREXPORT_EV_URL = f"{ATREXPORT_BASE}/carros-electricos-en-cuba/"

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
        print(f"  [Atrexport] Error fetching {url}: {e}")
        return None


def _parse_price(text: str) -> Optional[float]:
    m = re.search(r'([\d,.]+)\s*[\u20ac]', text)
    if m:
        try:
            return float(m.group(1).replace('.', '').replace(',', '.'))
        except ValueError:
            pass
    return None


def _extract_specs(text: str) -> Dict:
    specs = {}
    patterns = {
        'autonomia_km': r'Autonomia[:\s]*(\d+)\s*KM',
        'pax': r'PAX[:\s]*(\d+)',
        'segmento': r'Segmento[:\s]*([^\n]+)',
        'medidas': r'Medidas\s*\(L-W-H\)[:\s]*([^\n]+)',
    }
    for key, pat in patterns.items():
        m = re.search(pat, text, re.I)
        if m:
            val = m.group(1).strip()
            specs[key] = int(val) if val.isdigit() else val
    return specs


def get_atrexport_ads(max_results: int = 20) -> List[Dict]:
    """Obtiene catalogo de autos electricos de Atrexport."""
    print("  [Atrexport] Obteniendo catalogo de EVs...")

    html = _fetch(ATREXPORT_EV_URL)
    if not html:
        return []

    soup = BeautifulSoup(html, 'lxml')
    ads = []
    seen_urls = set()

    # Portfolio items link to /portfolio/<slug>/
    for link in soup.find_all('a', href=True):
        if len(ads) >= max_results:
            break
        href = link['href']
        if '/portfolio/' not in href or href in seen_urls:
            continue
        seen_urls.add(href)

        # Find title from adjacent h2/h3
        title_el = link.find_next_sibling(['h2', 'h3'])
        if not title_el:
            title_el = link.parent.find(['h2', 'h3'])
        title = title_el.get_text(strip=True) if title_el else link.get_text(strip=True)
        if not title or len(title) < 4:
            continue

        url = href if href.startswith('http') else f"{ATREXPORT_BASE}{href}"

        # Fetch detail page
        detail = _fetch(url)
        if not detail:
            continue

        dsoup = BeautifulSoup(detail, 'lxml')
        full_text = dsoup.get_text(separator=' ', strip=True)

        # Extract description
        content = dsoup.find('div', class_='entry-content') or dsoup.find('article')
        desc = content.get_text(separator=' ', strip=True)[:2000] if content else full_text[:2000]

        # Extract images from content
        images = []
        if content:
            for img in content.find_all('img'):
                src = img.get('src', '') or img.get('data-src', '')
                if src and ('wp-content' in src or 'atrexport' in src):
                    images.append(src)

        ads.append({
            'id': f"atrexport_{re.sub(r'[^a-z0-9]', '', title.lower())[:20]}",
            'title': title,
            'price': _parse_price(full_text),
            'currency': 'EUR',
            'url': url,
            'description': desc,
            'specs': _extract_specs(full_text) or None,
            'images': images[:3],
            'source': 'atrexport',
            'source_label': 'ATR Export',
            'contact_phone': '+34 672 36 21 80',
            'contact_whatsapp': '34672362180',
            'contact_name': 'ATR Export',
            'province': 'Importacion (Mariel)',
            'municipality': '',
        })

    print(f"  [Atrexport] {len(ads)} vehiculos encontrados")
    return ads


if __name__ == '__main__':
    ads = get_atrexport_ads(3)
    for ad in ads:
        print(f"\n--- {ad['title']} ---")
        print(f"Precio: {ad['price']} {ad['currency']}")
        print(f"URL: {ad['url']}")
