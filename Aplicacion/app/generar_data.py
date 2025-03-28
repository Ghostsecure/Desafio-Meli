# Script principal para generar datos de prueba para la base de datos
import os
import logging
import mysql.connector
from utils import setup_logging, connect_to_db, load_environment_variables
from generar_data_insert_trainings import TrainingsInserter
from generar_data_insert_users import UsersInserter
from generar_data_insert_user_trainings import UserTrainingsInserter

def main():
    """Funcion principal que ejecuta la generacion de datos."""
    # Configurar el logger
    logger = setup_logging()
    logger.info("Iniciando generacion de datos de prueba")
    
    try:
        # Establecer conexion a la base de datos
        connection = connect_to_db(logger)
        
        # Inicializar las clases para inserción de datos
        trainings_inserter = TrainingsInserter(logger)
        users_inserter = UsersInserter(logger)
        user_trainings_inserter = UserTrainingsInserter(logger)
        
        # Insertar datos en orden
        trainings_inserter.insert_trainings(connection)
        users_inserter.insert_users(connection)
        user_trainings_inserter.insert_user_trainings(connection)
        
        logger.info("Generacion de datos completada exitosamente")
    except Exception as e:
        logger.error(f"Error durante la generacion de datos: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            logger.info("Conexion a la base de datos cerrada")

if __name__ == "__main__":
    main()