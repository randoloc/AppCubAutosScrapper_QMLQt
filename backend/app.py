#!/usr/bin/env python3
"""
FastAPI Backend - API para busqueda de autos electricos en Cuba.
Expone los scrapers como endpoints REST con filtros.
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import threading

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BACKEND_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from scrapers.registry import registry
from enricher import enrich_ad

app = FastAPI(title="Cuba EV Scraper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "cache.db")
_cache_lock = threading.Lock()

ALL_SOURCE_IDS = ",".join(registry.source_ids)

DEFAULT_SOURCES = "revolico,atrexport,chinautoscuba,cubamotor"


@app.on_event("startup")
def startup_event():
    _init_db()


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            data TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def _cache_get(key: str, ttl_minutes: int = 30) -> Optional[list]:
    with _cache_lock:
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            "SELECT data, fetched_at FROM cache WHERE key = ?", (key,)
        ).fetchone()
        conn.close()
    if not row:
        return None
    fetched = datetime.fromisoformat(row[1])
    if datetime.now() - fetched > timedelta(minutes=ttl_minutes):
        return None
    try:
        return json.loads(row[0])
    except Exception:
        return None


def _cache_set(key: str, data: list):
    with _cache_lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR REPLACE INTO cache (key, data, fetched_at) VALUES (?, ?, ?)",
            (key, json.dumps(data, default=str), datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()


def _run_scrapers(sources: List[str], per_source: int) -> list:
    all_ads = []
    for src in sources:
        if registry.get(src):
            try:
                results = registry.run(src, per_source)
                all_ads.extend(results)
            except Exception as e:
                print(f"  [{src}] Error: {e}")
    return all_ads


def _filter_ads(ads: list, min_price: Optional[float], max_price: Optional[float],
                brand: Optional[str], province: Optional[str],
                fuel_type: Optional[str]) -> list:
    filtered = ads

    if min_price is not None:
        filtered = [a for a in filtered if a.get("price") is None or a["price"] >= min_price]

    if max_price is not None:
        filtered = [a for a in filtered if a["price"] is None or a["price"] <= max_price]

    if brand:
        b = brand.lower()
        filtered = [a for a in filtered if b in a.get("title", "").lower()
                    or b in a.get("description", "").lower()]

    if province:
        p = province.lower()
        filtered = [a for a in filtered if p in a.get("province", "").lower()
                    or p in a.get("municipality", "").lower()]

    if fuel_type:
        f = fuel_type.lower()
        filtered = [a for a in filtered if f in a.get("title", "").lower()
                    or f in a.get("description", "").lower()]

    enriched = []
    for ad in filtered:
        if not ad.get("specs"):
            ad = enrich_ad(ad)
        enriched.append(ad)

    return enriched


@app.get("/")
def root():
    return {"status": "ok", "service": "Cuba EV Scraper API"}


@app.get("/api/search")
def search(
    sources: str = Query(DEFAULT_SOURCES, description=f"Comma-separated: {ALL_SOURCE_IDS}"),
    max_ads: int = Query(50, ge=1, le=200),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    brand: Optional[str] = Query(None, description="Filter by brand/model"),
    province: Optional[str] = Query(None, description="Filter by province"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type"),
    cache_ttl: int = Query(30, ge=0, le=120, description="Cache TTL in minutes (0 = no cache)"),
):
    source_list = [s.strip() for s in sources.split(",") if s.strip()]
    if not source_list:
        source_list = list(registry.source_ids)

    cache_key = f"search_{sources}_{max_ads}_{min_price}_{max_price}_{brand}_{province}_{fuel_type}"

    if cache_ttl > 0:
        cached = _cache_get(cache_key, ttl_minutes=cache_ttl)
        if cached is not None:
            return {"results": cached, "cached": True, "count": len(cached)}

    per_source = max(1, max_ads // len(source_list))
    raw_ads = _run_scrapers(source_list, per_source)

    seen = set()
    unique = []
    for ad in raw_ads:
        key = ad.get("title", "").lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(ad)

    filtered = _filter_ads(unique, min_price, max_price, brand, province, fuel_type)
    filtered = filtered[:max_ads]

    if cache_ttl > 0:
        _cache_set(cache_key, filtered)

    return {
        "results": filtered,
        "cached": False,
        "count": len(filtered),
        "sources": source_list,
    }


@app.get("/api/sources")
def sources():
    return {"sources": registry.list_sources()}


@app.get("/api/brands")
def brands():
    return {
        "brands": [
            "BYD", "Tesla", "Nissan", "BMW", "Chevrolet", "Hyundai",
            "Kia", "Volkswagen", "MG", "Dongfeng", "Changan", "Toyota",
        ]
    }


@app.get("/api/health")
def health():
    return {"status": "healthy", "time": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    _init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
