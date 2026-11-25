# Viajes Aventura

Sistema de consola en Python para gestionar destinos, paquetes turísticos, reservas y avance de viajes.
Proyecto TI3021 · Unidad 4 · Arquitectura en 3 capas (presentación, lógica de negocio, persistencia).

## Preparar el entorno

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # Windows: copy .env.example .env
```

Edite `.env` y defina `ADMIN_PASSWORD` (mínimo 8 caracteres). El `.env` real nunca se sube a Git.

## Ejecutar

```bash
python src/main.py
```

Al iniciar se crean las tablas en SQLite y la cuenta administradora indicada en `.env`.

## Probar la conexión a SQLite (evidencia del Hito 1)

```bash
python -m unittest discover -s tests -v
```

La prueba usa una base temporal, así que se puede repetir sin afectar los datos locales.
Verifica: creación de tablas, claves foráneas activas, contraseñas como hash bcrypt, login,
permisos por rol y la regla de no eliminar destinos que pertenecen a un paquete.

## Estructura

| Carpeta | Capa | Contenido |
|---|---|---|
| `src/menus/` | Presentación | Menús de consola y lectura de datos |
| `src/services/` | Lógica de negocio | Autenticación, permisos y reglas del negocio |
| `src/domain/` | Lógica de negocio | Entidades y validaciones |
| `src/persistence/` | Persistencia | Conexión, creación de tablas y DAO (único lugar con SQL) |
| `docs/` | Documentación | Requerimientos, modelo físico y diagramas |

## Convenciones

- Código Python y SQL en inglés; mensajes al usuario en español.
- Ramas: `prefijo/clave-jira-descripcion` (`feature/`, `fix/`, `docs/`).
- Todo cambio a `main` entra por pull request aprobado por el compañero. No se hace push directo.

## Estado de requerimientos

| Requerimiento | Estado |
|---|---|
| RF-01 a RF-04 (destinos) | Implementado (DAO y menú de referencia) |
| RF-05 a RF-08 (paquetes y disponibilidad) | Dominio listo (clase Package); falta DAO, servicio y menú |
| RF-09, RF-10 (registro y login) | Implementado |
| RF-11, RF-12 (reservas e historial) | Dominio listo (clase Reservation); falta DAO, servicio y menú |
| RF-13, RF-14 (avance del viaje) | Dominio listo (ReservationProgress); falta DAO, servicio y menú |
