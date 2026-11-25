from domain.user import User
from persistence.base_dao import BaseDAO


class UserDAO(BaseDAO):
    TABLE = "users"
    COLUMNS = "id, full_name, email, password_hash, role"
    LABEL = "el usuario"

    @staticmethod
    def _convert(row):
        return User(id=row[0], full_name=row[1], email=row[2],
                    password_hash=row[3], role=row[4])

    @classmethod
    def find_by_email(cls, email):
        users = cls._list_where("email = ?", (email,), "buscar el usuario")
        return users[0] if users else None

    @classmethod
    def insert(cls, user):
        sql = "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)"
        _, new_id = cls._write(sql, (user.full_name, user.email, user.password_hash, user.role),
                               "registrar el usuario")
        user.id = new_id
        return user
