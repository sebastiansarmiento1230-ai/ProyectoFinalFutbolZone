import unittest
from auth import UserManager

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba para mantener un estado limpio."""
        self.manager = UserManager()

    def test_register_user_success(self):
        result = self.manager.register("usuario@email.com", "Password123")
        self.assertTrue(result)
        self.assertIn("usuario@email.com", self.manager.users)

    def test_register_invalid_email_fails(self):
        with self.assertRaises(ValueError):
            self.manager.register("correo-invalido", "Password123")

    def test_register_duplicate_email_fails(self):
        self.manager.register("usuario@email.com", "Password123")
        with self.assertRaises(ValueError):
            self.manager.register("usuario@email.com", "OtraPassword456")

    def test_register_short_password_fails(self):
        with self.assertRaises(ValueError) as ctx:
            self.manager.register("usuario@email.com", "Pass1")
        self.assertIn("al menos 8 caracteres", str(ctx.exception))

    def test_register_password_without_number_fails(self):
        with self.assertRaises(ValueError) as ctx:
            self.manager.register("usuario@email.com", "PasswordSinNumero")
        self.assertIn("al menos un número", str(ctx.exception))

    def test_register_password_without_uppercase_fails(self):
        with self.assertRaises(ValueError) as ctx:
            self.manager.register("usuario@email.com", "password123")
        self.assertIn("al menos una mayúscula", str(ctx.exception))


class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.manager = UserManager()
        self.manager.register("usuario@email.com", "Password123")

    def test_login_success(self):
        result = self.manager.login("usuario@email.com", "Password123")
        self.assertTrue(result)

    def test_login_wrong_password_fails(self):
        result = self.manager.login("usuario@email.com", "ClaveIncorrecta")
        self.assertFalse(result)

    def test_login_nonexistent_user_fails(self):
        result = self.manager.login("nadie@email.com", "Password123")
        self.assertFalse(result)


class TestSecurityFeatures(unittest.TestCase):
    def setUp(self):
        self.manager = UserManager()
        self.manager.register("usuario@email.com", "Password123")

    def test_account_locks_after_three_failed_logins(self):
        # 3 intentos fallidos
        self.manager.login("usuario@email.com", "Errada123")
        self.manager.login("usuario@email.com", "Errada123")
        self.manager.login("usuario@email.com", "Errada123")
        # El 4to intento con clave correcta debe fallar porque la cuenta se bloqueó
        with self.assertRaises(PermissionError) as ctx:
            self.manager.login("usuario@email.com", "Password123")
        self.assertIn("Cuenta bloqueada", str(ctx.exception))

    def test_successful_login_resets_failed_attempts(self):
        # 2 intentos fallidos y luego uno correcto
        self.manager.login("usuario@email.com", "Errada123")
        self.manager.login("usuario@email.com", "Errada123")
        self.assertTrue(self.manager.login("usuario@email.com", "Password123"))
        # Verificamos que el contador volvió a cero
        self.assertEqual(self.manager.users["usuario@email.com"]["failed_attempts"], 0)

    def test_generate_reset_token_success(self):
        token = self.manager.generate_reset_token("usuario@email.com")
        self.assertIsNotNone(token)
        self.assertEqual(len(token), 32)

    def test_reset_password_with_valid_token(self):
        token = self.manager.generate_reset_token("usuario@email.com")
        result = self.manager.reset_password("usuario@email.com", token, "NuevaPass456")
        self.assertTrue(result)
        # Verificar que la nueva contraseña funciona
        self.assertTrue(self.manager.login("usuario@email.com", "NuevaPass456"))

    def test_reset_password_with_invalid_token_fails(self):
        self.manager.generate_reset_token("usuario@email.com")
        with self.assertRaises(ValueError):
            self.manager.reset_password("usuario@email.com", "token-falso-12345", "NuevaPass456")


if __name__ == "__main__":
    unittest.main()
