from database.config import DatabaseConfig

def test_connection():
    print("🔍 Probando conexión a MySQL...")
    conn = DatabaseConfig.get_connection()
    if conn:
        print("✅ MySQL conectado exitosamente!")
        
        # Insertar datos de prueba
        cursor = conn.cursor()
        
        # Insertar paciente de prueba
        cursor.execute("""
            INSERT INTO pacientes (nombre, edad, diagnostico) 
            VALUES (%s, %s, %s)
        """, ('Juan Pérez', 5, 'TEA Nivel 1'))
        
        # Insertar sesión de prueba
        cursor.execute("""
            INSERT INTO sesiones_terapeuticas 
            (paciente_id, fecha, duracion_minutos, terapeuta_asignado) 
            VALUES (%s, %s, %s, %s)
        """, (1, '2024-11-15', 45, 'Dra. María Rodríguez'))
        
        # Insertar ejercicio de prueba (aplauso-sonido)
        cursor.execute("""
            INSERT INTO ejercicios_sensoriales 
            (sesion_id, nombre_ejercicio, tipo_ejercicio, completado, tiempo_respuesta_seg, nivel_dificultad) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (1, 'Coordinación Aplauso-Sonido', 'auditivo', True, 2.5, 'medio'))
        
        conn.commit()
        print("✅ Datos de prueba insertados!")
        
        # Mostrar datos insertados
        cursor.execute("""
            SELECT p.nombre, p.edad, s.fecha, e.nombre_ejercicio, e.tiempo_respuesta_seg 
            FROM pacientes p
            JOIN sesiones_terapeuticas s ON p.id = s.paciente_id
            JOIN ejercicios_sensoriales e ON s.id = e.sesion_id
        """)
        
        results = cursor.fetchall()
        print("📊 Datos en la base de datos:")
        for row in results:
            print(f"  Paciente: {row[0]}, Edad: {row[1]}, Fecha: {row[2]}")
            print(f"  Ejercicio: {row[3]}, Tiempo: {row[4]}s")
        
        cursor.close()
        conn.close()
    else:
        print("❌ Error en conexión MySQL")

if __name__ == "__main__":
    test_connection()
