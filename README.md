---
title: Cuba EV Scraper API
emoji: 🔋
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Cuba EV Scraper API

API para busqueda de autos electricos en Cuba con scraping multi-fuente.

## Endpoints

- `GET /` - Status del servicio
- `GET /api/search` - Buscar autos con filtros
- `GET /api/sources` - Listar fuentes disponibles
- `GET /api/brands` - Listar marcas conocidas
- `GET /api/health` - Health check

## Parametros de busqueda

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `sources` | string | todas | Comma-separated: revolico,atrexport,chinautoscuba,cubamotor |
| `max_ads` | int | 50 | Maximo de resultados (1-200) |
| `min_price` | float | null | Precio minimo |
| `max_price` | float | null | Precio maximo |
| `brand` | string | null | Filtrar por marca |
| `province` | string | null | Filtrar por provincia |
| `cache_ttl` | int | 30 | Cache TTL en minutos (0 = sin cache) |

## Ejemplo

```
GET /api/search?sources=revolico&max_ads=20&min_price=10000&brand=BYD
```

## Fuentes

- **Revolico** - Clasificados cubanos
- **Atrexport** - Catalogo de importacion
- **ChinautosCuba** - Catalogo BYD China
- **CubaMotor** - Clasificados automotrices
