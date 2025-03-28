# Automatización de Métricas para Capacitaciones de Ciberseguridad

Este proyecto implementa un sistema automatizado para el seguimiento del estado de capacitaciones de ciberseguridad destinado a colaboradores internos y externos de Mercado Libre. Permite calcular, almacenar y visualizar métricas mensuales del porcentaje de finalización de capacitaciones por unidad de negocio (BU).

## Arquitectura del Sistema

El proyecto utiliza un enfoque basado en contenedores Docker con los siguientes componentes:

- **Base de datos MySQL**: Almacena los datos de usuarios, capacitaciones y el histórico de métricas
- **Scripts Python**: Realizan la generación de datos, cálculo de métricas y transferencia a Elasticsearch
- **Elasticsearch**: Indexa y almacena los datos procesados para su visualización
- **Kibana**: Proporciona paneles de control y visualizaciones para los usuarios finales

## Requisitos Previos

- Docker y Docker Compose
- Git
- Puertos disponibles: 3306, 9200, 25601

## Instalación y Ejecución

### Requisitos previos comunes
- Asegurarse de tener Docker y Docker Compose instalados y funcionando correctamente
- Git instalado o posibilidad de descargar el repositorio como ZIP
- Puertos disponibles: 3306, 9200, 25601

### Para usuarios de Linux

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/meli-challenge.git
   cd meli-challenge
   ```

2. Iniciar el entorno:
   ```bash
   docker-compose up -d
   ```

3. Verificar que todos los contenedores estén en ejecución:
   ```bash
   docker ps
   ```

### Para usuarios de Windows

1. Clonar el repositorio:
   - Utilizando Git Bash:
     ```bash
     git clone https://github.com/tu-usuario/meli-challenge.git
     cd meli-challenge
     ```
   - O descargar como ZIP desde GitHub y descomprimirlo

2. Requisitos específicos para Windows:
   - Tener Docker Desktop para Windows instalado
   - Configurar Docker Desktop en modo WSL 2 o Hyper-V
   - Asegurarse de que Docker Desktop esté en ejecución

3. Iniciar el entorno (desde PowerShell o CMD):
   ```powershell
   docker-compose up -d
   ```

4. Verificar que todos los contenedores estén en ejecución:
   ```powershell
   docker ps
   ```

### Procesos comunes tras la inicialización

El comando `docker-compose up -d` iniciará todos los servicios necesarios y ejecutará automáticamente:
- Creación de tablas en MySQL
- Generación de datos de prueba
- Cálculo de métricas
- Transferencia a Elasticsearch

### Acceder a las visualizaciones

Una vez que el sistema esté en funcionamiento:
- Abrir Kibana en http://localhost:25601 (o http://127.0.0.1:25601)
- Usuario: elastic
- Contraseña: elastic_secure_password

## Estructura del Proyecto

```
Desafio Meli_/
  |_ Aplicacion/
      |_ .env
      |_ docker-compose.yml
      |_ Dockerfile
      |_ requirements.txt 
      |_ app/
          |_ calcular_metricas.py
          |_ calcular_metricas_date_utils.py
          |_ calcular_metricas_metrics_app.py
          |_ calcular_metricas_metrics_calculator.py
          |_ utils.py
          |_ main.py
          |_ generar_data.py
          |_ generar_data_insert_trainings.py
          |_ generar_data_insert_users.py
          |_ generar_data_insert_user_trainings.py
          |_ generar_data_random_date.py
          |_ transferir_a_elasticsearch.py
          |_ start.sh
      |_ data/ 
      |_ init-scripts/
          |_ creacion_de_tablas.sql
```

## Uso del Sistema

### Generar Nuevos Datos

Para generar nuevos datos o recalcular métricas en cualquier momento:

#### En Linux:

```bash
# Generar nuevos datos
docker exec -it meli_app python /app/generar_data.py

# Calcular métricas
docker exec -it meli_app python /app/calcular_metricas.py

# Transferir a Elasticsearch
docker exec -it meli_app python /app/transferir_a_elasticsearch.py
```

#### En Windows (usando PowerShell o CMD):

```powershell
# Generar nuevos datos
docker exec -it meli_app python /app/generar_data.py

# Calcular métricas
docker exec -it meli_app python /app/calcular_metricas.py

# Transferir a Elasticsearch
docker exec -it meli_app python /app/transferir_a_elasticsearch.py
```

Nota: Si experimenta problemas de permisos en Windows, puede ser necesario ejecutar PowerShell o CMD como administrador.

## Consultas SQL Útiles

### Para Linux:

#### Verificar usuarios activos:
```bash
docker exec -it meli_mysql mysql -u meli_user -p challenge_meli -e "SELECT SUM(CASE WHEN END_DATE IS NULL THEN 1 ELSE 0 END) as usuarios_activos, COUNT(*) as total_usuarios FROM usuarios;"
```

#### Ver métricas por unidad de negocio:
```bash
docker exec -it meli_mysql mysql -u meli_user -p challenge_meli -e "SELECT BUSINESS_UNIT, AVG(COMPLETION_PERCENTAGE) as promedio_finalizacion FROM metricas_de_capacitaciones GROUP BY BUSINESS_UNIT;"
```

### Para Windows:

#### Verificar usuarios activos:
```powershell
docker exec -it meli_mysql mysql -u meli_user -p challenge_meli -e "SELECT SUM(CASE WHEN END_DATE IS NULL THEN 1 ELSE 0 END) as usuarios_activos, COUNT(*) as total_usuarios FROM usuarios;"
```

#### Ver métricas por unidad de negocio:
```powershell
docker exec -it meli_mysql mysql -u meli_user -p challenge_meli -e "SELECT BUSINESS_UNIT, AVG(COMPLETION_PERCENTAGE) as promedio_finalizacion FROM metricas_de_capacitaciones GROUP BY BUSINESS_UNIT;"
```

Nota: En Windows, si el comando anterior presenta problemas con las comillas, puede ser necesario utilizar comillas simples dentro de comillas dobles o viceversa:

```powershell
docker exec -it meli_mysql mysql -u meli_user -p challenge_meli -e "SELECT BUSINESS_UNIT, AVG(COMPLETION_PERCENTAGE) as promedio_finalizacion FROM metricas_de_capacitaciones GROUP BY BUSINESS_UNIT;"
```

## Visualización con Elasticsearch y Kibana

Este proyecto utiliza Elasticsearch como motor de indexación y Kibana como plataforma de visualización para las métricas de capacitaciones.

### Acceso a Kibana

Una vez que el sistema esté en funcionamiento:

#### Para ambos sistemas operativos (Linux y Windows):
- Abrir Kibana en:
  - http://localhost:25601
  - Alternativamente: http://127.0.0.1:25601
- Usuario: elastic
- Contraseña: elastic_secure_password

#### Consideraciones para Windows:
- Si tienes problemas para acceder, verifica que Docker Desktop esté funcionando correctamente
- En algunos casos, puede ser necesario ajustar la configuración del firewall de Windows para permitir conexiones a los puertos utilizados
- Si estás utilizando WSL 2, asegúrate de que los puertos estén correctamente redirigidos

### Importación de Patrones de Índice y Paneles de Control

Para visualizar correctamente los datos, es necesario importar los patrones de índice y paneles de control preconfigurados:

#### Importar Patrones de Índice:

1. Ir a "Stack Management" > "Index Patterns"
2. Hacer clic en "Import index pattern"
3. Seleccionar los archivos desde la carpeta recursos/

#### Importar Paneles de Control:

1. Ir a "Stack Management" > "Saved Objects"
2. Hacer clic en "Import"
3. Seleccionar el archivo dashboard.ndjson desde la carpeta recursos
4. Confirmar la importación cuando se solicite
5. Asegurarse de que la opción "Include related objects" esté activada durante la importación

### Panel de Control de Capacitaciones

El panel de control principal "Capacitaciones Meli" incluye los siguientes componentes:

#### Indicadores Clave de Rendimiento (KPIs):

- Porcentaje de Completitud Global (medidor tipo Gauge)
- Total de Usuarios Activos (contador)
- Total de Capacitaciones Disponibles (contador)

#### Gráfico de Barras - Completitud por Unidad de Negocio:

- Visualiza el porcentaje de finalización de capacitaciones para cada BU
- Permite comparar rápidamente el rendimiento entre Mercado Libre, Mercado Pago y Mercado Envíos

#### Gráfico de Línea Temporal - Evolución de Completitud:

- Muestra las tendencias de completitud a lo largo del tiempo
- Separado por unidad de negocio para análisis comparativo

#### Tabla de Usuarios Destacados:

- Identifica los usuarios con más capacitaciones asignadas
- Ayuda a detectar patrones de asignación y finalización

### Estructura de Datos

El panel de control utiliza cuatro fuentes principales de datos:

#### meli_metrics_usuarios:
- Campos clave: ID, USERNAME, START_DATE, END_DATE, BUSINESS_UNIT, MANAGER, IS_EXTERNAL, HAS_END_DATE

#### meli_metrics_capacitaciones:
- Campos clave: ID, NAME, LINK, CREATION_DATE

#### meli_metrics_capacitaciones_usuarios:
- Campos clave: FK_USERNAME, FK_TRAINING, END_DATE, ASSIGNMENT_DATE, HAS_END_DATE

#### meli_metrics_metricas:
- Campos clave: BUSINESS_UNIT, MONTH, COMPLETION_PERCENTAGE, TOTAL_USERS, COMPLETED_TRAININGS

### Estructura de Carpeta de Recursos

```
/recursos
├──              
├── usuarios_pattern.ndjson
├── capacitaciones_pattern.ndjson
├── capacitaciones_usuarios_pattern.ndjson
└── metricas_pattern.ndjson
├── dashboard.ndjson
```

## Solución de Problemas Comunes

### Problemas generales:
- **No se muestran datos**: Verificar que el rango de tiempo seleccionado en Kibana incluya datos
- **Error en campos nulos**: Confirmar que los campos END_DATE nulos se han transformado correctamente con el campo HAS_END_DATE
- **Visualizaciones vacías**: Asegurarse de que los nombres de los campos coincidan exactamente con los utilizados en la configuración del panel de control
- **Datos no actualizados**: Ejecutar nuevamente el script de transferencia a Elasticsearch tras modificar datos en MySQL

### Problemas específicos en Windows:
- **Docker no inicia correctamente**: Verificar que Docker Desktop esté en ejecución y configurado correctamente
- **Problemas de permisos**: Ejecutar PowerShell o CMD como administrador
- **Puertos ya utilizados**: Verificar que los puertos 3306, 9200 y 25601 no estén siendo utilizados por otras aplicaciones
- **Problemas de red**: Comprobar la configuración de red de Docker y asegurarse de que no haya conflictos con VPNs o software de seguridad
- **Error "no such file or directory"**: Verificar las rutas y asegurarse de usar barras diagonales (/) en lugar de barras invertidas (\) en los comandos

### Reinicio de servicios:
```bash
# Para ambos sistemas operativos
docker-compose down
docker-compose up -d
```

### Para crear nuevas visualizaciones personalizadas:

1. Ir a "Analytics" > "Visualize Library"
2. Hacer clic en "Create new visualization"
3. Seleccionar el tipo de visualización (gráfico de barras, líneas, etc.)
4. Seleccionar el patrón de índice "meli_metrics_*" apropiado
5. Configurar los ejes y métricas según las necesidades

### Campos Importantes para Filtrado

- **HAS_END_DATE**: Campo que indica si un usuario/capacitación ha sido completado (1) o está pendiente (0)
- **BUSINESS_UNIT**: Unidad de negocio (Mercado Libre, Mercado Pago, Mercado Envíos)
- **IS_EXTERNAL**: Indica si el usuario es externo (true) o interno (false)
- **MONTH**: Fecha mensual para análisis temporal
- **COMPLETION_PERCENTAGE**: Porcentaje de finalización de capacitaciones

## Descripción de la Solución

### Elección de Herramientas

- **Docker**: Facilita la portabilidad y la configuración reproducible
- **MySQL**: Base de datos relacional robusta para almacenamiento estructurado
- **Python**: Lenguaje versátil y potente para el procesamiento de datos
- **Elasticsearch/Kibana**: Plataforma flexible para visualización y análisis de datos

### Problemas y Soluciones

- **Desafío**: Manejo de valores NULL en campos de fecha
  - **Solución**: Implementación de un campo adicional HAS_END_DATE para facilitar el conteo
  
- **Desafío**: Automatización del flujo de datos
  - **Solución**: Script start.sh que coordina la ejecución de todas las etapas

## Licencia

Este proyecto está licenciado bajo MIT License.