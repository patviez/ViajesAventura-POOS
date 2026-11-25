from menus.main_menu import run_authenticated_menu
from menus.user_menu import ask_client_registration, ask_login
from persistence.base_dao import DatabaseError
from persistence.create_db import create_tables
from seed import seed_initial_data


def main():
    create_tables()
    seed_initial_data()

    while True:
        print("\n" + "=" * 35)
        print("   BIENVENIDO A VIAJES AVENTURA")
        print("=" * 35)
        print("1. Iniciar sesión")
        print("2. Registrarse como cliente")
        print("0. Salir")
        option = input("\nSeleccione una opción: ").strip()

        try:
            if option == "1":
                session = ask_login()
                if session is not None:
                    run_authenticated_menu(session)
            elif option == "2":
                ask_client_registration()
            elif option == "0":
                print("\n¡Hasta pronto!")
                break
            else:
                print("\nOpción no válida.")
        except DatabaseError as error:
            print(f"\n{error}")


if __name__ == "__main__":
    main()
