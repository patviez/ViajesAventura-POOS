from domain.destination import Destination
from persistence.destination_dao import DestinationDAO
from services.permissions import require_admin


def create_destination(session, name, description, activities, base_cost):
    require_admin(session)
    destination = Destination(name, description, activities, base_cost)
    return DestinationDAO.insert(destination)


def list_destinations(session):
    require_admin(session)
    return DestinationDAO.list_all()


def update_destination(session, destination_id, name, description, activities, base_cost):
    require_admin(session)
    if DestinationDAO.find_by_id(destination_id) is None:
        raise ValueError("El destino no existe.")
    destination = Destination(name, description, activities, base_cost, id=destination_id)
    return DestinationDAO.update(destination)


def delete_destination(session, destination_id):
    require_admin(session)
    if DestinationDAO.find_by_id(destination_id) is None:
        raise ValueError("El destino no existe.")
    if DestinationDAO.is_in_package(destination_id):
        raise ValueError("No se puede eliminar: el destino pertenece a un paquete.")
    return DestinationDAO.delete(destination_id)
