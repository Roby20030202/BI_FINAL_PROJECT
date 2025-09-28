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


map_center = {"lat": 40.0, "lon": -74.5}

# Crear el mapa interactivo (Plotly hace la agrupación de densidad automáticamente
# si el número de puntos es grande)
fig = px.scatter_mapbox(
    df, # Usamos el DataFrame filtrado
    lat="latitude",
    lon="longitude",
    color="stars", # Podemos usar las estrellas para dar color o agrupar
    hover_name="address",
    zoom=7, # Nivel de zoom de NJ
    height=600,
    mapbox_style="carto-positron", # Un estilo de mapa limpio
    title="Mapa de Densidad de Negocios en NJ"
)

# Ajustar marcadores para mostrar la densidad visualmente
fig.update_traces(marker=dict(size=8, opacity=0.8), 
                  selector=dict(mode='markers'))

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True) 


