import getpass

from domain.user import User
from inputs import ask
from services.auth import authenticate, register_client


def ask_login():
    email = input("Correo: ")
    password = getpass.getpass("Contraseña: ")
    session = authenticate(email, password)
    if session is None:
        print("Correo o contraseña incorrectos.")
    else:
        print(f"Sesión iniciada. Bienvenido/a, {session['full_name']}.")
    return session


def ask_client_registration():
    name = ask("Nombre completo: ", User.validate_full_name)
    email = ask("Correo: ", User.normalize_email)
    password = ask("Contraseña: ", User.validate_password, getpass.getpass)
    if password != getpass.getpass("Repita la contraseña: "):
        print("Las contraseñas no coinciden.")
        return None
    try:
        user_id = register_client(name, email, password)
    except (TypeError, ValueError) as error:
        print(error)
        return None
    print(f"Cuenta creada correctamente. ID: {user_id}")
    return user_id
