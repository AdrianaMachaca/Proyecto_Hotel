import unittest
from app.modelos.base import conectar_db
from app.managers.reserva_manager import ReservaManager

class TestReservaManager(unittest.TestCase):
    
    def setUp(self):
        # Conectar a la base de datos y preparar el objeto de reserva
        self.conn = conectar_db()
        self.reserva_mgr = ReservaManager(self.conn)
    
    def test_crear_reserva(self):
        reserva_data = {
            'num_habit': 101,
            'id_cliente': 1,
            'fecha_entrada': '2025-10-01',
            'fecha_salida': '2025-10-05',
            'estado': 'Confirmada',
            'servicios': 'Desayuno',
            'cuenta': 500.0
        }
        
        reserva_id = self.reserva_mgr.crear_reserva(**reserva_data)
        
        self.assertGreater(reserva_id, 0)
    
    def test_consultar_reserva(self):
        # Supongamos que tenemos una reserva con id 1
        reserva = self.reserva_mgr.consultar_reservas(1)
        self.assertIsNotNone(reserva)
    
    def test_eliminar_reserva(self):
        # Intentar eliminar una reserva
        resultado = self.reserva_mgr.eliminar_reserva(1)
        self.assertTrue(resultado)

    def tearDown(self):
        # Limpiar después de las pruebas
        pass

if __name__ == '__main__':
    unittest.main()
