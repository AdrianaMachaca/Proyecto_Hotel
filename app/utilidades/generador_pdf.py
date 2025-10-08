from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.titulo, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()} | Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 0, "C")

def generar_pdf_clientes(clientes, filename="reporte_clientes.pdf"):
    pdf = PDF()
    pdf.titulo = "Reporte de Clientes"
    pdf.add_page()

    if not clientes:
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "No hay clientes registrados.", ln=True)
    else:
        headers = ["ID", "Nombre", "Apellido", "Telefono", "Correo"]
        widths = [20, 40, 40, 40, 50]

        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(200, 220, 255)
        for i in range(len(headers)):
            pdf.cell(widths[i], 10, headers[i], 1, 0, "C", fill=True)
        pdf.ln()

        pdf.set_font("Arial", "", 12)
        for idC, nombre, apellido, telefono, correo in clientes:
            pdf.cell(20, 10, str(idC), 1)
            pdf.cell(40, 10, nombre, 1)
            pdf.cell(40, 10, apellido, 1)
            pdf.cell(40, 10, telefono, 1)
            pdf.cell(50, 10, correo, 1, ln=True)

    pdf.output(filename)
    print(f"✅ PDF generado: {filename}")

def generar_pdf_habitaciones(habitaciones, filename="reporte_habitaciones.pdf"):
    pdf = PDF()
    pdf.titulo = "Reporte de Habitaciones"
    pdf.add_page()

    if not habitaciones:
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "No hay habitaciones registradas.", ln=True)
    else:
        headers = ["Numero","Tipo","Estado","Precio","Capacidad","Servicios","Observaciones"]
        widths = [20, 25, 25, 25, 20, 35, 40]

        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(200, 220, 255)
        for i in range(len(headers)):
            pdf.cell(widths[i], 10, headers[i], 1, 0, "C", fill=True)
        pdf.ln()

        pdf.set_font("Arial", "", 12)
        for num, tipo, estado, precio, capacidad, servicios, observ in habitaciones:
            pdf.cell(20, 10, str(num), 1)
            pdf.cell(25, 10, tipo, 1)
            pdf.cell(25, 10, estado, 1)
            pdf.cell(25, 10, str(precio), 1)
            pdf.cell(20, 10, str(capacidad), 1)
            pdf.cell(35, 10, servicios, 1)
            pdf.cell(40, 10, observ, 1, ln=True)

    pdf.output(filename)
    print(f"✅ PDF generado: {filename}")

def generar_pdf_reservas(reservas, filename="reporte_reservas.pdf"):
    pdf = PDF()
    pdf.titulo = "Reporte de Reservas"
    pdf.add_page()

    if not reservas:
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, "No hay reservas registradas.", ln=True)
    else:
        headers = ["ID","Habitacion","Cliente","Entrada","Salida","Estado","Servicios","Costo"]
        widths = [15, 25, 20, 25, 25, 25, 35, 20]

        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(200, 220, 255)
        for i in range(len(headers)):
            pdf.cell(widths[i], 10, headers[i], 1, 0, "C", fill=True)
        pdf.ln()

        pdf.set_font("Arial", "", 12)
        for idR, numHabit, idCliente, fechaEntrada, fechaSalida, estado, servicios, costo in reservas:
            pdf.cell(15, 10, str(idR), 1)
            pdf.cell(25, 10, str(numHabit), 1)
            pdf.cell(20, 10, str(idCliente), 1)
            pdf.cell(25, 10, fechaEntrada, 1)
            pdf.cell(25, 10, fechaSalida, 1)
            pdf.cell(25, 10, estado, 1)
            pdf.cell(35, 10, servicios, 1)
            pdf.cell(20, 10, str(costo), 1, ln=True)

    pdf.output(filename)
    print(f"✅ PDF generado: {filename}")
