import unittest
from app.modelos.base import conectar_db
from app.managers.cliente_manager import ClienteManager

class TestClienteManager(unittest.TestCase):
    
    def setUp(self):
        # Establecer conexión con la base de datos para las pruebas
        self.conn = conectar_db()
        self.cliente_mgr = ClienteManager(self.conn)
    
    def test_registrar_cliente(self):
        # Crear datos de cliente ficticios para prueba
        cliente_data = {
            'nombre': 'John',
            'apellido': 'Doe',
            'telefono': '1234567890',
            'correo': 'john.doe@example.com'
        }
        
        # Registrar cliente
        id_cliente = self.cliente_mgr.registrar_cliente(**cliente_data)
        
        # Verificar que el cliente fue registrado (ID debe ser mayor que 0)
        self.assertGreater(id_cliente, 0)
    
    def test_error_registrar_cliente(self):
        # Intentar registrar un cliente con datos inválidos
        cliente_data = {
            'nombre': '',
            'apellido': 'Doe',
            'telefono': '1234567890',
            'correo': 'john.doe@example.com'
        }
        
        # Comprobar que se levanta un error por datos faltantes
        with self.assertRaises(ValueError):
            self.cliente_mgr.registrar_cliente(**cliente_data)

    def tearDown(self):
        # Limpiar la base de datos después de las pruebas
        pass

if __name__ == '__main__':
    unittest.main()
