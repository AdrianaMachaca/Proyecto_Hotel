from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual import events

class PantallaLogin(Screen):
    def __init__(self, cabecera_panel):
        super().__init__()
        self.cabecera_panel = cabecera_panel

    def compose(self):
        # Mostrar el encabezado primero (puedes personalizarlo según tus necesidades)
        yield self.cabecera_panel
        
        # Mostrar un mensaje estático para el usuario
        yield Static("Ingrese sus credenciales", id="mensaje_credenciales")
        
        # Campos de entrada para el nombre de usuario y contraseña
        yield Input(placeholder="Usuario", id="usuario")
        yield Input(placeholder="Contraseña", id="contrasena", password=True)
        
        # Botón para iniciar sesión
        yield Button("Ingresar", id="btn_ingresar")

    async def on_button_pressed(self, event: events.ButtonPressed):
        if event.button.id == "btn_ingresar":
            # Capturar valores de usuario y contraseña
            usuario = self.query_one("#usuario", Input).value
            contrasena = self.query_one("#contrasena", Input).value
            
            # Validar las credenciales (esto es un ejemplo, puedes hacer la validación contra la base de datos)
            if usuario == "admin" and contrasena == "1234":
                # Si las credenciales son correctas, llevar al menú principal
                self.app.push_screen(self.app.menu_principal)
            else:
                # Si las credenciales son incorrectas, mostrar un mensaje de error
                self.app.push_screen(self.app.mensaje_error("Usuario o contraseña incorrectos"))

