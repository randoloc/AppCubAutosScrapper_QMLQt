#!/usr/bin/env python3
"""
Revolico Scraper - Extrae anuncios de autos eléctricos desde Revolico.com
"""

import requests
import re
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from config import REVOLICO_BASE_URL, EV_INDICATORS, SEARCH_KEYWORDS

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}


def is_electric_vehicle(title: str, description: str = "") -> bool:
    """Determina si un anuncio es de un vehículo eléctrico basado en palabras clave."""
    text = f"{title} {description}".lower()
    return any(indicator.lower() in text for indicator in EV_INDICATORS)


def fetch_search_page(query: str, page: int = 1) -> Optional[Dict]:
    """Obtiene una página de resultados de búsqueda de Revolico."""
    url = f"{REVOLICO_BASE_URL}/search"
    params = {
        "category": "vehiculos",
        "subcategory": "vehiculos-carros",
        "q": query,
        "page": page,
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return parse_next_data(response.text)
    except Exception as e:
        print(f"Error fetching search page: {e}")
        return None


def parse_next_data(html: str) -> Optional[Dict]:
    """Extrae el JSON de __NEXT_DATA__ del HTML."""
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def extract_ads_from_data(data: Dict) -> List[Dict]:
    """Extrae lista de anuncios desde los datos Apollo/GraphQL."""
    ads = []
    if not data:
        return ads
    
    apollo_state = data.get("props", {}).get("pageProps", {}).get("__APOLLO_STATE__", {})
    root_query = apollo_state.get("ROOT_QUERY", {})
    
    # Find adsPerPage key
    ads_key = None
    for key in root_query.keys():
        if "adsPerPage" in key:
            ads_key = key
            break
    
    if not ads_key:
        return ads
    
    ads_data = root_query[ads_key]
    if not isinstance(ads_data, dict):
        return ads
    
    edges = ads_data.get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        ref = node.get("__ref", "")
        if not ref:
            continue
        
        ad = apollo_state.get(ref)
        if not ad:
            continue
        
        ad_info = {
            "id": ad.get("id"),
            "title": ad.get("title", ""),
            "price": ad.get("price"),
            "currency": ad.get("currency", "USD"),
            "permalink": ad.get("permalink", ""),
            "url": f"{REVOLICO_BASE_URL}{ad.get('permalink', '')}",
            "images_count": ad.get("imagesCount", 0),
            "view_count": ad.get("viewCount", 0),
            "is_promoted": ad.get("isPromoted", False),
            "province_id": ad.get("provinceId"),
            "municipality_id": ad.get("municipalityId"),
            "contact_info": ad.get("contactInfo", {}),
            "phone_info": ad.get("phoneInfo", {}),
            "main_image": ad.get("mainImage"),
            "description": "",
            "contact_phone": None,
            "contact_whatsapp": None,
            "images": [],
        }
        
        # Extract phone info
        phone_info = ad.get("phoneInfo", {})
        if isinstance(phone_info, dict):
            ad_info["contact_phone"] = phone_info.get("number")
        
        ads.append(ad_info)
    
    return ads


def fetch_ad_details(ad: Dict) -> Dict:
    """Obtiene los detalles completos de un anuncio visitando su página."""
    url = ad["url"]
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        data = parse_next_data(response.text)
        if not data:
            return extract_details_from_html(response.text, ad)
        
        apollo_state = data.get("props", {}).get("pageProps", {}).get("__APOLLO_STATE__", {})
        ad_key = f"AdType:{ad['id']}"
        ad_data = apollo_state.get(ad_key)
        
        if not ad_data:
            # Fallback: try to extract from HTML
            return extract_details_from_html(response.text, ad)
        
        # Extract description
        ad["description"] = ad_data.get("description", "") or ad_data.get("shortDescription", "")
        
        # Extract images from readyImages (GraphQL refs)
        ad["images"] = []
        ready_images = ad_data.get("readyImages", [])
        for img_ref in ready_images[:5]:  # Limit to first 5
            if isinstance(img_ref, dict) and "__ref" in img_ref:
                ref = img_ref["__ref"]
                img_data = apollo_state.get(ref)
                if img_data and isinstance(img_data, dict) and "gcsKey" in img_data:
                    gcs = img_data["gcsKey"]
                    # Build URL using detail_desktop size
                    img_url = f"https://pic.revolico.com/{gcs}_detail_desktop.jpg"
                    ad["images"].append(img_url)
        
        # Fallback to mainImage if no readyImages
        if not ad["images"] and ad_data.get("mainImage"):
            main = ad_data["mainImage"]
            if isinstance(main, dict) and "gcsKey" in main:
                gcs = main["gcsKey"]
                ad["images"].append(f"https://pic.revolico.com/{gcs}_detail_desktop.jpg")
        
        # Extract contact info - seller name
        ad["contact_name"] = ad_data.get("name", "")
        
        # Extract phone info
        phone_info = ad_data.get("phoneInfo", {})
        if isinstance(phone_info, dict):
            first_phone = phone_info.get("firstPhone")
            if isinstance(first_phone, dict):
                prefix = first_phone.get("prefix", "")
                number = first_phone.get("number", "")
                if number:
                    ad["contact_phone"] = f"{prefix}{number}" if prefix else number
                    is_whatsapp = first_phone.get("isWhatsapp", False)
                    if is_whatsapp:
                        ad["contact_whatsapp"] = ad["contact_phone"]
            
            second_phone = phone_info.get("secondPhone")
            if isinstance(second_phone, dict):
                prefix2 = second_phone.get("prefix", "")
                number2 = second_phone.get("number", "")
                if number2 and not ad.get("contact_phone"):
                    ad["contact_phone"] = f"{prefix2}{number2}" if prefix2 else number2
        
        # Ensure WhatsApp falls back to phone
        if not ad.get("contact_whatsapp") and ad.get("contact_phone"):
            ad["contact_whatsapp"] = ad["contact_phone"]
        
        # Try to get price from ad_data if available
        if ad_data.get("price") is not None:
            ad["price"] = ad_data.get("price")
        
        # Extract location info - resolve __ref for province/municipality
        province_data = ad_data.get("province")
        municipality_data = ad_data.get("municipality")
        
        # Province can be a dict with __ref
        if isinstance(province_data, dict) and "__ref" in province_data:
            province_obj = apollo_state.get(province_data["__ref"])
            if province_obj:
                ad["province"] = province_obj.get("name", "")
        elif isinstance(province_data, dict):
            ad["province"] = province_data.get("name", "")
        elif isinstance(province_data, (int, str)):
            province_obj = apollo_state.get(f"ProvinceType:{province_data}")
            if province_obj:
                ad["province"] = province_obj.get("name", "")
        
        # Municipality can be a dict with __ref
        if isinstance(municipality_data, dict) and "__ref" in municipality_data:
            mun_obj = apollo_state.get(municipality_data["__ref"])
            if mun_obj:
                ad["municipality"] = mun_obj.get("name", "")
        elif isinstance(municipality_data, dict):
            ad["municipality"] = municipality_data.get("name", "")
        elif isinstance(municipality_data, (int, str)):
            mun_obj = apollo_state.get(f"MunicipalityType:{municipality_data}")
            if mun_obj:
                ad["municipality"] = mun_obj.get("name", "")
            
    except Exception as e:
        print(f"Error fetching details for ad {ad['id']}: {e}")
    
    return ad


def extract_details_from_html(html: str, ad: Dict) -> Dict:
    """Extracción fallback desde HTML si no hay datos Apollo."""
    soup = BeautifulSoup(html, 'lxml')
    
    # Try to find description
    desc_div = soup.find('div', string=re.compile(r'(?:Descripción|Detalles)', re.I))
    if desc_div:
        parent = desc_div.parent
        if parent:
            text = parent.get_text(separator='\n', strip=True)
            ad["description"] = text[:2000]
    
    # If no description found, try getting text from main content area
    if not ad["description"]:
        main_content = soup.find('main') or soup.find('article')
        if main_content:
            # Remove script and style elements
            for script in main_content.find_all(["script", "style"]):
                script.decompose()
            text = main_content.get_text(separator='\n', strip=True)
            ad["description"] = text[:2000]
    
    # Extract WhatsApp link
    wa_link = soup.find('a', href=re.compile(r'wa\.me'))
    if wa_link:
        href = wa_link.get('href', '')
        match = re.search(r'wa\.me/(\d+)', href)
        if match:
            ad["contact_whatsapp"] = match.group(1)
    
    # Extract all images
    img_tags = soup.find_all('img', src=re.compile(r'revolico\.com.*item.*\d+', re.I))
    ad["images"] = [img.get('src') for img in img_tags if img.get('src')][:10]
    
    return ad


def get_electric_ads(max_results: int = 20) -> List[Dict]:
    """Obtiene todos los anuncios de autos eléctricos disponibles."""
    all_ads = []
    seen_ids = set()
    
    # Use a few key search terms - most relevant for Cuba EV market
    search_terms = ["electrico", "tesla", "nissan leaf", "byd", "bmw i3", "kia ev"]
    
    for term in search_terms:
        print(f"Buscando: {term}...")
        data = fetch_search_page(term)
        if not data:
            continue
        
        ads = extract_ads_from_data(data)
        for ad in ads:
            if ad["id"] in seen_ids:
                continue
            
            # Check if it's electric
            if is_electric_vehicle(ad["title"]):
                seen_ids.add(ad["id"])
                all_ads.append(ad)
                if len(all_ads) >= max_results * 3:  # Get extra for filtering
                    break
        
        if len(all_ads) >= max_results * 3:
            break
    
    # Now fetch details for each ad
    print(f"Obteniendo detalles de {len(all_ads)} anuncios...")
    detailed_ads = []
    for ad in all_ads:
        detailed = fetch_ad_details(ad)
        # Re-check with description
        if not is_electric_vehicle(detailed["title"], detailed.get("description", "")):
            continue
        
        # Filter unrealistic prices (likely scams or parts)
        price = detailed.get("price")
        if price is not None and price < 1000:
            continue
            
        detailed_ads.append(detailed)
        if len(detailed_ads) >= max_results:
            break
    
    return detailed_ads


if __name__ == "__main__":
    ads = get_electric_ads(5)
    print(f"\nEncontrados {len(ads)} anuncios de autos eléctricos")
    for ad in ads:
        print(f"\n--- {ad['title']} ---")
        print(f"Precio: {ad['price']} {ad['currency']}")
        print(f"URL: {ad['url']}")
        print(f"Tel: {ad.get('contact_phone')} / WA: {ad.get('contact_whatsapp')}")
        print(f"Imágenes: {len(ad.get('images', []))}")
        print(f"Desc: {ad.get('description', '')[:200]}...")
