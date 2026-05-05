# CubAutosFinder

Desktop app (C++ Qt + QML) para buscar autos electricos en Cuba.

## Requisitos

- Qt 5.14.2 (ya instalado en `C:\Qt\Qt5.14.2`)
- Compilador MinGW (incluido con Qt)

## Compilar

```powershell
# Agregar Qt al PATH
$env:Path = "C:\Qt\Qt5.14.2\5.14.2\mingw73_64\bin;" + $env:Path

# Generar Makefile y compilar
cd CubAutosFinder
qmake CubAutosFinder.pro
mingw32-make
```

## Ejecutar

```powershell
release\CubAutosFinder.exe
```

## Configurar API

Por defecto conecta a `http://localhost:8000`. Para cambiar:

- En la app: cambiar la URL en el codigo o usar variable de entorno `EV_API_URL`

## Backend API

El scraper corre en un servidor FastAPI separado:
```bash
git clone https://github.com/randoloc/scrapper_autos_electricos.git
cd scrapper_autos_electricos
pip install -r requirements.txt fastapi uvicorn
python backend/app.py
```
