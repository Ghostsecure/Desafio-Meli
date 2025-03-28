# main.py
# Script principal para ejecutar el proceso completo

import time
import os
import schedule
from utils import setup_logging, load_environment_variables
from generar_data import main as generate_data
from calcular_metricas import main as calculate_metrics

# Configurar logging utilizando la funcion de utils.py
logger = setup_logging()

# Cargar variables de entorno
load_environment_variables()

def run_pipeline():
    """Ejecuta el pipeline completo de generacion de datos y calculo de metricas."""
    logger.info("Iniciando pipeline de procesamiento de datos")
    
    try:
        # Verificar si estamos en modo de inicializacion (primera ejecucion)
        if os.getenv('INITIALIZE_DATA', 'false').lower() == 'true':
            logger.info("Generando datos iniciales")
            generate_data()
        
        # Calcular metricas de capacitaciones
        calculate_metrics()
        
        logger.info("Pipeline de procesamiento de datos completado exitosamente")
    except Exception as e:
        logger.error(f"Error durante la ejecucion del pipeline: {e}")

def schedule_jobs():
    """Programa la ejecucion periodica de los trabajos."""
    report_frequency = os.getenv('REPORT_FREQUENCY', 'daily')
    
    if report_frequency == 'daily':
        schedule.every().day.at("00:00").do(run_pipeline)
    elif report_frequency == 'weekly':
        schedule.every().monday.at("00:00").do(run_pipeline)
    elif report_frequency == 'monthly':
        schedule.every().day.at("00:00").do(lambda: run_pipeline() if time.localtime().tm_mday == 1 else None)
    else:
        logger.warning(f"Frecuencia de reporte no reconocida: {report_frequency}. Se utilizara diaria por defecto.")
        schedule.every().day.at("00:00").do(run_pipeline)
    
    logger.info(f"Trabajos programados con frecuencia: {report_frequency}")

def main():
    """Funcion principal."""
    logger.info("Iniciando aplicacion")
    
    # Ejecutar el pipeline inmediatamente al iniciar
    run_pipeline()
    
    # Programar ejecuciones periodicas
    schedule_jobs()
    
    # Mantener la aplicacion en ejecucion
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto

if __name__ == "__main__":
    main()