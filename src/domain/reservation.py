class Reservation:
    STATUSES = ("confirmed", "cancelled")

    def __init__(self, user_id, package_id, reservation_date, travelers,
                 total_paid, status="confirmed", id=None):
        self.id = id
        self.user_id = user_id
        self.package_id = package_id
        self.reservation_date = reservation_date
        self.travelers = self.validate_travelers(travelers)
        self.total_paid = total_paid
        if status not in self.STATUSES:
            raise ValueError("Estado de reserva no permitido.")
        self.status = status

    @staticmethod
    def validate_travelers(value):
        if type(value) is not int or value <= 0:
            raise ValueError("El número de viajeros debe ser un entero mayor que 0.")
        return value

    def calculate_total(self, package_cost):
        """RF-11: monto = costo del paquete x número de viajeros."""
        return package_cost * self.travelers

    def cancel(self):
        self.status = "cancelled"
