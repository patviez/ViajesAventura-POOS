from domain.reservation import Reservation
from persistence.base_dao import BaseDAO


class ReservationDAO(BaseDAO):
    TABLE = "reservations"
    COLUMNS = "id, user_id, package_id, reservation_date, travelers, total_paid, status"
    LABEL = "la reserva"

    @staticmethod
    def _convert(row):
        return Reservation(id=row[0], user_id=row[1], package_id=row[2],
                           reservation_date=row[3], travelers=row[4],
                           total_paid=row[5], status=row[6])

    # TODO (RF-11): insert(reservation) y descuento de cupos en la misma transaccion,
    #               creando las filas 'pending' de reservation_progress.
    # TODO (RF-12): list_by_user(user_id) -> historial del cliente autenticado.
