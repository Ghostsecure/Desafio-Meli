import mysql.connector
from elasticsearch import Elasticsearch
from utils import setup_logging, load_environment_variables, connect_to_db
import os

def main():
    logger = setup_logging()
    logger.info("Iniciando transferencia de datos a Elasticsearch")
    
    # Configurar Elasticsearch
    es_config = {
        'hosts': [f"{os.getenv('ES_SCHEME', 'http')}://{os.getenv('ES_HOST', 'elasticsearch')}:{os.getenv('ES_PORT', '9200')}"],
        'basic_auth': (os.getenv('ES_USERNAME', 'elastic'), os.getenv('ES_PASSWORD', 'elastic_secure_password'))
    }
    
    es = Elasticsearch(**es_config)
    
    # Verificar conexion a Elasticsearch
    if not es.ping():
        logger.error("No se pudo conectar a Elasticsearch")
        return
    
    logger.info("Conexion a Elasticsearch exitosa")
    
    # Conectar a MySQL
    connection = connect_to_db(logger)
    cursor = connection.cursor(dictionary=True)
    
    # Crear indices en Elasticsearch si no existen
    indices = [

         {"name": "meli_metrics_usuarios", "query": "SELECT ID, USERNAME, START_DATE, END_DATE, (CASE WHEN END_DATE IS NULL THEN 0 ELSE 1 END) as HAS_END_DATE, BUSINESS_UNIT, MANAGER, LAST_UPDATE, IS_EXTERNAL FROM usuarios"},
    
         {"name": "meli_metrics_capacitaciones", "query": "SELECT * FROM capacitaciones"},
    
         {"name": "meli_metrics_capacitaciones_usuarios", "query": "SELECT cu.ID, cu.FK_USERNAME, cu.FK_TRAINING, cu.END_DATE, (CASE WHEN cu.END_DATE IS NULL THEN 0 ELSE 1 END) as HAS_END_DATE, cu.ASSIGNMENT_DATE, u.BUSINESS_UNIT, c.NAME as TRAINING_NAME FROM capacitaciones_por_usuarios cu JOIN usuarios u ON cu.FK_USERNAME = u.USERNAME JOIN capacitaciones c ON cu.FK_TRAINING = c.ID"},
    
         {"name": "meli_metrics_metricas", "query": "SELECT * FROM metricas_de_capacitaciones"}
    ]
    
    try:
        for index in indices:
            # Comprobar si el indice existe
            if not es.indices.exists(index=index["name"]):
                es.indices.create(index=index["name"])
                logger.info(f"indice {index['name']} creado")
            
            # Obtener datos de MySQL
            cursor.execute(index["query"])
            rows = cursor.fetchall()
            
            # Procesar fechas para que sean compatibles con Elasticsearch
            #for row in rows:
            #    for key, value in row.items():
            #        if isinstance(value, (bytes, bytearray)):
            #            row[key] = value.decode('utf-8')

            for row in rows:
                for key, value in list(row.items()):
                    if value is None:
            # Convertir NULL a 0 o a una cadena vacía o a cualquier valor que prefieras
                        row[key] = 0
                    elif isinstance(value, (bytes, bytearray)):
                        row[key] = value.decode('utf-8')

            # Indexar datos en Elasticsearch
            for i, row in enumerate(rows):
                es.index(index=index["name"], id=i+1, document=row)
            
            logger.info(f"Se transfirieron {len(rows)} registros al indice {index['name']}")
    
    except Exception as e:
        logger.error(f"Error durante la transferencia: {e}")
    finally:
        cursor.close()
        connection.close()
        logger.info("Transferencia de datos completada")

if __name__ == "__main__":
    main()
