import sqlite3
import os

def conectar_db():
    ruta = os.path.join(os.path.dirname(__file__), "..", "Base_Datos.db")
    ruta_abs = os.path.abspath(ruta)

    print("Usando base de datos en:", ruta_abs)

    try:
        conexion = sqlite3.connect(ruta_abs)
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cliente (
            idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Telefono TEXT,
            Correo TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Habitacion (
            Num_Habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
            Tipo TEXT NOT NULL,
            Estado TEXT NOT NULL,
            Precio REAL NOT NULL,
            Capacidad INTEGER NOT NULL,
            Servicios TEXT,
            Observaciones TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reserva (
            idReserva INTEGER PRIMARY KEY AUTOINCREMENT,
            numHabit INTEGER NOT NULL,
            idCliente INTEGER NOT NULL,
            fechaEntrada TEXT NOT NULL,
            fechaSalida TEXT NOT NULL,
            estadoReserva TEXT NOT NULL,
            serviciosExtras TEXT,
            costo REAL NOT NULL,
            FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
            FOREIGN KEY (numHabit) REFERENCES Habitacion(Num_Habitacion)
        )
        """)

        conexion.commit()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        print("Tablas existentes:", tablas)

        return conexion

    except sqlite3.Error as e:
        print(f"Error al conectar: {e}")
        return None
