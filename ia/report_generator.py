import ollama
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.model_name = model_name
        self._ensure_model_available()
    
    def _ensure_model_available(self):
        """Verificar que el MODELO este disponible"""
        try:
            print("=== DEPURACION: Verificacion de modelos ===")
            models = ollama.list()
            print(f"Modelos crudos: {models}")
            
            if 'models' in models and models['models']:
                model_names = []
                for model in models['models']:
                    name = model.model
                    model_names.append(name)
                    print(f"Modelo encontrado: '{name}'")
                
                print(f"Buscando: '{self.model_name}'")
                print(f"En lista: {model_names}")
                
                if self.model_name in model_names:
                    print(f"=== EXITO: Modelo {self.model_name} ENCONTRADO ===")
                    logger.info(f"El Modelo {self.model_name} esta disponible")
                else:
                    print(f"=== FALLO: Modelo {self.model_name} NO encontrado ===")
                    available_model = models['models'][0].model
                    print(f"Usando modelo alternativo: {available_model}")
                    logger.warning(f"NO SE ENCONTRO Modelo {self.model_name}. Usando: {available_model}")
                    self.model_name = available_model
            else:
                print("=== NO HAY MODELOS ===")
                logger.warning("NO se encontraron modelos. Usando modelo por defecto.")
                self.model_name = 'llama3.2:1b'
                
        except Exception as e:
            print(f"=== ERROR: {e} ===")
            logger.warning(f"Error verificando modelos: {e}. Continuando...")
    
    def generate_therapeutic_report(self, session_data: Dict[str, Any]) -> str:
        """Generar reporte terapeutico usando IA"""
        print("##### GENERAR reporte terapeutico")
        prompt = self._build_therapeutic_prompt(session_data)
        
        try:
            logger.info("-----------Iniciando generacion con Ollama...")
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                options={
                    'temperature': 0.3,
                    'top_p': 0.9,
                    'num_predict': 1500
                }
            )
            
            report_content = response['message']['content']
            logger.info("Generacion con Ollama completada")
            return report_content
            
        except Exception as e:
            logger.error(f"Error en generacion de reporte: {e}")
            return self._generate_fallback_report(session_data)
    
    def _build_therapeutic_prompt(self, data: Dict[str, Any]) -> str:
        """Construir prompt para analisis terapeutico"""
        print("##### CONSTRUIR prompt para el analisis terapeutico")
        
        ejercicios_text = ""
        for i, ej in enumerate(data.get('ejercicios', []), 1):
            status = "COMPLETADO" if ej['completado'] else "NO COMPLETADO"
            ejercicios_text += f"{i}. {ej['nombre_ejercicio']} ({ej['tipo_ejercicio']}) - {status}\n"
            if ej['tiempo_respuesta_seg']:
                ejercicios_text += f"   Tiempo: {ej['tiempo_respuesta_seg']}s | Dificultad: {ej['nivel_dificultad']}\n"
            if ej['observaciones']:
                ejercicios_text += f"   Observaciones: {ej['observaciones']}\n"
            ejercicios_text += "\n"
        
        prompt = f"""
Eres TERA-AI, un asistente especializado en analisis terapeutico para ninos con Trastorno del Espectro Autista (TEA).

DATOS CRUDOS DE LA SESION:

PACIENTE:
- Nombre: {data['paciente']['nombre']}
- Edad: {data['paciente']['edad']} anos
- Diagnostico: {data['paciente']['diagnostico']}

SESION:
- Fecha: {data['sesion']['fecha']}
- Duracion: {data['sesion']['duracion_minutos']} minutos
- Terapeuta: {data['sesion']['terapeuta']}

EJERCICIO ESPECIFICO REALIZADO:
- Nombre: {data['ejercicios'][0]['nombre_ejercicio']}
- Tipo: {data['ejercicios'][0]['tipo_ejercicio']}
- Completado: {'SI' if data['ejercicios'][0]['completado'] else 'NO'}
- Tiempo de respuesta: {data['ejercicios'][0]['tiempo_respuesta_seg']} segundos
- Dificultad: {data['ejercicios'][0]['nivel_dificultad']}
- Observaciones: {data['ejercicios'][0]['observaciones'] or 'Ninguna'}

METRICAS DE DESEMPENO:
- Ejercicios completados: {data['metricas']['ejercicios_completados']}/{data['metricas']['total_ejercicios']}
- Tasa de exito: {data['metricas']['porcentaje_completamiento']}%
- Tiempo promedio: {data['metricas']['tiempo_promedio_respuesta']}s

GENERA UN REPORTE MEJORADO CON:

# REPORTE TERAPEUTICO - {data['paciente']['nombre']}

## ANALISIS DE DATOS ESPECIFICOS
[Analiza los datos crudos mostrados arriba, enfocandote en los valores numericos y su significado clinico]

## INTERPRETACION DE RESULTADOS
[Explica que significan estos datos en el contexto del desarrollo del nino con TEA]

## OBJETIVOS ESPECIFICOS PARA PROXIMA SESION
[3 objetivos MEDIBLES basados en los datos actuales. Ejemplo:
1. "Reducir tiempo de respuesta en ejercicios auditivos de {data['metricas']['tiempo_promedio_respuesta']}s a Xs"
2. "Introducir variante del ejercicio actual con Y nivel de complejidad"
3. "Mantener tasa de exito del Z% en nuevos ejercicios"]

Basate unicamente en los datos proporcionados.
"""
        return prompt
    
    def _generate_fallback_report(self, session_data: Dict[str, Any]) -> str:
        """Generar reporte basico si falla la IA"""
        print("##### GENERAR reporte basico si falla la IA")
        return f"""
# REPORTE TERAPEUTICO - {session_data['paciente']['nombre']}

## RESUMEN EJECUTIVO
Sesion del {session_data['sesion']['fecha']} con {session_data['metricas']['porcentaje_completamiento']}% de ejercicios completados.

## DATOS DE LA SESION
- Paciente: {session_data['paciente']['nombre']}
- Edad: {session_data['paciente']['edad']} anos
- Ejercicios completados: {session_data['metricas']['ejercicios_completados']}/{session_data['metricas']['total_ejercicios']}
- Tiempo promedio: {session_data['metricas']['tiempo_promedio_respuesta']}s

[Reporte generado automaticamente - Modo de respaldo]
"""