from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual import events

class PantallaConsultar(Screen):
    def __init__(self, reserva_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr

    def compose(self):
        yield Static("Consultar Reserva")
        
        # Campo de entrada para ingresar el ID de la reserva
        yield Input(placeholder="ID Reserva", id="id_reserva")
        
        # Botones para consultar la reserva y volver
        yield Button("Consultar", id="btn_consultar")
        yield Button("Volver", id="btn_volver_consultar")
        
        # Área para mostrar el resultado de la consulta
        yield Static("", id="resultado_consulta")

    async def on_button_pressed(self, event: events.ButtonPressed):
        if event.button.id == "btn_volver_consultar":
            self.app.pop_screen()  # Volver al menú anterior
        elif event.button.id == "btn_consultar":
            try:
                # Obtener el ID de la reserva del campo de entrada
                id_reserva = int(self.query_one("#id_reserva", Input).value)
                
                # Consultar la reserva
                resultado = self.reserva_mgr.consultar_reservas(id_reserva)
                
                # Mostrar el resultado de la consulta
                self.query_one("#resultado_consulta", Static).update(str(resultado))
            except Exception as e:
                # Si hay un error, mostrar el error
                self.query_one("#resultado_consulta", Static).update(f"Error: {str(e)}")
