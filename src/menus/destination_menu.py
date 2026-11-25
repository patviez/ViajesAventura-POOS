from domain.destination import Destination
from inputs import ask
from persistence.base_dao import DatabaseError
from services import destination_service as service


def manage_destinations(session):
    while True:
        print("\n--- Gestión de destinos ---")
        print("1. Registrar destino")
        print("2. Listar destinos")
        print("3. Modificar destino")
        print("4. Eliminar destino")
        print("0. Volver")
        option = input("Opción: ").strip()

        try:
            if option == "1":
                _register(session)
            elif option == "2":
                _list(session)
            elif option == "3":
                _modify(session)
            elif option == "4":
                _delete(session)
            elif option == "0":
                return
            else:
                print("Opción no válida.")
        except (ValueError, TypeError, PermissionError, DatabaseError) as error:
            print(f"\n{error}")


def _register(session):
    name = ask("Nombre: ", lambda v: Destination.validate_text(v, "El nombre", 80))
    description = ask("Descripción: ", lambda v: Destination.validate_text(v, "La descripción", 500))
    activities = ask("Actividades: ", lambda v: Destination.validate_text(v, "Las actividades", 500))
    cost = ask("Costo base: ", Destination.validate_cost)
    created = service.create_destination(session, name, description, activities, cost)
    print(f"Destino registrado con ID {created.id}.")


def _list(session):
    destinations = service.list_destinations(session)
    if not destinations:
        print("No hay destinos registrados.")
    for destination in destinations:
        print(destination)


def _modify(session):
    destination_id = ask("ID del destino: ", int)
    current = next((d for d in service.list_destinations(session) if d.id == destination_id), None)
    if current is None:
        raise ValueError("El destino no existe.")
    print("(Deje vacío para mantener el valor actual)")
    name = input(f"Nombre [{current.name}]: ").strip() or current.name
    description = input(f"Descripción [{current.description}]: ").strip() or current.description
    activities = input(f"Actividades [{current.activities}]: ").strip() or current.activities
    cost = input(f"Costo base [{current.base_cost}]: ").strip() or current.base_cost
    service.update_destination(session, destination_id, name, description, activities, cost)
    print("Destino modificado.")


def _delete(session):
    destination_id = ask("ID del destino a eliminar: ", int)
    service.delete_destination(session, destination_id)
    print("Destino eliminado.")
