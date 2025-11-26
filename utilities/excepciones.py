class volver_al_menu(Exception):
    """Excepción para volver al menú principal desde cualquier input."""
    pass


class error_de_operacion(Exception):
    """Excepción para errores controldos durante operaciones CRUD."""
    pass