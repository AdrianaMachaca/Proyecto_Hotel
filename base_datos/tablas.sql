PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Habitacion (
    Num_Habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
    Tipo TEXT NOT NULL,
    Estado TEXT NOT NULL,
    Precio REAL NOT NULL,
    Capacidad INTEGER NOT NULL,
    Servicios TEXT,
    Observaciones TEXT
);
CREATE TABLE Cliente(
idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
Nombre TEXT NOT NULL,
Telefono TEXT,
Correo TEXT
);
CREATE TABLE Reserva (
    idReserva INTEGER PRIMARY KEY AUTOINCREMENT,
    numHabit INTEGER NOT NULL,
    idCliente TEXT,
    fechaEntrada TEXT NOT NULL,
    fechaSalida TEXT NOT NULL,
    estadoReserva TEXT NOT NULL,
    serviciosExtras TEXT
);
DELETE FROM sqlite_sequence;
COMMIT;
