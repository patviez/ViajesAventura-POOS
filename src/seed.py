import os

from domain.user import User
from persistence.user_dao import UserDAO
from services.auth import create_admin


def seed_initial_data():
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        print("Semilla omitida: defina ADMIN_EMAIL y ADMIN_PASSWORD en el .env.")
        return
    if UserDAO.find_by_email(User.normalize_email(email)) is None:
        create_admin("Administrador", email, password)
        print("Cuenta de administrador creada.")
