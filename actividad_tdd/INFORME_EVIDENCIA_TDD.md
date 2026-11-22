# INFORME DE LABORATORIO: DESARROLLO GUIADO POR PRUEBAS (TDD) EN PYTHON

**Programa de Formación:** Análisis y Desarrollo de Software (ADSO)  
**Centro de Formación:** SENA  
**Aprendiz:** Nicolas Felipe Paz Ortiz  
**Actividad:** Pruebas (TDD) para el aplicativo web  
**Tecnologías:** Python 3.x, Visual Studio Code, Módulo `unittest`, `unittest.mock`  

---

## 1. Introducción

En el desarrollo de software actual, garantizar la calidad y el correcto funcionamiento del código desde las primeras etapas es fundamental para evitar errores en producción. La metodología TDD (*Test-Driven Development* o Desarrollo Guiado por Pruebas) propone un enfoque invertido al tradicional: primero se definen los requerimientos en forma de pruebas unitarias automatizadas que fallan, y únicamente después se escribe el código de la aplicación necesario para que dichas pruebas pasen exitosamente.

En este taller implementamos un flujo completo de autenticación y seguridad en Python aplicando el ciclo estándar de TDD:
1. **Rojo (Red):** Escribir una prueba unitaria que falle para validar un requisito específico.
2. **Verde (Green):** Implementar la solución mínima en el código fuente para superar la prueba.
3. **Refactorizar (Refactor):** Limpiar, optimizar y estructurar el código garantizando que las pruebas continúen pasando.

A continuación se detalla la construcción paso a paso de cada uno de los módulos: Registro de usuarios, Inicio de sesión, Interfaz de consola con simulación de entrada/salida (Mocks), Validación de fortaleza de contraseña, Bloqueo por intentos fallidos y Recuperación de contraseña mediante tokens.

---

## 2. Estructura del Proyecto

Los archivos fueron creados y organizados en Visual Studio Code de la siguiente manera:

```text
actividad_tdd/
│
├── auth.py          # Lógica del modelo: clase UserManager con registro, login, bloqueo y tokens
├── test_auth.py     # Pruebas unitarias con unittest para la lógica de autenticación y seguridad
├── ui.py            # Interfaz de línea de comandos (CLI): clase AuthUI
└── test_ui.py       # Pruebas unitarias con unittest.mock para simular input() y print()
```

---

## 3. Desarrollo Paso a Paso de las Pruebas

---

### Prueba 1: Módulo de Registro de Usuarios

**Objetivo:** Validar que un usuario pueda registrarse correctamente, impidiendo correos con formato inválido y correos duplicados.

#### Paso 1 (Rojo): Definición de las pruebas
Se creó el archivo `test_auth.py` con la clase `TestUserRegistration`:
- `test_register_user_success`: Registro exitoso con correo y clave válidos.
- `test_register_invalid_email_fails`: Espera un `ValueError` si el correo no cumple el formato.
- `test_register_duplicate_email_fails`: Espera un `ValueError` si se intenta registrar un correo ya existente.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestUserRegistration
```

*Resultado obtenido (Fase Roja):*
Falla esperada debido a que el módulo `auth.py` o la clase `UserManager` aún no existen o no tienen implementado el método `register`.

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Código de test_auth.py y terminal mostrando el fallo en rojo]**

---

#### Paso 2 (Verde): Implementación mínima
Se creó el archivo `auth.py` con la clase `UserManager` y el método `register()`, utilizando expresiones regulares (`re`) para validar la estructura del correo y un diccionario interno `self.users` para verificar duplicados.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestUserRegistration
```

*Resultado obtenido (Fase Verde):*
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Código de auth.py y terminal mostrando las 3 pruebas pasando en verde (OK)]**

---

### Prueba 2: Módulo de Inicio de Sesión (Login)

**Objetivo:** Validar la autenticación de usuarios mediante credenciales válidas, rechazo por contraseña errónea y rechazo para correos no registrados.

#### Paso 1 (Rojo): Definición de las pruebas
Se añadió a `test_auth.py` la clase `TestUserLogin`:
- `test_login_success`: Retorna `True` cuando el correo y la contraseña coinciden.
- `test_login_wrong_password_fails`: Retorna `False` cuando la clave no coincide.
- `test_login_nonexistent_user_fails`: Retorna `False` si el correo no está en el sistema.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestUserLogin
```

*Resultado obtenido (Fase Roja):*
Falla con `AttributeError: 'UserManager' object has no attribute 'login'`, confirmando que aún no se ha escrito la lógica del login.

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Código de TestUserLogin y terminal mostrando el error de atributo en rojo]**

---

#### Paso 2 (Verde): Implementación del método login
En `auth.py` se agregó el método `login(self, email, password)` dentro de la clase `UserManager`, validando primero la existencia del correo en el diccionario y luego contrastando la contraseña almacenada.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestUserLogin
```

*Resultado obtenido (Fase Verde):*
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Método login en auth.py y terminal con las pruebas en OK]**

---

### Prueba 3: Interfaz de Usuario (CLI y Aislamiento con Mocks)

**Objetivo:** Probar el flujo de interacción por consola (menú de opciones, captura de datos por teclado y mensajes en pantalla) sin requerir interacción manual humana, utilizando `unittest.mock.patch`.

#### Paso 1 (Rojo): Definición de pruebas con Mocks
Se creó el archivo `test_ui.py` con la clase `TestAuthUI`. Con el decorador `@patch` se interceptó la función integrada `builtins.input` para proveer secuencias automáticas de respuestas (por ejemplo: opción "1", correo, contraseña y luego "3" para salir) y `builtins.print` para verificar mediante `assert_any_call` que el sistema imprima los mensajes esperados como `"¡Registro exitoso!"` e `"¡Inicio de sesión exitoso!"`.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_ui.py
```

*Resultado obtenido (Fase Roja):*
Falla con `ModuleNotFoundError: No module named 'ui'` debido a que el módulo de presentación aún no ha sido codificado.

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Código de test_ui.py con los mocks y terminal mostrando el fallo en rojo]**

---

#### Paso 2 (Verde): Implementación de la Interfaz AuthUI
Se creó el archivo `ui.py` con la clase `AuthUI`. Su método `start()` maneja un bucle interactivo que solicita la opción al usuario, captura los parámetros y delega las operaciones a la instancia inyectada de `UserManager`, mostrando los resultados y controlando las excepciones de validación.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_ui.py
```

*Resultado obtenido (Fase Verde):*
```text
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Archivo ui.py y terminal mostrando los 2 tests de UI en OK]**

---

### Prueba 4: Validación de Fortaleza de Contraseñas

**Objetivo:** Forzar reglas de seguridad mínimas para las contraseñas al momento del registro: longitud mínima de 8 caracteres, al menos un número y al menos una letra mayúscula.

#### Paso 1 (Rojo): Definición de pruebas de validación
Se agregaron tres métodos adicionales a la clase `TestUserRegistration` en `test_auth.py`:
- `test_register_short_password_fails`: Verifica que una contraseña corta (menos de 8 caracteres) lance `ValueError`.
- `test_register_password_without_number_fails`: Verifica que una contraseña sin dígitos lance `ValueError`.
- `test_register_password_without_uppercase_fails`: Verifica que una contraseña sin mayúsculas lance `ValueError`.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestUserRegistration
```

*Resultado obtenido (Fase Roja):*
Fallan los 3 nuevos tests con `AssertionError: ValueError not raised`, porque el método de registro permitía cualquier cadena sin verificar su complejidad.

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Nuevos métodos de prueba en test_auth.py y terminal mostrando las fallas]**

---

#### Paso 2 (Verde): Actualización del método register
Se actualizó el método `register` en `auth.py` para incluir validaciones explícitas de longitud y presencia de caracteres mediante `isdigit()` e `isupper()`. Además, se actualizó la estructura interna del usuario para soportar estados de seguridad posteriores (`failed_attempts`, `is_locked`, `reset_token`).

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestUserRegistration
```

*Resultado obtenido (Fase Verde):*
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Validaciones en auth.py y terminal con los 6 tests pasando en OK]**

---

### Prueba 5: Bloqueo de Cuenta por Intentos Fallidos

**Objetivo:** Proteger el sistema contra ataques de fuerza bruta bloqueando la cuenta tras 3 intentos consecutivos erróneos de inicio de sesión, y verificando que un login exitoso reinicie el contador de fallos.

#### Paso 1 (Rojo): Casos de prueba de seguridad
Se añadió la clase `TestSecurityFeatures` en `test_auth.py`:
- `test_account_locks_after_three_failed_logins`: Realiza 3 intentos fallidos consecutivos y luego intenta un 4to ingreso con la clave correcta, esperando un `PermissionError` con el mensaje de cuenta bloqueada.
- `test_successful_login_resets_failed_attempts`: Realiza 2 fallos y luego un acceso exitoso, confirmando que el contador `failed_attempts` se reinicie en `0`.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestSecurityFeatures
```

*Resultado obtenido (Fase Roja):*
Falla la prueba porque la cuenta sigue permitiendo el acceso tras los intentos erróneos (`AssertionError: PermissionError not raised`).

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Clase TestSecurityFeatures en test_auth.py y fallo en consola]**

---

#### Paso 2 (Verde): Control de intentos y bloqueo en el método login
Se modificó el método `login` en `auth.py`:
- Si la propiedad `is_locked` es `True`, lanza `PermissionError`.
- Si la contraseña es correcta, reinicia `failed_attempts = 0` y retorna `True`.
- Si la contraseña no coincide, incrementa `failed_attempts += 1`. Al llegar a 3, marca `is_locked = True`.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestSecurityFeatures
```

*Resultado obtenido (Fase Verde):*
```text
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Lógica de bloqueo en auth.py y terminal mostrando el OK]**

---

### Prueba 6: Generación y Uso de Token para Restablecimiento de Contraseña

**Objetivo:** Permitir a un usuario restablecer su contraseña de manera segura generando un token criptográfico de 32 caracteres hexadecimales, validando el token y actualizando la clave.

#### Paso 1 (Rojo): Definición del flujo de recuperación
Se integraron a la clase `TestSecurityFeatures` en `test_auth.py` las siguientes pruebas:
- `test_generate_reset_token_success`: Verifica que se genere un token no nulo y con una longitud exacta de 32 caracteres.
- `test_reset_password_with_valid_token`: Simula el cambio de clave exitoso con un token válido y comprueba que se pueda iniciar sesión con la nueva contraseña.
- `test_reset_password_with_invalid_token_fails`: Verifica que un token incorrecto lance `ValueError`.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestSecurityFeatures
```

*Resultado obtenido (Fase Roja):*
Falla con `AttributeError: 'UserManager' object has no attribute 'generate_reset_token'`.

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Nuevas pruebas de token en test_auth.py y terminal en rojo]**

---

#### Paso 2 (Verde): Implementación de tokens con la librería secrets
Se importó el módulo estándar `secrets` en `auth.py` y se implementaron dos nuevos métodos en `UserManager`:
- `generate_reset_token(self, email)`: Genera un token aleatorio seguro con `secrets.token_hex(16)` (32 caracteres) y lo asocia al usuario.
- `reset_password(self, email, token, new_password)`: Valida la existencia del usuario y la coincidencia del token, comprueba los requisitos de seguridad de la nueva contraseña, la actualiza, limpia el token temporal y desbloquea la cuenta si estaba bloqueada.

*Comando ejecutado en la terminal:*
```bash
python -m unittest test_auth.TestSecurityFeatures
```

*Resultado obtenido (Fase Verde):*
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA: Métodos generate_reset_token y reset_password en auth.py y terminal con los 5 tests en OK]**

---

## 4. Ejecución del Conjunto Completo de Pruebas

Para validar la integración total de todos los componentes y verificar que ningún cambio posterior rompió funcionalidades previas (pruebas de regresión), se ejecutó el descubridor automático de pruebas de Python en modo detallado (`-v`).

*Comando ejecutado:*
```bash
python -m unittest discover -v
```

*Salida completa obtenida en la terminal de Visual Studio Code:*
```text
test_account_locks_after_three_failed_logins (test_auth.TestSecurityFeatures.test_account_locks_after_three_failed_logins) ... ok
test_generate_reset_token_success (test_auth.TestSecurityFeatures.test_generate_reset_token_success) ... ok
test_reset_password_with_invalid_token_fails (test_auth.TestSecurityFeatures.test_reset_password_with_invalid_token_fails) ... ok
test_reset_password_with_valid_token (test_auth.TestSecurityFeatures.test_reset_password_with_valid_token) ... ok
test_successful_login_resets_failed_attempts (test_auth.TestSecurityFeatures.test_successful_login_resets_failed_attempts) ... ok
test_login_nonexistent_user_fails (test_auth.TestUserLogin.test_login_nonexistent_user_fails) ... ok
test_login_success (test_auth.TestUserLogin.test_login_success) ... ok
test_login_wrong_password_fails (test_auth.TestUserLogin.test_login_wrong_password_fails) ... ok
test_register_duplicate_email_fails (test_auth.TestUserRegistration.test_register_duplicate_email_fails) ... ok
test_register_invalid_email_fails (test_auth.TestUserRegistration.test_register_invalid_email_fails) ... ok
test_register_password_without_number_fails (test_auth.TestUserRegistration.test_register_password_without_number_fails) ... ok
test_register_password_without_uppercase_fails (test_auth.TestUserRegistration.test_register_password_without_uppercase_fails) ... ok
test_register_short_password_fails (test_auth.TestUserRegistration.test_register_short_password_fails) ... ok
test_register_user_success (test_auth.TestUserRegistration.test_register_user_success) ... ok
test_ui_login_successful_flow (test_ui.TestAuthUI.test_ui_login_successful_flow) ... ok
test_ui_register_flow (test_ui.TestAuthUI.test_ui_register_flow) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.001s

OK
```

> **[INSERTAR AQUÍ CAPTURA DE PANTALLA GENERAL: Visual Studio Code con el panel de archivos a la izquierda y la terminal inferior mostrando los 16 tests pasando exitosamente en OK]**

---

## 5. Conclusiones del Aprendizaje

1. **Efectividad del ciclo TDD:** La metodología de escribir primero las pruebas (Fase Roja) y posteriormente la implementación (Fase Verde) permite tener claridad sobre los requisitos antes de programar, reduciendo notablemente la cantidad de errores lógicos o casos no contemplados.
2. **Aislamiento mediante Mocks:** Se evidenció la utilidad de la librería `unittest.mock` para desacoplar las pruebas de la entrada manual por teclado, permitiendo simular flujos de usuario completos de manera instantánea y automatizada.
3. **Seguridad y Robustez:** Mediante las pruebas unitarias se verificaron aspectos críticos como el bloqueo por ataques de fuerza bruta y la generación de tokens criptográficamente seguros con `secrets`, asegurando que la lógica responda adecuadamente ante entradas no válidas o maliciosas.
4. **Mantenibilidad y Confianza:** Al contar con una batería de 16 pruebas automatizadas, cualquier modificación o refactorización futura del sistema puede validarse en milisegundos ejecutando `unittest discover`, garantizando que las funcionalidades existentes no se vean afectadas.
