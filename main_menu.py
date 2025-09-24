from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Button, Static, Input
from managers.cliente_manager import Ciente_manager
from managers.habitacion_manager import Habitacion_manager
from managers.reserva_manager import Reserva_manager
from modelos.base import conectar_db
from textual.screen import Screen

# ------------------ Pantalla Registrar Cliente ------------------
class PantallaCliente(Screen):
    def __init__(self, cliente_mgr):
        super().__init__()
        self.cliente_mgr = cliente_mgr

    def compose(self) -> ComposeResult:
        yield Static("Registrar Cliente", id="titulo_cliente")
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
            nombre = self.query_one("#nombre", Input).value
            apellido = self.query_one("#apellido", Input).value
            telefono = self.query_one("#telefono", Input).value
            correo = self.query_one("#correo", Input).value
            self.cliente_mgr.registrar_cliente(nombre, apellido, telefono, correo)
            self.app.pop_screen()

# ------------------ Pantalla Crear Reserva ------------------
class PantallaReserva(Screen):
    def __init__(self, reserva_mgr, cliente_mgr, habitacion_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr
        self.cliente_mgr = cliente_mgr
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Static("Crear Reserva", id="titulo_reserva")
        yield Input(placeholder="ID Cliente", id="id_cliente")
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
            id_cliente = int(self.query_one("#id_cliente", Input).value)
            num_habit = int(self.query_one("#num_habit", Input).value)
            fecha_entrada = self.query_one("#fecha_entrada", Input).value
            fecha_salida = self.query_one("#fecha_salida", Input).value
            estado = self.query_one("#estado", Input).value
            servicios = self.query_one("#servicios", Input).value
            cuenta = float(self.query_one("#cuenta", Input).value)
            self.reserva_mgr.crear_reserva(num_habit, id_cliente, fecha_entrada, fecha_salida, estado, servicios, cuenta)
            self.app.pop_screen()

# ------------------ Pantalla Consultar Reservas ------------------
class PantallaConsultar(Screen):
    def __init__(self, reserva_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr

    def compose(self) -> ComposeResult:
        yield Input(placeholder="ID Reserva", id="id_reserva")
        yield Button("Consultar", id="btn_consultar")
        yield Button("Volver", id="btn_volver_consultar")
        yield Static("", id="resultado_consulta")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_consultar":
            self.app.pop_screen()
        elif event.button.id == "btn_consultar":
            id_reserva = int(self.query_one("#id_reserva", Input).value)
            resultado = self.reserva_mgr.consultar_reservas(id_reserva)
            self.query_one("#resultado_consulta", Static).update(str(resultado))

# ------------------ Pantalla Mostrar Disponibilidad ------------------
class PantallaDisponibilidad(Screen):
    def __init__(self, habitacion_mgr):
        super().__init__()
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Número de habitación", id="num_habit")
        yield Button("Consultar", id="btn_consultar_disp")
        yield Button("Volver", id="btn_volver_disp")
        yield Static("", id="resultado_disp")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver_disp":
            self.app.pop_screen()
        elif event.button.id == "btn_consultar_disp":
            num_habit = int(self.query_one("#num_habit", Input).value)
            resultado = self.habitacion_mgr.Disponibilidad_habitaciones(num_habit)
            self.query_one("#resultado_disp", Static).update(str(resultado))

# ------------------ Pantalla Principal ------------------
class HotelDashboard(App):
    CSS_PATH = None

    def __init__(self):
        super().__init__()
        self.conn = conectar_db()
        self.cliente_mgr = Ciente_manager(self.conn)
        self.habitacion_mgr = Habitacion_manager(self.conn)
        self.reserva_mgr = Reserva_manager(self.conn)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Vertical(
                Button("Registrar cliente", id="menu_cliente"),
                Button("Crear reserva", id="menu_reserva"),
                Button("Consultar reservas", id="menu_consultar"),
                Button("Mostrar disponibilidad", id="menu_disponibilidad"),
                Button("Salir", id="menu_salir"),
            ),
            id="menu_principal"
        )
        yield Footer()

    def on_button_pressed(self, event):
        if event.button.id == "menu_cliente":
            self.push_screen(PantallaCliente(self.cliente_mgr))
        elif event.button.id == "menu_reserva":
            self.push_screen(PantallaReserva(self.reserva_mgr, self.cliente_mgr, self.habitacion_mgr))
        elif event.button.id == "menu_consultar":
            self.push_screen(PantallaConsultar(self.reserva_mgr))
        elif event.button.id == "menu_disponibilidad":
            self.push_screen(PantallaDisponibilidad(self.habitacion_mgr))
        elif event.button.id == "menu_salir":
            self.exit()


if __name__ == "__main__":
    HotelDashboard().run()
