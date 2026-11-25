import bcrypt

from domain.user import User
from persistence.user_dao import UserDAO

MAX_PASSWORD_BYTES = 72  # limite de bcrypt


def hash_password(password):
    password = User.validate_password(password)
    data = password.encode("utf-8")
    if len(data) > MAX_PASSWORD_BYTES:
        raise ValueError("La contraseña admite como máximo 72 bytes.")
    return bcrypt.hashpw(data, bcrypt.gensalt()).decode("utf-8")


def authenticate(email, password):
    try:
        email = User.normalize_email(email)
    except (TypeError, ValueError):
        return None
    if not isinstance(password, str):
        return None
    data = password.encode("utf-8")
    if not 0 < len(data) <= MAX_PASSWORD_BYTES:
        return None

    user = UserDAO.find_by_email(email)
    if user is None or not bcrypt.checkpw(data, user.password_hash.encode("utf-8")):
        return None
    return {"id": user.id, "full_name": user.full_name, "role": user.role}


def _create_user(full_name, email, password, role):
    user = User(full_name, email, hash_password(password), role)
    if UserDAO.find_by_email(user.email) is not None:
        raise ValueError("No se pudo crear la cuenta con esos datos.")
    return UserDAO.insert(user).id


def register_client(full_name, email, password):
    """Registro público (RF-09): el rol siempre es 'client'."""
    return _create_user(full_name, email, password, "client")


def create_admin(full_name, email, password):
    """Solo para la semilla inicial. No exponer en ningún menú."""
    return _create_user(full_name, email, password, "admin")
