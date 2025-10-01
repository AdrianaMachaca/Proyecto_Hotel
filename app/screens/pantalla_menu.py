from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.screen import Screen
from app.utilidades.generador_pdf import generar_pdf_clientes  # Importa la función para generar PDF
from app.screens.pantalla_mensaje import MensajePantalla

class MenuPrincipalScreen(Screen):
    def __init__(self, cliente_mgr, habitacion_mgr, reserva_mgr):
        super().__init__()
        self.cliente_mgr = cliente_mgr
        self.habitacion_mgr = habitacion_mgr
        self.reserva_mgr = reserva_mgr

    def compose(self) -> ComposeResult:
        # Aquí defines los botones del menú principal
        yield Static("Bienvenido al sistema de reservas")
        yield Button("Registrar cliente", id="menu_cliente")
        yield Button("Crear reserva", id="menu_reserva")
        yield Button("Consultar reservas", id="menu_consultar")
        yield Button("Eliminar reserva", id="menu_eliminar")
        yield Button("Mostrar disponibilidad", id="menu_disponibilidad")
        yield Button("Generar reporte PDF clientes", id="menu_pdf")  # Botón para generar PDF
        yield Button("Salir", id="menu_salir")

    def on_button_pressed(self, event):
        if event.button.id == "menu_cliente":
            self.app.push_screen(self.app.pantalla_cliente)
        elif event.button.id == "menu_reserva":
            self.app.push_screen(self.app.pantalla_reserva)
        elif event.button.id == "menu_consultar":
            self.app.push_screen(self.app.pantalla_consultar)
        elif event.button.id == "menu_eliminar":
            self.app.push_screen(self.app.pantalla_eliminar)
        elif event.button.id == "menu_disponibilidad":
            self.app.push_screen(self.app.pantalla_disponibilidad)
        elif event.button.id == "menu_pdf":
            self.generar_pdf()  # Llama a la función para generar el PDF
        elif event.button.id == "menu_salir":
            self.app.exit()

    def generar_pdf(self):
        try:
            # Obtener los datos de los clientes desde la base de datos
            cursor = self.cliente_mgr.cursor
            cursor.execute("SELECT * FROM Cliente")
            clientes = cursor.fetchall()

            # Llama a la función de generar PDF
            exito, mensaje = generar_pdf_clientes(clientes)

            # Muestra el mensaje según si la operación fue exitosa o no
            if exito:
                self.app.push_screen(MensajePantalla(mensaje))  # Pantalla de mensaje exitosa
            else:
                self.app.push_screen(MensajePantalla(f"Error al generar PDF: {mensaje}"))  # Pantalla de error

        except Exception as e:
            self.app.push_screen(MensajePantalla(f"Error al obtener los datos: {str(e)}"))
