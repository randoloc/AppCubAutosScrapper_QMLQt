"""
Scrapers package - Auto-descubrimiento de fuentes de datos.

Cada modulo en este directorio que exponga SOURCE_ID y get_ads()
se registra automaticamente como fuente de datos.

Uso:
    from scrapers.registry import registry
    ads = registry.run("revolico", max_results=10)
    all_ads = registry.run_all(max_results=5)
"""

from .registry import registry

__all__ = ["registry"]
