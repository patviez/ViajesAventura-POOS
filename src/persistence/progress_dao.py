from domain.progress import ReservationProgress
from persistence.base_dao import BaseDAO


class ProgressDAO(BaseDAO):
    TABLE = "reservation_progress"
    COLUMNS = "id, reservation_id, destination_id, status, registered_date"
    LABEL = "el avance del viaje"

    @staticmethod
    def _convert(row):
        return ReservationProgress(id=row[0], reservation_id=row[1], destination_id=row[2],
                                   status=row[3], registered_date=row[4])

    # TODO (RF-13): update_status(progress_id, status, date).
    # TODO (RF-14): list_by_reservation(reservation_id) ordenado por visit_order.
