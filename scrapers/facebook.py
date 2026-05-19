#!/usr/bin/env python3
"""
Facebook Marketplace / Groups Scraper

Nota: Facebook bloquea scraping automatizado. Esta implementacion
requiere cookies de sesion manuales o una API configurada.
"""

SOURCE_ID = "facebook"
SOURCE_LABEL = "Facebook"

from typing import List, Dict, Optional
import re
import os
import json

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


FACEBOOK_GROUP_URL = os.getenv("FACEBOOK_GROUP_URL", "")
FACEBOOK_COOKIES_FILE = os.getenv("FACEBOOK_COOKIES_FILE", "")


def get_facebook_ads(max_results: int = 20) -> List[Dict]:
    if not FACEBOOK_GROUP_URL:
        return []

    if not SELENIUM_AVAILABLE:
        return []

    ads = []

    try:
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(options=opts)

        if FACEBOOK_COOKIES_FILE and os.path.exists(FACEBOOK_COOKIES_FILE):
            with open(FACEBOOK_COOKIES_FILE) as f:
                cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.get(FACEBOOK_GROUP_URL)
        driver.implicitly_wait(10)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for post in soup.select('[class*=post], [class*=article], [role=article]')[:max_results]:
            try:
                text_el = post.select_one('p, [class*=message], [class*=content]')
                title = text_el.get_text(strip=True)[:100] if text_el else "Publicacion de Facebook"

                link_el = post.select_one('a[href*=/groups/], a[href*=/marketplace/]')
                url = link_el.get('href', '') if link_el else FACEBOOK_GROUP_URL
                if url and not url.startswith('http'):
                    url = 'https://facebook.com' + url

                img_el = post.select_one('img')
                images = [img_el.get('src', '')] if img_el and img_el.get('src') else []

                ads.append({
                    'id': f"facebook_{re.sub(r'[^a-z0-9]', '', title.lower())[:20]}",
                    'title': title,
                    'price': 0,
                    'currency': 'USD',
                    'url': url,
                    'description': title,
                    'specs': None,
                    'images': images[:3],
                    'source': 'facebook',
                    'source_label': 'Facebook',
                    'contact_phone': '',
                    'contact_whatsapp': '',
                    'contact_name': '',
                    'province': '',
                    'municipality': '',
                })
            except Exception:
                continue

        driver.quit()
    except Exception:
        pass

    return ads


if __name__ == '__main__':
    ads = get_facebook_ads(3)
    print(f"{len(ads)} anuncios")
