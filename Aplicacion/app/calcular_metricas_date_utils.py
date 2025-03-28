
import datetime

#Modulo de fechas
class DateUtils:
    @staticmethod
    def get_start_of_months(num_months):
        """Devuelve una lista con las fechas de inicio de los ultimos n meses."""
        current_date = datetime.datetime.now().date()
        first_day_current_month = current_date.replace(day=1)
        
        months = []
        for i in range(num_months):
            # Restar meses uno por uno
            month_date = first_day_current_month - datetime.timedelta(days=1)
            # Ir al primer dia del mes anterior
            month_date = month_date.replace(day=1)
            months.append(month_date)
            first_day_current_month = month_date
        
        # Invertir la lista para tener los meses en orden cronologico
        return list(reversed(months))