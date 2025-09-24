from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Button, Input
from textual.screen import Screen
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from fpdf import FPDF

from modelos.base import conectar_db
from managers.cliente_manager import Ciente_manager
from managers.habitacion_manager import Habitacion_manager
from managers.reserva_manager import Reserva_manager

# ------------------ Pantalla Mensaje ------------------
class MensajePantalla(Screen):
    def __init__(self, mensaje: str):
        super().__init__()
        self.mensaje = mensaje

    def compose(self) -> ComposeResult:
        yield Static(Panel(self.mensaje))
        yield Button("Ir al menú principal", id="btn_menu")

    def on_button_pressed(self, event):
        if event.button.id == "btn_menu":
            self.app.push_screen(self.app.menu_principal)

# ------------------ Pantalla Login con encabezado ------------------
class PantallaLogin(Screen):
    def __init__(self, cabecera_panel):
        super().__init__()
        self.cabecera_panel = cabecera_panel

    def compose(self) -> ComposeResult:
        yield self.cabecera_panel
        yield Static(Panel("Ingrese sus credenciales"))
        yield Input(placeholder="Usuario", id="usuario")
        yield Input(placeholder="Contraseña", id="contrasena", password=True)
        yield Button("Ingresar", id="btn_ingresar")

    def on_button_pressed(self, event):
        if event.button.id == "btn_ingresar":
            usuario = self.query_one("#usuario", Input).value
            contrasena = self.query_one("#contrasena", Input).value
            if usuario == "admin" and contrasena == "1234":
                self.app.push_screen(self.app.menu_principal)
            else:
                self.app.push_screen(MensajePantalla("Usuario o contraseña incorrectos"))

# ------------------ Pantalla Cliente ------------------
class PantallaCliente(Screen):
    def __init__(self, cliente_mgr, reserva_mgr, habitacion_mgr):
        super().__init__()
        self.cliente_mgr = cliente_mgr
        self.reserva_mgr = reserva_mgr
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Static(Panel("Registrar Cliente"))
        yield Input(placeholder="Nombre", id="nombre")
        yield Input(placeholder="Apellido", id="apellido")
        yield Input(placeholder="Teléfono", id="telefono")
        yield Input(placeholder="Correo", id="correo")
        yield Button("Registrar", id="btn_registrar")
        yield Button("Volver", id="btn_volver_cliente")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_cliente":
            self.app.pop_screen()
        elif event.button.id == "btn_registrar":
            try:
                nombre = self.query_one("#nombre", Input).value
                apellido = self.query_one("#apellido", Input).value
                telefono = self.query_one("#telefono", Input).value
                correo = self.query_one("#correo", Input).value

                id_cliente = self.cliente_mgr.registrar_cliente(nombre, apellido, telefono, correo)

                self.app.push_screen(PreguntarReserva(id_cliente, self.reserva_mgr, self.habitacion_mgr))
            except Exception as e:
                self.app.push_screen(MensajePantalla(f"Error al registrar cliente: {str(e)}"))

# ------------------ Pantalla Preguntar Reserva ------------------
class PreguntarReserva(Screen):
    def __init__(self, id_cliente, reserva_mgr, habitacion_mgr):
        super().__init__()
        self.id_cliente = id_cliente
        self.reserva_mgr = reserva_mgr
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Static(Panel(f"Cliente {self.id_cliente} registrado. ¿Desea crear una reserva ahora?"))
        yield Vertical(
            Button("Sí", id="btn_si"),
            Button("No", id="btn_no")
        )

    def on_button_pressed(self, event):
        if event.button.id == "btn_si":
            self.app.push_screen(PantallaReserva(self.reserva_mgr, self.id_cliente, self.habitacion_mgr))
        elif event.button.id == "btn_no":
            self.app.push_screen(self.app.menu_principal)

# ------------------ Pantalla Crear Reserva ------------------
class PantallaReserva(Screen):
    def __init__(self, reserva_mgr, id_cliente, habitacion_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr
        self.id_cliente = id_cliente
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Static(Panel("Crear Reserva"))
        yield Input(placeholder="Número Habitación", id="num_habit")
        yield Input(placeholder="Fecha Entrada (YYYY-MM-DD)", id="fecha_entrada")
        yield Input(placeholder="Fecha Salida (YYYY-MM-DD)", id="fecha_salida")
        yield Input(placeholder="Estado (Confirmada/Pendiente/Cancelada)", id="estado")
        yield Input(placeholder="Servicios extras", id="servicios")
        yield Input(placeholder="Costo total", id="cuenta")
        yield Button("Crear Reserva", id="btn_crear_reserva")
        yield Button("Volver", id="btn_volver_reserva")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_reserva":
            self.app.pop_screen()
        elif event.button.id == "btn_crear_reserva":
            try:
                num_habit = int(self.query_one("#num_habit", Input).value)
                fecha_entrada = self.query_one("#fecha_entrada", Input).value
                fecha_salida = self.query_one("#fecha_salida", Input).value
                estado = self.query_one("#estado", Input).value
                servicios = self.query_one("#servicios", Input).value
                cuenta = float(self.query_one("#cuenta", Input).value)
                self.reserva_mgr.crear_reserva(num_habit, self.id_cliente, fecha_entrada, fecha_salida, estado, servicios, cuenta)
                self.app.push_screen(MensajePantalla("Reserva creada correctamente"))
            except Exception as e:
                self.app.push_screen(MensajePantalla(f"Error: {str(e)}"))

# ------------------ Pantalla Consultar Reservas ------------------
class PantallaConsultar(Screen):
    def __init__(self, reserva_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr

    def compose(self) -> ComposeResult:
        yield Static(Panel("Consultar Reserva"))
        yield Input(placeholder="ID Reserva", id="id_reserva")
        yield Button("Consultar", id="btn_consultar")
        yield Button("Volver", id="btn_volver_consultar")
        yield Static("", id="resultado_consulta")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_consultar":
            self.app.pop_screen()
        elif event.button.id == "btn_consultar":
            try:
                id_reserva = int(self.query_one("#id_reserva", Input).value)
                resultado = self.reserva_mgr.consultar_reservas(id_reserva)
                self.query_one("#resultado_consulta", Static).update(str(resultado))
            except Exception as e:
                self.query_one("#resultado_consulta", Static).update(f"Error: {str(e)}")

# ------------------ Pantalla Eliminar Reserva ------------------
class PantallaEliminarReserva(Screen):
    def __init__(self, reserva_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr

    def compose(self) -> ComposeResult:
        yield Static(Panel("Eliminar Reserva"))
        yield Input(placeholder="ID Reserva a eliminar", id="id_reserva_eliminar")
        yield Button("Eliminar", id="btn_eliminar")
        yield Button("Volver", id="btn_volver_eliminar")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_eliminar":
            self.app.pop_screen()
        elif event.button.id == "btn_eliminar":
            try:
                id_reserva = int(self.query_one("#id_reserva_eliminar", Input).value)
                exito = self.reserva_mgr.eliminar_reserva(id_reserva)
                if exito:
                    self.app.push_screen(MensajePantalla(f"Reserva {id_reserva} eliminada correctamente"))
                else:
                    self.app.push_screen(MensajePantalla(f"No existe la reserva con ID {id_reserva}"))
            except Exception as e:
                self.app.push_screen(MensajePantalla(f"Error: {str(e)}"))

# ------------------ Pantalla Disponibilidad ------------------
class PantallaDisponibilidad(Screen):
    def __init__(self, habitacion_mgr):
        super().__init__()
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Static(Panel("Consultar Disponibilidad"))
        yield Input(placeholder="Número de habitación", id="num_habit")
        yield Button("Consultar", id="btn_consultar_disp")
        yield Button("Volver", id="btn_volver_disp")
        yield Static("", id="resultado_disp")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_disp":
            self.app.pop_screen()
        elif event.button.id == "btn_consultar_disp":
            try:
                num_habit = int(self.query_one("#num_habit", Input).value)
                resultado = self.habitacion_mgr.Disponibilidad_habitaciones(num_habit)
                self.query_one("#resultado_disp", Static).update(str(resultado))
            except Exception as e:
                self.query_one("#resultado_disp", Static).update(f"Error: {str(e)}")

# ------------------ Pantalla Menú Principal ------------------
class MenuPrincipalScreen(Screen):
    def __init__(self, cliente_mgr, habitacion_mgr, reserva_mgr):
        super().__init__()
        self.cliente_mgr = cliente_mgr
        self.habitacion_mgr = habitacion_mgr
        self.reserva_mgr = reserva_mgr

    def compose(self) -> ComposeResult:
        yield Vertical(
            Button("Registrar cliente", id="menu_cliente"),
            Button("Crear reserva", id="menu_reserva"),
            Button("Consultar reservas", id="menu_consultar"),
            Button("Eliminar reserva", id="menu_eliminar"),
            Button("Mostrar disponibilidad", id="menu_disponibilidad"),
            Button("Generar reporte PDF clientes", id="menu_pdf"),
            Button("Salir", id="menu_salir"),
        )

    def on_button_pressed(self, event):
        if event.button.id == "menu_cliente":
            self.app.push_screen(PantallaCliente(self.app.cliente_mgr, self.app.reserva_mgr, self.app.habitacion_mgr))
        elif event.button.id == "menu_reserva":
            self.app.push_screen(PantallaReserva(self.app.reserva_mgr, None, self.app.habitacion_mgr))
        elif event.button.id == "menu_consultar":
            self.app.push_screen(PantallaConsultar(self.app.reserva_mgr))
        elif event.button.id == "menu_eliminar":
            self.app.push_screen(PantallaEliminarReserva(self.app.reserva_mgr))
        elif event.button.id == "menu_disponibilidad":
            self.app.push_screen(PantallaDisponibilidad(self.app.habitacion_mgr))
        elif event.button.id == "menu_pdf":
            self.generar_pdf()
        elif event.button.id == "menu_salir":
            self.app.exit()

    def generar_pdf(self):
        try:
            cursor = self.app.cliente_mgr.cursor
            cursor.execute("SELECT * FROM Cliente")
            clientes = cursor.fetchall()
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Reporte de Clientes", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", "", 12)
            for c in clientes:
                idC, nombre, apellido, telefono, correo = c
                pdf.cell(0, 10, f"{idC}: {nombre} {apellido}, Tel: {telefono}, Correo: {correo}", ln=True)
            pdf.output("reporte_clientes.pdf")
            self.app.push_screen(MensajePantalla("PDF generado: reporte_clientes.pdf"))
        except Exception as e:
            self.app.push_screen(MensajePantalla(f"Error al generar PDF: {str(e)}"))

# ------------------ App principal ------------------
class HotelDashboard(App):
    CSS_PATH = "estilos.tcss"

    def __init__(self):
        super().__init__()
        self.conn = conectar_db()
        self.cliente_mgr = Ciente_manager(self.conn)
        self.habitacion_mgr = Habitacion_manager(self.conn)
        self.reserva_mgr = Reserva_manager(self.conn)

        # Panel ASCII para login
        f = Figlet(font='slant')
        ascii_art = f.renderText("THE DUNE PALACE")
        combined_text = Text(justify="center")
        combined_text.append("🏜️ 🏨 🌅 WELCOME TO THE DUNE PALACE 🌅 🏨 🏜️\n", style="bold yellow")
        combined_text.append(ascii_art, style="bold #DCC7AA")
        self.cabecera_panel = Static(Panel(combined_text, title="Hotel"), id="cabecera_panel")

        # Menú principal listo para usar
        self.menu_principal = MenuPrincipalScreen(self.cliente_mgr, self.habitacion_mgr, self.reserva_mgr)

    def on_mount(self):
        # Mostramos login con encabezado primero
        self.push_screen(PantallaLogin(self.cabecera_panel))

if __name__ == "__main__":
    HotelDashboard().run()
