from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.message import Message
from textual import on

from app.screens.pantalla_reserva import PantallaReserva

class PreguntarReserva(Screen):
    def __init__(self, id_cliente, reserva_mgr, habitacion_mgr):
        super().__init__()
        self.id_cliente = id_cliente
        self.reserva_mgr = reserva_mgr
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        # Mostrar mensaje al usuario
        yield Static(f"Cliente {self.id_cliente} registrado. ¿Desea crear una reserva ahora?")
        
        # Botones para sí/no
        yield Vertical(
            Button("Sí", id="btn_si"),
            Button("No", id="btn_no")
        )

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_si":
            self.app.push_screen(PantallaReserva(self.reserva_mgr, self.id_cliente, self.habitacion_mgr))
        elif event.button.id == "btn_no":
            self.app.push_screen(self.app.menu_principal)
