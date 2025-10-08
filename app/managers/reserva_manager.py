import sqlite3
from tabulate import tabulate
from app.modelos.base import conectar_db
from app.modelos.reserva import Reserva

class Reserva_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def crear_reserva(self, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo):
        try:
            self.cursor.execute("SELECT * FROM Cliente WHERE idCliente = ?", (idCliente,))
            if not self.cursor.fetchone():
                print("Cliente no registrado.")
                return None

            self.cursor.execute("""
                SELECT * FROM Reserva
                WHERE numHabit = ?
                AND NOT (fechaSalida < ? OR fechaEntrada > ?)
            """, (numHabit, fechaEntrada, fechaSalida))

            if self.cursor.fetchone():
                print("La habitación no está disponible en ese rango de tiempo.")
                return None

            self.cursor.execute("""
                INSERT INTO Reserva (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, serviciosExtras, costo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo))
            self.conn.commit()
            print(f"Reserva creada con éxito. ID asignado: {self.cursor.lastrowid}")
            return self.cursor.lastrowid

        except sqlite3.Error as e:
            print(f"Error al crear reserva: {e}")
            return None

    def listar_reservas_activas(self):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE estadoReserva != 'cancelada'")
            filas = self.cursor.fetchall()
            return filas
        except sqlite3.Error as e:
            print(f"Error al listar reservas activas: {e}")
            return []

    def listar_reservas_canceladas(self):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE estadoReserva = 'cancelada'")
            filas = self.cursor.fetchall()
            return filas
        except sqlite3.Error as e:
            print(f"Error al listar reservas canceladas: {e}")
            return []

    def listar_reservas_historial(self):
        try:
            self.cursor.execute("SELECT * FROM Reserva")
            filas = self.cursor.fetchall()
            return filas
        except sqlite3.Error as e:
            print(f"Error al listar historial de reservas: {e}")
            return []

    def consultar_reservas(self, idReserva):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE idReserva = ?", (idReserva,))
            reserva = self.cursor.fetchone()
            if reserva:
                return f"""
                ID Reserva: {reserva[0]}
                Numero Habitacion: {reserva[1]}
                ID Cliente: {reserva[2]}
                Fecha Entrada: {reserva[3]}
                Fecha Salida: {reserva[4]}
                Estado: {reserva[5]}
                Servicios: {reserva[6]}
                Costo: {reserva[7]}
                """
            else:
                return f"No existe una reserva con ID {idReserva}"
        except sqlite3.Error as e:
            print(f"Error al consultar reserva: {e}")
            return f"Error al consultar reserva con ID {idReserva}"

    def eliminar_reserva(self, idReserva):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE idReserva = ?", (idReserva,))
            reserva = self.cursor.fetchone()
            if reserva:
                self.cursor.execute("""
                    UPDATE Reserva
                    SET estadoReserva = 'cancelada'
                    WHERE idReserva = ?
                """, (idReserva,))
                self.conn.commit()
                print("Reserva cancelada con éxito (historial guardado).")
            else:
                print("Reserva no encontrada")
        except sqlite3.Error as e:
            print(f"Error al cancelar reserva: {e}")

    def exportar_reservas_csv(self):
        reservas = self.listar_reservas_historial()
        if reservas:
            datos = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in reservas]
            encabezados = ["ID", "Habitacion", "Cliente", "Entrada", "Salida", "Estado", "Servicios", "Costo"]
            # Aquí deberías implementar tu función exportar_csv(datos, encabezados, "reservas.csv")
        else:
            print("❌ No hay reservas para exportar")
