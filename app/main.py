from app import cliente_mgr, reserva_mgr, habitacion_mgr  # Importamos gestores inicializados
from app.screens import PantallaLogin, MenuPrincipalScreen
from textual.app import App
from rich.text import Text
from rich.panel import Panel
from pyfiglet import Figlet
from app.modelos.base import conectar_db


class HotelDashboard(App):
    CSS_PATH = "estilos.tcss"  # Define el archivo de estilos

    def __init__(self):
        super().__init__()
        
        # Configuración del encabezado con un arte ASCII
        f = Figlet(font='slant')
        ascii_art = f.renderText("THE DUNE PALACE")
        combined_text = Text(justify="center")
        combined_text.append("🏜️ 🏨 🌅 WELCOME TO THE DUNE PALACE 🌅 🏨 🏜️\n", style="bold yellow")
        combined_text.append(ascii_art, style="bold #DCC7AA")
        
        # Inicialización de la pantalla de login
        self.cabecera_panel = Panel(combined_text, title="Hotel", padding=(1, 2))
        
        # Inicialización de la pantalla del menú principal
        self.menu_principal = MenuPrincipalScreen(cliente_mgr, habitacion_mgr, reserva_mgr)

    def on_mount(self):
        # Cuando la app se monte, mostramos la pantalla de login primero
        self.push_screen(PantallaLogin(self.cabecera_panel))  # Muestra la pantalla de login con la cabecera

    def on_login_success(self):
        # Lógica para cambiar de la pantalla de login al menú principal
        self.push_screen(self.menu_principal)  # Muestra la pantalla del menú principal después de login


if __name__ == "__main__":
    HotelDashboard().run()  # Ejecutar la app
