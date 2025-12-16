"""
Utilidades para consultas a la API del SAB y análisis de datos
"""

import requests
import pandas as pd
from typing import Optional, List, Dict, Tuple
from datetime import datetime

# Configuración de APIs
CKAN_BASE_URL = "https://datosabiertos.bogota.gov.co/api/3/action"
SAB_WEB_URL = "https://app.sab.gov.co"

# IDs de recursos conocidos
RESOURCE_IDS = {
    "lluvia_diaria": "0f8e12d2-2115-49e2-9a05-1cfb55d26283",
    "catalogo_estaciones": None,  # Por determinar
    "radar": None  # Por determinar
}


class SABAPIClient:
    """Cliente para interactuar con la API del SAB via CKAN"""
    
    def __init__(self, base_url: str = CKAN_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BogotaRainPredictor/1.0'
        })
    
    def buscar_datasets(self, query: str, rows: int = 10) -> Optional[Dict]:
        """Busca datasets en el portal de datos abiertos"""
        try:
            url = f"{self.base_url}/package_search"
            params = {
                "q": query,
                "rows": rows
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['result']
            return None
        except Exception as e:
            print(f"Error buscando datasets: {e}")
            return None
    
    def obtener_recursos_dataset(self, dataset_id: str) -> Optional[List[Dict]]:
        """Obtiene los recursos de un dataset específico"""
        try:
            url = f"{self.base_url}/package_show"
            params = {"id": dataset_id}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['result'].get('resources', [])
            return None
        except Exception as e:
            print(f"Error obteniendo recursos: {e}")
            return None
    
    def consultar_datastore(
        self, 
        resource_id: str, 
        limit: int = 100,
        filters: Optional[Dict] = None,
        fields: Optional[List[str]] = None
    ) -> Optional[pd.DataFrame]:
        """Consulta el datastore de un recurso"""
        try:
            url = f"{self.base_url}/datastore_search"
            params = {
                "resource_id": resource_id,
                "limit": limit
            }
            
            if filters:
                params["filters"] = filters
            
            if fields:
                params["fields"] = ",".join(fields)
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    records = data['result']['records']
                    return pd.DataFrame(records)
            return None
        except Exception as e:
            print(f"Error consultando datastore: {e}")
            return None
    
    def consultar_sql(self, sql_query: str) -> Optional[pd.DataFrame]:
        """Ejecuta una consulta SQL en el datastore"""
        try:
            url = f"{self.base_url}/datastore_search_sql"
            params = {"sql": sql_query}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    records = data['result']['records']
                    return pd.DataFrame(records)
            return None
        except Exception as e:
            print(f"Error en consulta SQL: {e}")
            return None


class RainAnalyzer:
    """Analizador de datos de lluvia y predicción de ruta"""
    
    @staticmethod
    def calcular_distancia_haversine(
        coord1: Tuple[float, float], 
        coord2: Tuple[float, float]
    ) -> float:
        """
        Calcula distancia entre dos coordenadas usando fórmula de Haversine
        
        Args:
            coord1: (latitud, longitud) del punto 1
            coord2: (latitud, longitud) del punto 2
            
        Returns:
            Distancia en kilómetros
        """
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Radio de la Tierra en km
        
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    @staticmethod
    def punto_esta_cerca_ruta(
        punto: Tuple[float, float],
        origen: Tuple[float, float],
        destino: Tuple[float, float],
        tolerancia_km: float = 1.0
    ) -> bool:
        """
        Verifica si un punto está cerca de la ruta (línea recta) entre origen y destino
        
        Args:
            punto: Coordenadas del punto a evaluar
            origen: Coordenadas de origen
            destino: Coordenadas de destino
            tolerancia_km: Distancia máxima en km para considerar "cerca"
            
        Returns:
            True si el punto está cerca de la ruta
        """
        # Calcular distancia del punto a origen y destino
        dist_origen = RainAnalyzer.calcular_distancia_haversine(punto, origen)
        dist_destino = RainAnalyzer.calcular_distancia_haversine(punto, destino)
        dist_ruta = RainAnalyzer.calcular_distancia_haversine(origen, destino)
        
        # Si la suma de distancias es aproximadamente igual a la distancia de ruta,
        # el punto está en la línea
        suma_distancias = dist_origen + dist_destino
        diferencia = abs(suma_distancias - dist_ruta)
        
        return diferencia <= tolerancia_km
    
    @staticmethod
    def analizar_lluvia_en_ruta(
        datos_lluvia: pd.DataFrame,
        origen: Tuple[float, float],
        destino: Tuple[float, float],
        tolerancia_km: float = 2.0
    ) -> Dict:
        """
        Analiza datos de lluvia cerca de la ruta
        
        Args:
            datos_lluvia: DataFrame con datos de estaciones
            origen: Coordenadas de origen
            destino: Coordenadas de destino
            tolerancia_km: Radio de búsqueda en km
            
        Returns:
            Diccionario con análisis de lluvia en ruta
        """
        # Placeholder - requiere conocer estructura exacta de datos_lluvia
        # Esto dependerá de las columnas reales del dataset SAB
        
        resultado = {
            "hay_lluvia_activa": False,
            "estaciones_cercanas": [],
            "intensidad_promedio": 0.0,
            "recomendacion": "SALIR"
        }
        
        # TODO: Implementar lógica real cuando sepamos estructura de datos
        # Por ejemplo:
        # - Filtrar estaciones con lat/lon cerca de la ruta
        # - Identificar cuáles tienen lluvia activa
        # - Calcular intensidad promedio
        # - Generar recomendación
        
        return resultado


class WeatherAPIClient:
    """Cliente para APIs meteorológicas externas (OpenWeatherMap, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def obtener_clima_actual(self, lat: float, lon: float) -> Optional[Dict]:
        """Obtiene clima actual para coordenadas específicas"""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es"
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error obteniendo clima: {e}")
            return None
    
    def obtener_pronostico(self, lat: float, lon: float) -> Optional[Dict]:
        """Obtiene pronóstico para próximas horas"""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es",
                "cnt": 8  # Próximas 24 horas (cada 3 horas)
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error obteniendo pronóstico: {e}")
            return None


# Funciones de utilidad standalone

def obtener_coordenadas_bogota() -> Dict[str, Tuple[float, float]]:
    """Retorna coordenadas de ubicaciones comunes en Bogotá"""
    return {
        "centro": (4.5981, -74.0758),
        "norte": (4.7110, -74.0721),
        "sur": (4.5300, -74.1500),
        "modelia": (4.6892, -74.1063),
        "usaquen": (4.7022, -74.0307),
        "kennedy": (4.6316, -74.1469),
        "chapinero": (4.6533, -74.0653),
        "suba": (4.7475, -74.0814),
        "engativa": (4.7023, -74.1107),
        "fontibon": (4.6844, -74.1431),
    }


def formatear_timestamp(timestamp_str: str) -> str:
    """Formatea timestamp a formato legible"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


# Ejemplo de uso
if __name__ == "__main__":
    # Probar cliente SAB
    client = SABAPIClient()
    
    print("Buscando datasets de lluvia...")
    resultados = client.buscar_datasets("SAB lluvia", rows=5)
    
    if resultados:
        print(f"Encontrados {resultados['count']} datasets")
        for dataset in resultados['results']:
            print(f"  - {dataset['title']}")
    
    print("\nConsultando datos de lluvia...")
    datos = client.consultar_datastore(RESOURCE_IDS["lluvia_diaria"], limit=10)
    
    if datos is not None:
        print(f"Obtenidos {len(datos)} registros")
        print(datos.head())
