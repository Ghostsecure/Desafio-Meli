import datetime
import mysql.connector

class MetricsCalculator:
    def __init__(self, connection, logger):
        self.connection = connection
        self.logger = logger
    
    def calculate_completion_metrics_by_bu(self, month_dates):
        """Calcula metricas de finalizacion de capacitaciones por BU para los meses especificados."""
        cursor = self.connection.cursor()
        metrics = []
        
        for month_date in month_dates:
            # Formato de la fecha para la consulta
            month_str = month_date.strftime('%Y-%m-%d')
            next_month = (month_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
            next_month_str = next_month.strftime('%Y-%m-%d')
            
            # Consulta para obtener los datos de capacitaciones por BU
            query = """
            SELECT 
                u.BUSINESS_UNIT,
                COUNT(DISTINCT u.USERNAME) as total_users,
                COUNT(DISTINCT CASE WHEN ut.END_DATE IS NOT NULL AND ut.END_DATE < %s THEN ut.FK_USERNAME END) as users_with_completions,
                COUNT(DISTINCT ut.ID) as total_trainings,
                COUNT(CASE WHEN ut.END_DATE IS NOT NULL AND ut.END_DATE < %s THEN ut.ID END) as completed_trainings
            FROM 
                usuarios u
            LEFT JOIN 
                capacitaciones_por_usuarios ut ON u.USERNAME = ut.FK_USERNAME
            WHERE 
                (u.END_DATE IS NULL OR u.END_DATE >= %s)
                AND u.START_DATE < %s
                AND (ut.ASSIGNMENT_DATE IS NULL OR ut.ASSIGNMENT_DATE < %s)
            GROUP BY 
                u.BUSINESS_UNIT
            """
            
            cursor.execute(query, (next_month_str, next_month_str, month_str, next_month_str, next_month_str))
            results = cursor.fetchall()
            
            for row in results:
                business_unit, total_users, users_with_completions, total_trainings, completed_trainings = row
                
                # Calcular porcentaje de finalizacion
                completion_percentage = 0
                if total_trainings > 0:
                    completion_percentage = (completed_trainings / total_trainings) * 100
                
                metrics.append({
                    'business_unit': business_unit,
                    'month': month_str,
                    'completion_percentage': round(completion_percentage, 2),
                    'total_users': total_users,
                    'completed_trainings': completed_trainings
                })
        
        cursor.close()
        return metrics
    
    def save_metrics(self, metrics):
        """Guarda las metricas calculadas en la tabla metricas_de_capacitaciones."""
        cursor = self.connection.cursor()
        
        try:
            for metric in metrics:
                cursor.execute(
                    """
                    INSERT INTO metricas_de_capacitaciones 
                    (BUSINESS_UNIT, MONTH, COMPLETION_PERCENTAGE, TOTAL_USERS, COMPLETED_TRAININGS)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        metric['business_unit'],
                        metric['month'],
                        metric['completion_percentage'],
                        metric['total_users'],
                        metric['completed_trainings']
                    )
                )
            
            self.connection.commit()
            self.logger.info(f"Se guardaron {len(metrics)} registros de metricas")
        except mysql.connector.Error as error:
            self.logger.error(f"Error al guardar metricas: {error}")
            self.connection.rollback()
        finally:
            cursor.close()