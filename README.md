# Simulador de Vaciado de Desarenador

Este programa calcula la evolución del nivel de agua y el caudal de salida durante el vaciado de un **desarenador rectangular de fondo horizontal** (sin pendiente). Está pensado para ingenieros civiles, estudiantes o profesionales que quieran estimar rápidamente el tiempo de vaciado y las condiciones de flujo.

## 🔧 Supuestos del modelo

- **Geometría**: desarenador de sección rectangular constante (ancho W, largo L). El fondo se considera horizontal (pendiente cero).
- **Compuerta de salida**: rectangular, de ancho B y altura d. Se abre linealmente durante un tiempo `t_open` (desde 0 hasta d).
- **Régimen de flujo**: se considera una transición suave entre:
  - *Orificio*: cuando el nivel de agua es mayor que la apertura de la compuerta.
  - *Vertedero*: cuando el nivel está cerca o por debajo del borde superior de la compuerta.
  - La combinación se hace con una función sigmoide (transición continua).
- **Pérdidas**: solo se considera la pérdida de carga por contracción en la salida (coeficientes Cd_orif y Cd_weir). No se incluye fricción en el canal ni pérdidas locales adicionales.
- **Cálculo**: se resuelve la ecuación de continuidad (volumen = área del desarenador × nivel) mediante integración numérica (Runge‑Kutta) con un evento de parada cuando el nivel alcanza un valor mínimo `h_parada`.

## 📊 Resultados que entrega

- Gráfico interactivo de **nivel (m)** y **caudal (m³/s)** vs tiempo.
- Tiempo total de vaciado.
- Caudal máximo y el instante en que ocurre.
- Identificación visual de:
  - Fin de la apertura de la compuerta.
  - Transición orificio‑vertedero.
  - Nivel de parada.

## 🧪 Cómo usar

1. Ingresar los parámetros geométricos e hidráulicos en el panel izquierdo.
2. Presionar “Calcular”.
3. El gráfico y las estadísticas se actualizan automáticamente.

## 📁 Tecnología

- **Motor de cálculo**: Python (NumPy, SciPy) ejecutado en el navegador gracias a Pyodide.
- **Interfaz**: HTML5, CSS y JavaScript puro.
- **Gráficos**: Plotly.js (interactivos, zoom, exportación).
- **Despliegue**: GitHub Pages (estático, gratuito).

> **Nota**: El modelo es intencionalmente simplificado para facilitar su uso en anteproyectos o estudios preliminares. No incluye pendiente del fondo, pérdidas por fricción ni efectos tridimensionales. Para cálculos más detallados se recomienda un modelo hidráulico completo.
