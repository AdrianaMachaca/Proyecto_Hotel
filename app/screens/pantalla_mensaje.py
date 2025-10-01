from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.screen import Screen
from rich.panel import Panel

class MensajePantalla(Screen):
    def __init__(self, mensaje: str):
        super().__init__()
        self.mensaje = mensaje

    def compose(self) -> ComposeResult:
        yield Static(Panel(self.mensaje))
        yield Button("Volver al menú principal", id="btn_menu")

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_menu":
            self.app.push_screen(self.app.menu_principal)
