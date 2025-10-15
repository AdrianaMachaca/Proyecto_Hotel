class Reserva:
    def __init__(self, idReserva, numHabit, idCliente, fechaEntrada, fechaSalida, estadoReserva, serviciosExtras, costo, cuenta=None):
        self.idReserva = idReserva
        self.numHabit = numHabit
        self.idCliente = idCliente
        self.fechaEntrada = fechaEntrada
        self.fechaSalida = fechaSalida
        self.estadoReserva = estadoReserva
        self.serviciosExtras = serviciosExtras
        self.costo = costo
        self.cuenta = cuenta


    def mostrar_reserva(self):
        print(f"Reserva ID: {self.idReserva}")
        print(f"Habitación: {self.numHabit}")
        print(f"Cliente: {self.cliente.nombre} {self.cliente.apellido}")
        print(f"Entrada: {self.fechaEntrada}, Salida: {self.fechaSalida}")
        print(f"Estado: {self.estadoReserva}")
        print(f"Servicios extras: {self.servExtras}")   





