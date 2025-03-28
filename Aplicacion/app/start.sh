#!/bin/bash

# Función para verificar si MySQL está disponible
check_mysql() {
  python -c "
import mysql.connector
from utils import load_environment_variables
db_config = load_environment_variables()
try:
  conn = mysql.connector.connect(**db_config)
  conn.close()
  exit(0)
except Exception as e:
  exit(1)
"
  return $?
}

# Función para verificar si Elasticsearch está disponible
check_elasticsearch() {
  python -c "
from elasticsearch import Elasticsearch
import os
es_host = os.getenv('ES_HOST', 'elasticsearch')
es_port = os.getenv('ES_PORT', '9200')
es_scheme = os.getenv('ES_SCHEME', 'http')
try:
  es = Elasticsearch([f'{es_scheme}://{es_host}:{es_port}'])
  if es.ping():
    exit(0)
  else:
    exit(1)
except Exception as e:
  exit(1)
"
  return $?
}

# Esperar a que MySQL esté realmente disponible y listo
echo "Esperando que MySQL esté disponible..."
counter=0
max_attempts=30  # 5 minutos máximo (30 intentos x 10 segundos)

until check_mysql || [ $counter -ge $max_attempts ]; do
  echo "Esperando a MySQL... intento $counter de $max_attempts"
  counter=$((counter+1))
  sleep 10
done

if [ $counter -ge $max_attempts ]; then
  echo "Error: MySQL no está disponible después de esperar 5 minutos. Abortando."
  exit 1
fi

echo "MySQL está listo. Procediendo con la generación de datos..."

# Generar datos
echo "Generando datos iniciales..."
python /app/generar_data.py

# Calcular métricas
echo "Calculando métricas..."
python /app/calcular_metricas.py

# Verificar si Elasticsearch está disponible antes de intentar transferir datos
echo "Verificando disponibilidad de Elasticsearch..."
counter=0
max_attempts=12  # 2 minutos máximo (12 intentos x 10 segundos)

until check_elasticsearch || [ $counter -ge $max_attempts ]; do
  echo "Esperando a Elasticsearch... intento $counter de $max_attempts"
  counter=$((counter+1))
  sleep 10
done

# Transferir a Elasticsearch solo si está disponible
if [ $counter -lt $max_attempts ] && [ -f "/app/transferir_a_elasticsearch.py" ]; then
  echo "Elasticsearch está disponible. Transfiriendo datos..."
  python /app/transferir_a_elasticsearch.py
else
  echo "Elasticsearch no está disponible o no hay script de transferencia. Omitiendo transferencia de datos."
fi

# Iniciar el script principal
echo "Iniciando la aplicación principal..."
python /app/main.py