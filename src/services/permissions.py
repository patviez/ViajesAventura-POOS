def require_session(session):
    if not isinstance(session, dict) or session.get("role") not in ("admin", "client"):
        raise PermissionError("Inicie sesión para continuar.")
    if type(session.get("id")) is not int:
        raise PermissionError("Sesión inválida.")


def require_admin(session):
    require_session(session)
    if session["role"] != "admin":
        raise PermissionError("Acción permitida solo para el administrador.")


def require_client(session):
    require_session(session)
    if session["role"] != "client":
        raise PermissionError("Acción permitida solo para clientes.")
