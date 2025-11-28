from colorama import Fore, Back, Style, init

init(autoreset=True)

def print_personalized(message, type = "info"):
    """
    Imprime mensajes personalizados en la consola con diferentes estilos según el tipo de mensaje.
    """
    match type:
        case "info":
            print(Fore.LIGHTBLUE_EX + Back.WHITE + Style.BRIGHT + message)
        case "success":
            print(Fore.WHITE + Back.GREEN + Style.BRIGHT + message)
        case "warning":
            print(Fore.BLACK + Back.YELLOW + Style.BRIGHT + message)
        case "error":
            print(Fore.WHITE + Back.RED + Style.BRIGHT + message)
        case "title":
            print(Back.BLACK + Fore.WHITE + Style.BRIGHT + message)
        case "options":
            print(Fore.RED + Style.BRIGHT + message)
        case _:
            print(message)

def print_for_titles(message, type = "title", ancho_terminal = 100):

    match type:
        case "title":
            print(Back.BLACK + Fore.YELLOW + Style.BRIGHT + message.center(ancho_terminal))
        case _:
            print(message)