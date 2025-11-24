import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re
import logging

logger = logging.getLogger(__name__)

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configurar estilos personalizados"""
        if 'Title_Custom' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Title_Custom',  # Nombre único
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            ))
        
        if 'Heading2_Custom' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Heading2_Custom',  # Nombre único
                parent=self.styles['Heading2'],
                fontSize=12,
                spaceAfter=12,
                textColor='#2E86AB'
            ))
        
        if 'Body_Custom' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Body_Custom',  # Nombre único
                parent=self.styles['BodyText'],
                fontSize=10,
                spaceAfter=12,
                leading=14
            ))
    
    def export_to_pdf(self, report_content: str, output_filename: str):
        """Exportar reporte a PDF"""
        
        try:
            logger.info(f"Creando PDF: {output_filename}")
            doc = SimpleDocTemplate(
                output_filename,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Procesar el contenido del reporte
            sections = self._parse_report_sections(report_content)
            
            for section_title, section_content in sections.items():
                if section_title and section_title.strip():
                    # Usar estilos personalizados
                    story.append(Paragraph(section_title.strip(), self.styles['Heading2_Custom']))
                
                paragraphs = [p for p in section_content.split('\n\n') if p.strip()]
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), self.styles['Body_Custom']))
                        story.append(Spacer(1, 6))
                
                story.append(Spacer(1, 12))
            
            doc.build(story)
            logger.info(f"PDF creado: {output_filename}")
            
        except Exception as e:
            logger.error(f"Error al crear PDF: {e}")
            raise
    
    def _parse_report_sections(self, content: str) -> dict:
        """contenido en secciones"""
        sections = {}
        current_section = "Introduccion"
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detectar encabezados de seccion
            if line.startswith('# ') or line.startswith('## '):
                # Guardar seccion anterior
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                    current_content = []
                
                # Nueva seccion (limpiar #)
                current_section = re.sub(r'^#+\s*', '', line).strip()
            elif line:
                current_content.append(line)
        
        # Agregar la última seccion
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections