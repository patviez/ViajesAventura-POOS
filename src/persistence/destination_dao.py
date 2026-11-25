from domain.destination import Destination
from persistence.base_dao import BaseDAO


class DestinationDAO(BaseDAO):

    TABLE = "destinations"
    COLUMNS = "id, name, description, activities, base_cost"
    LABEL = "el destino"

    @staticmethod
    def _convert(row):
        return Destination(id=row[0], name=row[1], description=row[2],
                           activities=row[3], base_cost=row[4])

    @classmethod
    def insert(cls, destination):
        sql = ("INSERT INTO destinations (name, description, activities, base_cost) "
               "VALUES (?, ?, ?, ?)")
        params = (destination.name, destination.description,
                  destination.activities, destination.base_cost)
        _, new_id = cls._write(sql, params, "registrar el destino")
        destination.id = new_id
        return destination

    @classmethod
    def update(cls, destination):
        sql = ("UPDATE destinations SET name = ?, description = ?, activities = ?, "
               "base_cost = ? WHERE id = ?")
        params = (destination.name, destination.description, destination.activities,
                  destination.base_cost, destination.id)
        rowcount, _ = cls._write(sql, params, "modificar el destino")
        return rowcount > 0

    @classmethod
    def is_in_package(cls, destination_id):
        sql = "SELECT COUNT(*) FROM package_destinations WHERE destination_id = ?"
        rows = cls._query(sql, (destination_id,), "consultar los paquetes del destino")
        return rows[0][0] > 0
