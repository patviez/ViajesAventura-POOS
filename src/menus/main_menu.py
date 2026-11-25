from menus.destination_menu import manage_destinations
from menus.package_menu import check_availability, manage_packages
from menus.reservation_menu import (make_reservation, register_progress,
                                    show_history, show_progress)

ADMIN_OPTIONS = {
    "1": ("Gestionar destinos", manage_destinations),
    "2": ("Gestionar paquetes", manage_packages),
    "3": ("Consultar disponibilidad", check_availability),
    "4": ("Registrar avance de un viaje", register_progress),
    "5": ("Consultar avance de un viaje", show_progress),
}

CLIENT_OPTIONS = {
    "1": ("Consultar disponibilidad", check_availability),
    "2": ("Reservar un paquete", make_reservation),
    "3": ("Ver mi historial de reservas", show_history),
}


def run_authenticated_menu(session):
    options = ADMIN_OPTIONS if session["role"] == "admin" else CLIENT_OPTIONS
    while True:
        print(f"\n***** Viajes Aventura | {session['full_name']} ({session['role']}) *****")
        for key, (label, _) in options.items():
            print(f"{key}. {label}")
        print("9. Cerrar sesión")
        choice = input("\nSeleccione una opción: ").strip()

        if choice == "9":
            print("Sesión cerrada.")
            return
        if choice in options:
            options[choice][1](session)
        else:
            print("Opción no válida.")
