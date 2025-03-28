-- 01_create_users_table.sql
-- Script para crear la tabla de usuarios

CREATE TABLE IF NOT EXISTS usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(50) NOT NULL UNIQUE,
    START_DATE DATE NOT NULL,
    END_DATE DATE DEFAULT NULL,
    BUSINESS_UNIT VARCHAR(100) NOT NULL,
    MANAGER VARCHAR(50) NOT NULL,
    LAST_UPDATE DATE NOT NULL,
    IS_EXTERNAL BOOLEAN NOT NULL,
    INDEX idx_username (USERNAME),
    INDEX idx_business_unit (BUSINESS_UNIT),
    INDEX idx_end_date (END_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 02_create_trainings_table.sql
-- Script para crear la tabla de capacitaciones

CREATE TABLE IF NOT EXISTS capacitaciones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    LINK VARCHAR(255) NOT NULL,
    CREATION_DATE DATE NOT NULL,
    INDEX idx_name (NAME)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 03_create_user_trainings_table.sql
-- Script para crear la tabla de relación entre usuarios y capacitaciones

CREATE TABLE IF NOT EXISTS capacitaciones_por_usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    FK_USERNAME VARCHAR(50) NOT NULL,
    FK_TRAINING INT NOT NULL,
    END_DATE DATE DEFAULT NULL,
    ASSIGNMENT_DATE DATE NOT NULL,
    INDEX idx_fk_username (FK_USERNAME),
    INDEX idx_fk_training (FK_TRAINING),
    INDEX idx_end_date (END_DATE),
    FOREIGN KEY (FK_USERNAME) REFERENCES usuarios(USERNAME) ON DELETE CASCADE,
    FOREIGN KEY (FK_TRAINING) REFERENCES capacitaciones(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 04_create_metrics_table.sql
-- Script para crear la tabla de métricas históricas

CREATE TABLE IF NOT EXISTS metricas_de_capacitaciones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    BUSINESS_UNIT VARCHAR(100) NOT NULL,
    MONTH DATE NOT NULL,
    COMPLETION_PERCENTAGE DECIMAL(5,2) NOT NULL,
    TOTAL_USERS INT NOT NULL,
    COMPLETED_TRAININGS INT NOT NULL,
    CALCULATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_business_unit (BUSINESS_UNIT),
    INDEX idx_month (MONTH)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;