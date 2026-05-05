#!/usr/bin/env python3
"""
Enricher - Enriquece datos de autos con especificaciones técnicas de EPA/WLTP,
vida de batería, y busca imágenes adicionales.
"""

import re
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CarSpecs:
    model: str
    epa_range_km: Optional[float] = None  # EPA (US) range in km
    wltp_range_km: Optional[float] = None  # WLTP (Europe) range in km
    battery_capacity_kwh: Optional[float] = None
    battery_warranty_years: Optional[int] = None
    battery_warranty_km: Optional[int] = None  # km or miles
    real_world_range_km: Optional[str] = None  # Summary text
    charging_time_10_80: Optional[str] = None
    images: List[str] = None
    
    def __post_init__(self):
        if self.images is None:
            self.images = []


# Database of known EV specs ( Cuba-relevant models )
# This serves as cache + fallback when web search is not available
KNOWN_SPECS_DB = {
    "nissan_leaf": CarSpecs(
        model="Nissan Leaf",
        epa_range_km=240,
        wltp_range_km=270,
        battery_capacity_kwh=40,
        battery_warranty_years=8,
        battery_warranty_km=160000,
        real_world_range_km="200-240 km (EPA: 240 km, WLTP: 270 km)",
        charging_time_10_80="45-60 min (CHAdeMO 50kW)",
    ),
    "nissan_ariya": CarSpecs(
        model="Nissan Ariya",
        epa_range_km=490,
        wltp_range_km=533,
        battery_capacity_kwh=87,
        battery_warranty_years=8,
        battery_warranty_km=160000,
        real_world_range_km="450-500 km (EPA: 490 km, WLTP: 533 km)",
        charging_time_10_80="35 min (130kW DC)",
    ),
    "tesla_model_3": CarSpecs(
        model="Tesla Model 3",
        epa_range_km=438,
        wltp_range_km=491,
        battery_capacity_kwh=60,
        battery_warranty_years=8,
        battery_warranty_km=192000,
        real_world_range_km="400-450 km (EPA: 438 km, WLTP: 491 km)",
        charging_time_10_80="25-30 min (Supercharger 170kW)",
    ),
    "tesla_model_y": CarSpecs(
        model="Tesla Model Y",
        epa_range_km=531,
        wltp_range_km=533,
        battery_capacity_kwh=75,
        battery_warranty_years=8,
        battery_warranty_km=192000,
        real_world_range_km="480-530 km (EPA: 531 km, WLTP: 533 km)",
        charging_time_10_80="30 min (Supercharger 250kW)",
    ),
    "bmw_i3": CarSpecs(
        model="BMW i3",
        epa_range_km=246,
        wltp_range_km=285,
        battery_capacity_kwh=42,
        battery_warranty_years=8,
        battery_warranty_km=160000,
        real_world_range_km="200-250 km (EPA: 246 km, WLTP: 285 km)",
        charging_time_10_80="40 min (CCS 50kW)",
    ),
    "chevrolet_bolt": CarSpecs(
        model="Chevrolet Bolt EV",
        epa_range_km=416,
        wltp_range_km=440,
        battery_capacity_kwh=65,
        battery_warranty_years=8,
        battery_warranty_km=160000,
        real_world_range_km="380-420 km (EPA: 416 km, WLTP: 440 km)",
        charging_time_10_80="45 min (CCS 55kW)",
    ),
    "hyundai_kona_electric": CarSpecs(
        model="Hyundai Kona Electric",
        epa_range_km=415,
        wltp_range_km=484,
        battery_capacity_kwh=64,
        battery_warranty_years=8,
        battery_warranty_km=200000,
        real_world_range_km="380-420 km (EPA: 415 km, WLTP: 484 km)",
        charging_time_10_80="43 min (CCS 77kW)",
    ),
    "kia_ev6": CarSpecs(
        model="Kia EV6",
        epa_range_km=499,
        wltp_range_km=528,
        battery_capacity_kwh=77,
        battery_warranty_years=8,
        battery_warranty_km=200000,
        real_world_range_km="450-500 km (EPA: 499 km, WLTP: 528 km)",
        charging_time_10_80="18 min (800V 233kW)",
    ),
    "kia_niro_ev": CarSpecs(
        model="Kia Niro EV",
        epa_range_km=407,
        wltp_range_km=463,
        battery_capacity_kwh=64,
        battery_warranty_years=8,
        battery_warranty_km=200000,
        real_world_range_km="370-410 km (EPA: 407 km, WLTP: 463 km)",
        charging_time_10_80="43 min (CCS 77kW)",
    ),
    "volkswagen_id4": CarSpecs(
        model="Volkswagen ID.4",
        epa_range_km=422,
        wltp_range_km=520,
        battery_capacity_kwh=77,
        battery_warranty_years=8,
        battery_warranty_km=160000,
        real_world_range_km="400-450 km (EPA: 422 km, WLTP: 520 km)",
        charging_time_10_80="28 min (CCS 135kW)",
    ),
    "byd_dolphin": CarSpecs(
        model="BYD Dolphin",
        epa_range_km=340,
        wltp_range_km=340,
        battery_capacity_kwh=45,
        battery_warranty_years=8,
        battery_warranty_km=150000,
        real_world_range_km="300-340 km (WLTP: 340 km)",
        charging_time_10_80="30 min (CCS 60kW)",
    ),
    "byd_seal": CarSpecs(
        model="BYD Seal",
        epa_range_km=520,
        wltp_range_km=570,
        battery_capacity_kwh=82,
        battery_warranty_years=8,
        battery_warranty_km=150000,
        real_world_range_km="480-520 km (EPA: 520 km, WLTP: 570 km)",
        charging_time_10_80="26 min (800V 150kW)",
    ),
    "mg4": CarSpecs(
        model="MG4 EV",
        epa_range_km=350,
        wltp_range_km=350,
        battery_capacity_kwh=51,
        battery_warranty_years=7,
        battery_warranty_km=150000,
        real_world_range_km="320-350 km (WLTP: 350 km)",
        charging_time_10_80="35 min (CCS 117kW)",
    ),
    "mg5_ev": CarSpecs(
        model="MG5 EV",
        epa_range_km=310,
        wltp_range_km=344,
        battery_capacity_kwh=50,
        battery_warranty_years=7,
        battery_warranty_km=150000,
        real_world_range_km="280-310 km (EPA: 310 km, WLTP: 344 km)",
        charging_time_10_80="35 min (CCS 87kW)",
    ),
    "dongfeng_box": CarSpecs(
        model="Dongfeng Box 01",
        epa_range_km=270,
        wltp_range_km=310,
        battery_capacity_kwh=32,
        battery_warranty_years=8,
        battery_warranty_km=150000,
        real_world_range_km="250-270 km",
        charging_time_10_80="30 min",
    ),
}


def normalize_model_name(title: str) -> str:
    """Extrae el nombre del modelo normalizado del título del anuncio."""
    title_lower = title.lower()
    
    mapping = [
        ("nissan ariya", "nissan_ariya"),
        ("nissan leaf", "nissan_leaf"),
        ("tesla model 3", "tesla_model_3"),
        ("tesla model y", "tesla_model_y"),
        ("tesla model s", "tesla_model_s"),
        ("bmw i3", "bmw_i3"),
        ("chevrolet bolt", "chevrolet_bolt"),
        ("hyundai kona electric", "hyundai_kona_electric"),
        ("hyundai kona", "hyundai_kona_electric"),
        ("kia ev6", "kia_ev6"),
        ("kia niro ev", "kia_niro_ev"),
        ("volkswagen id.4", "volkswagen_id4"),
        ("vw id.4", "volkswagen_id4"),
        ("byd dolphin", "byd_dolphin"),
        ("byd seal", "byd_seal"),
        ("mg4", "mg4"),
        ("mg 4", "mg4"),
        ("mg5 electric", "mg5_ev"),
        ("mg5 ev", "mg5_ev"),
        ("dongfeng box", "dongfeng_box"),
    ]
    
    for pattern, key in mapping:
        if pattern in title_lower:
            return key
    
    return None


def enrich_ad(ad: Dict) -> Dict:
    """Enriquece un anuncio con datos técnicos y busca imágenes adicionales."""
    model_key = normalize_model_name(ad["title"])
    
    ad["specs"] = None
    ad["model_key"] = model_key
    
    if model_key and model_key in KNOWN_SPECS_DB:
        specs = KNOWN_SPECS_DB[model_key]
        ad["specs"] = {
            "model": specs.model,
            "epa_range_km": specs.epa_range_km,
            "wltp_range_km": specs.wltp_range_km,
            "battery_capacity_kwh": specs.battery_capacity_kwh,
            "battery_warranty": f"{specs.battery_warranty_years} años / {specs.battery_warranty_km:,} km",
            "real_world_range": specs.real_world_range_km,
            "charging_time_10_80": specs.charging_time_10_80,
        }
    else:
        # Try to extract from description
        ad["specs"] = extract_specs_from_description(ad.get("description", ""))
    
    # Ensure we have up to 3 images
    ad = ensure_images(ad)
    
    return ad


def extract_specs_from_description(description: str) -> Dict:
    """Intenta extraer especificaciones técnicas de la descripción del anuncio."""
    specs = {
        "model": "No especificado",
        "epa_range_km": None,
        "wltp_range_km": None,
        "battery_capacity_kwh": None,
        "battery_warranty": "No especificada",
        "real_world_range": None,
        "charging_time_10_80": None,
    }
    
    desc_lower = description.lower()
    
    # Look for autonomy/range patterns
    range_patterns = [
        r'(\d+)\s*km\s+de\s+autonom[ií]a',
        r'autonom[ií]a\s*:?\s*(\d+)\s*km',
        r'autonom[ií]a\s+de\s+(\d+)\s*km',
        r'autonom[ií]a\s+(\d+)\s*(?:km|kil[oó]metros?)',
        r'autonom[ií]a\s*:?\s*(\d+)\s*(?:km|kil[oó]metros?)',
        r'(\d+)\s*(?:km|kil[oó]metros?)\s+de\s+autonom[ií]a',
        r'(\d+)\s*(?:km|kil[oó]metros?)\s+reales\s+por\s+carga',
        r'(\d+)\s*(?:km|kil[oó]metros?)\s+por\s+carga',
        r'autonom[ií]a\s+real\s*:?\s*(\d+)\s*(?:km|kil[oó]metros?)',
    ]
    
    for pattern in range_patterns:
        match = re.search(pattern, desc_lower)
        if match:
            km = int(match.group(1))
            specs["real_world_range"] = f"{km} km (según anuncio)"
            # Estimate EPA/WLTP from real-world if not too high
            if km < 800:
                specs["wltp_range_km"] = int(km * 1.1)  # Rough estimate
                specs["epa_range_km"] = int(km * 0.95)   # Rough estimate
            break
    
    # Look for battery capacity
    battery_pattern = r'(\d+(?:\.\d+)?)\s*kwh'
    match = re.search(battery_pattern, desc_lower)
    if match:
        specs["battery_capacity_kwh"] = float(match.group(1))
    
    # Look for fast charging
    fast_patterns = [
        r'carga\s+r[aá]pida\s*:?\s*([^\n]+)',
        r'(?:80%)\s+en\s+([^\n]+)',
    ]
    for pattern in fast_patterns:
        match = re.search(pattern, desc_lower)
        if match:
            specs["charging_time_10_80"] = match.group(1).strip()
            break
    
    return specs


def ensure_images(ad: Dict) -> Dict:
    """Asegura que cada anuncio tenga hasta 3 imágenes."""
    images = ad.get("images", [])
    
    # Filter valid image URLs
    valid_images = []
    for img in images:
        if img and isinstance(img, str) and img.startswith("http"):
            valid_images.append(img)
    
    ad["images"] = valid_images[:3]
    return ad


if __name__ == "__main__":
    # Test
    test_specs = normalize_model_name("Vendo Nissan Ariya 2024 electrico")
    print(f"Normalized: {test_specs}")
    if test_specs:
        print(KNOWN_SPECS_DB[test_specs])
