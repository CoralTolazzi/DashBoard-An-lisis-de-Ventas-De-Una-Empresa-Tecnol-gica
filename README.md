# 📊 DashBoard - Análisis de Ventas de una Empresa Tecnológica

Este proyecto presenta un **análisis integral de ventas** de una empresa dedicada a la comercialización de productos tecnológicos.
Incluye dos implementaciones del dashboard: una versión en **Streamlit** y otra en **Jupyter Notebook**, ambas basadas en los mismos datos.

---

## 🧩 Archivos Principales

| Archivo                     | Descripción                                                                                                                                               |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`analisis_de_ventas.py`** | Dashboard interactivo desarrollado con **Streamlit**. Permite visualizar métricas, ventas por rubro, evolución mensual, reseñas y productos más vendidos. |
| **`dashboard.ipynb`**       | Dashboard estático y análisis exploratorio en **Jupyter Notebook**. Muestra visualizaciones y storytelling analítico del desempeño comercial.             |

---

## 📁 Estructura del Proyecto

```
DashBoard-Analisis-de-Ventas-De-Una-Empresa-Tecnologica/
│
├── analisis_de_ventas.py        # Dashboard con Streamlit
├── dashboard.ipynb              # Dashboard con Jupyter
├── csv de ventas/               # Carpeta con todos los archivos CSV utilizados
│   ├── cliente.csv
│   ├── factura.csv
│   ├── detalle_factura.csv
│   ├── producto.csv
│   ├── rubro.csv
│   └── reseña.csv
│
└── README.md
```

---

## 🧮 Datos Utilizados

Los datos se encuentran en la carpeta **`csv de ventas/`**.
Contienen información sobre clientes, facturas, productos, rubros y reseñas de envío, utilizados para generar las métricas y gráficos del dashboard.

---

## 🚀 Ejecución del Dashboard en Streamlit

1. Instalar las dependencias:

   ```bash
   pip install streamlit pandas matplotlib numpy
   ```

2. Ejecutar el dashboard:

   ```bash
   streamlit run analisis_de_ventas.py
   ```

---

## 📖 Nota Importante

🟡 *El storytelling analítico no fue subido al repositorio por limitaciones de formato, pero fue entregado en formato impreso como parte del informe del proyecto.*
