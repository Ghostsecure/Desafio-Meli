import datetime
import random

class RandomDateGenerator:
    """Clase para generar fechas aleatorias en un rango especifico."""
    
    @staticmethod
    def generate_random_date(start_date, end_date):
        """
        Genera una fecha aleatoria entre start_date y end_date.
        
        Args:
            start_date (datetime.date): Fecha de inicio del rango
            end_date (datetime.date): Fecha de fin del rango
            
        Returns:
            datetime.date: Una fecha aleatoria dentro del rango especificado
        """
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + datetime.timedelta(days=random_number_of_days)
