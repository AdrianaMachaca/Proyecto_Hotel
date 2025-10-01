from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult

class PantallaLogin(Screen):

    def __init__(self, cabecera_panel):
        super().__init__()
        self.cabecera_panel = cabecera_panel

    def compose(self) -> ComposeResult:
        yield self.cabecera_panel
        yield Static("Ingrese sus credenciales", id="mensaje_credenciales")
        yield Input(placeholder="Usuario", id="usuario")
        yield Input(placeholder="Contraseña", id="contrasena", password=True)
        yield Button("Ingresar", id="btn_ingresar")

    async def on_button_pressed(self, event) -> None:
        if event.button.id == "btn_ingresar":
            usuario = self.query_one("#usuario", Input).value
            contrasena = self.query_one("#contrasena", Input).value

            if usuario == "admin" and contrasena == "1234":
                self.app.push_screen(self.app.menu_principal)
            else:
                self.app.push_screen(self.app.mensaje_error("Usuario o contraseña incorrectos"))
