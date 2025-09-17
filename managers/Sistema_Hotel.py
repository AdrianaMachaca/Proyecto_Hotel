import sqlite3
from base import conectar_db
from cliente import Clientes
from habitacion import Habitacion
from reserva import Reserva

class Sistema_Hotel:
    def registrar_cliente(self, nombre, apellido, telefono, correo):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo)
            VALUES (?, ?, ?, ?)
        """, (nombre, apellido, telefono, correo))
        conn.commit()
        # Obtener el ID generado 
        #lastrowid genera el id de manera automatica
        id_generado = cursor.lastrowid
        conn.close()
        print(f"Cliente registrado con éxito. ID asignado: {id_generado}")
        return id_generado

    def crear_reserva(self, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo):
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Cliente WHERE idCliente = ?", (idCliente,))
        cliente = cursor.fetchone()
        if not cliente:
            print("Cliente no registrado.")
            conn.close()
            return

        cursor.execute("""
            SELECT * FROM Reserva
            WHERE numHabit = ? AND (
                (fechaEntrada <= ? AND fechaSalida >= ?) OR
                (fechaEntrada <= ? AND fechaSalida >= ?)
            )
        """, (numHabit, fechaEntrada, fechaEntrada, fechaSalida, fechaSalida))
        if cursor.fetchone():
            print("La habitación no está disponible en ese rango de tiempo.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO Reserva (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, serviciosExtras, costo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo))
        conn.commit()
        id_generado = cursor.lastrowid
        conn.close()
        print(f"Reserva creada con éxito. ID asignado: {id_generado}")

    def consultar_reservas(self,idReserva):
        conn = conectar_db() 
        cursor = conn.cursor() 
        cursor.execute(""" 
            SELECT * FROM Reserva WHERE idReserva = ? """,(idReserva,)) 
        reserva = conn.fetchone() 
        if reserva: 
            fil = Reserva(*reserva) 
            fil.mostrar_reserva() 
        else: 
            print("Reserva no encontrada") 
        conn.close()
        
    def eliminar_reserva(self, idReserva):
        conn = conectar_db()
        cursor =  conn.cursor()
        cursor.execute("""
            SELECT * FROM Reserva 
            WHERE idReserva = ?
        """,(idReserva,))
        reserva = conn.fetchone()
        if reserva :
            cursor.execute("DELETE FROM Reserva WHERE idReserva = ?", (idReserva,))
            conn.commit()
            print("Reserva eliminada con éxito.")
        else:
            print("Reserva no encontrada")
        conn.close()

    def Disponibilidad_habitaciones(self, numHabitacion):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Reserva
            WHERE numHabit = ?
        """,(numHabitacion,))
        disponible = cursor.fetchone()
        if disponible:
            print("Habitacion no esta disponible")
        else:
            print("Habitacion esta disponible")

def menu():
    sistema = Sistema_Hotel()

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrar cliente")
        print("2. Crear reserva")
        print("3. Consultar reservas")
        print("4. Eliminar reserva")
        print("5. Mostrar disponibilidad")
        print("6. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Entrada inválida. Debe ser un número.")
            continue

        match opcion:
            case 1:
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                telefono = input("Teléfono: ")
                correo = input("Correo: ")
                idCliente = sistema.registrar_cliente(nombre, apellido, telefono, correo)

                crear = input("¿Desea crear una reserva para este cliente ahora? (s/n): ")
                if crear.lower() == "s":
                    numHabit = int(input("Número de habitación: "))
                    fechaEntrada = input("Fecha de entrada (YYYY-MM-DD): ")
                    fechaSalida = input("Fecha de salida (YYYY-MM-DD): ")
                    estado = input("Estado (Confirmada/Pendiente/Cancelada): ")
                    servicios = input("Servicios extras: ")
                    cuenta = float(input("Costo total: "))
                    sistema.crear_reserva(numHabit, idCliente, fechaEntrada, fechaSalida, estado, servicios, cuenta)

            case 2:
                idCliente = int(input("ID del cliente: "))
                numHabit = int(input("Número de habitación: "))
                fechaEntrada = input("Fecha de entrada (YYYY-MM-DD): ")
                fechaSalida = input("Fecha de salida (YYYY-MM-DD): ")
                estado = input("Estado (Confirmada/Pendiente/Cancelada): ")
                servicios = input("Servicios extras: ")
                cuenta = float(input("Costo total: "))
                sistema.crear_reserva(numHabit, idCliente, fechaEntrada, fechaSalida, estado, servicios, cuenta)

            case 3:
                idReserva = int(input("ID de la reserva a consultar: "))
                sistema.consultar_reservas(idReserva)

            case 4:
                idReserva = int(input("ID de la reserva a eliminar: "))
                sistema.eliminar_reserva(idReserva)

            case 5:
                numHabit = int(input("Número de habitación a consultar: "))
                sistema.Disponibilidad_habitaciones(numHabit)
            case 6:
                print("Saliendo del sistema.")
                break

            case _:
                print("Opción inválida.")


if __name__ == "__main__":
    menu()
