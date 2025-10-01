import unittest
from app.modelos.base import conectar_db
from app.managers.habitacion_manager import HabitacionManager

class TestHabitacionManager(unittest.TestCase):
    
    def setUp(self):
        # Conexión a la base de datos
        self.conn = conectar_db()
        self.habitacion_mgr = HabitacionManager(self.conn)
    
    def test_registrar_habitacion(self):
        habitacion_data = {
            'numero': 101,
            'tipo': 'Sencilla',
            'estado': 'Disponible'
        }
        
        id_habitacion = self.habitacion_mgr.registrar_habitacion(**habitacion_data)
        self.assertGreater(id_habitacion, 0)
    
    def test_disponibilidad_habitacion(self):
        # Supongamos que la habitación 101 está disponible
        disponibilidad = self.habitacion_mgr.Disponibilidad_habitaciones(101)
        self.assertTrue(disponibilidad)

    def tearDown(self):
        # Limpiar después de las pruebas
        pass

if __name__ == '__main__':
    unittest.main()



