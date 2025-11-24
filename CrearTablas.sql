-- Tabla de pacientes
CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    diagnostico VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de sesiones terapéuticas
CREATE TABLE sesiones_terapeuticas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    fecha DATE NOT NULL,
    duracion_minutos INT,
    terapeuta_asignado VARCHAR(100),
    notas_terapeuta TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- Tabla de ejercicios sensoriales
CREATE TABLE ejercicios_sensoriales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sesion_id INT,
    nombre_ejercicio VARCHAR(100),
    tipo_ejercicio ENUM('visual', 'auditivo', 'tactil', 'motor', 'cognitivo'),
    completado BOOLEAN DEFAULT FALSE,
    tiempo_respuesta_seg DECIMAL(5,2),
    nivel_dificultad ENUM('bajo', 'medio', 'alto'),
    observaciones TEXT,
    FOREIGN KEY (sesion_id) REFERENCES sesiones_terapeuticas(id)
);

-- Tabla de métricas de sensores
CREATE TABLE metricas_sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sesion_id INT,
    metricas_kinect JSON,
    interacciones_esp32 JSON,
    patrones_movimiento JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sesion_id) REFERENCES sesiones_terapeuticas(id)
);