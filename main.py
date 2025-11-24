import logging
from database.db_handler import DatabaseHandler
from ia.report_generator import ReportGenerator
from utils.pdf_exporter import PDFExporter
import argparse

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Generar reporte terapéutico automático')
    parser.add_argument('--session_id', type=int, required=True, help='ID de la sesión terapéutica')
    parser.add_argument('--output', type=str, default='reporte_terapeutico.pdf', help='Archivo de salida PDF')
    
    args = parser.parse_args()
    
    try:
        logger.info(f"########Iniciando generación de reporte para sesión {args.session_id}#######")
        
        # 1. EXTRAER DATOS DE BD
        logger.info("-----Extrayendo datos de MySQL...")
        db_handler = DatabaseHandler()
        session_data = db_handler.get_complete_session_data(args.session_id)
        
        if not session_data:
            logger.error(f"XXXXXX NO se encontraron datos para la sesión {args.session_id}")
            return
        
        logger.info(f"BIEN - Datos extraídos: {len(session_data.get('ejercicios', []))} ejercicios")
        
        # 2. GENERAR REPORTE CON IA
        logger.info("-----Generando reporte con Ollama...")
        report_generator = ReportGenerator()
        report_content = report_generator.generate_therapeutic_report(session_data)
        
        logger.info(f"BIEN - Reporte generado: {len(report_content)} caracteres")
        
        # 3. EXPORTAR A PDF
        logger.info("-----Generando PDF...")
        pdf_exporter = PDFExporter()
        output_path = f"reports/{args.output}"
        pdf_exporter.export_to_pdf(report_content, output_path)
        
        logger.info(f"BIEN - Reporte generado: {args.output}")
        logger.info(f"%%%%%GUARDADO en: /home/azureuser/tea-ia-project/{args.output}")
        
    except Exception as e:
        logger.error(f"ERROR ERROR ERROR en la generación del reporte: {str(e)}")
        raise

if __name__ == "__main__":
    main()
