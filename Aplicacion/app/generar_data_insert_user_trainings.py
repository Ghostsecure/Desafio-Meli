import datetime
import random
import mysql.connector
import logging
from generar_data_random_date import RandomDateGenerator

class UserTrainingsInserter:
    """Clase para insertar datos de capacitaciones por usuario en la base de datos."""
    
    def __init__(self, logger=None):
        """
        Inicializa la clase UserTrainingsInserter.
        
        Args:
            logger (logging.Logger, optional): Logger para registrar informacion. Si es None, 
                                              se utilizara el logger por defecto.
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def insert_user_trainings(self, connection):
        """
        Inserta datos de capacitaciones por usuario en la tabla capacitaciones_por_usuarios.
        
        Args:
            connection (mysql.connector.connection.MySQLConnection): Conexion a la base de datos
            
        Returns:
            None
        """
        cursor = connection.cursor()
        
        # Obtener la lista de usuarios
        cursor.execute("SELECT USERNAME FROM usuarios")
        users = [user[0] for user in cursor.fetchall()]
        
        # Obtener la lista de capacitaciones
        cursor.execute("SELECT ID FROM capacitaciones")
        trainings = [training[0] for training in cursor.fetchall()]
        
        current_date = datetime.datetime.now().date()
        six_months_ago = current_date - datetime.timedelta(days=180)
        
        user_trainings_data = []
        training_id = 1
        
        for user in users:
            # Cada usuario tiene entre 1 y 5 capacitaciones asignadas
            num_trainings = random.randint(1, 5)
            assigned_trainings = random.sample(trainings, num_trainings)
            
            for training in assigned_trainings:
                assignment_date = RandomDateGenerator.generate_random_date(six_months_ago, current_date).strftime('%Y-%m-%d')
                
                # 70% de probabilidad de que la capacitacion este completada
                end_date = None
                if random.random() < 0.7:
                    assignment_date_obj = datetime.datetime.strptime(assignment_date, '%Y-%m-%d').date()
                    max_completion_date = min(current_date, assignment_date_obj + datetime.timedelta(days=30))
                    end_date = RandomDateGenerator.generate_random_date(assignment_date_obj, max_completion_date).strftime('%Y-%m-%d')
                
                user_trainings_data.append((training_id, user, training, end_date, assignment_date))
                training_id += 1
        
        try:
            cursor.executemany(
                "INSERT INTO capacitaciones_por_usuarios (ID, FK_USERNAME, FK_TRAINING, END_DATE, ASSIGNMENT_DATE) VALUES (%s, %s, %s, %s, %s)",
                user_trainings_data
            )
            connection.commit()
            self.logger.info(f"Se insertaron {cursor.rowcount} asignaciones de capacitaciones")
        except mysql.connector.Error as error:
            self.logger.error(f"Error al insertar asignaciones de capacitaciones: {error}")
            connection.rollback()
        finally:
            cursor.close()
