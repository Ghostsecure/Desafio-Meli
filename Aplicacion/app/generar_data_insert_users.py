import datetime
import random
import mysql.connector
import logging
from generar_data_random_date import RandomDateGenerator

class UsersInserter:
    """Clase para insertar datos de usuarios en la base de datos."""
    
    def __init__(self, logger=None):
        """
        Inicializa la clase UsersInserter.
        
        Args:
            logger (logging.Logger, optional): Logger para registrar informacion. Si es None, 
                                              se utilizara el logger por defecto.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.BUSINESS_UNITS = ["Mercado Libre", "Mercado Pago", "Mercado Envios"]
        self.MANAGERS = ["lsalme", "jgomez", "mrodriguez", "alopez", "pmartin"]
    
    def insert_users(self, connection):
        """
        Inserta datos de usuarios en la tabla usuarios.
        
        Args:
            connection (mysql.connector.connection.MySQLConnection): Conexion a la base de datos
            
        Returns:
            None
        """
        cursor = connection.cursor()
        current_date = datetime.datetime.now().date()
        one_year_ago = current_date - datetime.timedelta(days=365)
        
        users_data = []
        for i in range(1, 201):  # 200 usuarios
            is_external = random.random() < 0.3  # 30% de usuarios externos
            
            # Modificacion: Si es usuario interno, no tiene prefijo
            # Si es usuario externo, mantiene el prefijo "ext_"
            if is_external:
                username = f"ext_{random.choice(['jperez', 'agarcia', 'mlopez', 'srodriguez', 'tgonzalez'])}{i}"
            else:
                username = f"{random.choice(['jperez', 'agarcia', 'mlopez', 'srodriguez', 'tgonzalez'])}{i}"
                
            start_date = RandomDateGenerator.generate_random_date(one_year_ago, current_date).strftime('%Y-%m-%d')
            
            # 10% de usuarios con end_date (no activos)
            end_date = None
            if random.random() < 0.1:
                end_date_obj = RandomDateGenerator.generate_random_date(datetime.datetime.strptime(start_date, '%Y-%m-%d').date(), current_date)
                end_date = end_date_obj.strftime('%Y-%m-%d')
            
            business_unit = random.choice(self.BUSINESS_UNITS)
            manager = random.choice(self.MANAGERS)
            last_update = current_date.strftime('%Y-%m-%d')
            
            users_data.append((i, username, start_date, end_date, business_unit, manager, last_update, is_external))
        
        try:
            cursor.executemany(
                "INSERT INTO usuarios (ID, USERNAME, START_DATE, END_DATE, BUSINESS_UNIT, MANAGER, LAST_UPDATE, IS_EXTERNAL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                users_data
            )
            connection.commit()
            self.logger.info(f"Se insertaron {cursor.rowcount} usuarios")
        except mysql.connector.Error as error:
            self.logger.error(f"Error al insertar usuarios: {error}")
            connection.rollback()
        finally:
            cursor.close()
