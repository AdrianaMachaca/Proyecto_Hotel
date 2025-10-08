from textual.app import App
from textual.widgets import Static
from rich.text import Text
from pyfiglet import Figlet

from app.modelos.base import conectar_db
from app.managers.cliente_manager import Cliente_manager
from app.managers.habitacion_manager import Habitacion_manager
from app.managers.reserva_manager import Reserva_manager

from app.screens.pantalla_menu import MenuPrincipalScreen
from app.screens.pantalla_login import PantallaLogin
from app.screens.pantalla_cliente import PantallaCliente
from app.screens.pantalla_consultar import PantallaConsultar


class HotelDashboard(App):
    CSS_PATH = "estilos.tcss"  # Archivo de estilos

    def __init__(self):
        super().__init__()
        self.id_cliente = None  # ✅ Inicializa aquí

        # Conexión a la base de datos
        conn = conectar_db()
        self.cliente_mgr = Cliente_manager(conn)
        self.habitacion_mgr = Habitacion_manager(conn)
        self.reserva_mgr = Reserva_manager(conn)

        # Cabecera con arte ASCII
        f = Figlet(font='slant')
        ascii_art = f.renderText("THE DUNE PALACE")
        combined_text = Text(justify="center")
        combined_text.append("🏜️ 🏨 🌅 WELCOME TO THE DUNE PALACE 🌅 🏨 🏜️\n", style="bold yellow")
        combined_text.append(ascii_art, style="bold #DCC7AA")
        self.cabecera_panel = Static(combined_text, id="cabecera_panel")

        # Pantallas que no dependen del cliente
        self.pantalla_cliente = PantallaCliente(self.cliente_mgr, self.reserva_mgr, self.habitacion_mgr)
        self.pantalla_consultar = PantallaConsultar(self.reserva_mgr)

    def on_mount(self):
        # Mostrar pantalla de login al iniciar
        self.push_screen(PantallaLogin(self.cabecera_panel))

    def on_login_success(self, id_cliente: int):
        # Guardar el ID del cliente
        self.id_cliente = id_cliente

        # Crear el menú principal con el cliente logueado
        self.menu_principal = MenuPrincipalScreen(
            self.cliente_mgr,
            self.habitacion_mgr,
            self.reserva_mgr,
            id_cliente=id_cliente  # ✅ Ahora sí puedes pasarlo
        )

        # Mostrar el menú principal
        self.push_screen(self.menu_principal)

    def on_logout(self):
        # Cerrar sesión y mostrar la pantalla de login
        self.id_cliente = None
        self.pop_screen()
        self.push_screen(PantallaLogin(self.cabecera_panel))

if __name__ == "__main__":
    HotelDashboard().run()
