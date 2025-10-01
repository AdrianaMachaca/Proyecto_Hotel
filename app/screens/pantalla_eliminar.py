from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual import events

class PantallaEliminarReserva(Screen):
    def __init__(self, reserva_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr

    def compose(self):
        yield Static("Eliminar Reserva")
        
        # Campo de entrada para ingresar el ID de la reserva a eliminar
        yield Input(placeholder="ID Reserva a eliminar", id="id_reserva_eliminar")
        
        # Botones para eliminar reserva y volver
        yield Button("Eliminar", id="btn_eliminar")
        yield Button("Volver", id="btn_volver_eliminar")

    async def on_button_pressed(self, event):
        if event.button.id == "btn_volver_eliminar":
            self.app.pop_screen()  # Volver a la pantalla anterior
        elif event.button.id == "btn_eliminar":
            try:
                # Obtener el ID de la reserva del campo de entrada
                id_reserva = int(self.query_one("#id_reserva_eliminar", Input).value)
                
                # Llamar al manager para eliminar la reserva
                exito = self.reserva_mgr.eliminar_reserva(id_reserva)
                
                # Mostrar mensaje de éxito o error dependiendo de si se pudo eliminar
                if exito:
                    self.app.push_screen(self.app.mensaje_exito(f"Reserva {id_reserva} eliminada correctamente"))
                else:
                    self.app.push_screen(self.app.mensaje_error(f"No existe la reserva con ID {id_reserva}"))
            except Exception as e:
                # Si ocurre un error, mostrar mensaje de error
                self.app.push_screen(self.app.mensaje_error(f"Error: {str(e)}"))
