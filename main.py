#!/usr/bin/env python3
"""
Sistema de Alertas de Autos Eléctricos para Cuba

Este script orquesta el pipeline completo:
1. Scraping de Revolico.com para encontrar autos eléctricos
2. Enriquecimiento con datos técnicos (EPA/WLTP)
3. Generación de reporte HTML profesional
4. Envío por correo electrónico

Uso:
    python main.py              # Ejecución manual
    python main.py --save-only  # Solo guardar, no enviar correo
    python main.py --max-ads 10 # Limitar resultados

Programación automática (cada 1 hora):
    - Linux/Mac: crontab -e, agregar: 0 * * * * cd /ruta/al/script && python main.py
    - Windows: Programador de tareas
    - Raspberry Pi/Server: systemd timer
"""

import argparse
import sys
import os
from datetime import datetime

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MAX_RESULTS_PER_RUN, TEMP_DIR
from revolico_scraper import get_electric_ads
from enricher import enrich_ad
from email_builder import build_email_html
from email_sender import send_email_report, save_report_locally


def run_pipeline(max_ads: int = MAX_RESULTS_PER_RUN, send_email: bool = True) -> bool:
    """Ejecuta el pipeline completo de alertas."""
    print("=" * 60)
    print(f"⚡ INICIANDO ALERTA DE AUTOS ELÉCTRICOS - CUBA")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: Scrape Revolico
    print("\n🔍 PASO 1: Buscando anuncios en Revolico.com...")
    ads = get_electric_ads(max_ads)
    
    if not ads:
        print("⚠️ No se encontraron autos eléctricos en esta ejecución.")
        # Send a notification email anyway so user knows system is running
        if send_email:
            empty_html = build_empty_report()
            send_email_report([], empty_html, 
                f"⚡ Alerta EV Cuba - Sin ofertas nuevas {datetime.now().strftime('%d/%m %H:%M')}")
        return False
    
    print(f"✅ Encontrados {len(ads)} anuncios de autos eléctricos")
    
    # Step 2: Enrich with technical specs
    print("\n📊 PASO 2: Enriqueciendo con datos técnicos EPA/WLTP...")
    enriched_ads = []
    for i, ad in enumerate(ads, 1):
        print(f"  [{i}/{len(ads)}] {ad['title'][:50]}...", end=" ")
        enriched = enrich_ad(ad)
        enriched_ads.append(enriched)
        specs = enriched.get("specs", {})
        if specs and specs.get("model") != "No especificado":
            print(f"✓ {specs.get('model', '')}")
        else:
            print(f"⚠ Sin specs en DB")
    
    # Step 3: Build email
    print("\n📧 PASO 3: Generando reporte HTML...")
    run_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    html_content = build_email_html(enriched_ads, run_date)
    
    # Step 4: Save locally
    print("\n💾 PASO 4: Guardando copia local...")
    os.makedirs(TEMP_DIR, exist_ok=True)
    filename = os.path.join(TEMP_DIR, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    save_report_locally(html_content, filename)
    
    # Step 5: Send email
    if send_email:
        print("\n📤 PASO 5: Enviando correo electrónico...")
        subject = f"⚡ Alerta EV Cuba - {len(enriched_ads)} ofertas ({datetime.now().strftime('%d/%m %H:%M')})"
        success = send_email_report(enriched_ads, html_content, subject)
        return success
    else:
        print("\n⏭️ PASO 5: Envío de correo omitido (--save-only)")
        return True


def build_empty_report() -> str:
    """Construye un reporte HTML para cuando no hay resultados."""
    run_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <h1 style="color: #1a5f2a;">⚡ Alerta Autos Eléctricos Cuba</h1>
        <p><strong>Fecha:</strong> {run_date}</p>
        <p>No se encontraron anuncios de autos eléctricos en esta ejecución.</p>
        <p>El sistema sigue funcionando correctamente y seguirá monitoreando Revolico.com cada hora.</p>
        <hr>
        <p style="font-size: 12px; color: #888;">Sistema de Alertas de Autos Eléctricos para Cuba</p>
    </body>
    </html>
    """


def main():
    parser = argparse.ArgumentParser(description="Sistema de Alertas de Autos Eléctricos Cuba")
    parser.add_argument("--save-only", action="store_true", help="Solo guardar HTML, no enviar correo")
    parser.add_argument("--max-ads", type=int, default=MAX_RESULTS_PER_RUN, help=f"Máximo de anuncios a procesar (default: {MAX_RESULTS_PER_RUN})")
    parser.add_argument("--test", action="store_true", help="Modo test: no enviar correo, solo mostrar en consola")
    
    args = parser.parse_args()
    
    send_email = not args.save_only and not args.test
    
    try:
        success = run_pipeline(max_ads=args.max_ads, send_email=send_email)
        if success:
            print("\n" + "=" * 60)
            print("✅ PROCESO COMPLETADO EXITOSAMENTE")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n" + "=" * 60)
            print("⚠️ PROCESO COMPLETADO CON ADVERTENCIAS")
            print("=" * 60)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
