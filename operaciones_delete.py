from db.conexion import get_db_conection
from utilities.verificador_input import verificador_de_inputs
from utilities.print_estilo import print_personalized, print_for_titles
from utilities.excepciones import volver_al_menu, error_de_operacion


def delete_art_collection():
    try:
       
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            while True:
                    
                    print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
                    print_personalized('\nBusque una colección por su tipo, o por el nombre/código de un artículo.', "info")
                    input_busqueda = verificador_de_inputs('Buscar: ', str.lower, 'Debe ingresar un término de búsqueda válido.', lambda x: bool(x))

                    if input_busqueda == 'menu' or input_busqueda == 'm':
                        return

                    termino_de_busqueda = f'%{input_busqueda}%'

                    cursor.execute('SELECT id_coleccion, nombre_coleccion, tipo_coleccion FROM colecciones WHERE tipo_coleccion LIKE ? UNION SELECT c.id_coleccion, c.nombre_coleccion, c.tipo_coleccion FROM colecciones c JOIN articulos a ON c.id_coleccion = a.id_coleccion WHERE a.nombre_art LIKE ? OR a.codigo_art LIKE ?' 
                    , (termino_de_busqueda, termino_de_busqueda, termino_de_busqueda))


                    colecciones_disponibles = cursor.fetchall()

                    if not colecciones_disponibles:
                        raise error_de_operacion(f'No se encontraron colecciones para el término "{input_busqueda}".')
                
                    mapa_de_collec = {}
                    for id, nombre, tipo in colecciones_disponibles:
                        mapa_de_collec[id] = nombre
                        print_personalized(f'Codigo_Coleccion: {id} - Nombre: {nombre} - Tipo: {tipo}', "info")

                    id_coleccion_select = verificador_de_inputs('Ingrese el codigo de la coleccion: ', int, 'Debe ingresar un codigo de la lista.', lambda x: x in mapa_de_collec)

                    if not id_coleccion_select:
                        raise error_de_operacion('Coleccion no encontrada.')

                    cursor.execute('SELECT id_articulo,nombre_art,codigo_art FROM articulos WHERE id_coleccion = ? ', (id_coleccion_select,))

                    articulos_en_colec = cursor.fetchall()

                    if not articulos_en_colec:
                        raise error_de_operacion(f'No hay articulos en la coleccion "{mapa_de_collec[id_coleccion_select]}".')

                    mapa_art = {}
                    print_for_titles("\n--- Artículos en esta Colección ---", "info", 40)
                    for id_art, nombre_art, codigo_art in articulos_en_colec:
                        mapa_art[id_art] = nombre_art
                        print_personalized(f'  [ID: {id_art}] - Nombre: {nombre_art} - Código: {codigo_art}', "info")
                    print_personalized("----------------------------------\n", "info")

                    id_articulo_selecc = verificador_de_inputs('Ingrese el ID del articulo a eliminar: ', int, 'Debe ingresar un ID de la lista.', lambda x: x is not None and x in mapa_art)

                    if not id_articulo_selecc:
                        raise error_de_operacion('Articulo no encontrado.')
                    
                    cursor.execute('DELETE FROM articulos WHERE id_articulo = ?', (id_articulo_selecc,))

                    print_personalized(f'El articulo "{mapa_art[id_articulo_selecc]}" (ID: {id_articulo_selecc}) ha sido eliminado correctamente.', "info")

                    otra_vez = verificador_de_inputs("¿Desea eliminar otro artículo? (s/n): ", str.lower, "Respuesta no válida.", lambda x: x in ['s', 'n'])
                    if otra_vez == 'n':
                        break 
    
    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")

    except error_de_operacion as e:
        print_personalized(f'Error: {e}', "error")

    except Exception as e:
        print_personalized(f'Error al eliminar el articulo: {e}', "error")
        
def delete_collection():
    try:    
            print_personalized('Busca una colección por su nombre, código o tipo para eliminarla.', "info")
            print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
            input_busqueda = verificador_de_inputs('Ingrese el nombre o código o tipo de la colección a eliminar: ', str, 'Debe ingresar un término de búsqueda válido.', lambda x: True)

            termino_real = input_busqueda if input_busqueda is not None else ""

            termino_de_busqueda = f'%{termino_real}%'

            with get_db_conection() as conexion:
                cursor = conexion.cursor()
                cursor.execute('SELECT id_coleccion, nombre_coleccion, tipo_coleccion FROM colecciones WHERE nombre_coleccion LIKE ? OR id_coleccion LIKE ? OR tipo_coleccion LIKE ?', (termino_de_busqueda, termino_de_busqueda, termino_de_busqueda))

                colecciones_encontradas = cursor.fetchall()

                if not colecciones_encontradas:
                    raise error_de_operacion(f'No se encontraron colecciones para el término "{input_busqueda}".')
                
                print_personalized("\n--- Colecciones Encontradas ---", "info")
                mapa_colec = {}
                for id_col, nombre_col, tipo_col in colecciones_encontradas:
                    mapa_colec[id_col] = nombre_col
                    print_personalized(f'  [ID: {id_col}] - Nombre: {nombre_col} - Tipo: {tipo_col}', "info")
                print_personalized("----------------------------------\n", "info")

                id_coleccion_eliminar = verificador_de_inputs('Ingrese el ID de la coleccion a eliminar: ', int, 'Debe ingresar un ID de la lista.', lambda x: x is not None and x in mapa_colec)


                if not id_coleccion_eliminar:
                    raise error_de_operacion('Colección no encontrada.')
                
                print_personalized('Advertencia: Al eliminar una colección, se eliminarán todos los artículos asociados a ella debido a que estan enlazados', "info")

                print_personalized('Desea continuar con la eliminación de la colección y sus artículos asociados?', "info")
                confirmar = verificador_de_inputs('Escriba "si" para confirmar o "no" para cancelar: ', str.lower, 'Respuesta no válida.', lambda x: x in ['si', 'no'])

                if confirmar != 'si':
                    print_personalized('Eliminación cancelada.', "info")
                    return
                
                cursor.execute('DELETE FROM colecciones WHERE id_coleccion = ?', (id_coleccion_eliminar,))

                print_personalized(f'La colección "{mapa_colec[id_coleccion_eliminar]}" (ID: {id_coleccion_eliminar}) ha sido eliminada correctamente.', "info")

    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")
    
    except error_de_operacion as e:
        print_personalized(f'Error: {e}', "error")

    except Exception as e:
        print_personalized(f'Error al eliminar la coleccion: {e}', "error")

if __name__ == '__main__':
    delete_art_collection()
    delete_collection()
