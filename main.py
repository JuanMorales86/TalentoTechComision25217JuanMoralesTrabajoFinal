# Gestor de Coleccion Digital 
from chekeo_configuracion import check_status_db
from operaciones_read import operacion_read_articles, operacion_read_collections,operacion_read_collection_types
from operaciones_create import create_art_in_collections, create_colections, create_types_collections
from operaciones_update import update_art_collection, update_collection
from operaciones_delete import delete_art_collection, delete_collection
from utilities.print_estilo import print_personalized, print_for_titles



def user_monitor():

    titulo = "Bienvenido al Gestor de Coleccion Digital"
    subtitulo = "Gestiona tus colecciones de Libros, Música, Videojuegos y Películas"
    titulo_menu = "--- Menú de Opciones ---"
    print_personalized("\n-----------------------------------------------------------------------------------------", "title")
    print_for_titles(titulo, "title", 100)
    print_for_titles(subtitulo, "title", 100)
    print_for_titles(titulo_menu, "title", 100)
    print_personalized("-----------------------------------------------------------------------------------------\n", "title")

    menu = ["1. Agregar Articulos", "2. Actualizar Articulos","3. Eliminar Articulos", "4. Buscar Articulos", "5. Listar Colecciones", "6. Agregar una Coleccion", "7, Actualizar una Coleccion", "8. Eliminar una Coleccion", "9. Listar Tipos de Colecciones", "10. Agregar un Tipo de Coleccion", "11. Salir del Sistema"]

    for opcion in menu:
        print_personalized(opcion, "options")

def user_monitor_rerun():
    print_personalized("\n-----------------------------------------------------------------------------------------", "title")
    print_for_titles("Volviendo al Menú Principal...", "info", 100)
    print_personalized("-----------------------------------------------------------------------------------------\n", "title")

    menu = ["1. Agregar Articulos", "2. Actualizar Articulos","3. Eliminar Articulos", "4. Buscar Articulos", "5. Listar Colecciones", "6. Agregar una Coleccion", "7, Actualizar una Coleccion", "8. Eliminar una Coleccion", "9. Listar Tipos de Colecciones", "10. Agregar un Tipo de Coleccion", "11. Salir del Sistema"]

    for opcion in menu:
        print_personalized(opcion, "options")

def main():
    
    while True:
        if 'selection' in locals(): # me devuelve un diccionario con las variables locales, yo lo hago con el fin de que no se imprima la bienvenida dos veces al usar recurrentemente el menu
            user_monitor_rerun()
        else:
            user_monitor()

        selection = input("Seleccione una opción del menú: ")

        match selection:
            case '1':
                create_art_in_collections()
            case '2':
                update_art_collection()
            case '3':
                delete_art_collection()
            case '4':
                operacion_read_articles()
            case '5':
                operacion_read_collections()
            case '6':
                create_colections()
            case '7':
                update_collection()
            case '8':
                delete_collection()
            case '9':
                operacion_read_collection_types(imprimir=True)
            case '10':
                create_types_collections()
            case '11':
                print_personalized("Saliendo del sistema...", "warning")
                break
            case _:
                print_personalized("Opción no válida. Por favor, seleccione una opción del menú.", "error")
                continue
            

if __name__ == '__main__':
    check_status_db()
    main()
