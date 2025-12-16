# 🚀 Guía Rápida de Despliegue

## ⏱️ Tiempo estimado: 10 minutos

---

## 📋 Pre-requisitos

✅ Cuenta de GitHub (ya la tienes)  
✅ Streamlit Cloud autorizado (ya lo hiciste)  
✅ Git instalado (opcional, puedes usar la interfaz web de GitHub)

---

## 🎯 Pasos para Desplegar

### **Paso 1: Crear Repositorio en GitHub** (2 min)

1. Ve a: https://github.com/new
2. Configura:
   - **Repository name:** `bogota-rain-predictor`
   - **Description:** `Predictor de lluvia para motociclistas en Bogotá basado en datos del SAB`
   - **Visibility:** ✅ Public (para usar Streamlit Cloud gratis)
   - ❌ NO inicialices con README, .gitignore, ni license (ya los tenemos)

3. Haz clic en **"Create repository"**

### **Paso 2: Subir Archivos al Repositorio** (3 min)

**Opción A: Interfaz Web de GitHub (Más fácil)**

1. En la página del nuevo repositorio, haz clic en **"uploading an existing file"**
2. Arrastra estos archivos:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `utils.py` (opcional)
   - `test_api.py` (opcional)

3. En "Commit changes":
   - Mensaje: `Initial commit - Rain predictor app`
   - Haz clic en **"Commit changes"**

**Opción B: Línea de Comandos (Si prefieres)**

```bash
cd /ruta/donde/estan/los/archivos

git init
git add .
git commit -m "Initial commit - Rain predictor app"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/bogota-rain-predictor.git
git push -u origin main
```

### **Paso 3: Desplegar en Streamlit Cloud** (5 min)

1. Ve a: https://share.streamlit.io/

2. Haz clic en **"New app"**

3. Completa el formulario:
   - **Repository:** `TU-USUARIO/bogota-rain-predictor`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (opcional):** `bogota-rain` o el nombre que prefieras

4. Haz clic en **"Deploy!"**

5. Espera 2-3 minutos mientras:
   - Streamlit clona tu repo
   - Instala las dependencias del `requirements.txt`
   - Inicia la aplicación

6. **¡Listo!** Tu app estará disponible en:
   ```
   https://TU-USUARIO-bogota-rain-predictor-app-xxxxx.streamlit.app
   ```

---

## 🎉 ¡Aplicación Desplegada!

### **¿Qué puedes hacer ahora?**

✅ Compartir el link con otros motociclistas  
✅ Usar la app desde cualquier dispositivo  
✅ Actualizar el código (los cambios se desplegarán automáticamente)  
✅ Ver estadísticas de uso en el dashboard de Streamlit

---

## 🔧 Solución de Problemas

### **Error: "Requirements file not found"**
- Verifica que `requirements.txt` esté en la raíz del repo
- Asegúrate que el archivo se subió correctamente

### **Error: "Module not found"**
- Revisa que todas las dependencias estén en `requirements.txt`
- Intenta agregar versiones específicas: `streamlit==1.28.0`

### **App no carga / Error 404**
- Espera 5 minutos y recarga
- Verifica que el path del main file sea correcto: `app.py`
- Revisa los logs en Streamlit Cloud dashboard

### **API del SAB no responde**
- Es normal, el portal a veces está lento
- La app tiene caché de 5 minutos
- Intenta en horarios de menor tráfico

---

## 🔄 Actualizar la Aplicación

Para hacer cambios en el futuro:

1. **Edita los archivos** en tu repositorio de GitHub
2. **Haz commit** de los cambios
3. **Streamlit detectará automáticamente** el cambio
4. La app se **redesplegaría automáticamente** en 1-2 minutos

---

## 📱 Probar Localmente Primero (Opcional)

Si quieres probar antes de desplegar:

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la app
streamlit run app.py

# 3. Abrir en navegador
# http://localhost:8501
```

---

## 🧪 Verificar API del SAB (Opcional)

Antes de desplegar, puedes verificar que la API funcione:

```bash
python test_api.py
```

Esto ejecutará pruebas de conectividad y te mostrará si los datos están disponibles.

---

## 📊 Dashboard de Streamlit Cloud

Una vez desplegado, accede a:
https://share.streamlit.io/

Ahí podrás:
- ✅ Ver logs en tiempo real
- ✅ Reiniciar la app si es necesario
- ✅ Ver estadísticas de uso
- ✅ Configurar variables de entorno (si las necesitas)
- ✅ Pausar/reanudar la app

---

## 🔐 Configuración Avanzada (Opcional)

### **Agregar API Key de OpenWeatherMap**

1. Consigue una API key gratis en: https://openweathermap.org/api
2. En Streamlit Cloud dashboard → **Settings** → **Secrets**
3. Agrega:
   ```toml
   OPENWEATHER_API_KEY = "tu-api-key-aqui"
   ```
4. En el código, accede con: `st.secrets["OPENWEATHER_API_KEY"]`

---

## 🎓 Próximos Pasos Sugeridos

Una vez la app esté funcionando:

1. **Prueba con diferentes rutas** en Bogotá
2. **Comparte con amigos motociclistas** para obtener feedback
3. **Observa el comportamiento** de la API del SAB en diferentes horarios
4. **Mejora la predicción** basándote en datos reales
5. **Agrega características** como:
   - Histórico de lluvia por hora del día
   - Notificaciones (usando servicios externos)
   - Integración con Google Maps para rutas alternativas

---

## 📞 Ayuda

Si encuentras problemas:

1. **Revisa los logs** en Streamlit Cloud
2. **Verifica el status** del portal Datos Abiertos Bogotá
3. **Prueba localmente** primero para aislar el problema
4. **Consulta la documentación** de Streamlit: https://docs.streamlit.io/

---

## ✅ Checklist Final

Antes de compartir tu app públicamente:

- [ ] App desplegada y funcionando
- [ ] Probada con diferentes rutas
- [ ] README actualizado con tu URL de Streamlit
- [ ] Descripción clara en el repositorio de GitHub
- [ ] Al menos 1 screenshot en el README
- [ ] Licencia agregada (MIT recomendada)

---

**¡Listo para arrancar! 🏍️💨**
