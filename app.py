# Sección de importación de módulos
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from Modules.UI.Header import show_header
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster

# =========================================================
# === 1. DEFINICIÓN DE COLUMNAS ===
# =========================================================

COFFEE_COLUMNS = ['Coffee & Tea',
    'Cafes',
    'Restaurants',
    'Breakfast & Brunch',
    'Bakeries',
    'Desserts',
    'Grocery',
    'Specialty Food',
    'Convenience Stores',
    'Coffee Roasteries',
    'Food Trucks',
    'Bars',
    'Donuts',
    'Bagels']

# Seción para crear la GUI
show_header("Análisis de Negocios NJ")

url = 'https://raw.githubusercontent.com/Roby20030202/BI_FINAL_PROJECT/refs/heads/main/filtered_yelp_NJ.csv'
# url_mapa ya no es necesario

df = pd.read_csv(url,index_col=0)

# definiendo columnas del dataset
columns = ['address','city','state','latitude','longitude','stars','review_count','is_open'] + COFFEE_COLUMNS
df = df[columns]

# Aseguramos que el DataFrame principal solo contenga negocios relevantes
condition = (df[COFFEE_COLUMNS] == 1).any(axis=1)
df = df[condition]

# =========================================================
# === 2. WIDGETS DE FILTRADO ===
# =========================================================

st.sidebar.title("Opciones de Filtrado")

# WIDGET 1: Filtro por Tipo de Establecimiento (MULTISELECT)
categorias_seleccionadas = st.sidebar.multiselect(
    '1. Selecciona el Tipo(s) de Establecimiento:',
    options=COFFEE_COLUMNS, 
    default=[COFFEE_COLUMNS[0]] # Selecciona 'Coffee & Tea' por defecto
)

# WIDGET 2: Filtro por Estrellas (Slider)
min_stars = st.sidebar.slider(
    '2. Calificación Mínima de Estrellas (stars):',
    min_value=1.0, 
    max_value=5.0, 
    value=3.5, # Valor por defecto
    step=0.5  
)

# =========================================================
# === 3. APLICACIÓN DEL DOBLE FILTRO (Lógica ajustada) ===
# =========================================================

# Manejar el caso donde no hay categorías seleccionadas
if not categorias_seleccionadas:
    st.error("Por favor, selecciona al menos un tipo de establecimiento.")
    # Usamos un DataFrame vacío para evitar errores en las gráficas
    df_filtrado_final = df.head(0) 
else:
    # PASO A: Filtrar por Categorías seleccionadas (¡Lógica Multiselect!)
    # Creamos una máscara booleana: un negocio califica si es 1 en CUALQUIERA
    # de las columnas seleccionadas (usando sum() > 0)
    condicion_multiselect = (df[categorias_seleccionadas].sum(axis=1) >= 1)
    df_categoria = df[condicion_multiselect].copy()

    # PASO B: Filtrar el resultado anterior por la Calificación Mínima
    df_filtrado_final = df_categoria[df_categoria['stars'] >= min_stars].copy()


st.subheader(f"Mapa de Negocios Seleccionados")
st.write(f"Mostrando **{len(df_filtrado_final)}** negocios con **{min_stars}** estrellas o más, en las categorías: **{', '.join(categorias_seleccionadas)}**.")

# =========================================================
# === 4. GENERACIÓN DEL MAPA (Plotly Express) ===
# =========================================================

map_center = {"lat": 40.0, "lon": -74.5}

fig = px.scatter_mapbox(
    df_filtrado_final, 
    lat="latitude",
    lon="longitude",
    color="stars", 
    hover_data=['address', 'city', 'stars', 'review_count'], 
    zoom=7, 
    height=600,
    mapbox_style="carto-positron", 
    title=f"Ubicación de Negocios en NJ ({min_stars}+ estrellas)"
)

# Ajustes de marcadores y layout
fig.update_traces(marker=dict(size=8, opacity=0.8), selector=dict(mode='markers'))
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)

# =========================================================
# === 5. GRÁFICA SUNBURST (Distribución Jerárquica) ===
# =========================================================

st.markdown("---") 
st.subheader("Distribución de Negocios por Tipo y Calificación")

# La preparación para Sunburst sigue siendo válida, pero ahora usa el MULTISELECT.
if len(df_filtrado_final) > 0:
    
    # Preparamos COFFEE_COLUMNS con las categorías seleccionadas, no todas.
    # Esto es crucial para que el Sunburst refleje SÓLO las selecciones del usuario.
    df_melted = df_filtrado_final.melt(
        id_vars=['stars'], 
        value_vars=categorias_seleccionadas, # <-- ¡Solo las seleccionadas!
        var_name='Category_Name', 
        value_name='Is_Member'
    )

    # Filtrar para obtener solo las asignaciones donde el negocio es miembro (valor == 1)
    df_sunburst = df_melted[df_melted['Is_Member'] == 1].copy()

    # Creamos una columna 'Count' simple para el recuento.
    df_sunburst['Count'] = 1 

    # Crear la columna de agrupamiento de estrellas (para la jerarquía)
    df_sunburst['Stars_Group'] = df_sunburst['stars'].apply(
        lambda x: f"{int(x)} Estrellas" if x.is_integer() else f"{x} Estrellas"
    )

    # Generación de la Gráfica Sunburst
    fig_sunburst = px.sunburst(
        df_sunburst,
        path=['Category_Name', 'Stars_Group'], 
        values='Count', 
        color='Stars_Group', 
        hover_data=['stars'],
        title="Jerarquía de Categorías con Calificación Mínima Aplicada"
    )
    
    # Mostrar la gráfica Sunburst en Streamlit
    st.plotly_chart(fig_sunburst, use_container_width=True)
else:
    st.warning("No hay datos para mostrar el Sunburst con los filtros actuales.")

# =========================================================
# === 6. VISTA DE TABLA DE DATOS FILTRADOS ===
# =========================================================

st.markdown("---")
st.subheader("Tabla de Registros Filtrados (Ordenados por Revisiones)")

if len(df_filtrado_final) > 0:
    # Creamos una copia para ordenar y la ordenamos de mayor a menor (ascending=False)
    df_tabla_ordenada = df_filtrado_final.sort_values(
        by='review_count', 
        ascending=False
    )
    
    # Seleccionamos solo las columnas clave para una mejor visualización en la tabla
    columnas_tabla = ['address', 'city', 'stars', 'review_count'] + categorias_seleccionadas
    
    # Mostramos el DataFrame ordenado como una tabla interactiva
    st.dataframe(df_tabla_ordenada[columnas_tabla])
else:
    st.info("No hay registros para mostrar en la tabla con los criterios de filtro seleccionados.")
