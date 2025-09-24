from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Input
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from textual.screen import Screen


# ------------------ Pantalla de registro ------------------
class PantallaRegistro(Screen):
    def compose(self) -> ComposeResult:
        # Contenedor horizontal para usuario y contraseña
        yield Horizontal(
            Vertical(
                Static(Panel("Usuario", title="Nombre de usuario")),
                Input(placeholder="Ingresa tu usuario", id="usuario"),
                id="panel_usuario"
            ),
            Vertical(
                Static(Panel("Contraseña", title="Contraseña")),
                Input(placeholder="Ingresa tu contraseña", password=True, id="contrasena"),
                id="panel_contrasena"
            ),
            id="contenedor_campos"
        )

        # Botones
        yield Horizontal(
            Button("Iniciar sesión", id="btn_iniciar"),
            Button("Volver", id="btn_volver"),
            id="botones_registro"
        )

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver":
            self.app.pop_screen()
        elif event.button.id == "btn_iniciar":
            usuario = self.query_one("#usuario", Input).value
            contrasena = self.query_one("#contrasena", Input).value
            self.app.push_screen(MensajePantalla(f"Hola {usuario}, intentaste iniciar sesión"))


# ------------------ Pantalla de mensaje ------------------
class MensajePantalla(Screen):
    def __init__(self, mensaje: str):
        super().__init__()
        self.mensaje = mensaje

    def compose(self) -> ComposeResult:
        yield Static(self.mensaje)
        yield Button("Volver", id="btn_volver")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver":
            self.app.pop_screen()


# ------------------ Pantalla principal ------------------
class HotelDashboard(App):
    CSS_PATH = None

    def __init__(self):
        super().__init__()
        # Crear arte ASCII solo una vez
        f = Figlet(font='slant')
        self.ascii_art = f.renderText("THE DUNE PALACE")

        # Cabecera
        combined_text = Text(justify="center")
        combined_text.append("🏜️ 🏨 🌅 WELCOME TO THE DUNE PALACE 🌅 🏨 🏜️\n", style="bold yellow")
        combined_text.append(self.ascii_art, style="bold #DCC7AA")
        self.cabecera_panel = Panel(combined_text, title="Registro", style="white on blue")

        # Panel de registro
        self.registro_panel = Panel(Text("Panel de registro", justify="center"), title="Registrarse", style="black on #F5F5DC")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Contenedor principal: cabecera y registro lado a lado
        yield Container(
            Horizontal(
                Vertical(
                    Static(self.cabecera_panel),
                    id="panel_cabecera"
                ),
                Vertical(
                    Static(self.registro_panel),
                    Button("Ir a pantalla de registro", id="btn_siguiente"),
                    id="panel_registro"
                ),
                id="main_panel"
            )
        )

        yield Footer()

    def on_button_pressed(self, event):
        if event.button.id == "btn_siguiente":
            self.push_screen(PantallaRegistro())


# ------------------ Ejecutar app ------------------
if __name__ == "__main__":
    HotelDashboard().run()
