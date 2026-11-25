class ReservationProgress:
    STATUSES = ("pending", "in_progress", "completed")

    def __init__(self, reservation_id, destination_id, status="pending",
                 registered_date=None, id=None):
        if status not in self.STATUSES:
            raise ValueError("Estado de avance no permitido.")
        self.id = id
        self.reservation_id = reservation_id
        self.destination_id = destination_id
        self.status = status
        self.registered_date = registered_date

    def start(self):
        self.status = "in_progress"

    def complete(self, date):
        if not date:
            raise ValueError("Debe indicar la fecha en que se completó la etapa.")
        self.status = "completed"
        self.registered_date = date
