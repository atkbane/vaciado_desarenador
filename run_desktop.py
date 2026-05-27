"""
Punto de entrada para la simulación de vaciado de desarenador (PySide6).
Ejecuta la interfaz gráfica con Qt.
"""
import sys
from PySide6.QtWidgets import QApplication
from interfaz import VentanaPrincipal


def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()