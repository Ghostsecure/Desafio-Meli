import datetime
import mysql.connector
import logging
from generar_data_random_date import RandomDateGenerator

class TrainingsInserter:
    """Clase para insertar datos de capacitaciones en la base de datos."""
    
    def __init__(self, logger=None):
        """
        Inicializa la clase TrainingsInserter.
        
        Args:
            logger (logging.Logger, optional): Logger para registrar informacion. Si es None, 
                                              se utilizara el logger por defecto.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.TRAINING_NAMES = [
            "Ciberseguridad", 
            "Introduccion a ML", 
            "Analisis de Datos", 
            "Programacion Python", 
            "Gestion de Proyectos",
            "Docker y Contenedores",
            "Elasticsearch Basics",
            "APIs RESTful",
            "Metodologias Agiles",
            "SQL Avanzado"
        ]
    
    def insert_trainings(self, connection):
        """
        Inserta datos de capacitaciones en la tabla capacitaciones.
        
        Args:
            connection (mysql.connector.connection.MySQLConnection): Conexion a la base de datos
            
        Returns:
            None
        """
        cursor = connection.cursor()
        current_date = datetime.datetime.now().date()
        six_months_ago = current_date - datetime.timedelta(days=180)
        
        trainings_data = []
        for i, name in enumerate(self.TRAINING_NAMES, 1):
            creation_date = RandomDateGenerator.generate_random_date(six_months_ago, current_date).strftime('%Y-%m-%d')
            link = f"https://meli.{name.lower().replace(' ', '')}.training.com"
            trainings_data.append((i, name, link, creation_date))
        
        try:
            cursor.executemany(
                "INSERT INTO capacitaciones (ID, NAME, LINK, CREATION_DATE) VALUES (%s, %s, %s, %s)",
                trainings_data
            )
            connection.commit()
            self.logger.info(f"Se insertaron {cursor.rowcount} capacitaciones")
        except mysql.connector.Error as error:
            self.logger.error(f"Error al insertar capacitaciones: {error}")
            connection.rollback()
        finally:
            cursor.close()
