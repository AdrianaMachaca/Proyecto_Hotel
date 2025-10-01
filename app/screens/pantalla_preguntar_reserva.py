from textual.screen import Screen
from textual.widgets import Static, Button
from textual import events
from app.screens.pantalla_reserva import PantallaReserva

class PreguntarReserva(Screen):
    def __init__(self, id_cliente, reserva_mgr, habitacion_mgr):
        super().__init__()
        self.id_cliente = id_cliente
        self.reserva_mgr = reserva_mgr
        self.habitacion_mgr = habitacion_mgr

    def compose(self):
        # Mostrar mensaje al usuario
        yield Static(f"Cliente {self.id_cliente} registrado. ¿Desea crear una reserva ahora?")
        
        # Botones para sí/no
        yield Button("Sí", id="btn_si")
        yield Button("No", id="btn_no")

    async def on_button_pressed(self, event):
        if event.button.id == "btn_si":
            # Si elige sí, ir a la pantalla de crear reserva
            self.app.push_screen(PantallaReserva(self.reserva_mgr, self.id_cliente, self.habitacion_mgr))
        elif event.button.id == "btn_no":
            # Si elige no, volver al menú principal
            self.app.push_screen(self.app.menu_principal)
