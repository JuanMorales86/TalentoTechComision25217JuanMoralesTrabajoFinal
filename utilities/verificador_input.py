from .print_estilo import print_personalized
from .excepciones import volver_al_menu


def verificador_de_inputs(prompt, input_type=str, error_message="Entrada no valida.", validation_function=None):
    '''
    Verifica y valida la entrada del usuario.
    Todo la funcion la hago para manejar modularmente los inputs y validaciones 
    '''
    while True:
        user_input = input(prompt).strip()

        if user_input.lower() == 'menu' or user_input.lower() == 'm':
            raise volver_al_menu()
        
        # Si la entrada esta vacia
        if not user_input:
            # Si la función de validación existe y acepta None, devolvemos None sin error.
            if validation_function and validation_function(None):
                return None
            # Si es un string, una cadena vacia es valida.
            if input_type == str and (validation_function is None or validation_function("")):
                return ""

        try:
            value = input_type(user_input)# formateo el input al tipo que quiero
            if validation_function is None or validation_function(value):
                return value
            else:
                print_personalized(error_message, "error")
        except ValueError:
            print_personalized(error_message, "error")