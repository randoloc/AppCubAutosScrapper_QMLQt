#!/usr/bin/env python3
"""
Cuba EV Finder - App Qt para buscar autos electricos en Cuba.
Se conecta al backend FastAPI y muestra resultados filtrados.
"""

import sys
import json
import requests
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox, QLabel, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QMessageBox,
    QTextEdit, QSplitter, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QDesktopServices, QIcon
from PySide6.QtNetwork import QNetworkAccessManager

API_BASE = "http://localhost:8000"


class SearchWorker(QThread):
    finished = Signal(list)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, filters: dict):
        super().__init__()
        self.filters = filters

    def run(self):
        try:
            self.progress.emit("Conectando al servidor...")
            params = {}

            sources = []
            if self.filters.get("src_revolico"):
                sources.append("revolico")
            if self.filters.get("src_atrexport"):
                sources.append("atrexport")
            if self.filters.get("src_chinautoscuba"):
                sources.append("chinautoscuba")
            if self.filters.get("src_cubamotor"):
                sources.append("cubamotor")
            if not sources:
                sources = ["revolico", "atrexport", "chinautoscuba", "cubamotor"]
            params["sources"] = ",".join(sources)

            params["max_ads"] = self.filters.get("max_ads", 50)
            if self.filters.get("min_price") is not None and self.filters["min_price"] > 0:
                params["min_price"] = self.filters["min_price"]
            if self.filters.get("max_price") is not None and self.filters["max_price"] > 0:
                params["max_price"] = self.filters["max_price"]
            if self.filters.get("brand"):
                params["brand"] = self.filters["brand"]
            if self.filters.get("province"):
                params["province"] = self.filters["province"]

            self.progress.emit(f"Buscando en {len(sources)} fuentes...")
            resp = requests.get(f"{API_BASE}/api/search", params=params, timeout=120)
            resp.raise_for_status()
            data = resp.json()

            self.progress.emit(f"Recibidos {data.get('count', 0)} resultados")
            self.finished.emit(data.get("results", []))
        except requests.ConnectionError:
            self.error.emit(
                f"No se pudo conectar al servidor en {API_BASE}.\n"
                "Asegurate de que el backend esta corriendo:\n"
                "  python backend/app.py"
            )
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cuba EV Finder")
        self.setMinimumSize(1200, 800)
        self.results = []

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Top bar
        top_bar = QHBoxLayout()
        api_label = QLabel(f"API: {API_BASE}")
        api_label.setStyleSheet("color: #888; font-size: 11px;")
        top_bar.addWidget(api_label)
        top_bar.addStretch()
        self.status_label = QLabel("Listo")
        self.status_label.setStyleSheet("color: #1a5f2a; font-weight: bold;")
        top_bar.addWidget(self.status_label)
        main_layout.addLayout(top_bar)

        # Splitter for filters + results
        splitter = QSplitter(Qt.Vertical)

        # Filter panel
        filter_group = QGroupBox("Filtros de Busqueda")
        filter_layout = QFormLayout()

        # Price range
        price_layout = QHBoxLayout()
        self.min_price = QDoubleSpinBox()
        self.min_price.setRange(0, 500000)
        self.min_price.setPrefix("$ ")
        self.min_price.setValue(0)
        price_layout.addWidget(QLabel("Min:"))
        price_layout.addWidget(self.min_price)
        price_layout.addWidget(QLabel("Max:"))
        self.max_price = QDoubleSpinBox()
        self.max_price.setRange(0, 500000)
        self.max_price.setPrefix("$ ")
        self.max_price.setValue(0)
        self.max_price.setSpecialValueText("Sin limite")
        price_layout.addWidget(self.max_price)
        filter_layout.addRow("Precio:", price_layout)

        # Brand filter
        self.brand_combo = QComboBox()
        self.brand_combo.addItem("Todas")
        for b in ["BYD", "Tesla", "Nissan", "BMW", "Chevrolet", "Hyundai",
                   "Kia", "Volkswagen", "MG", "Dongfeng", "Changan", "Toyota",
                   "Honda", "Audi", "Mercedes"]:
            self.brand_combo.addItem(b)
        filter_layout.addRow("Marca:", self.brand_combo)

        # Province filter
        self.province_combo = QComboBox()
        self.province_combo.addItem("Todas")
        for p in ["La Habana", "Matanzas", "Villa Clara", "Cienfuegos",
                   "Camaguey", "Holguin", "Santiago de Cuba", "Pinar del Rio",
                   "Importacion"]:
            self.province_combo.addItem(p)
        filter_layout.addRow("Provincia:", self.province_combo)

        # Max results
        self.max_ads_spin = QSpinBox()
        self.max_ads_spin.setRange(5, 200)
        self.max_ads_spin.setValue(50)
        self.max_ads_spin.setSingleStep(10)
        filter_layout.addRow("Max resultados:", self.max_ads_spin)

        # Sources
        sources_group = QGroupBox("Fuentes")
        sources_layout = QHBoxLayout()
        self.src_revolico = QCheckBox("Revolico")
        self.src_revolico.setChecked(True)
        self.src_atrexport = QCheckBox("Atrexport")
        self.src_atrexport.setChecked(True)
        self.src_chinautoscuba = QCheckBox("ChinautosCuba")
        self.src_chinautoscuba.setChecked(True)
        self.src_cubamotor = QCheckBox("CubaMotor")
        self.src_cubamotor.setChecked(True)
        sources_layout.addWidget(self.src_revolico)
        sources_layout.addWidget(self.src_atrexport)
        sources_layout.addWidget(self.src_chinautoscuba)
        sources_layout.addWidget(self.src_cubamotor)
        sources_layout.addStretch()
        filter_layout.addRow(sources_group)

        filter_group.setLayout(filter_layout)
        filter_layout.insertRow(4, "", sources_layout)

        # Search button
        btn_layout = QHBoxLayout()
        self.search_btn = QPushButton("Buscar")
        self.search_btn.setStyleSheet(
            "QPushButton { background-color: #1a5f2a; color: white; "
            "font-size: 14px; padding: 8px 24px; border-radius: 4px; }"
            "QPushButton:hover { background-color: #238b3e; }"
            "QPushButton:disabled { background-color: #888; }"
        )
        self.search_btn.clicked.connect(self._do_search)
        btn_layout.addStretch()
        btn_layout.addWidget(self.search_btn)
        btn_layout.addStretch()

        filter_widget = QWidget()
        filter_layout_final = QVBoxLayout(filter_widget)
        filter_layout_final.addWidget(filter_group)
        filter_layout_final.addLayout(btn_layout)
        splitter.addWidget(filter_widget)

        # Results
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(0, 0, 0, 0)

        self.results_info = QLabel("Sin resultados")
        self.results_info.setStyleSheet("color: #666; padding: 4px;")
        results_layout.addWidget(self.results_info)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Fuente", "Titulo", "Precio", "Marca/Modelo",
            "Autonomia", "Ubicacion", "Contacto", "URL"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self._open_url)
        results_layout.addWidget(self.table)

        # Detail panel
        detail_group = QGroupBox("Detalle")
        detail_layout = QVBoxLayout(detail_group)
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumHeight(150)
        detail_layout.addWidget(self.detail_text)
        self.table.selectionModel().selectionChanged.connect(self._show_detail)
        results_layout.addWidget(detail_group)

        splitter.addWidget(results_widget)
        splitter.setSizes([280, 520])

        main_layout.addWidget(splitter)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

    def _do_search(self):
        self.search_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.status_label.setText("Buscando...")

        filters = {
            "min_price": self.min_price.value(),
            "max_price": self.max_price.value(),
            "brand": self.brand_combo.currentText() if self.brand_combo.currentIndex() > 0 else "",
            "province": self.province_combo.currentText() if self.province_combo.currentIndex() > 0 else "",
            "max_ads": self.max_ads_spin.value(),
            "src_revolico": self.src_revolico.isChecked(),
            "src_atrexport": self.src_atrexport.isChecked(),
            "src_chinautoscuba": self.src_chinautoscuba.isChecked(),
            "src_cubamotor": self.src_cubamotor.isChecked(),
        }

        self.worker = SearchWorker(filters)
        self.worker.finished.connect(self._on_results)
        self.worker.error.connect(self._on_error)
        self.worker.progress.connect(lambda m: self.status_label.setText(m))
        self.worker.start()

    def _on_results(self, results: list):
        self.results = results
        self.search_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.progress.setRange(0, 100)

        self.results_info.setText(
            f"{len(results)} resultados encontrados - {datetime.now().strftime('%H:%M:%S')}"
        )

        self.table.setRowCount(len(results))
        for i, ad in enumerate(results):
            src = ad.get("source_label", ad.get("source", ""))
            self.table.setItem(i, 0, QTableWidgetItem(src))

            title = ad.get("title", "")[:80]
            self.table.setItem(i, 1, QTableWidgetItem(title))

            price = ad.get("price")
            currency = ad.get("currency", "")
            if price:
                self.table.setItem(i, 2, QTableWidgetItem(f"{price:,.0f} {currency}"))
            else:
                self.table.setItem(i, 2, QTableWidgetItem("Consultar"))

            specs = ad.get("specs", {})
            model = ""
            if isinstance(specs, dict):
                model = specs.get("model", "")
                if not model:
                    model = specs.get("segmento", "")
            self.table.setItem(i, 3, QTableWidgetItem(model))

            autonomia = ""
            if isinstance(specs, dict):
                if specs.get("autonomia_km"):
                    autonomia = f"{specs['autonomia_km']} km"
                elif specs.get("real_world_range"):
                    autonomia = str(specs["real_world_range"])[:30]
            self.table.setItem(i, 4, QTableWidgetItem(autonomia))

            province = ad.get("province", "")
            municipality = ad.get("municipality", "")
            loc = f"{municipality}, {province}" if municipality else province
            self.table.setItem(i, 5, QTableWidgetItem(loc))

            phone = ad.get("contact_phone", "")
            wa = ad.get("contact_whatsapp", "")
            contact = f"WA: {wa}" if wa else phone
            self.table.setItem(i, 6, QTableWidgetItem(contact))

            self.table.setItem(i, 7, QTableWidgetItem(ad.get("url", "")))

        self.status_label.setText(f"{len(results)} resultados")
        if results:
            self.table.selectRow(0)

    def _on_error(self, message: str):
        self.search_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.progress.setRange(0, 100)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Error", message)

    def _show_detail(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        row = rows[0].row()
        ad = self.results[row]

        parts = []
        parts.append(f"Titulo: {ad.get('title', '')}")
        parts.append(f"Fuente: {ad.get('source_label', ad.get('source', ''))}")
        price = ad.get("price")
        if price:
            parts.append(f"Precio: {price:,.0f} {ad.get('currency', '')}")
        specs = ad.get("specs", {})
        if isinstance(specs, dict):
            for k, v in specs.items():
                if v:
                    parts.append(f"{k}: {v}")
        if ad.get("contact_phone"):
            parts.append(f"Telefono: {ad['contact_phone']}")
        if ad.get("contact_whatsapp"):
            parts.append(f"WhatsApp: {ad['contact_whatsapp']}")
        if ad.get("description"):
            parts.append(f"\nDescripcion:\n{ad['description'][:500]}")

        self.detail_text.setText("\n".join(parts))

    def _open_url(self, index):
        row = index.row()
        if row < len(self.results):
            url = self.results[row].get("url", "")
            if url:
                QDesktopServices.openUrl(url)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
