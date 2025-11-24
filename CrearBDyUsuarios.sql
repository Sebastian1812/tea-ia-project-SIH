-- Dentro de MySQL, ejecuta estos comandos:

-- Crear base de datos
CREATE DATABASE tesis_tea;

-- Crear usuario específico para la aplicación
CREATE USER 'tea_user'@'localhost' IDENTIFIED BY 'TeaPassword123!';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON tesis_tea.* TO 'tea_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Cambiar a la base de datos
USE tesis_tea;