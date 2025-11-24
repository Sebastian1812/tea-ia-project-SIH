from database.db_handler import DatabaseHandler

def verificar_datos_sesion():
    db = DatabaseHandler()
    datos = db.get_complete_session_data(1)
    
    print("=== DATOS REALES EN BASE DE DATOS ===")
    print(f"Paciente: {datos['paciente']['nombre']}")
    print(f"Edad: {datos['paciente']['edad']}")
    print(f"Diagnóstico: {datos['paciente']['diagnostico']}")
    print(f"Sesión: {datos['sesion']['fecha']}")
    print(f"Terapeuta: {datos['sesion']['terapeuta']}")
    print(f"Duración: {datos['sesion']['duracion_minutos']} minutos")
    
    print("\n=== EJERCICIOS ===")
    for i, ej in enumerate(datos['ejercicios'], 1):
        print(f"Ejercicio {i}:")
        print(f"  Nombre: {ej['nombre_ejercicio']}")
        print(f"  Tipo: {ej['tipo_ejercicio']}")
        print(f"  Completado: {ej['completado']}")
        print(f"  Tiempo respuesta: {ej['tiempo_respuesta_seg']}s")
        print(f"  Dificultad: {ej['nivel_dificultad']}")
        print(f"  Observaciones: {ej['observaciones']}")
    
    print("\n=== MÉTRICAS CALCULADAS ===")
    print(f"Total ejercicios: {datos['metricas']['total_ejercicios']}")
    print(f"Ejercicios completados: {datos['metricas']['ejercicios_completados']}")
    print(f"Porcentaje completamiento: {datos['metricas']['porcentaje_completamiento']}%")
    print(f"Tiempo promedio: {datos['metricas']['tiempo_promedio_respuesta']}s")

if __name__ == "__main__":
    verificar_datos_sesion()
