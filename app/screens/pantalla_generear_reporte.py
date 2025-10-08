from textual.screen import Screen
from textual.widgets import Static, Button
from textual.app import ComposeResult
from textual import on

from app.utilidades.generador_pdf import generar_pdf_clientes
from app.screens.pantalla_mensaje import MensajePantalla

class PantallaGenerarReporte(Screen):
    def __init__(self, cliente_mgr):
        super().__init__()
        self.cliente_mgr = cliente_mgr

    def compose(self) -> ComposeResult:
        yield Static("📄 Generar Reporte de Clientes")
        yield Button("Generar PDF", id="btn_generar_pdf")
        yield Button("Volver", id="btn_volver_reporte")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_volver_reporte":
            self.app.pop_screen()
        elif event.button.id == "btn_generar_pdf":
            try:
                clientes = self.cliente_mgr.obtener_todos_los_clientes()
                generar_pdf_clientes(clientes)
                self.app.push_screen(MensajePantalla("✅ Reporte PDF generado correctamente"))
            except Exception as e:
                self.app.push_screen(MensajePantalla(f"❌ Error al generar PDF: {str(e)}"))
