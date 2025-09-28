# Sección de importación de módulos

from Modules.UI.Header import show_header
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
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

nj = gpd.read_file(url_mapa)

nj_data = gpd.read_file(url_mapa)


if 'NAME' in nj_data.columns:
    county_names = nj_data['NAME']
else:
    col_name = [c for c in nj_data.columns if "NAME" in c]
    if col_name:
        county_names = nj_data[col_name[0]].map(lambda x: str(x).replace('NAME:"','').replace('"',''))
    else:
        county_names = ["Unknown"] * len(nj_data) 


nj = nj.copy() 
nj["NAME"] = county_names.values


nj["centroid"] = nj.geometry.centroid

# === 3. Crear el mapa hexagonal ===
fig, axs = plt.subplots(figsize=(12, 10), facecolor="white")

hb = axs.hexbin(
    df_coffee_tea["longitude"],
    df_coffee_tea["latitude"],
    gridsize=10,          # tamaño de los hexágonos
    cmap="CMRmap_r",
    mincnt=1,             # solo mostrar hexágonos con datos
    alpha=0.9,

)

# Contorno del mapa
nj.boundary.plot(ax=axs, edgecolor="black", linewidth=1.2)

# Barra de color
cb = fig.colorbar(hb, ax=axs)
cb.set_label("Número de Coffee & Tea Shops")

# === 4. Colocar etiquetas en los centroides ===
for idx, row in nj.iterrows():
    # Ensure row["centroid"] is a valid point geometry
    if row["centroid"] is not None and row["centroid"].is_valid:
        axs.text(
            row["centroid"].x,
            row["centroid"].y,
            row["NAME"],
            fontsize=8,
            color="gray",
            ha="center",
            va="center",
            weight="bold",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", boxstyle="round,pad=0.2")
        )

# Ajustes finales
axs.axis("off")
axs.set_title("Coffee & Tea Shops in NJ", fontsize=18, weight="bold")
plt.tight_layout()
st.pyplot(fig)


