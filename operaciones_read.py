from db.conexion import get_db_conection
from utilities.print_estilo import print_personalized, print_for_titles
from utilities.excepciones import error_de_operacion
from utilities.excepciones import volver_al_menu


def operacion_read_articles():
    try:
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            cursor.execute('SELECT * FROM articulos')
            articulos_leidas = cursor.fetchall()

            for id_art, id_col, codigo_art, nomb_art, descr_art, ano_lanz, visto_art, val_art in articulos_leidas:
                visto_lanza = 'Si' if visto_art else 'No'
                print_personalized(f'\nID: \t {id_art}, \nID Coleccion: \t {id_col}, \nCodigo Articulo: \t {codigo_art}, \nNombre: \t {nomb_art}, \nDescripcion: \t {descr_art}, \nAño Lanzamiento: \t {ano_lanz}, \nYa Visto?: \t {visto_lanza}, \nValoracion: \t {val_art}.', "info")
                print_personalized("---------------------------------------", "info")

    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")

    except error_de_operacion as e:
        print_personalized(f"Error: {e}", "error")

    except Exception as e:
        print_personalized(f"Error al leer los articulos: {e}", "error")

def operacion_read_collections():
    try:
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            cursor.execute('SELECT * FROM colecciones')
            colecciones_leidas = cursor.fetchall()

            for id_col, nombre, tipo_cole, fecha_cole in colecciones_leidas:
                print_personalized(f'\t Id de Coleccion: {id_col} - Nombre de Coleccion: {nombre} - Tipo de Coleccion: {tipo_cole} - Fecha de Creacion: {fecha_cole}', "info")
    
    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")

    except Exception as e:
        print_personalized(f"Error al leer las colecciones: {e}", "error")

def operacion_read_collection_types(imprimir=True):
    try:
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            cursor.execute('SELECT nombre_tipo FROM tiposdecolecciones')
            tipos_colecciones_leidas = cursor.fetchall()


            lista_de_tipos = [tipo[0] for tipo in tipos_colecciones_leidas] # aqui extraemos los nombres de los tipos de colecciones que llega como una tupla desde el fetchall y los ponemos en una lista de tipo string

            if imprimir:
                print_for_titles("--- Tipos de Colecciones Disponibles ---", "title", 40)
                if not lista_de_tipos:
                    print_personalized("No hay tipos de colecciones disponibles.", "info")
                else:
                    for id_db, nombre_db in enumerate(lista_de_tipos, 1):
                        print_personalized(f'\t {id_db} - {nombre_db}', "info")
                    print("---------------------------------------")
            return lista_de_tipos

    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")

    except error_de_operacion as e:
        print_personalized(f"Error: {e}", "error")

    except Exception as e:
        print(f"Error al leer los tipos de colecciones: {e}")
        return []

if __name__ == '__main__':
    operacion_read_articles()
    operacion_read_collections()
    operacion_read_collection_types()



