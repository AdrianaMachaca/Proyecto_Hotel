from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Static
from textual.containers import Vertical
from rich.text import Text

from app.utilidades.generador_pdf import generar_pdf_clientes
from app.screens.pantalla_mensaje import MensajePantalla
from app.screens.pantalla_reserva import PantallaReserva
from app.screens.pantalla_eliminar import PantallaEliminarReserva
from app.screens.pantalla_disponibilidad import PantallaDisponibilidad

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Static
from textual.containers import Vertical
from rich.text import Text

class MenuPrincipalScreen(Screen):
    def __init__(self, cliente_mgr, habitacion_mgr, reserva_mgr,id_cliente):
        super().__init__()
        self.cliente_mgr = cliente_mgr
        self.habitacion_mgr = habitacion_mgr
        self.reserva_mgr = reserva_mgr
        self.id_cliente = id_cliente

    def compose(self) -> ComposeResult:
        titulo = Static()
        titulo.update(Text("📋 Bienvenido al sistema de reservas", style="bold white on dark_blue"))

        # Aquí los botones con texto coloreado usando Text
        yield Vertical(
            titulo,
            Button(Text("👤 Registrar cliente", style="bold white"), id="menu_cliente"),
            Button(Text("🛏️ Crear reserva", style="bold black"), id="menu_reserva"),
            Button(Text("🔍 Consultar reservas", style="bold black"), id="menu_consultar"),
            Button(Text("❌ Eliminar reserva", style="bold white"), id="menu_eliminar"),
            Button(Text("📆 Mostrar disponibilidad", style="bold white"), id="menu_disponibilidad"),
            Button(Text("📄 Generar reporte PDF clientes", style="bold white"), id="menu_pdf"),
            Button(Text("🚪 Salir", style="bold white"), id="menu_salir"),
            id="menu_container"
        )

    # resto del código...


    async def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "menu_cliente":
                self.app.push_screen(self.app.pantalla_cliente)

            case "menu_reserva":
                reserva_screen = PantallaReserva(
                    self.reserva_mgr,
                    self.id_cliente,
                    self.habitacion_mgr
                )

                self.app.push_screen(reserva_screen)

            case "menu_consultar":
                self.app.push_screen(self.app.pantalla_consultar)

            case "menu_eliminar":
                eliminar_screen = PantallaEliminarReserva(self.app.reserva_mgr)
                self.app.push_screen(eliminar_screen)

            case "menu_disponibilidad":
                disponibilidad_screen = PantallaDisponibilidad(self.app.habitacion_mgr)
                self.app.push_screen(disponibilidad_screen)

            case "menu_pdf":
                self.generar_pdf()

            case "menu_salir":
                self.app.exit()

    def generar_pdf(self):
        try:
            cursor = self.cliente_mgr.cursor
            cursor.execute("SELECT * FROM Cliente")
            clientes = cursor.fetchall()

            exito, mensaje = generar_pdf_clientes(clientes)

            pantalla_mensaje = MensajePantalla(
                mensaje if exito else f"❌ Error al generar PDF: {mensaje}"
            )
            self.app.push_screen(pantalla_mensaje)

        except Exception as e:
            self.app.push_screen(MensajePantalla(f"❌ Error al obtener los datos: {str(e)}"))
