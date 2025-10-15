import sqlite3
from app.modelos.base import conectar_db
from app.modelos.habitacion import Habitacion
from tabulate import tabulate

class Habitacion_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def crear_habitacion(self, numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones):
        try:
            self.cursor.execute("SELECT * FROM Habitacion WHERE Num_Habitacion = ?", (numHabitacion,))
            habita = self.cursor.fetchone()

            if habita:
                print("La habitación ya existe")
                return Habitacion(*habita)
            else:
                self.cursor.execute("""
                    INSERT INTO Habitacion (Num_Habitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones))
                self.conn.commit()
                print(f"Habitación creada con éxito")
                return Habitacion(numHabitacion, Tipo, Estado, Precio, Capacidad, Servicios, Observaciones)
        except sqlite3.Error as e:
            print(f"Error al crear habitación: {e}")
            return None

    def listar_habitaciones(self):
            try:
                self.cursor.execute("SELECT * FROM Habitacion")
                return self.cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error al listar habitaciones: {e}")
                return []
            
            # Devuelve los datos sin imprimir
    def obtener_habitaciones(self):
        try:
            self.cursor.execute("SELECT * FROM Habitacion")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener habitaciones: {e}")
            return []

    # Imprime la tabla en consola
    def mostrar_habitaciones(self):
        filas = self.obtener_habitaciones()
        if filas:
            tabla = [[f[0], f[1], f[2], f[3], f[4], f[5], f[6]] for f in filas]
            print(tabulate(tabla, headers=["Num", "Tipo", "Estado", "Precio", "Capacidad", "Servicios", "Observaciones"], tablefmt="grid"))
        else:
            print("❌ No hay habitaciones registradas.")

    def disponibilidad_habitaciones(self, numHabitacion):
        try:
            # Primero revisamos si existe la habitación
            self.cursor.execute("SELECT * FROM Habitacion WHERE Num_Habitacion = ?", (numHabitacion,))
            hab = self.cursor.fetchone()
            if not hab:
                return f"❌ La habitación {numHabitacion} no existe."

            # Revisamos si está reservada
            self.cursor.execute("SELECT * FROM Reserva WHERE numHabit = ? AND estadoReserva='confirmada'", (numHabitacion,))
            reserva = self.cursor.fetchone()
            if reserva:
                return f"Habitación {numHabitacion} NO está disponible"
            else:
                return f"Habitación {numHabitacion} está disponible"
        except sqlite3.Error as e:
            return f"Error al comprobar disponibilidad: {e}"
