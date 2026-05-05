#!/usr/bin/env python3
"""
Email Sender - Envía correos electrónicos con los reportes de autos eléctricos.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import List, Dict
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_TO, EMAIL_TO_LIST


def send_email_report(ads: List[Dict], html_content: str, subject: str = None) -> bool:
    """Envía el reporte por correo electrónico."""
    if not all([EMAIL_USER, EMAIL_PASSWORD]) or not EMAIL_TO_LIST:
        print("ERROR: Faltan credenciales de correo. Configura EMAIL_USER, EMAIL_PASSWORD y EMAIL_TO en .env")
        return False
    
    if subject is None:
        from datetime import datetime
        subject = f"⚡ Alerta Autos Eléctricos Cuba - {datetime.now().strftime('%d/%m/%Y %H:%M')} ({len(ads)} ofertas)"
    
    try:
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = ", ".join(EMAIL_TO_LIST)
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # Connect to SMTP and send
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Correo enviado exitosamente a {', '.join(EMAIL_TO_LIST)}")
        print(f"   Asunto: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando correo: {e}")
        return False


def save_report_locally(html_content: str, filename: str = None) -> str:
    """Guarda una copia del reporte localmente."""
    if filename is None:
        from datetime import datetime
        filename = f"/tmp/cuba_ev_alerts/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"💾 Reporte guardado localmente: {filename}")
    return filename


if __name__ == "__main__":
    print("Email sender module. Use main.py to run the full pipeline.")
