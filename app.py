# Sección de importación de módulos
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from Modules.UI.Header import show_header
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster

# Seción para crear la GUI
show_header("Mi primera GUI en Streamlit")

url = 'https://raw.githubusercontent.com/Roby20030202/BI_FINAL_PROJECT/refs/heads/main/filtered_yelp_NJ.csv'
url_mapa = "https://raw.githubusercontent.com/edavgaun/topojson/080eb96a46307efd0c4a31f4c11ccabeee5e97dd/countries/us-states/NJ-34-new-jersey-counties.json"

df = pd.read_csv(url,index_col=0)

# definiendo columnas del dataset
columns = ['address','city','state','latitude','longitude','stars','review_count','is_open','Coffee & Tea',
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
df = df[columns]

coffee_columns = ['Coffee & Tea',
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
df = df[coffee_columns + ['address','city','state','latitude','longitude','stars','review_count','is_open']]
condition = (df[coffee_columns] == 1).any(axis=1)
df = df[condition]

st.sidebar.title("Opciones de Filtrado")

# WIDGET 1: Filtro por Tipo de Establecimiento (Selectbox)
categoria_seleccionada = st.sidebar.selectbox(
    '1. Selecciona el Tipo de Establecimiento:',
    options=COFFEE_COLUMNS, 
    index=0  # 'Coffee & Tea' por defecto
)

# WIDGET 2: Filtro por Estrellas (Slider)
min_stars = st.sidebar.slider(
    '2. Calificación Mínima de Estrellas (stars):',
    min_value=1.0, 
    max_value=5.0, 
    value=3.5, # Valor por defecto
    step=0.5  
)

# PASO A: Filtrar por Categoría seleccionada (Solo negocios donde la columna es 1)
df_categoria = df[df[categoria_seleccionada] == 1].copy()

# PASO B: Filtrar el resultado anterior por la Calificación Mínima
df_filtrado_final = df_categoria[df_categoria['stars'] >= min_stars].copy()


st.subheader(f"Mapa de {categoria_seleccionada}")
st.write(f"Mostrando **{len(df_filtrado_final)}** negocios con **{min_stars}** estrellas o más.")

map_center = {"lat": 40.0, "lon": -74.5}

fig = px.scatter_mapbox(
    df_filtrado_final, # <-- ¡CLAVE! Usar el DataFrame DOBLEMENTE FILTRADO
    lat="latitude",
    lon="longitude",
    color="stars", # Colorea los puntos según las estrellas
    hover_data=['address', 'city', 'stars', 'review_count'], # Muestra estos datos al pasar el mouse
    zoom=7, 
    height=600,
    mapbox_style="carto-positron", 
    title=f"Ubicación de {categoria_seleccionada} en NJ ({min_stars}+ estrellas)"
)

# Ajustes de marcadores y layout
fig.update_traces(marker=dict(size=8, opacity=0.8), selector=dict(mode='markers'))
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)

