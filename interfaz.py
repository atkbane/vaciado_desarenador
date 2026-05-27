"""
Interfaz gráfica con PySide6 para la simulación de vaciado de desarenador.
Layout de 2 columnas: datos a la izquierda, gráfico a la derecha.
"""
import sys
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox, QLineEdit, QPushButton, QLabel,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from calculos import simular_vaciado


VALORES_DEFECTO = {
    'L': '36.0',
    'W': '5.6',
    'B': '1.0',
    'd': '1.0',
    't_open': '200',
    'h0': '5.3',
    'h_parada': '0.10',
    'Cd_orif': '0.60',
    'Cd_weir': '0.56',
    'nombre_proyecto': 'Simulación de Vaciado de Desarenador',
}


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1 = self.fig.add_subplot(111)
        super().__init__(self.fig)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vaciado de Desarenador - v2 (PySide6)")
        self.setMinimumSize(1100, 600)
        self.resize(1300, 700)

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout_h = QHBoxLayout(central)
        layout_h.setContentsMargins(10, 10, 10, 10)
        layout_h.setSpacing(10)

        # ---- COLUMNA IZQUIERDA ----
        panel_izq = QFrame()
        panel_izq.setFrameShape(QFrame.Shape.Box)
        panel_izq.setMinimumWidth(320)
        panel_izq.setMaximumWidth(380)
        layout_izq = QVBoxLayout(panel_izq)
        layout_izq.setSpacing(6)

        # Título del panel
        lbl_titulo = QLabel("DATOS DE ENTRADA")
        lbl_titulo.setStyleSheet("font-size: 13px; font-weight: bold; margin-bottom: 5px;")
        layout_izq.addWidget(lbl_titulo)

        # Nombre del proyecto
        lbl_nombre = QLabel("Nombre del proyecto:")
        lbl_nombre.setStyleSheet("font-weight: bold;")
        layout_izq.addWidget(lbl_nombre)
        self.edit_nombre = QLineEdit(VALORES_DEFECTO['nombre_proyecto'])
        layout_izq.addWidget(self.edit_nombre)

        # ----- DIMENSIONES -----
        gb_dim = QGroupBox("Dimensiones del desarenador")
        form_dim = QFormLayout(gb_dim)
        self.edit_L = QLineEdit(VALORES_DEFECTO['L'])
        self.edit_W = QLineEdit(VALORES_DEFECTO['W'])
        form_dim.addRow("Largo (m):", self.edit_L)
        form_dim.addRow("Ancho (m):", self.edit_W)
        layout_izq.addWidget(gb_dim)

        # ----- COMPUERTA -----
        gb_comp = QGroupBox("Compuerta")
        form_comp = QFormLayout(gb_comp)
        self.edit_B = QLineEdit(VALORES_DEFECTO['B'])
        self.edit_d = QLineEdit(VALORES_DEFECTO['d'])
        self.edit_t_open = QLineEdit(VALORES_DEFECTO['t_open'])
        form_comp.addRow("Ancho B (m):", self.edit_B)
        form_comp.addRow("Altura d (m):", self.edit_d)
        form_comp.addRow("T. apertura (s):", self.edit_t_open)
        layout_izq.addWidget(gb_comp)

        # ----- NIVEL INICIAL -----
        gb_nivel = QGroupBox("Nivel inicial")
        form_nivel = QFormLayout(gb_nivel)
        self.edit_h0 = QLineEdit(VALORES_DEFECTO['h0'])
        form_nivel.addRow("Tirante h0 (m):", self.edit_h0)
        layout_izq.addWidget(gb_nivel)

        # ----- COEFICIENTES -----
        gb_coef = QGroupBox("Coeficientes de descarga")
        form_coef = QFormLayout(gb_coef)
        self.edit_Cd_orif = QLineEdit(VALORES_DEFECTO['Cd_orif'])
        self.edit_Cd_weir = QLineEdit(VALORES_DEFECTO['Cd_weir'])
        form_coef.addRow("Cd orificio:", self.edit_Cd_orif)
        form_coef.addRow("Cd vertedero:", self.edit_Cd_weir)
        layout_izq.addWidget(gb_coef)

        # ----- TIRANTE DE PARADA -----
        gb_parada = QGroupBox("Tirante de parada")
        form_parada = QFormLayout(gb_parada)
        self.edit_h_parada = QLineEdit(VALORES_DEFECTO['h_parada'])
        form_parada.addRow("h mínimo (m):", self.edit_h_parada)
        layout_izq.addWidget(gb_parada)

        # ----- BOTONES -----
        layout_botones = QHBoxLayout()
        btn_calcular = QPushButton("CALCULAR")
        btn_calcular.clicked.connect(self.ejecutar_calculo)
        btn_salir = QPushButton("SALIR")
        btn_salir.clicked.connect(self.close)
        layout_botones.addWidget(btn_calcular)
        layout_botones.addWidget(btn_salir)
        layout_izq.addLayout(layout_botones)

        layout_izq.addStretch()

        # ---- COLUMNA DERECHA ----
        panel_der = QFrame()
        panel_der.setFrameShape(QFrame.Shape.Box)
        layout_der = QVBoxLayout(panel_der)

        self.canvas = MplCanvas(self, width=8, height=5, dpi=100)
        self.canvas.ax1.text(0.5, 0.5, 'Presione "CALCULAR"\npara generar el gráfico',
                             transform=self.canvas.ax1.transAxes,
                             ha='center', va='center', fontsize=14, color='gray')
        self.canvas.ax1.set_xlabel('Tiempo (s)')
        self.canvas.ax1.set_ylabel('Nivel de agua (m)')
        self.canvas.ax1.grid(True, alpha=0.3)
        self.canvas.fig.tight_layout()
        self.canvas.draw()

        layout_der.addWidget(self.canvas)

        # Agregar paneles al layout horizontal principal
        layout_h.addWidget(panel_izq)
        layout_h.addWidget(panel_der, stretch=1)

        self.resultado = None

    def obtener_parametros(self):
        try:
            return {
                'L': float(self.edit_L.text()),
                'W': float(self.edit_W.text()),
                'B': float(self.edit_B.text()),
                'd': float(self.edit_d.text()),
                't_open': float(self.edit_t_open.text()),
                'h0': float(self.edit_h0.text()),
                'h_parada': float(self.edit_h_parada.text()),
                'Cd_orif': float(self.edit_Cd_orif.text()),
                'Cd_weir': float(self.edit_Cd_weir.text()),
                'nombre': self.edit_nombre.text().strip(),
            }
        except ValueError:
            raise ValueError("Todos los campos numéricos deben contener valores válidos.")

    def ejecutar_calculo(self):
        try:
            p = self.obtener_parametros()
        except ValueError as e:
            QMessageBox.warning(self, "Error de entrada", str(e))
            return

        try:
            res = simular_vaciado(
                L=p['L'], W=p['W'], B=p['B'], d=p['d'],
                t_open=p['t_open'], h0=p['h0'], h_parada=p['h_parada'],
                Cd_orif=p['Cd_orif'], Cd_weir=p['Cd_weir']
            )
            self.resultado = res
            self.actualizar_grafico(res, p['nombre'])
        except Exception as e:
            QMessageBox.critical(self, "Error de simulación", str(e))

    def actualizar_grafico(self, res, nombre_proyecto):
        t_res = res['t_res']
        h_res = res['h_res']
        q_res = res['q_res']
        t_parada = res['t_parada']
        t_apertura = res['t_apertura_total']
        indices_trans = res['indices_transicion']
        p = res['parametros']

        ax1 = self.canvas.ax1
        ax1.clear()
        self.canvas.fig.set_size_inches(8, 5)

        # Título
        ax1.set_title(nombre_proyecto, fontsize=12, fontweight='bold')

        # Eje izquierdo: Nivel
        ax1.set_xlabel('Tiempo (s)', fontsize=11)
        ax1.set_ylabel('Nivel de agua (m)', color='tab:blue', fontsize=11)
        ax1.plot(t_res, h_res, color='tab:blue', linewidth=2, label='Nivel (h)')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, t_parada * 1.05)
        ax1.set_ylim(0, p['h0'] * 1.05)

        # Eje derecho: Caudal
        ax2 = ax1.twinx()
        ax2.set_ylabel('Caudal de salida (m³/s)', color='tab:red', fontsize=11)
        ax2.plot(t_res, q_res, color='tab:red', linestyle='--', linewidth=2, label='Caudal (Q)')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        ax2.set_xlim(0, t_parada * 1.05)
        ax2.set_ylim(0, max(q_res) * 1.1)

        # Línea: Apertura total
        ax1.axvline(x=t_apertura, color='green', linestyle=':', linewidth=1.5, alpha=0.7)
        ax1.text(t_apertura + 15, ax1.get_ylim()[1] * 0.92,
                 f'Apertura total\nt = {t_apertura:.0f} s',
                 fontsize=9, color='green', verticalalignment='top')

        # Línea: Nivel de parada
        ax1.axhline(y=p['h_parada'], color='orange', linestyle=':', linewidth=1.5, alpha=0.7)
        ax1.text(t_parada * 0.45, p['h_parada'] + 0.10,
                 f'h = {p["h_parada"]:.2f} m (parada)\nt = {t_parada:.0f} s',
                 fontsize=9, color='orange', verticalalignment='bottom')

        # Transiciones
        for idx in indices_trans:
            if idx < len(t_res):
                ax1.axvline(x=t_res[idx], color='purple', linestyle='--', linewidth=1.0, alpha=0.5)
                ax1.plot(t_res[idx], h_res[idx], 'o', color='purple', markersize=6, alpha=0.7)

        if indices_trans and indices_trans[0] < len(t_res):
            idx0 = indices_trans[0]
            ax1.annotate('Transición\norificio↔vertedero',
                         xy=(t_res[idx0], h_res[idx0]),
                         xytext=(t_res[idx0] + 40, h_res[idx0] + 0.5),
                         fontsize=8, color='purple',
                         arrowprops=dict(arrowstyle='->', color='purple', alpha=0.7,
                                         connectionstyle='arc3,rad=0.2'),
                         bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.6))

        # Leyenda combinada
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # Info
        texto_info = (f"L = {p['L']} m | W = {p['W']} m | "
                      f"B = {p['B']} m | d = {p['d']} m\n"
                      f"Apertura: {p['t_open']} s | "
                      f"Cd_o = {p['Cd_orif']} | Cd_v = {p['Cd_weir']}")
        ax1.text(0.02, 0.02, texto_info, transform=ax1.transAxes,
                 fontsize=7, verticalalignment='bottom',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

        self.canvas.fig.tight_layout()
        self.canvas.draw()