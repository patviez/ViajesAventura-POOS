from datetime import date


class Package:
    MIN_DESTINATIONS = 2

    def __init__(self, name, start_date, end_date, available_slots, id=None):
        self.id = id
        self.name = self._validate_name(name)
        self.start_date, self.end_date = self.validate_dates(start_date, end_date)
        self.available_slots = self._validate_slots(available_slots)
        self.destinations = []

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del paquete no puede estar vacío.")
        return name.strip()

    @staticmethod
    def _validate_slots(value):
        if type(value) is not int or value < 0:
            raise ValueError("Los cupos deben ser un número entero mayor o igual a 0.")
        return value

    @staticmethod
    def validate_dates(start, end):
        try:
            start_d, end_d = date.fromisoformat(start), date.fromisoformat(end)
        except (TypeError, ValueError):
            raise ValueError("Las fechas deben tener el formato AAAA-MM-DD.")
        if end_d < start_d:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio.")
        return start, end

    def calculate_total_cost(self):
        return sum(destination.base_cost for destination in self.destinations)

    def is_available(self):
        return self.available_slots > 0
