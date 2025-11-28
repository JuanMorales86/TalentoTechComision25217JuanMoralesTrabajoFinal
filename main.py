# Gestor de Coleccion Digital 
from chekeo_configuracion import check_status_db
from operaciones_read import operacion_read_articles, operacion_read_collections,operacion_read_collection_types
from operaciones_create import create_art_in_collections, create_colections, create_types_collections
from operaciones_update import update_art_collection, update_collection, update_types_collection
from operaciones_delete import delete_art_collection, delete_collection
from utilities.print_estilo import print_personalized, print_for_titles


menu_principal = [
    "1. Gestionar Artículos", 
    "2. Gestionar Colecciones", 
    "3. Gestionar Tipos de Colecciones", 
    "4. Salir del Sistema"
]

menu_articulos = [
    "1. Listar todos los Artículos", 
    "2. Agregar un Artículo nuevo", 
    "3. Modificar un Artículo existente", 
    "4. Eliminar un Artículo", 
    "5. Volver al Menú Principal"
]

menu_colecciones = [
    "1. Listar todas las Colecciones", 
    "2. Agregar una Colección nueva", 
    "3. Modificar una Colección existente", 
    "4. Eliminar una Colección", 
    "5. Volver al Menú Principal"
]

menu_tipos = [
    "1. Listar Tipos de Colecciones", 
    "2. Agregar un Tipo de Colección", 
    "3. Modificar un Tipo de Colección", 
    "4. Eliminar un Tipo de Colección",
    "5. Volver al Menú Principal"
]

def user_monitor(titulo, menu_lista):
    print_personalized("\n-----------------------------------------------------------------------------------------", "title")
    print_for_titles(titulo, "title", 100)
    print_personalized("-----------------------------------------------------------------------------------------\n", "title")

    for opcion in menu_lista:
        print_personalized(opcion, "options")

def gestionar_articulos():
    while True:
        user_monitor("--- Gestión de Artículos ---", menu_articulos)
        seleccion = input("Seleccione una opción: ")
        match seleccion:
            case '1': operacion_read_articles()
            case '2': create_art_in_collections()
            case '3': update_art_collection()
            case '4': delete_art_collection()
            case '5': break
            case _: print_personalized("Opción no válida.", "error")

def gestionar_colecciones():
    while True:
        user_monitor("--- Gestión de Colecciones ---", menu_colecciones)
        seleccion = input("Seleccione una opción: ")
        match seleccion:
            case '1': operacion_read_collections()
            case '2': create_colections()
            case '3': update_collection()
            case '4': delete_collection()
            case '5': break
            case _: print_personalized("Opción no válida.", "error")

def gestionar_tipos_de_colecciones():
    while True:
        user_monitor("--- Gestión de Tipos de Colección ---", menu_tipos)
        seleccion = input("Seleccione una opción: ")
        match seleccion:
            case '1': operacion_read_collection_types(imprimir=True)
            case '2': create_types_collections()
            case '3': update_types_collection()
            case '5': break
            case _: print_personalized("Opción no válida.", "error")

def main():
    user_monitor("Bienvenido al Gestor de Colección Digital", ["Gestiona tus colecciones de Libros, Música, Videojuegos y Películas"])
    while True:
        user_monitor("--- Menú Principal ---", menu_principal)
        selection = input("Seleccione una opción del menú: ")

        match selection:
            case '1': gestionar_articulos()
            case '2': gestionar_colecciones()
            case '3': gestionar_tipos_de_colecciones()
            case '4':
                print_personalized("Saliendo del sistema...", "warning")
                break
            case _:
                print_personalized("Opción no válida. Por favor, seleccione una opción del menú.", "error")
                continue
            

if __name__ == '__main__':
    check_status_db()
    main()
