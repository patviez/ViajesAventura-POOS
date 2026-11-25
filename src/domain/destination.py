class Destination:
    def __init__(self, name, description, activities, base_cost, id=None):
        self.id = id
        self.name = self.validate_text(name, "El nombre", 80)
        self.description = self.validate_text(description, "La descripción", 500)
        self.activities = self.validate_text(activities, "Las actividades", 500)
        self.base_cost = self.validate_cost(base_cost)

    @staticmethod
    def validate_text(value, label, max_length):
        if not isinstance(value, str):
            raise TypeError(f"{label} debe ser texto.")
        value = value.strip()
        if not value:
            raise ValueError(f"{label} no puede estar vacío.")
        if len(value) > max_length:
            raise ValueError(f"{label} admite como máximo {max_length} caracteres.")
        return value

    @staticmethod
    def validate_cost(value):
        try:
            cost = float(value)
        except (TypeError, ValueError):
            raise ValueError("El costo base debe ser un número.")
        if cost < 0:
            raise ValueError("El costo base no puede ser negativo.")
        return cost

    def __str__(self):
        return f"[{self.id}] {self.name} - ${self.base_cost:,.0f} | {self.activities}"
