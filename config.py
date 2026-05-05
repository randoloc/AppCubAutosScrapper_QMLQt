#!/usr/bin/env python3
"""
Configuración del sistema de alertas de autos eléctricos para Cuba.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_TO = os.getenv("EMAIL_TO", "randolo92cromix@gmail.com")
EMAIL_TO_LIST = [e.strip() for e in EMAIL_TO.split(",") if e.strip()] if EMAIL_TO else []

# Search Configuration
REVOLICO_BASE_URL = "https://www.revolico.com"
ATREXPORT_URL = "https://atrexport.com/carros-electricos-en-cuba/"
AUTOCUBANA_URL = "https://autocubana.com/electric_cars?car_type=carros&ev_type=ev"
CHINAUTOSCUBA_URL = "https://chinautoscuba.com/byd/"
CUBAMOTOR_URL = "https://www.cubamotor.com/autos/"
EMAIL_TO_LIST = [e.strip() for e in EMAIL_TO.split(",") if e.strip()] if EMAIL_TO else []

# Search Configuration
REVOLICO_BASE_URL = "https://www.revolico.com"
ATREXPORT_BASE_URL = "https://atrexport.com"
AUTOCUBANA_BASE_URL = "https://autocubana.com"
CHINAUTOSCUBA_BASE_URL = "https://chinautoscuba.com"
CUBAMOTOR_BASE_URL = "https://www.cubamotor.com"
SEARCH_KEYWORDS = [
    "electrico",
    "electrica", 
    "EV",
    "tesla",
    "nissan leaf",
    "nissan ariya",
    "bmw i3",
    "chevrolet bolt",
    "hyundai kona electric",
    "byd",
    "dongfeng box",
    "kia ev",
    "volkswagen id",
    "mg4",
    "mg5 electric",
]

# Filtros adicionales en título/descripción para identificar EVs
EV_INDICATORS = [
    "electrico", "eléctrico", "electrica", "eléctrica",
    "100% electrico", "100% eléctrico",
    "ev", "hev", "phev", "hibrido enchufable", "híbrido enchufable",
    "zero emission", "cero emisiones",
    "bateria", "batería", "autonomia", "autonomía",
    "kwh", "kw/h", "kilowatt",
    "carga rapida", "carga rápida",
    "tesla", "nissan leaf", "nissan ariya", "bmw i3", "chevrolet bolt",
    "hyundai kona electric", "kia niro ev", "kia soul ev", "kia ev6",
    "volkswagen id.3", "volkswagen id.4", "volkswagen id.5",
    "byd dolphin", "byd seal", "byd tang", "byd yuan",
    "mg4", "mg5 ev", "mg zs ev",
    "dongfeng box", "dongfeng eπ", "dongfeng vigo",
    "jac e", "jac iev",
    "wuling", "mini ev",
    "renault zoe", "peugeot e", "opel corsa e",
]

# Sources
SOURCES = {
    "revolico": True,
    "dongfeng_cuba": False,  # Requiere scraping adicional
    "cuban_cargo": False,    # Requiere scraping adicional
}

# Output
MAX_RESULTS_PER_RUN = 20
MAX_IMAGES_PER_CAR = 3
TEMP_DIR = "/tmp/cuba_ev_alerts"
