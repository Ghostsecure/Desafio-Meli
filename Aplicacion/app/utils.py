import mysql.connector
import os
import logging
from dotenv import load_dotenv


#configuracion de logging
def setup_logging():
    """Configura y devuelve un logger."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

#configuracion de variables de entonco
def load_environment_variables():
    """Carga variables de entorno desde el archivo .env."""
    load_dotenv()
    return {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'meli_user'),
        'password': os.getenv('MYSQL_PASSWORD', 'complex_password_456!'),
        'database': os.getenv('DB_NAME', 'challenge_meli')
    }

#conexion a la base de datos
def connect_to_db(logger=None):
    """Establece conexion con la base de datos MySQL."""
    if logger is None:
        logger = logging.getLogger(__name__)
    
    db_config = load_environment_variables()
    
    try:
        connection = mysql.connector.connect(**db_config)
        logger.info("Conexion a la base de datos establecida correctamente")
        return connection
    except mysql.connector.Error as error:
        logger.error(f"Error al conectar con la base de datos: {error}")
        raise