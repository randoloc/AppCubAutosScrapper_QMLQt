"""
Scraper Registry - Auto-descubrimiento de modulos scraper.

Busca automaticamente todos los modulos .py en scrapers/ que
expongan SOURCE_ID y get_ads(), y los registra en un dict central.

Para agregar una nueva fuente:
    1. Crear scrapers/mi_fuente.py
    2. Definir SOURCE_ID, SOURCE_LABEL y funcion get_ads()
    3. ¡Listo! El registry lo detecta automaticamente.
"""

import importlib
import inspect
import os
import pkgutil
from typing import Callable, Dict, List, Optional, Tuple


class ScraperEntry:
    """Representa una fuente de datos registrada."""

    def __init__(self, source_id: str, label: str, module_name: str,
                 func: Callable):
        self.source_id = source_id
        self.label = label
        self.module_name = module_name
        self.func = func

    def run(self, max_results: int = 20) -> list:
        return self.func(max_results)

    def to_dict(self) -> dict:
        return {
            "id": self.source_id,
            "label": self.label,
            "module": self.module_name,
        }


class ScraperRegistry:
    """Registro central de scrapers con auto-descubrimiento."""

    def __init__(self):
        self._scrapers: Dict[str, ScraperEntry] = {}
        self._discover()

    def _discover(self):
        package_dir = os.path.dirname(__file__)
        package_name = __package__ or "scrapers"

        for importer, modname, ispkg in pkgutil.iter_modules([package_dir]):
            if modname in ("__init__", "registry", "base"):
                continue
            if ispkg:
                continue

            try:
                module = importlib.import_module(f".{modname}", package=package_name)
            except Exception:
                continue

            self._register_module(module, modname)

    def _register_module(self, module, modname: str):
        source_id = getattr(module, "SOURCE_ID", None)
        func = getattr(module, "get_ads", None)

        if not source_id or not func:
            return

        label = getattr(module, "SOURCE_LABEL", source_id.capitalize())

        self._scrapers[source_id] = ScraperEntry(
            source_id=source_id,
            label=label,
            module_name=modname,
            func=func,
        )

    def register(self, source_id: str, label: str, func: Callable):
        """Registra manualmente un scraper."""
        self._scrapers[source_id] = ScraperEntry(
            source_id=source_id,
            label=label,
            module_name="manual",
            func=func,
        )

    def get(self, source_id: str) -> Optional[ScraperEntry]:
        return self._scrapers.get(source_id)

    def run(self, source_id: str, max_results: int = 20) -> list:
        entry = self.get(source_id)
        if not entry:
            return []
        return entry.run(max_results)

    def run_all(self, max_results: int = 10) -> list:
        all_ads = []
        for entry in self._scrapers.values():
            try:
                ads = entry.run(max_results)
                all_ads.extend(ads)
            except Exception:
                continue
        return all_ads

    def list_sources(self) -> List[dict]:
        return [e.to_dict() for e in self._scrapers.values()]

    @property
    def source_ids(self) -> List[str]:
        return list(self._scrapers.keys())

    def __len__(self) -> int:
        return len(self._scrapers)

    def __iter__(self):
        return iter(self._scrapers.values())


registry = ScraperRegistry()
