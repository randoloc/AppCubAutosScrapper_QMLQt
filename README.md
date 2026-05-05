# ⚡ Sistema de Alertas de Autos Eléctricos para Cuba

Sistema automatizado de monitoreo y alertas por correo electrónico que busca ofertas de autos eléctricos disponibles para Cuba, extrae información detallada y envía reportes organizados cada hora.

## 📋 Contenido del Reporte

Cada correo incluye por vehículo:
- **Precio** en USD
- **Autonomía EPA** (estándar estadounidense) en km
- **Autonomía WLTP** (estándar europeo) en km
- **Autonomía real estimada** para condiciones cubanas
- **Vida/Garantía de batería** (años y kilómetros)
- **Capacidad de batería** (kWh)
- **Tiempo de carga rápida** (10% a 80%)
- **Hasta 3 fotos reales** del vehículo
- **Contacto del vendedor** (teléfono, WhatsApp, nombre)
- **Ubicación** en Cuba
- **Enlace al anuncio original**

## 🗂️ Fuentes de Datos

| Fuente | Tipo | Estado |
|--------|------|--------|
| [Revolico.com](https://revolico.com) | Clasificados de particulares | ✅ Activo |
| [Dongfeng Cuba](https://dongfengcuba.com) | Concesionario oficial | ⚠️ Pendiente |
| [Cuban Cargo](https://cubancargos.com) | Importadora | ⚠️ Pendiente |

## 🚀 Instalación Rápida

### Requisitos
- Python 3.8 o superior
- pip

### Paso 1: Clonar/Descargar
```bash
cd cuba_ev_scraper
```

### Paso 2: Instalar dependencias
```bash
pip install requests beautifulsoup4 python-dotenv lxml
```

### Paso 3: Configurar correo
```bash
cp .env.example .env
nano .env  # Editar con tus datos
```

Configurar las variables:
```
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASSWORD=xxxx_xxxx_xxxx_xxxx  # App Password de Gmail
EMAIL_TO=randolo92cromix@gmail.com
```

> **Importante:** Para Gmail debes usar una **[App Password](https://myaccount.google.com/apppasswords)**, no tu contraseña normal. Activa primero la verificación en 2 pasos.

### Paso 4: Ejecutar manualmente
```bash
python main.py
```

### Paso 5: Programar ejecución automática cada 1 hora

#### Linux / Mac (crontab)
```bash
crontab -e
```
Agregar esta línea:
```cron
0 * * * * cd /ruta/completa/al/cuba_ev_scraper && /usr/bin/python3 main.py >> /tmp/cuba_ev_cron.log 2>&1
```

#### Windows (Programador de Tareas)
1. Abrir "Programador de Tareas"
2. Crear tarea básica → Diaria → Repetir cada 1 hora
3. Acción: Iniciar programa
4. Programa: `python.exe`
5. Argumentos: `main.py`
6. Iniciar en: `C:\ruta\al\cuba_ev_scraper`

#### Raspberry Pi / Servidor Linux (systemd)
Ver archivo `cuba-ev-alerts.service` en este repositorio (si está disponible).

## 📖 Uso

### Ejecución normal (scrape + email)
```bash
python main.py
```

### Solo guardar HTML sin enviar correo
```bash
python main.py --save-only
```

### Limitar cantidad de resultados
```bash
python main.py --max-ads 10
```

### Modo test (sin enviar correo)
```bash
python main.py --test
```

### GitHub Actions (Recomendado - Sin servidor propio)

Este repositorio incluye un workflow de GitHub Actions que ejecuta el pipeline automáticamente cada hora.

#### Configurar GitHub Secrets

1. Ir a **Settings → Secrets and variables → Actions → New repository secret**
2. Agregar los siguientes secrets:

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `EMAIL_USER` | Correo de Gmail emisor | `tu_correo@gmail.com` |
| `EMAIL_PASSWORD` | App Password de Gmail | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | Correo destinatario | `tu_correo@gmail.com` |
| `EMAIL_HOST` | Servidor SMTP | `smtp.gmail.com` |
| `EMAIL_PORT` | Puerto SMTP | `587` |

> **Importante:** `EMAIL_PASSWORD` debe ser un **App Password** de Google, no tu contraseña normal. Ve a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

#### Ejecutar manualmente

Ir a **Actions → Cuba EV Alerts → Run workflow** (opcional: cambiar `max_ads`).

#### Disparadores

| Evento | Frecuencia |
|--------|------------|
| `schedule` (cron) | Cada hora (`0 * * * *`) |
| `workflow_dispatch` | Manual desde la pestaña Actions |

## 🛠️ Arquitectura

```
main.py              ← Orquestador
├── revolico_scraper.py   ← Extrae anuncios de Revolico
├── enricher.py           ← Agrega specs EPA/WLTP y fotos
├── email_builder.py      ← Genera HTML profesional
├── email_sender.py       ← Envía vía SMTP
└── config.py             ← Configuración centralizada
```

## 📊 Base de Datos de Especificaciones

El sistema incluye una base de datos técnica con modelos comúnmente disponibles para Cuba:

| Modelo | EPA (km) | WLTP (km) | Batería (kWh) | Garantía Batería |
|--------|----------|-----------|---------------|------------------|
| Nissan Leaf | 240 | 270 | 40 | 8 años / 160,000 km |
| Nissan Ariya | 490 | 533 | 87 | 8 años / 160,000 km |
| Tesla Model 3 | 438 | 491 | 60 | 8 años / 192,000 km |
| Tesla Model Y | 531 | 533 | 75 | 8 años / 192,000 km |
| BMW i3 | 246 | 285 | 42 | 8 años / 160,000 km |
| Chevrolet Bolt | 416 | 440 | 65 | 8 años / 160,000 km |
| Hyundai Kona EV | 415 | 484 | 64 | 8 años / 200,000 km |
| Kia EV6 | 499 | 528 | 77 | 8 años / 200,000 km |
| VW ID.4 | 422 | 520 | 77 | 8 años / 160,000 km |
| BYD Seal | 520 | 570 | 82 | 8 años / 150,000 km |
| MG4 EV | 350 | 350 | 51 | 7 años / 150,000 km |

Para modelos no listados, el sistema intenta extraer datos desde la descripción del anuncio.

## ⚠️ Limitaciones Conocidas

1. **Revolico**: Los anuncios son publicados por particulares; la calidad y veracidad de los datos depende del vendedor
2. **Fotos**: Se extraen las fotos del anuncio. Si el vendedor no subió fotos, aparecerá "Sin fotos disponibles"
3. **Specs técnicos**: Si el modelo no está en la base de datos, se estima desde la descripción o se marca como "Consultar"
4. **Disponibilidad**: El sistema detecta anuncios nuevos pero no puede verificar si el vehículo sigue disponible
5. **Fuentes adicionales**: Dongfeng Cuba y Cuban Cargo requieren scrapers adicionales (pendientes)

## 🔒 Seguridad

- Las credenciales de correo se almacenan en archivo `.env` (nunca subir a Git)
- Se recomienda usar App Password de Gmail en lugar de la contraseña principal
- El archivo `.env` ya está incluido en `.gitignore` (si existe)

## 📝 Licencia

Uso personal y educativo. El sistema es un agregador de información pública; no garantiza la disponibilidad ni precisión de los anuncios.

## 🆘 Soporte

Si tienes problemas:
1. Verifica que tu `.env` tiene las credenciales correctas
2. Para Gmail: asegúrate de usar [App Password](https://myaccount.google.com/apppasswords)
3. Prueba en modo test: `python main.py --test`
4. Revisa los logs en `/tmp/cuba_ev_alerts/`

---

**Nota:** Este sistema fue generado el 5 de mayo de 2026. Las fuentes de datos (Revolico) pueden cambiar su estructura, lo cual requería actualizaciones del scraper.
