def ask(message, validator, reader=input):
    while True:
        try:
            return validator(reader(message))
        except (TypeError, ValueError) as error:
            print(f"{error} Intente nuevamente.")
