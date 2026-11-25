import re


class User:
    ROLES = ("admin", "client")
    MIN_PASSWORD = 8
    _EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, full_name, email, password_hash, role="client", id=None):
        self.id = id
        self.full_name = self.validate_full_name(full_name)
        self.email = self.normalize_email(email)
        self.password_hash = password_hash
        self.role = self.validate_role(role)

    @classmethod
    def validate_full_name(cls, name):
        if not isinstance(name, str):
            raise TypeError("El nombre debe ser texto.")
        name = name.strip()
        if not 2 <= len(name) <= 80:
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")
        return name

    @classmethod
    def normalize_email(cls, email):
        if not isinstance(email, str):
            raise TypeError("El correo debe ser texto.")
        email = email.strip().lower()
        if len(email) > 120 or not cls._EMAIL.match(email):
            raise ValueError("El correo no tiene un formato válido.")
        return email

    @classmethod
    def validate_password(cls, password):
        if not isinstance(password, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(password) < cls.MIN_PASSWORD:
            raise ValueError(f"La contraseña debe tener al menos {cls.MIN_PASSWORD} caracteres.")
        return password

    @classmethod
    def validate_role(cls, role):
        if role not in cls.ROLES:
            raise ValueError("Rol no permitido.")
        return role
