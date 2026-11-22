import re
import secrets

class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, email: str, password: str) -> bool:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Formato de correo electrónico inválido.")
        if email in self.users:
            raise ValueError("El correo electrónico ya está registrado.")
        
        # Validaciones de contraseña
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not any(char.isupper() for char in password):
            raise ValueError("La contraseña debe contener al menos una mayúscula.")
        
        self.users[email] = {
            "password": password,
            "failed_attempts": 0,
            "is_locked": False,
            "reset_token": None
        }
        return True

    def login(self, email: str, password: str) -> bool:
        if email not in self.users:
            return False
        
        user = self.users[email]
        if user["is_locked"]:
            raise PermissionError("Cuenta bloqueada por demasiados intentos fallidos.")
        
        if user["password"] == password:
            user["failed_attempts"] = 0
            return True
        
        user["failed_attempts"] += 1
        if user["failed_attempts"] >= 3:
            user["is_locked"] = True
        return False

    def generate_reset_token(self, email: str) -> str:
        if email not in self.users:
            raise ValueError("Usuario no encontrado.")
        token = secrets.token_hex(16)
        self.users[email]["reset_token"] = token
        return token

    def reset_password(self, email: str, token: str, new_password: str) -> bool:
        if email not in self.users:
            raise ValueError("Usuario no encontrado.")
        user = self.users[email]
        if not user["reset_token"] or user["reset_token"] != token:
            raise ValueError("Token de restablecimiento inválido.")
        
        if len(new_password) < 8 or not any(c.isdigit() for c in new_password) or not any(c.isupper() for c in new_password):
            raise ValueError("La nueva contraseña no cumple los requisitos de seguridad.")
        
        user["password"] = new_password
        user["reset_token"] = None
        user["is_locked"] = False
        user["failed_attempts"] = 0
        return True
