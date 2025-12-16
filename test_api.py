"""
Script de prueba para verificar conectividad con API del SAB
Ejecutar con: python test_api.py
"""

import requests
import json
from datetime import datetime

# URLs base
CKAN_BASE = "https://datosabiertos.bogota.gov.co/api/3/action"
LLUVIA_RESOURCE_ID = "0f8e12d2-2115-49e2-9a05-1cfb55d26283"

def test_connection():
    """Prueba de conectividad básica"""
    print("=" * 60)
    print("TEST 1: Conectividad básica con Datos Abiertos Bogotá")
    print("=" * 60)
    
    try:
        response = requests.get(f"{CKAN_BASE}/package_list", timeout=10)
        if response.status_code == 200:
            print("✅ Conexión exitosa")
            data = response.json()
            print(f"   Total de datasets disponibles: {len(data['result'])}")
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_search_sab():
    """Busca datasets relacionados con SAB"""
    print("\n" + "=" * 60)
    print("TEST 2: Búsqueda de datasets SAB")
    print("=" * 60)
    
    try:
        url = f"{CKAN_BASE}/package_search"
        params = {
            "q": "SAB lluvia",
            "rows": 5
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                results = data['result']
                print(f"✅ Encontrados {results['count']} datasets")
                print("\nPrimeros 3 datasets:")
                for i, dataset in enumerate(results['results'][:3], 1):
                    print(f"\n{i}. {dataset['title']}")
                    print(f"   ID: {dataset['id']}")
                    print(f"   Recursos: {len(dataset['resources'])}")
                return True
        print("❌ No se encontraron resultados")
        return False
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return False

def test_datastore_access():
    """Prueba acceso al datastore de lluvia"""
    print("\n" + "=" * 60)
    print("TEST 3: Acceso a datos de lluvia")
    print("=" * 60)
    
    try:
        url = f"{CKAN_BASE}/datastore_search"
        params = {
            "resource_id": LLUVIA_RESOURCE_ID,
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                records = data['result']['records']
                fields = data['result']['fields']
                
                print(f"✅ Datos obtenidos exitosamente")
                print(f"   Total de registros disponibles: {data['result']['total']}")
                print(f"   Campos disponibles: {len(fields)}")
                
                print("\n📋 Estructura de campos:")
                for field in fields[:10]:  # Primeros 10 campos
                    print(f"   - {field['id']}: {field['type']}")
                
                if records:
                    print("\n📊 Muestra de datos (primer registro):")
                    first_record = records[0]
                    for key, value in list(first_record.items())[:10]:
                        print(f"   {key}: {value}")
                
                return True
            else:
                print(f"❌ API retornó success=false: {data.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error accediendo al datastore: {e}")
        return False

def test_package_show():
    """Obtiene información detallada del dataset SAB"""
    print("\n" + "=" * 60)
    print("TEST 4: Información del dataset SAB")
    print("=" * 60)
    
    try:
        # Primero buscamos el package_id correcto
        search_url = f"{CKAN_BASE}/package_search"
        search_params = {"q": "SAB Sistema de Alerta", "rows": 1}
        search_response = requests.get(search_url, params=search_params, timeout=10)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data['success'] and search_data['result']['results']:
                package_id = search_data['result']['results'][0]['id']
                
                # Ahora obtenemos detalles completos
                show_url = f"{CKAN_BASE}/package_show"
                show_params = {"id": package_id}
                show_response = requests.get(show_url, params=show_params, timeout=10)
                
                if show_response.status_code == 200:
                    show_data = show_response.json()
                    if show_data['success']:
                        package = show_data['result']
                        
                        print(f"✅ Dataset encontrado")
                        print(f"\n📦 Información del dataset:")
                        print(f"   Nombre: {package['title']}")
                        print(f"   ID: {package['id']}")
                        print(f"   Organización: {package['organization']['title']}")
                        print(f"   Última actualización: {package.get('metadata_modified', 'N/A')[:10]}")
                        print(f"   Total de recursos: {len(package['resources'])}")
                        
                        print(f"\n📁 Recursos disponibles:")
                        for i, resource in enumerate(package['resources'][:5], 1):
                            print(f"   {i}. {resource['name']}")
                            print(f"      ID: {resource['id']}")
                            print(f"      Formato: {resource.get('format', 'N/A')}")
                            print(f"      Tamaño: {resource.get('size', 'N/A')}")
                        
                        return True
        
        print("❌ No se pudo obtener información del dataset")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sql_query():
    """Prueba consultas SQL al datastore"""
    print("\n" + "=" * 60)
    print("TEST 5: Consulta SQL personalizada")
    print("=" * 60)
    
    try:
        # Consulta SQL simple
        sql_query = f'SELECT * FROM "{LLUVIA_RESOURCE_ID}" LIMIT 3'
        
        url = f"{CKAN_BASE}/datastore_search_sql"
        params = {"sql": sql_query}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                records = data['result']['records']
                print(f"✅ Consulta SQL ejecutada exitosamente")
                print(f"   Registros retornados: {len(records)}")
                
                if records:
                    print("\n📊 Primeros registros:")
                    for i, record in enumerate(records, 1):
                        print(f"\n   Registro {i}:")
                        for key, value in list(record.items())[:5]:
                            print(f"      {key}: {value}")
                
                return True
        
        print("❌ Error ejecutando consulta SQL")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecuta todos los tests"""
    print("\n" + "🌧️" * 20)
    print("PRUEBAS DE CONECTIVIDAD - API SAB BOGOTÁ")
    print("🌧️" * 20)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Ejecutar tests
    results.append(("Conectividad básica", test_connection()))
    results.append(("Búsqueda de datasets", test_search_sab()))
    results.append(("Acceso a datastore", test_datastore_access()))
    results.append(("Información de dataset", test_package_show()))
    results.append(("Consulta SQL", test_sql_query()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! La API está funcionando correctamente.")
        print("   Puedes proceder a desplegar la aplicación en Streamlit.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Verifica:")
        print("   1. Tu conexión a internet")
        print("   2. Que el portal de Datos Abiertos esté disponible")
        print("   3. Los IDs de recursos sean correctos")

if __name__ == "__main__":
    main()
