<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:00c853,100:00e676&height=200&section=header&text=CubAutosFinder&fontSize=60&fontColor=fff&animation=fadeIn">
  <img alt="CubAutosFinder" src="https://capsule-render.vercel.app/api?type=waving&color=0:00c853,100:00e676&height=200&section=header&text=CubAutosFinder&fontSize=60&fontColor=fff&animation=fadeIn">
</picture>

<p align="center">
  <img alt="Qt" src="https://img.shields.io/badge/Qt-5.14.2-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img alt="QML" src="https://img.shields.io/badge/QML-Frontend-FF6F00?style=for-the-badge&logo=qml&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

<p align="center">
  <b>Monitoriza ofertas de autos eléctricos en Cuba</b><br>
  Scraping multi-fuente + app de escritorio Qt/QML + alertas por email
</p>

---

## ✨ Funcionalidades

- 🔍 **Scraping multi-fuente** — Revolico, Atrexport, ChinautosCuba, CubaMotor
- 🖥️ **App de escritorio Qt/QML** — UI moderna con tema oscuro, galería de imágenes y filtros en tiempo real
- 📧 **Alertas por email** — Reportes automáticos con datos EPA/WLTP enriquecidos
- ⚡ **API REST** — Backend FastAPI para acceso programático
- 🐳 **Docker ready** — Despliegue en un comando

## 🖼️ Screenshots

> _Próximamente_

## 🏗️ Arquitectura

```
┌──────────────────────┐     ┌──────────────────────────────┐
│   CubAutosFinder     │     │     Python Backend (API)      │
│   (Qt/QML Desktop)   │◄───►│     (FastAPI + Scrapers)      │
│                      │     │                              │
│  ┌────────────────┐  │     │  ┌──────────┐ ┌───────────┐  │
│  │  QML UI        │  │     │  │ FastAPI  │ │ Scrapers  │  │
│  │  Dark Theme    │  │     │  │ REST API │ │ x4 fuentes│  │
│  │  Gallery View  │  │     │  └──────────┘ └───────────┘  │
│  │  Live Filters  │  │     │  ┌──────────┐ ┌───────────┐  │
│  │  Search Bar    │  │     │  │Email     │ │Enricher   │  │
│  └────────────────┘  │     │  │Sender    │ │EPA/WLTP   │  │
│                      │     │  └──────────┘ └───────────┘  │
│  C++ (Qt5 / QML)     │     │  ┌──────────┐                │
│  Network + Models    │     │  │  Cache   │                │
└──────────────────────┘     │  │  SQLite  │                │
                             │  └──────────┘                │
                             └──────────────────────────────┘
```

## 🚀 Empezar

### Prerrequisitos

- **Python 3.10+**
- **Qt 5.14.2** (MinGW 7.3.0 64-bit) — [Descargar](https://www.qt.io/offline-installers)
- **Git**

### 1. Backend (API + Scrapers)

```bash
git clone https://github.com/randoloc/AppCubAutosScrapper_QMLQt.git
cd AppCubAutosScrapper_QMLQt
pip install -r requirements.txt
python backend/app.py
```

La API arranca en `http://localhost:8000`.

### 2. Frontend (App de escritorio)

```powershell
# Configurar PATH de Qt
$env:Path = "C:\Qt\Qt5.14.2\5.14.2\mingw73_64\bin;" + $env:Path

# Compilar
qmake CubAutosFinder.pro
mingw32-make

# Ejecutar
release\CubAutosFinder.exe
```

> 💡 O simplemente ejecuta `run_app.bat` si Qt ya está instalado.

### 3. Pipeline de alertas

```bash
# Ejecutar scraping manual
python main.py

# Solo guardar reporte, no enviar email
python main.py --save-only

# Modo test (consola solamente)
python main.py --test

# Limitar resultados
python main.py --max-ads 10
```

## 🔧 API Endpoints

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Status del servicio |
| `GET /api/search` | Buscar autos con filtros |
| `GET /api/sources` | Listar fuentes disponibles |
| `GET /api/brands` | Listar marcas conocidas |
| `GET /api/health` | Health check |

### Parámetros de búsqueda

| Parámetro | Tipo | Default | Descripción |
|------------|------|---------|-------------|
| `sources` | string | todas | Fuentes separadas por coma |
| `max_ads` | int | 50 | Máximo de resultados |
| `min_price` | float | — | Precio mínimo USD |
| `max_price` | float | — | Precio máximo USD |
| `brand` | string | — | Filtrar por marca |
| `province` | string | — | Filtrar por provincia |
| `cache_ttl` | int | 30 | Cache en minutos (0 = sin cache) |

## 📡 Fuentes de datos

| Fuente | Tipo | Descripción |
|--------|------|-------------|
| [Revolico](https://revolico.com) | Clasificados | Anuncios de particulares |
| [Atrexport](https://atrexport.com) | Catálogo | Autos de importadora |
| [ChinautosCuba](https://chinautoscuba.com) | Catálogo | BYD y marcas chinas |
| [CubaMotor](https://cubamotor.com) | Clasificados | Anuncios automotrices |

## 🧱 Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| **Frontend** | Qt 5.14.2 / QML / C++17 |
| **Backend** | Python 3.10+ / FastAPI |
| **Scraping** | Requests + BeautifulSoup4 |
| **Enriquecimiento** | Datos EPA / WLTP |
| **Email** | SMTP + HTML templates |
| **Cache** | SQLite |
| **Infra** | Docker / Docker Compose |

## 📁 Estructura del proyecto

```
AppCubAutosScrapper_QMLQt/
├── src/                    # Código fuente C++ (Qt)
│   └── main.cpp
├── qml/                    # Interfaz QML
│   ├── main.qml
│   └── ...
├── app_qt/                 # Recursos Qt adicionales
├── backend/                # API FastAPI
│   └── app.py
├── cuba_ev_qml/            # Recursos QML del scraper
├── release/                # Binario compilado
├── resources/              # Recursos (imágenes, iconos)
├── *.scraper.py            # Módulos de scraping
├── enricher.py             # Enriquecimiento EPA/WLTP
├── email_builder.py        # Generación de HTML
├── email_sender.py         # Envío de correos
├── config.py               # Configuración central
├── main.py                 # Pipeline de scraping
├── Dockerfile              # Docker image
└── requirements.txt        # Dependencias Python
```

## 🤝 Contribuir

1. Fork del repo
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'feat: agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

MIT © [randoloc](https://github.com/randoloc)

---

<p align="center">
  <sub>Hecho con ❤️ para la comunidad cubana de autos eléctricos</sub>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:00e676,100:00c853&height=120&section=footer">
  <img alt="footer" src="https://capsule-render.vercel.app/api?type=waving&color=0:00e676,100:00c853&height=120&section=footer">
</picture>
