from utils import setup_logging, connect_to_db
from calcular_metricas_date_utils import DateUtils
from calcular_metricas_metrics_calculator import MetricsCalculator

class MetricsApp:
    def __init__(self):
        self.logger = setup_logging()
    
    def run(self):
        """Funcion principal que ejecuta el calculo de metricas."""
        self.logger.info("Iniciando calculo de metricas de capacitaciones")
        
        connection = None
        try:
            connection = connect_to_db(self.logger)
            
            # Obtener los ultimos 6 meses
            month_dates = DateUtils.get_start_of_months(6)
            
            # Inicializar calculador de metricas
            calcular_metricas_metrics_calculator = MetricsCalculator(connection, self.logger)
            
            # Calcular metricas
            metrics = calcular_metricas_metrics_calculator.calculate_completion_metrics_by_bu(month_dates)
            
            # Guardar metricas
            calcular_metricas_metrics_calculator.save_metrics(metrics)
            
            self.logger.info("Calculo de metricas completado exitosamente")
        except Exception as e:
            self.logger.error(f"Error durante el calculo de metricas: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
                self.logger.info("Conexion a la base de datos cerrada")