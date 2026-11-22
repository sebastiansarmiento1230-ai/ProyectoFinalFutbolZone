import unittest
from unittest.mock import patch
from auth import UserManager
from ui import AuthUI

class TestAuthUI(unittest.TestCase):
    def setUp(self):
        self.manager = UserManager()
        self.ui = AuthUI(self.manager)

    @patch('builtins.input', side_effect=["1", "test@email.com", "Password123", "3"])
    @patch('builtins.print')
    def test_ui_register_flow(self, mock_print, mock_input):
        self.ui.start()
        mock_print.assert_any_call("¡Registro exitoso!")

    @patch('builtins.input', side_effect=["2", "test@email.com", "Password123", "3"])
    @patch('builtins.print')
    def test_ui_login_successful_flow(self, mock_print, mock_input):
        self.manager.register("test@email.com", "Password123")
        self.ui.start()
        mock_print.assert_any_call("¡Inicio de sesión exitoso!")

if __name__ == "__main__":
    unittest.main()
