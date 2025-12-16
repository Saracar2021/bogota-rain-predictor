import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import json

# Configuración de la página
st.set_page_config(
    page_title="🏍️ ¿Me voy a mojar?",
    page_icon="🌧️",
    layout="wide"
)

# Título principal
st.title("🏍️ Predictor de Lluvia para Motociclistas - Bogotá")
st.markdown("**Sistema basado en datos del SAB (Sistema de Alerta de Bogotá - IDIGER)**")

# Constantes
CKAN_BASE_URL = "https://datosabiertos.bogota.gov.co/api/3/action"
LLUVIA_RESOURCE_ID = "0f8e12d2-2115-49e2-9a05-1cfb55d26283"

# Coordenadas de referencia de Bogotá
BOGOTA_CENTER = [4.6533, -74.0836]
MODELIA_COORDS = [4.6892, -74.1063]  # Aproximado de Modelia

# Función para consultar la API del SAB
@st.cache_data(ttl=300)  # Cache por 5 minutos
def obtener_datos_lluvia():
    """Obtiene datos de lluvia del SAB via API CKAN"""
    try:
        url = f"{CKAN_BASE_URL}/datastore_search"
        params = {
            "resource_id": LLUVIA_RESOURCE_ID,
            "limit": 100
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                records = data['result']['records']
                df = pd.DataFrame(records)
                return df
            else:
                return None
        else:
            return None
    except Exception as e:
        st.error(f"Error al consultar API: {str(e)}")
        return None

# Función para obtener estaciones del catálogo
@st.cache_data(ttl=3600)  # Cache por 1 hora
def obtener_catalogo_estaciones():
    """Obtiene el catálogo de estaciones hidrometeorológicas"""
    # ID del recurso del catálogo de estaciones (puede variar)
    # Este es un placeholder - necesitaremos el ID correcto
    try:
        url = f"{CKAN_BASE_URL}/package_search"
        params = {
            "q": "Catalogo Estaciones Hidrometeorológicas",
            "rows": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data['result']['results']:
                # Aquí procesaríamos los recursos del dataset
                return data['result']['results']
        return None
    except Exception as e:
        st.warning(f"No se pudo obtener el catálogo de estaciones: {str(e)}")
        return None

# Función para crear mapa interactivo
def crear_mapa(origen_coords, destino_coords, datos_lluvia=None):
    """Crea un mapa de Folium con la ruta y datos de lluvia"""
    
    # Centrar el mapa entre origen y destino
    center_lat = (origen_coords[0] + destino_coords[0]) / 2
    center_lon = (origen_coords[1] + destino_coords[1]) / 2
    
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Marcador de origen (Modelia)
    folium.Marker(
        origen_coords,
        popup="🏠 Origen (Modelia)",
        tooltip="Punto de partida",
        icon=folium.Icon(color='green', icon='home')
    ).add_to(mapa)
    
    # Marcador de destino
    folium.Marker(
        destino_coords,
        popup="🎯 Destino",
        tooltip="Punto de llegada",
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(mapa)
    
    # Línea de ruta
    folium.PolyLine(
        [origen_coords, destino_coords],
        color='blue',
        weight=4,
        opacity=0.7,
        popup='Tu ruta en moto'
    ).add_to(mapa)
    
    # TODO: Agregar marcadores de estaciones con lluvia activa
    # Esto requiere procesar datos_lluvia si está disponible
    
    return mapa

# Función para calcular distancia aproximada
def calcular_distancia(coord1, coord2):
    """Calcula distancia aproximada entre dos coordenadas (fórmula de Haversine simplificada)"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Radio de la Tierra en km
    
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distancia = R * c
    return distancia

# Función para estimar tiempo de viaje
def estimar_tiempo_viaje(distancia_km, velocidad_promedio=25):
    """Estima tiempo de viaje en minutos"""
    tiempo_horas = distancia_km / velocidad_promedio
    tiempo_minutos = tiempo_horas * 60
    return tiempo_minutos

# Sidebar para inputs
st.sidebar.header("⚙️ Configuración de Viaje")

# Input de origen (por defecto Modelia)
st.sidebar.subheader("📍 Origen")
origen_lat = st.sidebar.number_input("Latitud origen", value=MODELIA_COORDS[0], format="%.6f")
origen_lon = st.sidebar.number_input("Longitud origen", value=MODELIA_COORDS[1], format="%.6f")

# Input de destino
st.sidebar.subheader("🎯 Destino")
destino_lat = st.sidebar.number_input("Latitud destino", value=4.6097, format="%.6f")
destino_lon = st.sidebar.number_input("Longitud destino", value=-74.0817, format="%.6f")

# Velocidad promedio en moto
velocidad = st.sidebar.slider("🏍️ Velocidad promedio (km/h)", 15, 40, 25)

# Botón de análisis
analizar = st.sidebar.button("🔍 Analizar Ruta", type="primary")

# Sección principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Mapa de tu Ruta")
    
    origen_coords = [origen_lat, origen_lon]
    destino_coords = [destino_lat, destino_lon]
    
    # Obtener datos de lluvia
    datos_lluvia = obtener_datos_lluvia()
    
    # Crear y mostrar mapa
    mapa = crear_mapa(origen_coords, destino_coords, datos_lluvia)
    st_folium(mapa, width=700, height=500)

with col2:
    st.subheader("📊 Análisis de Ruta")
    
    # Calcular métricas
    distancia = calcular_distancia(origen_coords, destino_coords)
    tiempo = estimar_tiempo_viaje(distancia, velocidad)
    
    st.metric("📏 Distancia", f"{distancia:.2f} km")
    st.metric("⏱️ Tiempo estimado", f"{tiempo:.1f} min")
    st.metric("🏍️ Velocidad promedio", f"{velocidad} km/h")
    
    st.divider()
    
    if analizar:
        st.subheader("🌧️ Estado de Lluvia")
        
        if datos_lluvia is not None and not datos_lluvia.empty:
            # Análisis básico de los datos
            st.success("✅ Datos del SAB obtenidos correctamente")
            
            # Mostrar información de los datos
            st.write(f"**Total de registros:** {len(datos_lluvia)}")
            
            # Intentar identificar columnas relevantes
            st.write("**Columnas disponibles:**")
            st.write(list(datos_lluvia.columns))
            
            # Vista previa de datos
            with st.expander("📋 Ver datos crudos"):
                st.dataframe(datos_lluvia.head(10))
            
            # Predicción básica (placeholder)
            st.info("🔮 **Análisis en desarrollo**")
            st.write("""
            Para completar la predicción necesitamos:
            - Identificar estaciones activas cerca de tu ruta
            - Analizar intensidad de lluvia actual
            - Obtener dirección y velocidad del viento
            - Proyectar movimiento de las lluvias
            """)
            
        else:
            st.warning("⚠️ No se pudieron obtener datos del SAB")
            st.write("Esto puede deberse a:")
            st.write("- Problemas de conectividad")
            st.write("- API temporalmente no disponible")
            st.write("- ID de recurso incorrecto")
            
            st.info("💡 **Modo Demo**")
            st.write("En modo demo, recomendamos:")
            st.write("- Consultar directamente https://app.sab.gov.co/sab/lluvias.htm")
            st.write("- Verificar visualmente las estaciones activas")

# Sección de información
st.divider()
st.subheader("ℹ️ Información del Sistema")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("**📡 Fuente de Datos**")
    st.write("Sistema de Alerta de Bogotá (SAB) - IDIGER")
    st.write("62 estaciones hidrometeorológicas")
    st.write("Actualización en tiempo real")

with col_info2:
    st.markdown("**🎯 Funcionalidades Actuales**")
    st.write("✅ Cálculo de distancia y tiempo")
    st.write("✅ Visualización de ruta")
    st.write("⏳ Predicción de lluvia (en desarrollo)")

with col_info3:
    st.markdown("**🚀 Próximas Mejoras**")
    st.write("🔄 Integración con OpenWeatherMap")
    st.write("🔄 Análisis de dirección de viento")
    st.write("🔄 Predicción ML con históricos")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p>Desarrollado para motociclistas de Bogotá 🏍️ | Datos: <a href='https://www.sab.gov.co/' target='_blank'>SAB IDIGER</a></p>
    <p>⚠️ Esta es una herramienta de referencia. Siempre verifica condiciones climáticas antes de salir.</p>
</div>
""", unsafe_allow_html=True)

# Debug info (solo en desarrollo)
if st.sidebar.checkbox("🔧 Mostrar info de debug"):
    st.sidebar.json({
        "origen": origen_coords,
        "destino": destino_coords,
        "distancia_km": round(distancia, 2),
        "tiempo_min": round(tiempo, 1),
        "velocidad_kmh": velocidad,
        "datos_disponibles": datos_lluvia is not None
    })
