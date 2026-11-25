from abc import ABC, abstractmethod
from persistence.connection import DB_ERRORS, open_connection, placeholder

class DatabaseError(Exception):

class BaseDAO(ABC):

    TABLE = ""
    COLUMNS = ""
    LABEL = ""

    @staticmethod
    @abstractmethod
    def _convert(row):

    @staticmethod
    def _prepare(sql):
        return sql.replace("?", placeholder())

    @staticmethod
    def _write(sql, params, action):
        connection = None
        try:
            connection = open_connection()
            cursor = connection.cursor()
            cursor.execute(BaseDAO._prepare(sql), params)
            connection.commit()
            return cursor.rowcount, cursor.lastrowid
        except DB_ERRORS as error:
            if connection is not None:
                connection.rollback()
            raise DatabaseError(f"Error al {action}: {error}") from error
        finally:
            if connection is not None:
                connection.close()

    @staticmethod
    def _query(sql, params, action):
        connection = None
        try:
            connection = open_connection()
            cursor = connection.cursor()
            cursor.execute(BaseDAO._prepare(sql), params)
            return cursor.fetchall()
        except DB_ERRORS as error:
            raise DatabaseError(f"Error al {action}: {error}") from error
        finally:
            if connection is not None:
                connection.close()

    @classmethod
    def _list_where(cls, condition, params, action, order="id"):
        sql = f"SELECT {cls.COLUMNS} FROM {cls.TABLE} WHERE {condition} ORDER BY {order}"
        return [cls._convert(row) for row in cls._query(sql, params, action)]

    @classmethod
    def find_by_id(cls, entity_id):
        sql = f"SELECT {cls.COLUMNS} FROM {cls.TABLE} WHERE id = ?"
        rows = cls._query(sql, (entity_id,), f"buscar {cls.LABEL}")
        return cls._convert(rows[0]) if rows else None

    @classmethod
    def list_all(cls):
        sql = f"SELECT {cls.COLUMNS} FROM {cls.TABLE} ORDER BY id"
        return [cls._convert(row) for row in cls._query(sql, (), f"listar {cls.LABEL}")]

    @classmethod
    def delete(cls, entity_id):
        sql = f"DELETE FROM {cls.TABLE} WHERE id = ?"
        rowcount, _ = cls._write(sql, (entity_id,), f"eliminar {cls.LABEL}")
        return rowcount > 0
