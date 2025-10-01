from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Input, Button
from textual.containers import Vertical
from rich.text import Text

from app.screens.pantalla_mensaje import MensajePantalla

class PantallaEliminarReserva(Screen):
    def __init__(self, reserva_mgr):
        super().__init__()
        self.reserva_mgr = reserva_mgr

    def compose(self) -> ComposeResult:
        titulo = Static()
        titulo.update(Text("❌ Eliminar Reserva", style="bold red"))

        yield Vertical(
            titulo,
            Input(placeholder="ID de la reserva a eliminar", id="id_reserva"),
            Button("Eliminar", id="btn_eliminar"),
            Button("Volver", id="btn_volver"),
            id="eliminar_container"
        )

    async def on_button_pressed(self, event: Button.Pressed):
        btn_id = event.button.id
        if btn_id == "btn_volver":
            # Volver atrás
            self.app.pop_screen()
            return

        if btn_id == "btn_eliminar":
            # Intentar obtener el input
            try:
                input_widget = self.query_one("#id_reserva", Input)
                valor = input_widget.value
            except Exception as e:
                # No encontró el input
                self.app.push_screen(MensajePantalla(f"❌ Error de interfaz: {str(e)}"))
                return

            # Intentar convertir a entero
            try:
                id_reserva = int(valor)
            except ValueError:
                self.app.push_screen(MensajePantalla("❌ ID inválido: debe ser un número entero"))
                return

            # Llamar al método para eliminar
            try:
                self.reserva_mgr.eliminar_reserva(id_reserva)
            except Exception as e:
                self.app.push_screen(MensajePantalla(f"❌ Error al eliminar: {str(e)}"))
                return

            # Si todo salió bien
            self.app.push_screen(MensajePantalla("✅ Reserva eliminada correctamente"))
