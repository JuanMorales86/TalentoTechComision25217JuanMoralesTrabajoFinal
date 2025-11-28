from db.conexion import get_db_conection
from utilities.verificador_input import verificador_de_inputs
from operaciones_read import operacion_read_collection_types
from utilities.excepciones import volver_al_menu, error_de_operacion
from utilities.print_estilo import print_personalized, print_for_titles



def update_art_collection():
    try:
        
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            input_tipo_coleccion = verificador_de_inputs('Busque una colección por tipo (o deje en blanco para ver todas): ', str.lower, '', lambda x: True)

            busqueda_real = input_tipo_coleccion if input_tipo_coleccion is not None else ""
            
            termino_busqueda = f'%{busqueda_real}%'

            cursor.execute('SELECT id_coleccion, nombre_coleccion, tipo_coleccion FROM colecciones WHERE tipo_coleccion LIKE ?', (termino_busqueda,))

            colecciones_disponi = cursor.fetchall()

            if not colecciones_disponi:
                raise error_de_operacion(f'No hay colecciones disponibles del tipo"{input_tipo_coleccion}".')

            print_for_titles('Colecciones disponibles:', 'subtitle', 50)
            mapa_collec = {}
            for id_coleccion, nombre_coleccion, tipo_coleccion in colecciones_disponi:
                mapa_collec[id_coleccion] = nombre_coleccion #relacion simple id - nombre
                print_personalized(f'Codigo_Coleccion: {id_coleccion} - Nombre: {nombre_coleccion} - Tipo: {tipo_coleccion}', "info")

            
            id_coleccion_seleccionado = verificador_de_inputs('Ingrese el codigo de coleccion para ver sus articulos: ', int, 'Debe ingresar un codigo de la lista.', lambda x: x in mapa_collec)

            if not id_coleccion_seleccionado:
                raise error_de_operacion('Coleccion no encontrada.')
            
            cursor.execute('SELECT id_articulo, codigo_art, nombre_art FROM articulos WHERE id_coleccion = ?',(id_coleccion_seleccionado,))

            articulo_en_coleccion = cursor.fetchall()

            if not articulo_en_coleccion:
                raise error_de_operacion(f'No hay articulos en la coleccion "{mapa_collec[id_coleccion_seleccionado]}".')

            mapa_articulos = {}
            print_for_titles('Articulos en la coleccion:', "title", 50)
            for id_articulo, codigo_art, nombre_art in articulo_en_coleccion:
                mapa_articulos[id_articulo] = nombre_art
                print_personalized(f'ID: {id_articulo} - Codigo: {codigo_art} - Nombre: {nombre_art}', "info")

            id_articulo_actualizar = verificador_de_inputs('Ingrese el ID del articulo a actualizar: ', int, 'Debe ingresar un ID de articulo valido.', lambda x: x in mapa_articulos)

            if not id_articulo_actualizar:
                raise error_de_operacion('No hay articulos con ese ID')
            
            cursor.execute('SELECT nombre_art, descripcion_art, ano_lanzamiento_art,visto_art, valoracion_art FROM articulos WHERE id_articulo = ?', (id_articulo_actualizar,))

            articulo_actual = cursor.fetchone()
            (nombre_actual, descrip_actual, ano_actual, visto_actual, valora_actual) = articulo_actual

            print_personalized('Ingrese los nuevos datos del articulo.', "info")
            print_personalized('Deje el campo en blanco si no desea actualizar.', "info")

            input_nombre_actualizar = verificador_de_inputs(f'Nuevo nombre [{nombre_actual}]: ', str.lower, '', lambda x: True)

            input_descripcion_actualizar = verificador_de_inputs(f'Nueva descripcion [{descrip_actual}]: ', str.lower, '', lambda x: True)

            input_ano_lanzamiento_actualizar = verificador_de_inputs(f'Nuevo año [{ano_actual}]: ', int, 'Año invalido', lambda x: (1900 < x < 2100) if x is not None else True)

            input_visto_actualizar = verificador_de_inputs(f'Visto? (si/no) [Actual: {"si" if visto_actual else "no" }]:  ', str.lower, 'Respuesta no válida.', lambda x: x in ['si', 'no', ''])

            input_valoracion_art = verificador_de_inputs(f'Valoracion (1-5) [Actual: {valora_actual}]: ', int, 'Valoracion Invalido', lambda x: (0 < x <= 5) if x is not None else True)

            if input_valoracion_art is None or input_valoracion_art == 0:
                input_valoracion_art = 0

            parametros = (
                input_nombre_actualizar or nombre_actual, input_descripcion_actualizar or descrip_actual, input_ano_lanzamiento_actualizar if input_ano_lanzamiento_actualizar is not None else ano_actual, (input_visto_actualizar == "si") if input_visto_actualizar else bool (visto_actual), input_valoracion_art if input_valoracion_art is not None else valora_actual, id_articulo_actualizar
            )

            cursor.execute('UPDATE articulos SET nombre_art = ?, descripcion_art = ?, ano_lanzamiento_art = ?, visto_art = ?, valoracion_art = ? WHERE id_articulo = ?', parametros)

            print_personalized(f'El articulo "{nombre_actual}" ha sido actualizado a "{input_nombre_actualizar or nombre_actual}".', "info")

    except volver_al_menu:
        print_personalized("Operación cancelada. Volviendo al menú principal.", "info")

    except error_de_operacion as e:
        print_personalized(f'Error: {e}', "error")

    except Exception as e:
        print_personalized(f'Error al actualizar el articulo: {e}', "error")

def update_collection():
    try:
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            cursor.execute('SELECT id_coleccion, nombre_coleccion FROM colecciones')
            colecciones_disponibles = cursor.fetchall()

            if not colecciones_disponibles:
                raise error_de_operacion('No hay colecciones disponibles para actualizar.')
            
            print_for_titles('Colecciones disponibles:', 'subtitle', 50)
            for id_coleccion, nombre_coleccion in colecciones_disponibles:
                print_personalized(f'Codigo_Coleccion: {id_coleccion} - Nombre: {nombre_coleccion}', "info")

            
            id_coleccion_actualizar = verificador_de_inputs('Ingrese el ID de la coleccion en cuestion: ', int, 'Debe ingresar un ID valido. ', lambda x: bool(x))

            cursor.execute('SELECT id_coleccion, nombre_coleccion FROM colecciones WHERE id_coleccion = ?', (id_coleccion_actualizar,))

            coleccion_actual = cursor.fetchone()

            if not coleccion_actual:
                raise error_de_operacion('Coleccion no encontrada.')
            
            id_coleccion_actual, nombre_coleccion_actual = coleccion_actual

            print_personalized(f'Coleccion actual: {nombre_coleccion_actual}', "info")
            print_personalized('----------------------------------------------------', "info")
            print_personalized('Ingrese los nuevos datos de la coleccion.', "info")
            print_personalized('Deje el campo en blanco si no desea actualizar.', "info")

            input_nombre_coleccion = verificador_de_inputs('Nuevo nombre de la coleccion: ', str.upper, '', lambda x: True)


            parametros = (input_nombre_coleccion or nombre_coleccion_actual, id_coleccion_actualizar)

            cursor.execute('UPDATE colecciones SET nombre_coleccion = ? WHERE id_coleccion = ?', parametros)

            print_personalized(f'La coleccion "{nombre_coleccion_actual}" ha sido actualizada a "{input_nombre_coleccion or nombre_coleccion_actual}".', "info")


    except volver_al_menu:
        print_personalized("Operación cancelada. Volviendo al menú principal.", "info")

    except error_de_operacion as e:
        print_personalized(f'Error: {e}', "error")

    except Exception as e:
        print_personalized(f'Error al actualizar la coleccion: {e}', "error")

def update_types_collection():
    try:
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            input_busca_usuario = verificador_de_inputs('Ingrese el nombre de el tipo de coleccion que quiere modificar: ', str, '', lambda x: True)

            busqueda_real = input_busca_usuario if input_busca_usuario is not None else ''

            termino_verificado = f'%{busqueda_real}%'

            cursor.execute('SELECT id_tipo, nombre_tipo FROM tiposdecolecciones WHERE nombre_tipo LIKE ?', (termino_verificado,))

            res_tipo = cursor.fetchall()

            if not res_tipo:
                raise error_de_operacion(f'No hay tipos de colecciones con ese: {input_busca_usuario}')

            mapa_tipo = {}
            for id_tipos , nombre_tipos in res_tipo:
                mapa_tipo[id_tipos] = nombre_tipos
                print_personalized(f'\n ID de Tipos: {id_tipos} -- Nombre de los Tipos: {nombre_tipos}', "info")
            

            id_seleccionado_tipo = verificador_de_inputs('Ingrese el id del tipo de coleccion a modificar: ', int, 'Debe ingresar un id valido', lambda x: x in mapa_tipo)

            
            cursor.execute('SELECT id_tipo, nombre_tipo FROM tiposdecolecciones WHERE id_tipo = ?', (id_seleccionado_tipo,))

            res_id_tipo = cursor.fetchone()
            
            if not res_id_tipo:
                raise error_de_operacion('No existe ese id con en el tipo de coleccion')
            
            id_tipo_actual, nombre_tipo_actual = res_id_tipo

            input_actualizar_tipo = verificador_de_inputs('Ingresar la actualizacion del nombre tipo: ', str.upper, '', lambda x: True)

            parametros = (
                input_actualizar_tipo or nombre_tipo_actual, id_seleccionado_tipo
            )

            cursor.execute('UPDATE tiposdecolecciones SET nombre_tipo = ? WHERE id_tipo = ?', parametros)

            print_personalized(f'El tipo de colección "{nombre_tipo_actual}" ha sido actualizado a "{input_actualizar_tipo or nombre_tipo_actual}".', "info")
    
    except volver_al_menu:
        print_personalized("Operación cancelada. Volviendo al menú principal.", "info")


    except error_de_operacion as e:
        print_personalized(f'Error {e}', "error")

    except ValueError as e:
        print_personalized(f'Error al actualizar en el sistema.{e}', "error" )
        return

if __name__ == '__main__':
    update_art_collection()
    update_collection()
    update_types_collection()
