#!/usr/bin/env python3
"""
Email Builder - Genera correos HTML profesionales con la información de autos eléctricos.
"""

import os
import base64
from typing import List, Dict
from datetime import datetime
import mimetypes


def build_email_html(ads: List[Dict], run_date: str = None) -> str:
    """Construye el cuerpo HTML del correo con todos los anuncios."""
    if run_date is None:
        run_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    total_ads = len(ads)
    
    html_parts = []
    html_parts.append(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Alerta Autos Eléctricos Cuba</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; margin: 0; padding: 20px; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #1a5f2a 0%, #2ecc71 100%); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .header p {{ margin: 8px 0 0; opacity: 0.9; font-size: 14px; }}
            .stats {{ display: flex; justify-content: center; gap: 30px; padding: 15px; background: #e8f5e9; }}
            .stat {{ text-align: center; }}
            .stat-value {{ font-size: 20px; font-weight: bold; color: #1a5f2a; }}
            .stat-label {{ font-size: 12px; color: #666; }}
            .content {{ padding: 25px; }}
            .car-card {{ border: 1px solid #e0e0e0; border-radius: 10px; margin-bottom: 25px; overflow: hidden; background: #fafafa; }}
            .car-header {{ background: #fff; padding: 15px 20px; border-bottom: 2px solid #2ecc71; }}
            .car-title {{ font-size: 18px; font-weight: 600; color: #1a5f2a; margin: 0; }}
            .car-price {{ font-size: 22px; font-weight: bold; color: #e74c3c; margin-top: 5px; }}
            .car-body {{ padding: 20px; }}
            .image-gallery {{ display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }}
            .car-image {{ width: 220px; height: 160px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd; background: #eee; }}
            .specs-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 15px 0; }}
            .spec-item {{ background: white; padding: 12px; border-radius: 6px; border-left: 3px solid #2ecc71; }}
            .spec-label {{ font-size: 11px; text-transform: uppercase; color: #888; letter-spacing: 0.5px; margin-bottom: 4px; }}
            .spec-value {{ font-size: 14px; font-weight: 600; color: #333; }}
            .description {{ background: white; padding: 15px; border-radius: 6px; margin: 15px 0; font-size: 13px; line-height: 1.6; color: #555; }}
            .contact-box {{ background: #e8f5e9; padding: 15px; border-radius: 6px; margin-top: 15px; }}
            .contact-title {{ font-size: 12px; text-transform: uppercase; color: #1a5f2a; font-weight: 600; margin-bottom: 8px; }}
            .contact-info {{ font-size: 14px; color: #333; }}
            .contact-info a {{ color: #1a5f2a; text-decoration: none; font-weight: 600; }}
            .footer {{ background: #f5f7fa; padding: 20px; text-align: center; font-size: 12px; color: #888; border-top: 1px solid #e0e0e0; }}
            .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-left: 8px; }}
            .badge-ev {{ background: #d4edda; color: #155724; }}
            .badge-promoted {{ background: #fff3cd; color: #856404; }}
            .source-link {{ display: inline-block; margin-top: 10px; padding: 8px 16px; background: #1a5f2a; color: white; text-decoration: none; border-radius: 4px; font-size: 13px; font-weight: 500; }}
            @media (max-width: 600px) {{
                .specs-grid {{ grid-template-columns: 1fr; }}
                .car-image {{ width: 100%; height: 200px; }}
                .stats {{ flex-direction: column; gap: 10px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>&#9889; Alerta Autos Eléctricos Cuba</h1>
                <p>Reporte de ofertas actualizado - {run_date}</p>
            </div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{total_ads}</div>
                    <div class="stat-label">VEHÍCULOS ENCONTRADOS</div>
                </div>
                <div class="stat">
                    <div class="stat-value">REVOLICO</div>
                    <div class="stat-label">FUENTE PRINCIPAL</div>
                </div>
            </div>
            <div class="content">
    """)
    
    for idx, ad in enumerate(ads, 1):
        html_parts.append(build_car_card(ad, idx))
    
    html_parts.append(f"""
            </div>
            <div class="footer">
                <p>Este reporte fue generado automáticamente el {run_date}</p>
                <p>Datos extraídos de Revolico.com | Especificaciones técnicas: EPA (EE.UU.) y WLTP (Europa)</p>
                <p style="margin-top:10px; color:#aaa;">Sistema de Alertas de Autos Eléctricos para Cuba</p>
            </div>
        </div>
    </body>
    </html>
    """)
    
    return "\n".join(html_parts)


def build_car_card(ad: Dict, index: int) -> str:
    """Construye la tarjeta HTML de un vehículo."""
    specs = ad.get("specs", {})
    
    # Build image gallery
    images_html = []
    for img_url in ad.get("images", [])[:3]:
        images_html.append(f'<img src="{img_url}" class="car-image" alt="Foto del auto" loading="lazy">')
    
    if not images_html:
        images_html.append('<div class="car-image" style="display:flex;align-items:center;justify-content:center;background:#eee;color:#888;font-size:12px;">Sin fotos disponibles</div>')
    
    # Determine badges
    badges = '<span class="badge badge-ev">⚡ ELÉCTRICO</span>'
    if ad.get("is_promoted"):
        badges += '<span class="badge badge-promoted">⭐ DESTACADO</span>'
    
    # Build specs
    specs_rows = []
    
    # EPA Range (US)
    epa_range = specs.get("epa_range_km")
    if epa_range:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Autonomía EPA (EE.UU.)</div>
            <div class="spec-value">{epa_range} km</div>
        </div>
        """)
    
    # WLTP Range (Europe)
    wltp_range = specs.get("wltp_range_km")
    if wltp_range:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Autonomía WLTP (Europa)</div>
            <div class="spec-value">{wltp_range} km</div>
        </div>
        """)
    
    # Real world range summary
    real_range = specs.get("real_world_range")
    if real_range:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Autonomía Real Estimada</div>
            <div class="spec-value">{real_range}</div>
        </div>
        """)
    
    # Battery capacity
    battery_kwh = specs.get("battery_capacity_kwh")
    if battery_kwh:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Capacidad Batería</div>
            <div class="spec-value">{battery_kwh} kWh</div>
        </div>
        """)
    
    # Battery warranty (vida de batería)
    battery_warranty = specs.get("battery_warranty")
    if battery_warranty:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Vida/Garantía Batería</div>
            <div class="spec-value">{battery_warranty}</div>
        </div>
        """)
    else:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Vida/Garantía Batería</div>
            <div class="spec-value">Consultar con vendedor</div>
        </div>
        """)
    
    # Charging time
    charging = specs.get("charging_time_10_80")
    if charging:
        specs_rows.append(f"""
        <div class="spec-item">
            <div class="spec-label">Carga Rápida (10%-80%)</div>
            <div class="spec-value">{charging}</div>
        </div>
        """)
    
    # Build contact info
    contact_parts = []
    
    phone = ad.get("contact_phone")
    if phone:
        contact_parts.append(f"📞 Teléfono: <strong>{phone}</strong>")
    
    whatsapp = ad.get("contact_whatsapp")
    if whatsapp:
        wa_link = f"https://wa.me/{whatsapp.replace('+', '').replace(' ', '')}"
        contact_parts.append(f'💬 WhatsApp: <a href="{wa_link}">{whatsapp}</a>')
    
    contact_name = ad.get("contact_name", "")
    if contact_name:
        contact_parts.insert(0, f"👤 {contact_name}")
    
    location_parts = []
    if ad.get("municipality"):
        location_parts.append(ad["municipality"])
    if ad.get("province"):
        location_parts.append(ad["province"])
    location_str = ", ".join(location_parts) if location_parts else "Cuba"
    
    contact_html = "<br>".join(contact_parts) if contact_parts else "Contacto: Ver anuncio en Revolico"
    
    # Description
    description = ad.get("description", "")
    if len(description) > 500:
        description = description[:497] + "..."
    desc_html = f'<div class="description"><strong>Descripción del vendedor:</strong><br>{description.replace(chr(10), "<br>")}</div>' if description else ""
    
    card_html = f"""
    <div class="car-card">
        <div class="car-header">
            <div class="car-title">#{index} {ad.get('title', 'Sin título')} {badges}</div>
            <div class="car-price">💰 {ad.get('price', 'Consultar')} {ad.get('currency', 'USD')}</div>
        </div>
        <div class="car-body">
            <div class="image-gallery">
                {"".join(images_html)}
            </div>
            <div class="specs-grid">
                {"".join(specs_rows)}
            </div>
            {desc_html}
            <div class="contact-box">
                <div class="contact-title">📍 {location_str} | Contacto del vendedor</div>
                <div class="contact-info">
                    {contact_html}
                </div>
                <a href="{ad.get('url', '#')}" class="source-link" target="_blank">Ver anuncio original en Revolico →</a>
            </div>
        </div>
    </div>
    """
    
    return card_html


if __name__ == "__main__":
    # Test
    test_ads = [
        {
            "title": "Nissan Ariya Engage 2024 Electrico",
            "price": 57000,
            "currency": "USD",
            "url": "https://www.revolico.com/item/test",
            "images": [],
            "description": "Auto electrico con 360km de autonomia",
            "contact_phone": "+53 63973583",
            "contact_whatsapp": "+53 63973583",
            "province": "La Habana",
            "municipality": "Habana Vieja",
            "is_promoted": True,
            "specs": {
                "model": "Nissan Ariya",
                "epa_range_km": 490,
                "wltp_range_km": 533,
                "battery_capacity_kwh": 87,
                "battery_warranty": "8 años / 160,000 km",
                "real_world_range": "450-500 km (EPA: 490 km, WLTP: 533 km)",
                "charging_time_10_80": "35 min (130kW DC)",
            }
        }
    ]
    html = build_email_html(test_ads)
    with open("/tmp/test_email.html", "w") as f:
        f.write(html)
    print("Test email written to /tmp/test_email.html")
