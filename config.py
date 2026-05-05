#!/usr/bin/env python3
"""
Configuracion del sistema de alertas de autos electricos para Cuba.
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

ATREXPORT_BASE_URL = "https://atrexport.com"
AUTOCUBANA_BASE_URL = "https://autocubana.com"
CHINAUTOSCUBA_BASE_URL = "https://chinautoscuba.com"
CUBAMOTOR_BASE_URL = "https://www.cubamotor.com"

SEARCH_KEYWORDS = [
    "electrico", "electrica", "EV", "tesla", "nissan leaf", "nissan ariya",
    "bmw i3", "chevrolet bolt", "hyundai kona electric", "byd", "dongfeng box",
    "kia ev", "volkswagen id", "mg4", "mg5 electric",
]

EV_INDICATORS = [
    "electrico", "electrico", "electrica", "electrica",
    "100% electrico", "100% electrico",
    "ev", "hev", "phev", "hibrido enchufable", "hibrido enchufable",
    "zero emission", "cero emisiones",
    "bateria", "bateria", "autonomia", "autonomia",
    "kwh", "kw/h", "kilowatt",
    "carga rapida", "carga rapida",
    "tesla", "nissan leaf", "nissan ariya", "bmw i3", "chevrolet bolt",
    "hyundai kona electric", "kia niro ev", "kia soul ev", "kia ev6",
    "volkswagen id.3", "volkswagen id.4", "volkswagen id.5",
    "byd dolphin", "byd seal", "byd tang", "byd yuan",
    "mg4", "mg5 ev", "mg zs ev",
    "dongfeng box", "dongfeng e", "dongfeng vigo",
    "jac e", "jac iev",
    "wuling", "mini ev",
    "renault zoe", "peugeot e", "opel corsa e",
]

SOURCES = {
    "revolico": True,
    "dongfeng_cuba": False,
    "cuban_cargo": False,
}

MAX_RESULTS_PER_RUN = 20
MAX_IMAGES_PER_CAR = 3
TEMP_DIR = "/tmp/cuba_ev_alerts"
