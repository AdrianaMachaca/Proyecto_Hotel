from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual import events

class PantallaReserva(Screen):
    def __init__(self, reserva_mgr, id_cliente, habitacion_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr
        self.id_cliente = id_cliente
        self.habitacion_mgr = habitacion_mgr

    def compose(self):
        yield Static("Crear Reserva")
        
        # Campos de entrada para crear una reserva
        yield Input(placeholder="Número de Habitación", id="num_habit")
        yield Input(placeholder="Fecha Entrada (YYYY-MM-DD)", id="fecha_entrada")
        yield Input(placeholder="Fecha Salida (YYYY-MM-DD)", id="fecha_salida")
        yield Input(placeholder="Estado (Confirmada/Pendiente/Cancelada)", id="estado")
        yield Input(placeholder="Servicios extras", id="servicios")
        yield Input(placeholder="Costo total", id="cuenta")
        
        # Botones para crear reserva y volver
        yield Button("Crear Reserva", id="btn_crear_reserva")
        yield Button("Volver", id="btn_volver_reserva")

    async def on_button_pressed(self, event):
        if event.button.id == "btn_volver_reserva":
            self.app.pop_screen()  # Regresar a la pantalla anterior
        elif event.button.id == "btn_crear_reserva":
            try:
                # Obtener valores de los campos de entrada
                num_habit = int(self.query_one("#num_habit", Input).value)
                fecha_entrada = self.query_one("#fecha_entrada", Input).value
                fecha_salida = self.query_one("#fecha_salida", Input).value
                estado = self.query_one("#estado", Input).value
                servicios = self.query_one("#servicios", Input).value
                cuenta = float(self.query_one("#cuenta", Input).value)

                # Crear la reserva
                self.reserva_mgr.crear_reserva(num_habit, self.id_cliente, fecha_entrada, fecha_salida, estado, servicios, cuenta)

                # Mostrar mensaje de éxito
                self.app.push_screen(self.app.mensaje_exito("Reserva creada correctamente"))
            except Exception as e:
                # Si ocurre un error, mostrar mensaje de error
                self.app.push_screen(self.app.mensaje_error(f"Error: {str(e)}"))
