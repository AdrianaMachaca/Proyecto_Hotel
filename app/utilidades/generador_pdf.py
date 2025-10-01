# utils/pdf_generator.py

from fpdf import FPDF

def generar_pdf_clientes(clientes, filename="reporte_clientes.pdf"):
    """
    Función para generar un reporte PDF de los clientes.
    
    :param clientes: Lista de tuplas de clientes (idC, nombre, apellido, telefono, correo)
    :param filename: Nombre del archivo PDF a generar
    """
    try:
        # Crear un objeto PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Título
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Reporte de Clientes", ln=True, align="C")
        pdf.ln(10)

        # Cuerpo
        pdf.set_font("Arial", "", 12)
        for c in clientes:
            idC, nombre, apellido, telefono, correo = c
            pdf.cell(0, 10, f"{idC}: {nombre} {apellido}, Tel: {telefono}, Correo: {correo}", ln=True)
        
        # Guardar PDF
        pdf.output(filename)
    except Exception as e:
        raise Exception(f"Error al generar el PDF: {str(e)}")
