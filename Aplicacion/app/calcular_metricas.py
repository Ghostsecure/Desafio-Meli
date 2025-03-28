#!/usr/bin/env python
# Script modular para calcular metricas de capacitaciones por BU

from calcular_metricas_metrics_app import MetricsApp

def main():
    """Funcion principal que inicia la aplicacion."""
    app = MetricsApp()
    app.run()

# Punto de entrada
if __name__ == "__main__":
    main()
    