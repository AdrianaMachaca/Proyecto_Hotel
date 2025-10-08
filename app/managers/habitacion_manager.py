import sqlite3
from tabulate import tabulate
from app.modelos.base import conectar_db
from app.modelos.habitacion import Habitacion

class Habitacion_manager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def disponibilidad_habitaciones(self, numHabitacion):
        try:
            # 1️⃣ Verificar que la habitacion exista
            self.cursor.execute("SELECT * FROM Habitacion WHERE Num_Habitacion = ?", (numHabitacion,))
            habitacion = self.cursor.fetchone()
            if not habitacion:
                return f"❌ La habitación {numHabitacion} no existe."

            # 2️⃣ Verificar si hay reservas activas
            self.cursor.execute("""
                SELECT * FROM Reserva 
                WHERE numHabit = ? AND estadoReserva != 'cancelada'
            """, (numHabitacion,))
            reserva = self.cursor.fetchone()

            if reserva:
                return f"Habitación {numHabitacion} NO está disponible"
            else:
                return f"Habitación {numHabitacion} está disponible"

        except sqlite3.Error as e:
            print(f"Error al comprobar disponibilidad: {e}")
            return "Error al verificar disponibilidad."



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
        
    # Solo devuelve los datos
    def obtener_habitaciones(self):
        try:
            self.cursor.execute("SELECT * FROM Habitacion")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener habitaciones: {e}")
            return []

    # Solo imprime la tabla
    def mostrar_habitaciones(self):
        filas = self.obtener_habitaciones()
        if filas:
            tabla = [[f[0], f[1], f[2], f[3], f[4], f[5], f[6]] for f in filas]
            print(tabulate(tabla, headers=["Num", "Tipo", "Estado", "Precio", "Capacidad", "Servicios", "Observaciones"], tablefmt="grid"))
        else:
            print("❌ No hay habitaciones registradas.")

