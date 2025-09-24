import sqlite3
from modelos.base import conectar_db
from modelos.reserva import Reserva

class Reserva_manager:
    def __init__(self,conn):
        self.conn = conn
        self.cursor  = self.conn.cursor()

    def crear_reserva(self, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo):
        self.cursor.execute("SELECT * FROM Cliente WHERE idCliente = ?", (idCliente,))
        cliente = self.cursor.fetchone()
        if not cliente:
            print("Cliente no registrado.")
            self.conn.close()
            return

        self.cursor.execute("""
            SELECT * FROM Reserva
            WHERE numHabit = ? AND (
                (fechaEntrada <= ? AND fechaSalida >= ?) OR
                (fechaEntrada <= ? AND fechaSalida >= ?)
            )
        """, (numHabit, fechaEntrada, fechaEntrada, fechaSalida, fechaSalida))
        if self.cursor.fetchone():
            print("La habitación no está disponible en ese rango de tiempo.")
            self.conn.close()
            return

        self.cursor.execute("""
            INSERT INTO Reserva (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, serviciosExtras, costo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, servExtras, costo))
        self.conn.commit()
        id_generado = self.cursor.lastrowid
        print(f"Reserva creada con éxito. ID asignado: {id_generado}")


    def listar_reservas(self):
        self.cursor.execute("SELECT * FROM Reserva")
        filas = self.cursor.fetchall()
        return [Reserva(*fila) for fila in filas]
    
    def consultar_reservas(self, idReserva):
        self.cursor.execute("""
            SELECT * FROM Reserva
            WHERE idReserva = ?
        """,(idReserva,))
        disponible = self.cursor.fetchone()
        if disponible:
            print("Habitacion no esta disponible")
        else:
            print("Habitacion esta disponible")

    def eliminar_reserva(self, idReserva):
        self.cursor.execute("""
            SELECT * FROM Reserva 
            WHERE idReserva = ?
        """,(idReserva,))
        reserva = self.cursor.fetchone()
        if reserva :
            self.cursor.execute("DELETE FROM Reserva WHERE idReserva = ?", (idReserva,))
            self.conn.commit()
            print("Reserva eliminada con éxito.")
        else:
            print("Reserva no encontrada")


