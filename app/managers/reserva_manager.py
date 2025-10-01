import sqlite3
from app.modelos.base import conectar_db
from app.modelos.reserva import Reserva

class Reserva_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    # ---------------------------------------------------------
    #  Crear nueva reserva
    # ---------------------------------------------------------
    def crear_reserva(self, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo):
        try:
            # Verificar cliente
            self.cursor.execute("SELECT * FROM Cliente WHERE idCliente = ?", (idCliente,))
            cliente = self.cursor.fetchone()
            if not cliente:
                print("Cliente no registrado.")
                return None

            # Verificar disponibilidad
            self.cursor.execute("""
                SELECT * FROM Reserva 
                WHERE numHabit = ? 
                AND NOT (fechaSalida < ? OR fechaEntrada > ?)
            """, (numHabit, fechaEntrada, fechaSalida))

            if self.cursor.fetchone():
                print("La habitacion no esta disponible en ese rango de tiempo.")
                return None

            # Insertar nueva reserva
            self.cursor.execute("""
                INSERT INTO Reserva (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, serviciosExtras, costo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo))

            self.conn.commit()
            id_generado = self.cursor.lastrowid
            print(f"Reserva creada con exito. ID asignado: {id_generado}")
            return id_generado

        except sqlite3.Error as e:
            print(f"Error al crear reserva: {e}")
            return None

    # ---------------------------------------------------------
    #  Listar todas las reservas
    # ---------------------------------------------------------
    def listar_reservas(self):
        try:
            self.cursor.execute("SELECT * FROM Reserva")
            filas = self.cursor.fetchall()
            return [Reserva(*fila) for fila in filas]
        except sqlite3.Error as e:
            print(f"Error al listar reservas: {e}")
            return []

    # ---------------------------------------------------------
    #  Consultar reserva por ID
    # ---------------------------------------------------------
    def consultar_reservas(self, idReserva):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE idReserva = ?", (idReserva,))
            fila = self.cursor.fetchone()
            if fila:
                return Reserva(*fila)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al consultar reserva: {e}")
            return None

    # ---------------------------------------------------------
    #  Eliminar reserva
    # ---------------------------------------------------------
    def eliminar_reserva(self, idReserva):
        try:
            self.cursor.execute("SELECT * FROM Reserva WHERE idReserva = ?", (idReserva,))
            reserva = self.cursor.fetchone()
            if reserva:
                self.cursor.execute("DELETE FROM Reserva WHERE idReserva = ?", (idReserva,))
                self.conn.commit()
                print("Reserva eliminada con exito.")
            else:
                print("Reserva no encontrada.")
        except sqlite3.Error as e:
            print(f"Error al eliminar reserva: {e}")

    # ---------------------------------------------------------
    #  Listar reservas activas
    # ---------------------------------------------------------
    def listar_reservas_activas(self):
        try:
            self.cursor.execute("""
                SELECT * FROM Reserva 
                WHERE LOWER(estadoReserva) IN (?, ?)
            """, ('confirmada', 'activa'))
            filas = self.cursor.fetchall()
            return [Reserva(*fila) for fila in filas]
        except sqlite3.Error as e:
            print(f"Error al listar reservas activas: {e}")
            return []

    # ---------------------------------------------------------
    #  Listar reservas canceladas
    # ---------------------------------------------------------
    def listar_reservas_canceladas(self):
        try:
            self.cursor.execute("""
                SELECT * FROM Reserva 
                WHERE LOWER(estadoReserva) = ?
            """, ('cancelada',))
            filas = self.cursor.fetchall()
            return [Reserva(*fila) for fila in filas]
        except sqlite3.Error as e:
            print(f"Error al listar reservas canceladas: {e}")
            return []

    # ---------------------------------------------------------
    # Historial de reservas
    # ---------------------------------------------------------
    def listar_reservas_historial(self):
        try:
            self.cursor.execute("SELECT * FROM Reserva")
            filas = self.cursor.fetchall()
            return [Reserva(*fila) for fila in filas]
        except sqlite3.Error as e:
            print(f"Error al listar historial de reservas: {e}")
            return []

import sqlite3
from app.modelos.base import conectar_db
from app.modelos.reserva import Reserva

class Reserva_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def crear_reserva(self, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo):
        try:
            # Verificamos si el cliente existe
            self.cursor.execute("SELECT * FROM Cliente WHERE idCliente = ?", (idCliente,))
            cliente = self.cursor.fetchone()
            if not cliente:
                print("Cliente no registrado.")
                return None

            # Verificamos si la habitación está disponible
            self.cursor.execute("""
                SELECT * FROM Reserva WHERE numHabit = ? AND (
                    (fechaEntrada <= ? AND fechaSalida >= ?) OR
                    (fechaEntrada <= ? AND fechaSalida >= ?)
                )
            """, (numHabit, fechaEntrada, fechaEntrada, fechaSalida, fechaSalida))

            if self.cursor.fetchone():
                print("La habitación no está disponible en ese rango de tiempo.")
                return None

            # Insertamos la nueva reserva
            self.cursor.execute("""
                INSERT INTO Reserva (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, serviciosExtras, costo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo))
            self.conn.commit()
            id_generado = self.cursor.lastrowid
            print(f"Reserva creada con éxito. ID asignado: {id_generado}")
            return id_generado

        except sqlite3.Error as e:
            print(f"Error al crear reserva: {e}")
            return None

    def listar_reservas(self):
        try:
            self.cursor.execute("SELECT * FROM Reserva")
            filas = self.cursor.fetchall()
            return [Reserva(*fila) for fila in filas]
        except sqlite3.Error as e:
            print(f"Error al listar reservas: {e}")
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
                self.cursor.execute("DELETE FROM Reserva WHERE idReserva = ?", (idReserva,))
                self.conn.commit()
                print("Reserva eliminada con éxito.")
            else:
                print("Reserva no encontrada")
        except sqlite3.Error as e:
            print(f"Error al eliminar reserva: {e}")
