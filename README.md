# Sistema de Generación Automática de Reportes Terapéuticos para TEA
Sistema basado en IA que genera reportes terapéuticos automáticos para niños con Trastorno del Espectro Autista (TEA), procesando información de sesiones sensoriales de una base de datos con una estructura definida, mediante modelos de lenguaje local.
## Características
- **Generación automática** de reportes terapéuticos
- **Integración con MySQL** para gestión de datos
- **Modelos de IA local** via Ollama
- **Exportación a PDF** profesional
- **Análisis de ejercicios sensoriales**
- Los "test" y "PRUEBA" son para verificar conexiones y funcionamientos del sistema

## Instalación

### Prerrequisitos
- Python 3.8+
- MySQL Server
- Ollama (con modelos Llama 3.1:8b/3.2:1b)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tuusuario/tea-ia-project.git
cd tea-ia-Project
```
### 2. Configurar entorno virtual
python3 -m venv tea-env
source tea-env/bin/activate  # Linux/Mac
# tea-env\Scripts\activate  # Windows

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Configurar base de datos MySQL
CREATE DATABASE tesis_tea;
CREATE USER 'tea_user'@'localhost' IDENTIFIED BY 'TuPassword123!';
GRANT ALL PRIVILEGES ON tesis_tea.* TO 'tea_user'@'localhost';
FLUSH PRIVILEGES;

### 5. Configurar Ollama
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo
ollama pull llama3.1:8b
ollama pull llama3.2:1b

### 6. Configurar Ollama
cp .env.example .env
# Editar .env con tus credenciales



USO

# Generar reporte
python main.py --session_id 1 --output mi_reporte.pdf

# RECURSOS DE PROCESAMIENTO:
SE RECOMIENDA USAR UNA GPU PARA GENERAR UNA MAYOR CANTIDAD DE REPORTES EN POCO TIEMPO, EN CASO DE USAR CPU, PODRÍA TARDAR ENTRE 5 A 15 MINUTOS.

# VM UTILIZADA:
	Tipo: Standard D4s v3 (4 vCPUs, 16 GB RAM)
	SO: Ubuntu 22.04 LTS
	Disco: SSD Premium 64GB

# AUTOR
    Sebastián Jiménez Rojas - Desarrollo e implementación
