import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time
import graphviz

st.set_page_config(page_title="SeviciMap", page_icon="bike", layout="wide")
sevici_image="./sevicilogo.jpg"
url = "./sevicidist.csv"
sevici = pd.read_csv(url)
sevici.pop("Unnamed: 0")
st.sidebar.title("Sevici Visualization App")
st.sidebar.image(sevici_image)
menu = st.sidebar.selectbox("Menu", ["Problema de Negocio", "Datos", "Visualizacion", "Filtrado", "BONUS"])


if menu == "Datos":
    st.metric("Número total de bicis en sevilla", value=sevici["CAPACITY"].sum(), delta=20)
    st.dataframe(sevici)
elif menu == "Problema de Negocio":
    st.title("Hipotetico Problema de negocio donde posicionar bicis electricas en sevilla")
    graph = graphviz.Digraph()
    graph.edge('Problema Real', 'Hipotesis')
    graph.edge('Hipotesis', 'Estrategia')
    graph.edge('Estrategia', 'POC')
    graph.edge('POC', 'Estrategia')
    graph.edge('POC', 'Producto Final')

    graph2= graphviz.Digraph()
    graph2.edge('Obtencion de Datos', 'Investigación')
    graph2.edge('Investigación', 'Consumo API overpass')
    graph2.edge('Investigación', 'Pruebo en Notebooks')
    graph2.edge('Consumo API overpass', 'Streamlit.py')
    graph2.edge('Pruebo en Notebooks', 'Streamlit.py')

    col1, col2 =st.columns(2)
    col1.graphviz_chart(graph)
    col2.graphviz_chart(graph2)

    st.write("Una empresa de bicis electricas nos contrata como Data Scientists y el primer proyecto\
           en el que vamos a trabajar consiste en crear un pequeño dashboard de visualizacion para obtener\
           informacion geográfica sobre las estaciones Sevici en Sevilla.")
elif menu == "Visualizacion":
    st.map(sevici)
elif menu == "Filtrado":
    radio = st.sidebar.radio("Seleccione una opción de filtro", ["Calle", "Capacidad & Distrito"])
    if radio == "Calle":
        calle = st.sidebar.selectbox("Calles", sevici["CALLE"])
        street_mask = sevici["CALLE"] == calle
        st.dataframe(sevici[street_mask])
        st.map(sevici[street_mask])
    elif radio == "Capacidad & Distrito":
        radio2 = st.sidebar.radio("Capacidades", ["<20", ">=20"])
        radio3 =st.sidebar.radio("Distritos", [1, 2, 3, 4])
        capacity_20_mask = sevici["CAPACITY"] <20
        capacity_21_mask = sevici["CAPACITY"] >= 20
        district_mask = sevici["Distrito"] == radio3
        if (radio2 == "<20") & (radio3 == 1):
            filtered_street = sevici[district_mask & capacity_20_mask]
            st.dataframe(filtered_street)
            st.map(filtered_street)
        elif (radio2 == "<20") & (radio3 == 2):
            filtered_street = sevici[district_mask & capacity_20_mask]
            st.dataframe(filtered_street)
            st.map(filtered_street)
        elif (radio2 == "<20") & (radio3 == 3):
            filtered_street = sevici[district_mask & capacity_20_mask]
            st.dataframe(filtered_street)
            st.map(filtered_street) 
        elif (radio2 == "<20") & (radio3 == 4):
            filtered_street = sevici[district_mask & capacity_20_mask]
            st.dataframe(filtered_street)
            st.map(filtered_street)            
        elif (radio2 == ">=20") & (radio3 == 1):
            filtered_street2 = sevici[district_mask & capacity_21_mask]
            st.dataframe(filtered_street2)
            st.map(filtered_street2)
        elif (radio2 == ">=20") & (radio3 == 2):
            filtered_street2 = sevici[district_mask & capacity_21_mask]
            st.dataframe(filtered_street2)
            st.map(filtered_street2)
        elif (radio2 == ">=20") & (radio3 == 3):
            filtered_street2 = sevici[district_mask & capacity_21_mask]
            st.dataframe(filtered_street2)
            st.map(filtered_street2)
        elif (radio2 == ">=20") & (radio3 == 4):
            filtered_street2 = sevici[district_mask & capacity_21_mask]
            st.dataframe(filtered_street2)
            st.map(filtered_street2)
elif menu == "BONUS":
    progress_text = "Cargando"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.005)
        my_bar.progress(percent_complete + 1, text=progress_text)
    with st.spinner(""):
            time.sleep(1)

    st.title("Mapa 3d")
    st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.4,
        longitude=-6,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=sevici,
           get_position='[LON, LAT]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=sevici,
            get_position='[LON, LAT]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))