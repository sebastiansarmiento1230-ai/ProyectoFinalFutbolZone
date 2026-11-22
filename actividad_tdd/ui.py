class AuthUI:
    def __init__(self, user_manager):
        self.manager = user_manager

    def start(self):
        while True:
            print("\n1. Registrar\n2. Iniciar Sesión\n3. Salir")
            option = input("Seleccione una opción: ")

            if option == "1":
                email = input("Email: ")
                password = input("Contraseña: ")
                try:
                    self.manager.register(email, password)
                    print("¡Registro exitoso!")
                except ValueError as e:
                    print(f"Error: {e}")

            elif option == "2":
                email = input("Email: ")
                password = input("Contraseña: ")
                if self.manager.login(email, password):
                    print("¡Inicio de sesión exitoso!")
                else:
                    print("Credenciales incorrectas.")

            elif option == "3":
                break
