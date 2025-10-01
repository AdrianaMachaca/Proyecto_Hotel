from fpdf import FPDF

# ---------------- GENERAR PDF ----------------

def generar_pdf_clientes(clientes, filename="clientes.pdf"):
    if clientes:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reporte de Clientes", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        headers = ["ID", "Nombre", "Apellido", "Telefono", "Correo"]
        for h in headers:
            pdf.cell(38, 10, h, 1)
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        for c in clientes:
            for valor in c:
                pdf.cell(38, 10, str(valor), 1)
            pdf.ln()
        pdf.output(filename)
        print(f"📄 PDF de clientes generado: {filename}")
    else:
        print("❌ No hay clientes para generar PDF")


def generar_pdf_habitaciones(habitaciones, filename="habitaciones.pdf"):
    if habitaciones:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reporte de Habitaciones", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        headers = ["Numero","Tipo","Estado","Precio","Capacidad","Servicios","Observaciones"]
        for h in headers:
            pdf.cell(27, 10, h, 1)
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        for h in habitaciones:
            for valor in h:
                pdf.cell(27, 10, str(valor), 1)
            pdf.ln()
        pdf.output(filename)
        print(f"📄 PDF generado: {filename}")
    else:
        print("❌ No hay habitaciones para generar PDF")

def generar_pdf_reservas(reservas, filename="reservas.pdf"):
    if reservas:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reporte de Reservas", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        headers = ["ID","Habitacion","Cliente","Entrada","Salida","Estado","Servicios","Costo"]
        for h in headers:
            pdf.cell(25, 10, h, 1)
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        for r in reservas:
            for valor in r:
                pdf.cell(25, 10, str(valor), 1)
            pdf.ln()
        pdf.output(filename)
        print(f"📄 PDF de reservas generado: {filename}")
    else:
        print("❌ No hay reservas para generar PDF")
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

