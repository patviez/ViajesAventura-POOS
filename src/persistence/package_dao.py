from domain.package import Package
from persistence.base_dao import BaseDAO


class PackageDAO(BaseDAO):
    TABLE = "packages"
    COLUMNS = "id, name, start_date, end_date, available_slots"
    LABEL = "el paquete"

    @staticmethod
    def _convert(row):
        return Package(id=row[0], name=row[1], start_date=row[2],
                       end_date=row[3], available_slots=row[4])

    # TODO (RF-05): insert(package, destination_ids) -> guardar el paquete y sus filas
    #               en package_destinations (con visit_order) en una sola transaccion.
    # TODO (RF-06): total_cost(package_id) -> SUM(base_cost) de sus destinos.
    # TODO (RF-07): update(package) y bloqueo de eliminacion si tiene reservas.
    # TODO (RF-08): list_available() -> paquetes con available_slots > 0.
