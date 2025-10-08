from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical
from textual.app import ComposeResult
from textual import on

class PantallaDisponibilidad(Screen):
    def __init__(self, habitacion_mgr):
        super().__init__()
        self.habitacion_mgr = habitacion_mgr

    def compose(self) -> ComposeResult:
        yield Static("Consultar Disponibilidad")

        yield Vertical(
            Input(placeholder="Número de habitación", id="num_habit"),
            Button("Consultar", id="btn_consultar_disp"),
            Button("Volver", id="btn_volver_disp"),
            Static("", id="resultado_disp")
        )

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_volver_disp":
            self.app.pop_screen()
        elif event.button.id == "btn_consultar_disp":
            try:
                num_habit = int(self.query_one("#num_habit", Input).value)
                resultado = self.habitacion_mgr.Disponibilidad_habitaciones(num_habit)
                self.query_one("#resultado_disp", Static).update(str(resultado))
            except Exception as e:
                self.query_one("#resultado_disp", Static).update(f"Error: {str(e)}")
