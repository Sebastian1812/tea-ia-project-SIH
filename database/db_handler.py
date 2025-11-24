import mysql.connector
from mysql.connector import Error
from database.config import DatabaseConfig
import json
from typing import Dict, Any

class DatabaseHandler:
    def __init__(self):
        self.config = DatabaseConfig()
    
    def get_complete_session_data(self, session_id: int) -> Dict[str, Any]:
        """
        Obtener datos completos de una sesión para el reporte
        """
        try:
            connection = self.config.get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            # Consulta para obtener datos completos de la sesión
            query = """
            SELECT 
                p.id as paciente_id,
                p.nombre as paciente_nombre,
                p.edad as paciente_edad,
                p.diagnostico as paciente_diagnostico,
                s.id as sesion_id,
                s.fecha as sesion_fecha,
                s.duracion_minutos as sesion_duracion,
                s.terapeuta_asignado as terapeuta,
                s.notas_terapeuta as notas_terapeuta,
                COUNT(e.id) as total_ejercicios,
                SUM(CASE WHEN e.completado = 1 THEN 1 ELSE 0 END) as ejercicios_completados,
                AVG(e.tiempo_respuesta_seg) as tiempo_promedio_respuesta
            FROM sesiones_terapeuticas s
            JOIN pacientes p ON s.paciente_id = p.id
            LEFT JOIN ejercicios_sensoriales e ON s.id = e.sesion_id
            WHERE s.id = %s
            GROUP BY s.id
            """
            
            cursor.execute(query, (session_id,))
            session_info = cursor.fetchone()
            
            if not session_info:
                return {}
            
            # Obtener detalles de ejercicios
            ejercicios_query = """
            SELECT 
                nombre_ejercicio,
                tipo_ejercicio,
                completado,
                tiempo_respuesta_seg,
                nivel_dificultad,
                observaciones
            FROM ejercicios_sensoriales
            WHERE sesion_id = %s
            """
            
            cursor.execute(ejercicios_query, (session_id,))
            ejercicios = cursor.fetchall()
            
            # Obtener métricas de sensores
            metricas_query = """
            SELECT 
                metricas_kinect,
                interacciones_esp32,
                patrones_movimiento
            FROM metricas_sensores
            WHERE sesion_id = %s
            ORDER BY timestamp DESC
            LIMIT 1
            """
            
            cursor.execute(metricas_query, (session_id,))
            metricas = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            # Estructurar datos para el reporte
            structured_data = {
                'paciente': {
                    'id': session_info['paciente_id'],
                    'nombre': session_info['paciente_nombre'],
                    'edad': session_info['paciente_edad'],
                    'diagnostico': session_info['paciente_diagnostico']
                },
                'sesion': {
                    'id': session_info['sesion_id'],
                    'fecha': str(session_info['sesion_fecha']),
                    'duracion_minutos': session_info['sesion_duracion'],
                    'terapeuta': session_info['terapeuta'],
                    'notas_terapeuta': session_info['notas_terapeuta'] or "Sin notas adicionales"
                },
                'ejercicios': ejercicios,
                'metricas': {
                    'total_ejercicios': session_info['total_ejercicios'],
                    'ejercicios_completados': session_info['ejercicios_completados'],
                    'porcentaje_completamiento': round(
                        (session_info['ejercicios_completados'] / session_info['total_ejercicios'] * 100) 
                        if session_info['total_ejercicios'] > 0 else 0, 2
                    ),
                    'tiempo_promedio_respuesta': round(session_info['tiempo_promedio_respuesta'] or 0, 2),
                    'datos_sensores': metricas or {}
                }
            }
            
            return structured_data
            
        except Error as e:
            print(f"ERROR en base de datos: {e}")
            return {}
