from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual import events
from app.screens.pantalla_preguntar_reserva import PreguntarReserva

class PantallaCliente(Screen):
    def __init__(self, cliente_mgr, reserva_mgr, habitacion_mgr):
        super().__init__()
        self.cliente_mgr = cliente_mgr
        self.reserva_mgr = reserva_mgr
        self.habitacion_mgr = habitacion_mgr

    def compose(self):
        # Mostrar el encabezado de la pantalla
        yield Static("Registrar Cliente")
        
        # Campos de entrada para registrar un nuevo cliente
        yield Input(placeholder="Nombre", id="nombre")
        yield Input(placeholder="Apellido", id="apellido")
        yield Input(placeholder="Teléfono", id="telefono")
        yield Input(placeholder="Correo", id="correo")
        
        # Botón para registrar cliente
        yield Button("Registrar", id="btn_registrar")
        yield Button("Volver", id="btn_volver_cliente")

    async def on_button_pressed(self, event):
        if event.button.id == "btn_volver_cliente":
            self.app.pop_screen()  # Volver al menú anterior
        elif event.button.id == "btn_registrar":
            try:
                # Obtener los valores de los campos de entrada
                nombre = self.query_one("#nombre", Input).value
                apellido = self.query_one("#apellido", Input).value
                telefono = self.query_one("#telefono", Input).value
                correo = self.query_one("#correo", Input).value

                # Llamar a la función del manager para registrar el cliente
                id_cliente = self.cliente_mgr.registrar_cliente(nombre, apellido, telefono, correo)

                # Preguntar al usuario si quiere crear una reserva
                self.app.push_screen(PreguntarReserva(id_cliente, self.reserva_mgr, self.habitacion_mgr))
            except Exception as e:
                # Si hay un error, mostrar mensaje de error
                self.app.push_screen(self.app.mensaje_error(f"Error al registrar cliente: {str(e)}"))
