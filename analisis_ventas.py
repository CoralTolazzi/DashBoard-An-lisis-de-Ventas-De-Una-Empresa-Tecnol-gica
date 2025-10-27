import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ----------------------------------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------------------------------
st.set_page_config(page_title="Análisis de Ventas - Empresa Tecnológica", layout="wide")
st.title("📊 **Análisis de Ventas de una Empresa de Productos Tecnológicos**")

st.markdown("""
Este dashboard realiza un **análisis integral** de las ventas y reseñas de una empresa dedicada
a la comercialización de productos tecnológicos.  
A partir de archivos CSV, se analizan:
- Rendimiento general de ventas  
- Rubros más rentables  
- Clientes con mayor volumen de compra  
- Evolución mensual de las ventas  
- Productos más vendidos  
- Promedio de reseñas y desempeño de envíos  
""")

# ----------------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------------
st.header("📂 Carga de Datos")

base_path = "csv de ventas_2025/"
archivos = ["cliente.csv", "factura.csv", "detalle_factura.csv", "producto.csv", "rubro.csv", "reseña.csv"]

faltantes = [f for f in archivos if not os.path.exists(os.path.join(base_path, f))]

if faltantes:
    st.error("❌ No se encontraron los siguientes archivos requeridos:")
    for f in faltantes:
        st.write(f"   - {f}")
    st.stop()
else:
    clientes = pd.read_csv(base_path + "cliente.csv")
    facturas = pd.read_csv(base_path + "factura.csv")
    detalle = pd.read_csv(base_path + "detalle_factura.csv")
    productos = pd.read_csv(base_path + "producto.csv")
    rubros = pd.read_csv(base_path + "rubro.csv")
    reseñas = pd.read_csv(base_path + "reseña.csv")
    st.success("✅ Archivos cargados correctamente.")

# ----------------------------------------------------
# PREPARACIÓN DE DATOS
# ----------------------------------------------------
df = detalle.merge(productos, on="id_producto", how="left")
df = df.merge(rubros, on="id_rubro", how="left")
df = df.merge(facturas, on="id_factura", how="left")
df = df.merge(clientes, on="id_cliente", how="left")
df = df.merge(reseñas[['id_factura', 'puntaje', 'fecha_reseña']], on="id_factura", how="left")

df["subtotal"] = df["cantidad"] * df["precio_unitario"]
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
df["fecha_reseña"] = pd.to_datetime(df["fecha_reseña"], errors="coerce")

# ----------------------------------------------------
# MÉTRICAS PRINCIPALES
# ----------------------------------------------------
st.header("📈 Métricas Generales")

total_ventas = df["subtotal"].sum()
total_facturas = df["id_factura"].nunique()
total_clientes = df["id_cliente"].nunique()
total_productos = df["id_producto"].nunique()
ventas_cantidad = df.groupby("descripcion")["cantidad"].sum().sort_values(ascending=False)

# ----------------------------------------------------
# LIMPIEZA DE FECHAS Y FILTRO DE 2025
# ----------------------------------------------------
# Convertimos la columna a datetime (ignorando errores)
reseñas["fecha_reseña"] = pd.to_datetime(reseñas["fecha_reseña"], errors="coerce")

# Ahora filtramos solo las reseñas válidas con fecha en 2025
reseñas_unicas_2025 = reseñas[reseñas["fecha_reseña"].notna() & (reseñas["fecha_reseña"].dt.year == 2025)]

# Si no hay reseñas válidas, mostramos una advertencia
if reseñas_unicas_2025.empty:
    st.warning("⚠️ No hay reseñas registradas para el año 2025.")
    reseña_promedio = 0
    total_reseñas_texto = 0
else:
    reseña_promedio = reseñas_unicas_2025['puntaje'].mean()
    total_reseñas_texto = len(reseñas_unicas_2025)
reseña_promedio = reseñas_unicas_2025['puntaje'].mean() if not reseñas_unicas_2025.empty else 0
total_reseñas_texto = len(reseñas_unicas_2025) if not reseñas_unicas_2025.empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Ventas", f"${total_ventas:,.2f}")
col2.metric("🧾 Total Facturas", f"{total_facturas}")
col3.metric("👥 Clientes Únicos", f"{total_clientes}")
col4.metric("📦 Productos Vendidos", f"{total_productos}")

st.metric("⭐ Reseña Promedio 2025", f"{reseña_promedio:.1f}/5 ({total_reseñas_texto} reseñas)")

# ----------------------------------------------------
# VENTAS POR RUBRO
# ----------------------------------------------------
st.header("🏷️ Ventas por Rubro")

ventas_rubro = df.groupby("nombre_rubro")["subtotal"].sum().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(7, 5))
colors_rubro = plt.cm.Set3(np.linspace(0, 1, len(ventas_rubro)))
ax.barh(ventas_rubro.index, ventas_rubro.values, color=colors_rubro)
ax.set_title("Ventas por Rubro")
ax.set_xlabel("Monto en $")
st.pyplot(fig)

# ----------------------------------------------------
# TOP CLIENTES
# ----------------------------------------------------
st.header("👑 Top Clientes")

top_clientes = df.groupby("nombre")["subtotal"].sum().sort_values(ascending=False).head(8)
fig, ax = plt.subplots(figsize=(7, 5))
colors_clientes = plt.cm.viridis(np.linspace(0.2, 0.8, len(top_clientes)))
ax.barh(top_clientes.index, top_clientes.values, color=colors_clientes)
ax.set_title("Top Clientes (por Monto)")
ax.set_xlabel("Monto en $")
ax.invert_yaxis()
st.pyplot(fig)

# ----------------------------------------------------
# EVOLUCIÓN MENSUAL DE VENTAS
# ----------------------------------------------------
st.header("📆 Evolución Mensual de Ventas 2025")

df_2025 = df[df["fecha"].dt.year == 2025]
ventas_2025_mes = df_2025.groupby(df_2025["fecha"].dt.month)["subtotal"].sum().reindex(range(1, 13), fill_value=0)
meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

fig, ax = plt.subplots(figsize=(8, 4))
ax.fill_between(range(1, 13), ventas_2025_mes.values, alpha=0.3, color='green')
ax.plot(range(1, 13), ventas_2025_mes.values, marker='o', color='green', linewidth=2)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(meses)
ax.set_title("Evolución Mensual de Ventas (2025)")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ----------------------------------------------------
# TOP PRODUCTOS
# ----------------------------------------------------
st.header("📊 Productos Más Vendidos")

top_productos_cantidad = ventas_cantidad.head(10).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8, 5))
colors_productos = plt.cm.plasma(np.linspace(0.2, 0.8, len(top_productos_cantidad)))
ax.barh(top_productos_cantidad.index, top_productos_cantidad.values, color=colors_productos)
ax.set_title("Top Productos Más Vendidos (por Cantidad)")
ax.set_xlabel("Cantidad vendida")
st.pyplot(fig)

# ----------------------------------------------------
# RESEÑAS DE ENVÍOS
# ----------------------------------------------------
st.header("📦 Reseñas de Envíos (2025)")

reseñas_2025 = df[df["fecha_reseña"].dt.year == 2025].copy()
if not reseñas_2025.empty:
    reseñas_mensuales = reseñas_2025.groupby(reseñas_2025["fecha_reseña"].dt.month).agg({
        'puntaje': 'mean',
        'id_factura': 'count'
    }).reindex(range(1, 13), fill_value=0)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    color_linea = 'red'
    ax1.plot(range(1, 13), reseñas_mensuales['puntaje'], marker='o', color=color_linea, linewidth=3)
    ax1.set_ylabel('Puntaje Promedio (1-5)', color=color_linea)
    ax1.tick_params(axis='y', labelcolor=color_linea)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(meses)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color_barras = 'skyblue'
    ax2.bar(range(1, 13), reseñas_mensuales['id_factura'], alpha=0.6, color=color_barras)
    ax2.set_ylabel('Cantidad de Reseñas', color=color_barras)
    ax2.tick_params(axis='y', labelcolor=color_barras)

    fig.suptitle("Evolución de Reseñas de Envíos (2025)")
    st.pyplot(fig)

    puntaje_promedio_total = reseñas_mensuales['puntaje'].mean()
    total_reseñas = reseñas_mensuales['id_factura'].sum()
    st.info(f"**Puntaje Promedio General:** {puntaje_promedio_total:.2f}/5 | **Total Reseñas:** {total_reseñas}")
else:
    st.warning("No hay reseñas registradas para 2025.")

# ----------------------------------------------------
# RESUMEN EJECUTIVO
# ----------------------------------------------------
st.header("🧾 Resumen Ejecutivo")

st.subheader("Top 5 Clientes")
for i, (cliente, monto) in enumerate(top_clientes.head(5).items(), 1):
    st.write(f"**{i}. {cliente}** — ${monto:,.2f}")

st.subheader("Top 5 Productos Más Vendidos")
for i, (producto, cantidad) in enumerate(ventas_cantidad.head(5).items(), 1):
    monto_producto = df[df["descripcion"] == producto]["subtotal"].sum()
    st.write(f"**{i}. {producto}** — {cantidad} unidades | ${monto_producto:,.2f}")

st.subheader("Ventas por Rubro")
for rubro, venta in ventas_rubro.sort_values(ascending=False).items():
    porcentaje = (venta / total_ventas) * 100
    st.write(f"- **{rubro}**: ${venta:,.2f} ({porcentaje:.1f}%)")
