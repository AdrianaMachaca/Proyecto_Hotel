import sqlite3
import csv
from fpdf import FPDF
from tabulate import tabulate
from app.modelos.base import conectar_db
from app.managers.cliente_manager import Cliente_manager
from app.managers.habitacion_manager import Habitacion_manager
from app.managers.reserva_manager import Reserva_manager


# ---------------- UTILIDADES ----------------
def leer_numero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("⚠️ Debes ingresar un numero valido.")


# ---------------- CLASE CONSOLA ----------------
class Consola:
    def __init__(self):
        self.conn = conectar_db()
        self.clientes = Cliente_manager(self.conn)
        self.habitaciones = Habitacion_manager(self.conn)
        self.reservas = Reserva_manager(self.conn)

    # ---------------- LOGIN ----------------
    def registrar_usuario(self):
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Usuario (nombreUsuario, contrasena) VALUES (?, ?)",
                (usuario, contrasena)
            )
            self.conn.commit()
            print("✅ Usuario registrado correctamente")
        except sqlite3.IntegrityError:
            print("❌ El usuario ya existe")

    def login(self):
        print("\n===== 🔐 LOGIN =====")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM Usuario WHERE username = ? AND password = ?",
            (usuario, contrasena)
        )
        datos = cursor.fetchone()

        if datos:
            print(f"✅ Bienvenido, {usuario}!")
            return True
        else:
            print("❌ Usuario o contraseña incorrectos")
            return False

    # ---------------- MENU PRINCIPAL ----------------
    def mostrar_menu(self):
        while True:
            print("\n===== 🏨 MENU PRINCIPAL =====")
            print("1️⃣ Gestionar Clientes")
            print("2️⃣ Gestionar Habitaciones")
            print("3️⃣ Gestionar Reservas")
            print("4️⃣ Salir")

            opcion = leer_numero("Elige una opcion: ")

            if opcion == 1:
                self.menu_clientes()
            elif opcion == 2:
                self.menu_habitaciones()
            elif opcion == 3:
                self.menu_reservas()
            elif opcion == 4:
                print("👋 Saliendo del sistema...")
                break
            else:
                print("❌ Opcion invalida.")

    # ---------------- MENU CLIENTES ----------------
    def menu_clientes(self):
        while True:
            print("\n--- 👤 MENU CLIENTES ---")
            print("1️⃣ Registrar cliente")
            print("2️⃣ Listar clientes")
            print("3️⃣ Buscar cliente por ID")
            print("4️⃣ Eliminar cliente")
            print("5️⃣ Exportar clientes a CSV")
            print("6️⃣ Generar PDF de clientes")  
            print("7️⃣ Volver al menu principal")

            opcion = leer_numero("Elige una opcion: ")

            if opcion == 1:
                self.registrar_cliente()
            elif opcion == 2:
                self.listar_clientes()
            elif opcion == 3:
                self.buscar_cliente()
            elif opcion == 4:
                self.eliminar_cliente()
            elif opcion == 5:
                self.exportar_clientes_csv()
            elif opcion == 6:
                self.generar_pdf_clientes_menu()
            elif opcion == 7:    
                break
            else:
                print("❌ Opcion invalida.")

    # ---------------- MENU HABITACIONES ----------------
    def menu_habitaciones(self):
        while True:
            print("\n--- 🛏️ MENU HABITACIONES ---")
            print("1️⃣ Crear habitacion")
            print("2️⃣ Consultar disponibilidad")
            print("3️⃣ Listar habitaciones")
            print("4️⃣ Generar PDF de habitaciones") 
            print("5️⃣ Volver al menu principal")

            opcion = leer_numero("Elige una opcion: ")

            if opcion == 1:
                self.crear_habitacion()
            elif opcion == 2:
                self.ver_disponibilidad()
            elif opcion == 3:
                self.ver_habitaciones()
            elif opcion == 4:
                self.generar_pdf_habitaciones_menu()
            elif opcion == 5:
                break
            else:
                print("❌ Opcion invalida.")

    # ---------------- MENU RESERVAS ----------------
    def menu_reservas(self):
        while True:
            print("\n--- 📋 MENU RESERVAS ---")
            print("1️⃣ Crear reserva")
            print("2️⃣ Listar reservas activas")
            print("3️⃣ Consultar reserva por ID")
            print("4️⃣ Cancelar reserva")
            print("5️⃣ Ver historial de reservas")
            print("6️⃣ Listar reservas canceladas")
            print("7️⃣ Exportar reservas a CSV")
            print("8️⃣ Generar PDF de reservas") 
            print("9️⃣ Volver al menu principal")

            opcion = leer_numero("Elige una opcion: ")

            if opcion == 1:
                self.crear_reserva()
            elif opcion == 2:
                self.listar_reservas_activas()
            elif opcion == 3:
                self.consultar_reserva()
            elif opcion == 4:
                self.eliminar_reserva()
            elif opcion == 5:
                self.listar_historial_reservas()
            elif opcion == 6:
                self.listar_reservas_canceladas()
            elif opcion == 7:
                self.exportar_reservas_csv()
            elif opcion == 8:
                self.generar_pdf_reservas_menu()
            elif opcion == 9:
                break
            else:
                print("❌ Opcion invalida.")

    # ---------------- MÉTODOS CLIENTES ----------------
    def registrar_cliente(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        telefono = input("Telefono: ")
        correo = input("Correo: ")
        id_cliente = self.clientes.registrar_cliente(nombre, apellido, telefono, correo)
        if id_cliente:
            print(f"✅ Cliente registrado correctamente con ID {id_cliente}")
        else:
            print("❌ Error al registrar cliente.")

    def listar_clientes(self):
        clientes = self.clientes.listar_Clientes()
        self.clientes.mostrar_tabla_clientes(clientes)

    def buscar_cliente(self):
        id_cliente = leer_numero("Ingrese el ID del cliente: ")
        cliente = self.clientes.buscar_Clientes(id_cliente)
        if cliente:
            print(f"\n👤 Cliente encontrado:")
            print(f"ID: {cliente.idCliente}")
            print(f"Nombre: {cliente.Nombre} {cliente.Apellido}")
            print(f"Telefono: {cliente.Telefono}")
            print(f"Correo: {cliente.Correo}")
        else:
            print("❌ Cliente no encontrado.")

    def eliminar_cliente(self):
        id_cliente = leer_numero("ID del cliente a eliminar: ")
        confirm = input("⚠️ Seguro que quieres eliminar este cliente? (s/n): ").lower()
        if confirm == "s":
            resultado = self.clientes.eliminar_cliente(id_cliente)
            if resultado:
                print(f"✅ Cliente con ID {id_cliente} eliminado correctamente.")
            else:
                print("❌ No se pudo eliminar el cliente.")
        else:
            print("❌ Eliminacion cancelada.")

    def exportar_clientes_csv(self):
        clientes = self.clientes.listar_Clientes()
        if clientes:
            datos = [(c.idCliente, c.Nombre, c.Apellido, c.Telefono, c.Correo) for c in clientes]
            encabezados = ["ID", "Nombre", "Apellido", "Telefono", "Correo"]
            self.exportar_csv(datos, encabezados, "clientes.csv")
        else:
            print("❌ No hay clientes para exportar")

    # ---------------- MÉTODOS HABITACIONES ----------------
    def crear_habitacion(self):
        try:
            num = input("Numero de habitacion: ")
            tipo = input("Tipo: ")
            estado = input("Estado: ")
            precio = float(input("Precio: "))
            capacidad = leer_numero("Capacidad: ")
            servicios = input("Servicios: ")
            observ = input("Observaciones: ")
            self.habitaciones.crear_habitacion(num, tipo, estado, precio, capacidad, servicios, observ)
            print("✅ Habitacion creada correctamente.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_habitaciones(self):
        habitaciones = self.habitaciones.listar_habitaciones()
        if habitaciones:
            tabla = [[h[0], h[1], h[2], h[3], h[4], h[5], h[6]] for h in habitaciones]
            headers = ["Numero", "Tipo", "Estado", "Precio", "Capacidad", "Servicios", "Observaciones"]
            print(tabulate(tabla, headers=headers, tablefmt="grid"))
        else:
            print("❌ No hay habitaciones registradas.")

    def ver_disponibilidad(self):
        num = input("Numero de habitacion: ")
        print(self.habitaciones.disponibilidad_habitaciones(num))

    # ---------------- MÉTODOS RESERVAS ----------------
    def crear_reserva(self):
        try:
            numHabit = input("Numero de habitacion: ")
            idCliente = leer_numero("ID del cliente: ")
            fechaEntrada = input("Fecha de entrada (YYYY-MM-DD): ")
            fechaSalida = input("Fecha de salida (YYYY-MM-DD): ")
            estado = input("Estado de la reserva: ")
            servicios = input("Servicios extras: ")
            costo = float(input("Costo total: "))
            self.reservas.crear_reserva(numHabit, idCliente, fechaEntrada, fechaSalida, estado, servicios, costo)
        except Exception as e:
            print(f"❌ Error: {e}")

    def mostrar_reservas_tabla(self, reservas, titulo="Reservas"):
        if reservas:
            tabla = [[
                r.idReserva,
                r.numHabit,
                r.idCliente,
                r.fechaEntrada,
                r.fechaSalida,
                r.estadoReserva,
                r.serviciosExtras,
                r.costo
            ] for r in reservas]
            headers = ["ID", "Habitacion", "Cliente", "Entrada", "Salida", "Estado", "Servicios", "Costo"]
            print(f"\n--- 📋 {titulo} ---")
            print(tabulate(tabla, headers=headers, tablefmt="grid"))
        else:
            print(f"❌ No hay {titulo.lower()}.")


    def listar_reservas_activas(self):
        reservas = self.reservas.listar_reservas_activas()
        self.mostrar_reservas_tabla(reservas, "Reservas Activas")

    def listar_reservas_canceladas(self):
        reservas = self.reservas.listar_reservas_canceladas()
        self.mostrar_reservas_tabla(reservas, "Reservas Canceladas")

    def listar_historial_reservas(self):
        reservas = self.reservas.listar_reservas_historial()
        self.mostrar_reservas_tabla(reservas, "Historial de Reservas")

    def consultar_reserva(self):
        idReserva = leer_numero("ID de la reserva: ")
        reserva = self.reservas.consultar_reservas(idReserva)
        if reserva:
            print("\n--- 🧾 DATOS DE LA RESERVA ---")
            print(f"ID: {reserva.idReserva}")
            print(f"Habitacion: {reserva.numHabit}")
            print(f"Cliente: {reserva.idCliente}")
            print(f"Fecha entrada: {reserva.fechaEntrada}")
            print(f"Fecha salida: {reserva.fechaSalida}")
            print(f"Estado: {reserva.estadoReserva}")
            print(f"Servicios extras: {reserva.serviciosExtras}")
            print(f"Costo: {reserva.costo}")
            print("-----------------------------\n")
        else:
            print("❌ No se encontro ninguna reserva con ese ID.")


    def eliminar_reserva(self):
        idReserva = leer_numero("ID de la reserva a cancelar: ")
        self.reservas.eliminar_reserva(idReserva)

    def exportar_reservas_csv(self):
        reservas = self.reservas.listar_reservas_historial()
        if reservas:
            datos = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in reservas]
            encabezados = ["ID", "Habitacion", "Cliente", "Entrada", "Salida", "Estado", "Servicios", "Costo"]
            self.exportar_csv(datos, encabezados, "reservas.csv")
        else:
            print("❌ No hay reservas para exportar")

    # ---------------- GENERAR PDF ----------------
    def generar_pdf_clientes_menu(self):
        clientes = self.clientes.listar_Clientes()
        if clientes:
            clientes_tuplas = [(c.idCliente, c.Nombre, c.Apellido, c.Telefono, c.Correo) for c in clientes]
            from app.utilidades.generador_pdf import generar_pdf_clientes
            generar_pdf_clientes(clientes_tuplas)
            print("📄 PDF generado con exito: reporte_clientes.pdf")
        else:
            print("❌ No hay clientes para generar PDF.")

    def generar_pdf_habitaciones_menu(self):
        habitaciones = self.habitaciones.listar_habitaciones()
        if habitaciones:
            habitaciones_tuplas = [tuple(h) for h in habitaciones]
            from app.utilidades.generador_pdf import generar_pdf_habitaciones
            generar_pdf_habitaciones(habitaciones_tuplas)
            print("📄 PDF generado con exito: reporte_habitaciones.pdf")
        else:
            print("❌ No hay habitaciones para generar PDF.")

    def generar_pdf_reservas_menu(self):
        reservas = self.reservas.listar_reservas_historial()
        if reservas:
            reservas_tuplas = [
                (
                    r.idReserva,
                    r.numHabit,
                    r.idCliente,
                    r.fechaEntrada,
                    r.fechaSalida,
                    r.estadoReserva,
                    r.serviciosExtras,
                    r.costo
                )
                for r in reservas
            ]
            from app.utilidades.generador_pdf import generar_pdf_reservas
            generar_pdf_reservas(reservas_tuplas)
            print("📄 PDF generado con exito: reporte_reservas.pdf")
        else:
            print("❌ No hay reservas para generar PDF.")


    # ---------------- EXPORTAR CSV GENERAL ----------------
    def exportar_csv(self, datos, encabezados, nombre_archivo):
        if datos:
            with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(encabezados)
                writer.writerows(datos)
            print(f"✅ Datos exportados a {nombre_archivo}")
        else:
            print("❌ No hay datos para exportar")


# ---------------- EJECUCIÓN PRINCIPAL ----------------
if __name__ == "__main__":
    app = Consola()
    if app.login():
        app.mostrar_menu()
