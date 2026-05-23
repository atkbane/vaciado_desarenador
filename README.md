# Simulador de Vaciado de Desarenador

Aplicación web para calcular la evolución del nivel de agua y el caudal de salida durante el vaciado de un **desarenador rectangular de fondo horizontal**. Pensada para ingenieros civiles, estudiantes o profesionales que necesiten estimar rápidamente el tiempo de vaciado y las condiciones de flujo.

## 🔧 Supuestos del modelo

- **Geometría**: sección rectangular constante (largo `L`, ancho `W`). Fondo horizontal (pendiente cero).
- **Compuerta de salida**: rectangular, de ancho `B` y altura `d`. Se abre linealmente desde 0 hasta `d` durante un tiempo `t_open`.
- **Régimen de flujo**: transición suave entre dos regímenes mediante una función sigmoide:
  - *Orificio*: cuando el nivel de agua supera la apertura de la compuerta.
  - *Vertedero*: cuando el nivel está cerca o por debajo del borde superior de la compuerta.
- **Pérdidas**: solo se consideran las pérdidas por contracción en la salida (`Cd_orif`, `Cd_weir`). No se incluye fricción en el canal ni pérdidas locales adicionales.
- **Integración numérica**: se resuelve la ecuación de continuidad mediante Runge‑Kutta de orden 4/5 (RK45), con un evento de parada cuando el nivel alcanza el valor mínimo `h_parada`.

## 📊 Resultados que entrega

- Gráfico interactivo de **nivel h (m)** y **caudal Q (m³/s)** vs. tiempo (doble eje Y).
- Panel de resumen con:
  - Tiempo total de vaciado.
  - Caudal máximo alcanzado.
  - Tiempo de apertura total de la compuerta.
  - Nivel inicial `h0`.
- Identificación visual en el gráfico de:
  - Fin de la apertura de la compuerta (línea verde).
  - Instante de vaciado completo, cuando `h = h_parada` (línea roja).
  - Puntos de transición orificio‑vertedero (marcadores).

## 🧪 Cómo usar

1. Ingresar los parámetros geométricos e hidráulicos en el panel izquierdo.
2. Presionar **Calcular**.
3. El gráfico y el panel de resumen se actualizan automáticamente.

> La aplicación funciona completamente en el navegador. No envía datos a ningún servidor.

## 📁 Estructura del proyecto

```
vaciado_desarenador/
├── calculos.py      # Lógica hidráulica (caudal, solver ODE)
├── web_main.py      # Puente Python/Pyodide para la web
├── index.html       # Interfaz web completa
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Despliegue en GitHub Pages

1. Sube los 3 archivos (`index.html`, `web_main.py`, `calculos.py`) a un repositorio público.
2. Ve a **Settings → Pages**.
3. En "Source", selecciona **Deploy from a branch**.
4. Elige `main` y la carpeta `/ (root)`.
5. En ~1 minuto el sitio estará disponible en `https://tu-usuario.github.io/tu-repo/`.

Para publicar actualizaciones:

```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

## 🛠️ Tecnologías

- [Pyodide v0.26.4](https://pyodide.org/) — Python en el navegador (WebAssembly)
- [Plotly.js v2.35.2](https://plotly.com/javascript/) — gráficos interactivos
- HTML5, CSS3, JavaScript vanilla
- Python 3.12 con NumPy y SciPy (biblioteca estándar de Pyodide)

> **Nota**: el modelo es intencionalmente simplificado para anteproyectos o estudios preliminares. No incluye pendiente del fondo, pérdidas por fricción ni efectos tridimensionales. Para cálculos detallados se recomienda un modelo hidráulico completo.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.
