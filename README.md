# 🏍️ Predictor de Lluvia para Motociclistas - Bogotá

Aplicación web para predecir si te vas a mojar en tu trayecto en moto, basada en datos en tiempo real del Sistema de Alerta de Bogotá (SAB - IDIGER).

## 🎯 Características

- 📍 Configuración de origen y destino personalizados
- 🗺️ Visualización interactiva de ruta en mapa
- 📊 Cálculo de distancia y tiempo de viaje
- 🌧️ Integración con API del SAB (CKAN) para datos de lluvia en tiempo real
- ⚡ Actualización automática cada 5 minutos

## 🚀 Despliegue en Streamlit Cloud

### 1. Preparar Repositorio en GitHub

1. Crea un nuevo repositorio en GitHub:
   - Ve a https://github.com/new
   - Nombre sugerido: `bogota-rain-predictor`
   - Descripción: "Predictor de lluvia para motociclistas en Bogotá"
   - Hazlo **público** (para usar Streamlit Cloud gratis)

2. Sube estos archivos al repositorio:
   ```
   bogota-rain-predictor/
   ├── app.py
   ├── requirements.txt
   └── README.md
   ```

### 2. Desplegar en Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Haz clic en "New app"
3. Autoriza Streamlit (como ya lo hiciste)
4. Configura:
   - **Repository:** tu-usuario/bogota-rain-predictor
   - **Branch:** main
   - **Main file path:** app.py
5. Haz clic en "Deploy!"

⏱️ El despliegue toma 2-3 minutos la primera vez.

## 🖥️ Ejecución Local (Opcional)

Si prefieres probarlo localmente primero:

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/bogota-rain-predictor.git
cd bogota-rain-predictor

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
```

La app estará disponible en http://localhost:8501

## 📋 Uso de la Aplicación

### Configurar tu Viaje

1. **Origen** (por defecto Modelia):
   - Latitud: 4.6892
   - Longitud: -74.1063

2. **Destino**:
   - Usa Google Maps para obtener coordenadas:
     - Click derecho en el mapa → Primera línea son las coordenadas
     - Ejemplo: `4.6097, -74.0817`

3. **Velocidad Promedio**:
   - Ajusta según tu velocidad típica en moto (15-40 km/h)
   - Valor recomendado: 25 km/h para Bogotá

4. **Analizar**:
   - Haz clic en "🔍 Analizar Ruta"
   - Espera el análisis de datos del SAB

## 🔧 Estructura del Proyecto

```
app.py                 # Aplicación principal
├── Configuración
├── Funciones de API
│   ├── obtener_datos_lluvia()
│   └── obtener_catalogo_estaciones()
├── Visualización
│   └── crear_mapa()
├── Cálculos
│   ├── calcular_distancia()
│   └── estimar_tiempo_viaje()
└── UI/UX
```

## 🌐 APIs Utilizadas

### API CKAN - Datos Abiertos Bogotá

**Base URL:** `https://datosabiertos.bogota.gov.co/api/3/action`

**Endpoints:**
- `datastore_search`: Consulta datos de recursos
- `package_search`: Busca datasets

**Recursos:**
- ID Lluvia Diaria: `0f8e12d2-2115-49e2-9a05-1cfb55d26283`

## 🚧 Estado del Desarrollo

### ✅ Implementado
- [x] Interfaz de usuario con Streamlit
- [x] Mapa interactivo con Folium
- [x] Cálculo de distancia y tiempo
- [x] Integración básica con API SAB
- [x] Visualización de ruta

### ⏳ En Desarrollo
- [ ] Predicción real de lluvia basada en datos SAB
- [ ] Análisis de estaciones cercanas a la ruta
- [ ] Integración con OpenWeatherMap para viento
- [ ] Proyección de movimiento de lluvia

### 🔮 Futuras Mejoras
- [ ] Machine Learning con históricos
- [ ] Notificaciones push
- [ ] Sugerencias de rutas alternativas
- [ ] App móvil nativa
- [ ] Análisis de patrones históricos por día/hora

## 📊 Datos y Fuentes

- **SAB (Sistema de Alerta de Bogotá)**
  - IDIGER - Instituto Distrital de Gestión de Riesgos
  - 62 estaciones hidrometeorológicas
  - Actualización en tiempo real
  - Web: https://www.sab.gov.co/

- **Datos Abiertos Bogotá**
  - Portal CKAN con API REST
  - Datos históricos desde 2021
  - Web: https://datosabiertos.bogota.gov.co/

## 🔐 Seguridad y Privacidad

- ✅ Sin recolección de datos personales
- ✅ Sin seguimiento de ubicación GPS
- ✅ Coordenadas ingresadas manualmente
- ✅ API pública del SAB sin autenticación
- ✅ Código abierto y auditable

## 📝 Notas Importantes

⚠️ **Disclaimer:** Esta es una herramienta de referencia. Siempre verifica las condiciones climáticas actuales en https://app.sab.gov.co/sab/lluvias.htm antes de salir en moto.

## 🐛 Problemas Conocidos

1. **API CKAN puede estar lenta**: El portal de Datos Abiertos Bogotá a veces tiene latencia alta.
2. **Certificado SSL**: El sitio del SAB tiene problemas con su certificado SSL.
3. **Formato de datos**: La estructura exacta de los datos de lluvia puede variar.

## 🤝 Contribuciones

Para mejorar la app:
1. Fork el repositorio
2. Crea una branch: `git checkout -b feature/mejora`
3. Commit: `git commit -m "Descripción de mejora"`
4. Push: `git push origin feature/mejora`
5. Abre un Pull Request

## 📧 Contacto

Desarrollado por Diego para la comunidad de motociclistas de Bogotá 🏍️

## 📄 Licencia

MIT License - Libre para usar y modificar

---

**¿Te sirvió la app? ⭐ Dale una estrella al repo!**
