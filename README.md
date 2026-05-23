# Simulador de Vaciado de Desarenador

Aplicación web para calcular la evolución del nivel de agua y el caudal de salida durante el vaciado de un **desarenador rectangular de fondo horizontal**. Pensada para ingenieros civiles, estudiantes o profesionales que necesiten estimar el tiempo de vaciado y las condiciones de flujo.

## 🔧 Supuestos del modelo

- **Geometría**: sección rectangular constante (largo `L`, ancho `W`). Fondo horizontal, sin pendiente.
- **Compuerta de salida**: rectangular, de ancho `B` y altura `d`. Se abre linealmente desde 0 hasta `d` en un tiempo `t_open`.
- **Régimen de flujo**: transición suave entre dos regímenes mediante una función sigmoide:
  - *Orificio*: cuando el nivel supera la apertura de la compuerta.
  - *Vertedero*: cuando el nivel está cerca o por debajo del borde superior de la compuerta.
- **Pérdidas**: únicamente por contracción en la salida (`Cd_orif`, `Cd_weir`). No se considera fricción en el canal ni pérdidas locales adicionales.
- **Integración numérica**: ecuación de continuidad resuelta con Runge‑Kutta RK45, con evento de parada al alcanzar el nivel mínimo `h_parada`.

## 📊 Resultados

- Gráfico interactivo de **nivel h (m)** y **caudal Q (m³/s)** vs. tiempo (doble eje Y).
- Panel de resumen con:
  - Tiempo total de vaciado.
  - Caudal máximo alcanzado.
  - Tiempo de apertura total de la compuerta.
  - Nivel inicial `h0`.
- Marcadores en el gráfico:
  - Fin de apertura de la compuerta (línea verde).
  - Instante de vaciado completo, cuando `h = h_parada` (línea roja).
  - Puntos de transición orificio‑vertedero.

## 🧪 Cómo usar

1. Ingresar los parámetros geométricos e hidráulicos en el panel izquierdo.
2. Presionar **Calcular**.
3. El gráfico y el panel de resumen se actualizan automáticamente.

> La aplicación corre completamente en el navegador. No envía datos a ningún servidor.

## 🛠️ Tecnologías

- [Pyodide v0.26.4](https://pyodide.org/) — Python en el navegador vía WebAssembly
- [Plotly.js v2.35.2](https://plotly.com/javascript/) — gráficos interactivos
- HTML5, CSS3, JavaScript vanilla
- Python 3.12 con NumPy y SciPy

## 📁 Estructura del proyecto

```
vaciado_desarenador/
├── calculos.py      # Lógica hidráulica (caudal, solver ODE)
├── web_main.py      # Puente Python/Pyodide para la web
├── index.html       # Interfaz web
├── .gitignore
├── LICENSE
└── README.md
```

> **Nota**: el modelo es simplificado para anteproyectos o estudios preliminares. No incluye pendiente de fondo, fricción en el canal ni efectos tridimensionales.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
