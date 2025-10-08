from app.managers.cliente_manager import Cliente_manager
from app.managers.habitacion_manager import Habitacion_manager
from app.managers.reserva_manager import Reserva_manager

from app.screens.pantalla_login import PantallaLogin
from app.screens.pantalla_menu import MenuPrincipalScreen
from textual.app import App
from rich.text import Text
from rich.panel import Panel
from pyfiglet import Figlet
from textual.widgets import Static, Button
from app.modelos.base import conectar_db


class HotelDashboard(App):
    CSS_PATH = "estilos.tcss"  # Define el archivo de estilos

    def __init__(self):
        super().__init__()

        # Conexión a la base de datos
        conn = conectar_db()
        self.cliente_mgr = Cliente_manager(conn)
        self.habitacion_mgr = Habitacion_manager(conn)
        self.reserva_mgr = Reserva_manager(conn)

        # Configuración del encabezado con arte ASCII
        f = Figlet(font='slant')
        ascii_art = f.renderText("THE DUNE PALACE")
        combined_text = Text(justify="center")
        combined_text.append("🏜️ 🏨 🌅 WELCOME TO THE DUNE PALACE 🌅 🏨 🏜️\n", style="bold yellow")
        combined_text.append(ascii_art, style="bold #DCC7AA")
        self.cabecera_panel = Static(combined_text, id="cabecera_panel")

        # Pantalla principal
        self.menu_principal = MenuPrincipalScreen(self.cliente_mgr, self.habitacion_mgr, self.reserva_mgr)


    def on_mount(self):
        # Cuando la app se monte, mostramos la pantalla de login primero
        self.push_screen(PantallaLogin(self.cabecera_panel))  # Muestra la pantalla de login con la cabecera

    def on_login_success(self):
        # Lógica para cambiar de la pantalla de login al menú principal
        self.push_screen(self.menu_principal)  # Muestra la pantalla del menú principal después de login


if __name__ == "__main__":
    HotelDashboard().run()  # Ejecutar la app
