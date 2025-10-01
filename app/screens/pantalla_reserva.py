from textual.screen import Screen
from textual.widgets import Input, Button, Static
from textual.containers import Vertical
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Button

class PantallaReserva(Screen):
    def __init__(self, reserva_mgr, id_cliente, habitacion_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr
        self.id_cliente = id_cliente
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(Text("📝 Crear Reserva", style="bold underline green")),
            Input(placeholder="Número de Habitación", id="num_habit"),
            Input(placeholder="Fecha Entrada (YYYY-MM-DD)", id="fecha_entrada"),
            Input(placeholder="Fecha Salida (YYYY-MM-DD)", id="fecha_salida"),
            Input(placeholder="Estado (Confirmada/Pendiente/Cancelada)", id="estado"),
            Input(placeholder="Servicios extras", id="servicios"),
            Input(placeholder="Costo total", id="cuenta"),
            Button("✅ Crear Reserva", id="btn_crear_reserva"),
            Button("🔙 Volver", id="btn_volver_reserva"),
            Static("", id="mensaje_reserva"),  # ✅ Espacio para mensajes
            id="reserva_container"
        )

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_volver_reserva":
            self.app.pop_screen()  # ✅ sin await
        elif event.button.id == "btn_crear_reserva":
            try:
                input_num = self.query_one("#num_habit", Input)
                input_fecha_ent = self.query_one("#fecha_entrada", Input)
                input_fecha_sal = self.query_one("#fecha_salida", Input)
                input_estado = self.query_one("#estado", Input)
                input_serv = self.query_one("#servicios", Input)
                input_cuenta = self.query_one("#cuenta", Input)
            except Exception as e:
                self.mostrar_mensaje(f"Error de interfaz: {str(e)}", estilo="bold red")
                return

            try:
                num_habit = int(input_num.value)
                cuenta = float(input_cuenta.value)
                fecha_entrada = input_fecha_ent.value
                fecha_salida = input_fecha_sal.value
                estado = input_estado.value
                servicios = input_serv.value
            except ValueError as e:
                self.mostrar_mensaje(f"Valores inválidos: {str(e)}", estilo="bold red")
                return

            try:
                self.reserva_mgr.crear_reserva(
                    num_habit,
                    self.id_cliente,
                    fecha_entrada,
                    fecha_salida,
                    estado,
                    servicios,
                    cuenta
                )
            except Exception as e:
                self.mostrar_mensaje(f"Error en lógica de reserva: {str(e)}", estilo="bold red")
                return

            self.mostrar_mensaje("✅ Reserva creada correctamente", estilo="bold green")

    def mostrar_mensaje(self, texto, estilo="bold"):
        mensaje_widget = self.query_one("#mensaje_reserva", Static)
        mensaje_widget.update(Text(texto, style=estilo))
