from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual import events

class PantallaDisponibilidad(Screen):
    def __init__(self, habitacion_mgr):
        super().__init__()
        self.habitacion_mgr = habitacion_mgr

    def compose(self):
        yield Static("Consultar Disponibilidad")
        
        # Campo de entrada para ingresar el número de la habitación
        yield Input(placeholder="Número de habitación", id="num_habit")
        
        # Botones para consultar disponibilidad y volver
        yield Button("Consultar", id="btn_consultar_disp")
        yield Button("Volver", id="btn_volver_disp")
        
        # Área para mostrar el resultado de la consulta de disponibilidad
        yield Static("", id="resultado_disp")

    async def on_button_pressed(self, event):
        if event.button.id == "btn_volver_disp":
            self.app.pop_screen()  # Volver al menú anterior
        elif event.button.id == "btn_consultar_disp":
            try:
                # Obtener el número de la habitación
                num_habit = int(self.query_one("#num_habit", Input).value)
                
                # Consultar la disponibilidad de la habitación
                resultado = self.habitacion_mgr.Disponibilidad_habitaciones(num_habit)
                
                # Mostrar el resultado de la consulta (disponible/no disponible)
                self.query_one("#resultado_disp", Static).update(str(resultado))
            except Exception as e:
                # Si ocurre un error, mostrar mensaje de error
                self.query_one("#resultado_disp", Static).update(f"Error: {str(e)}")
