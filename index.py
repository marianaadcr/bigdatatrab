import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap


st.set_page_config(page_title="Análise de Dados de Pedidos", layout="wide")

st.sidebar.image("natura.png",caption='natura' )

file_path = 'separated.csv'  
df = pd.read_csv(file_path, sep=';', encoding='latin1')

df.columns = df.columns.str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

zonas_coordenadas = {
    'sul': [-22.9756, -43.2237],
    'norte': [-22.8598, -43.2400],
    'oeste': [-22.9112, -43.3149],
    'central': [-22.9068, -43.1729]
}

df['latitude'] = df['zona'].map(lambda x: zonas_coordenadas[x][0] if x in zonas_coordenadas else None)
df['longitude'] = df['zona'].map(lambda x: zonas_coordenadas[x][1] if x in zonas_coordenadas else None)

df = df.dropna(subset=['latitude', 'longitude'])

st.title('🛍️ Análise de Dados de Pedidos')

st.subheader('📊 Visualização dos Dados:')
st.dataframe(df)

st.subheader('📊 Análise de Níveis por Quantidade de Pedidos:')
nivel_counts = df['Nivel'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=nivel_counts.index, y=nivel_counts.values, palette='viridis', ax=ax)
ax.set_title('Quantidade de Pedidos por Nível')
ax.set_xlabel('Nível')
ax.set_ylabel('Quantidade de Pedidos')
st.pyplot(fig)

st.write("🚀 Carregando análise...")
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.05)
    progress_bar.progress(i + 1)

situacoes_unicas = list(df['Situacao do pedido'].unique())
if "Cancelado" not in situacoes_unicas:
    situacoes_unicas.append("Cancelado")

st.subheader('🔍 Filtrar Pedidos por Situação:')
situacao = st.selectbox('Selecione a situação do pedido', situacoes_unicas)
df_filtrado = df[df['Situacao do pedido'] == situacao]
st.write(f'Dados filtrados para "{situacao}":')
st.dataframe(df_filtrado)

st.subheader('📊 Análise de Zonas por Quantidade de Pedidos:')
zona_counts = df_filtrado['zona'].value_counts()
fig3, ax3 = plt.subplots()
sns.barplot(x=zona_counts.index, y=zona_counts.values, palette='coolwarm', ax=ax3)
ax3.set_title('Quantidade de Pedidos por Zona')
ax3.set_xlabel('Zona')
ax3.set_ylabel('Quantidade de Pedidos')
st.pyplot(fig3)


total_pedidos = len(df)
pedidos_por_zona = df['zona'].value_counts().to_dict()

map_center = [df['latitude'].mean(), df['longitude'].mean()]  
m = folium.Map(location=map_center, zoom_start=11)

folium.Marker(
    location=map_center,
    popup=f"Total de pedidos: {total_pedidos}",
    icon=folium.Icon(color="red",icon="info-sign")
).add_to(m)




for _, row in df.iterrows():
    zona = row['zona']
    quantidade_pedidos = pedidos_por_zona.get(zona, 0)  
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Zona: {zona}<br>Quantidade de Pedidos: {quantidade_pedidos}",
    ).add_to(m)

st.subheader('🗺️ Mapa de Zonas:')
folium_static(m)

map_center = [df['latitude'].mean(), df['longitude'].mean()]  
m = folium.Map(location=map_center, zoom_start=11)

# Adicionando o mapa de calor ao mapa folium
heat_data = [[row['latitude'], row['longitude']] for _, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

st.subheader('🗺️ Mapa de Calor de Pedidos por Zona:')
folium_static(m)


st.write("🔚 Fim da Análise!")
