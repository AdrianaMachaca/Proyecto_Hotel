from textual.app import App
from textual.widgets import Header, Footer, Button, Static

class DashboardApp(App):
    def compose(self):
        yield Header()  # Barra superior
        yield Static("Menu lateral", id="left")  # Panel izquierdo
        yield Static("Contenido principal", id="center")  # Panel central
        yield Static("Panel derecho", id="right")  # Panel derecho
        yield Footer()  # Barra inferior (opcional)

DashboardApp().run()