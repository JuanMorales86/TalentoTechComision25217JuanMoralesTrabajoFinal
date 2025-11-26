from db.conexion import get_db_conection
from operaciones_read import operacion_read_collection_types
from utilities.verificador_input import verificador_de_inputs
from utilities.auto_incre import auto_incrementar_id
from utilities.excepciones import volver_al_menu, error_de_operacion
from utilities.print_estilo import print_personalized, print_for_titles
from datetime import datetime

def create_art_in_collections():

    try:
        
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            input_tipo_coleccion = verificador_de_inputs('Busque una colección por tipo (o deje en blanco para ver todas): ', str.lower, '', lambda x: True)

            busqueda_real = input_tipo_coleccion if input_tipo_coleccion is not None else ""  # si el usuario deja el input en blanco, convertimos a una cadena vacia por que si no devuelve None como termino y cae en el if not q esta ams abajo

            termino_busqueda = f'%{busqueda_real}%'

            cursor.execute('SELECT id_coleccion, nombre_coleccion, tipo_coleccion FROM colecciones WHERE tipo_coleccion LIKE ?', (termino_busqueda,))

            colecciones_disponibles = cursor.fetchall()

            if not colecciones_disponibles:
                raise error_de_operacion(f'No hay colecciones disponibles del tipo "{input_tipo_coleccion}".')

            print('\n--- Colecciones Disponibles ---')

            # validar mejor la seleccion del ussuario agrupandolo en un diccionario id - nombre
            mapa_colecciones = {}
            for id_coleccion, nombre_coleccion, tipo_coleccion in colecciones_disponibles:
                mapa_colecciones[id_coleccion] = nombre_coleccion
                print_personalized(f'  [ID: {id_coleccion}] - Nombre: {nombre_coleccion} - Tipo: {tipo_coleccion}', "info")
            print('-----------------------------\n')

            id_coleccion_seleccionada = verificador_de_inputs('Ingrese el ID de la colección donde desea agregar el artículo: ',int, 'Debe ingresar un ID numérico válido que esté en la lista.', lambda x: x in mapa_colecciones)

            if id_coleccion_seleccionada is None:
                raise error_de_operacion('ID de colección no válido. Operación cancelada.')

            id_personalizable = auto_incrementar_id(cursor)

            input_nombre_ar = verificador_de_inputs('Ingrese el nombre del artículo: ', str.capitalize, 'Debe ingresar un nombre de artículo válido.', lambda x: bool(x))

            input_descrpcion_ar = verificador_de_inputs('Ingrese la descripción del artículo: ', str.lower, 'Debe ingresar una descripción válida.', lambda x: bool(x))

            input_ano_lanzamiento_ar = verificador_de_inputs('Ingrese el año de lanzamiento (si lo deja en blanco se le asignara la fecha actual): ', int, 'Debe ingresar un año válido (ej: 2023).', lambda x: x is not None and 1900 < x < 2100)

            if input_ano_lanzamiento_ar is None:
                input_ano_lanzamiento_ar = datetime.now().year

            visto_input = verificador_de_inputs('¿Ya ha visto/leído/jugado el artículo? (si/no): ', str.lower, 'Respuesta no válida.', lambda x: x in ['si', 'no', ''])
            input_visto_ar = (visto_input == 'si')

            input_valoracion_art = verificador_de_inputs('Ingrese la valoración del artículo (1-5) o déjelo en blanco: ', int, 'Debe ingresar una valoración válida (1-5).', lambda x: (0 < x <= 5) if x is not None else True)

            if input_valoracion_art is None:
                input_valoracion_art = 0

            parametros = (
                id_coleccion_seleccionada, id_personalizable, input_nombre_ar,
                input_descrpcion_ar, input_ano_lanzamiento_ar,
                input_visto_ar, input_valoracion_art
            )

            cursor.execute('''
                INSERT INTO articulos(id_coleccion,codigo_art, nombre_art, descripcion_art, ano_lanzamiento_art, visto_art, valoracion_art) VALUES (?,?,?,?,?,?,?)
            ''', parametros)

            # El commit es automático al menu o m del bloque 'with' sin errores.
            print_personalized('Articulo creado exitosamente.', "success")
            print(f'\nArtículo "{input_nombre_ar}" creado exitosamente en la colección "{mapa_colecciones[id_coleccion_seleccionada]}".')

    except volver_al_menu:
        print_personalized("Operación cancelada. Volviendo al menú principal.", "info")
        
    except error_de_operacion as e:
        print_personalized(f'Error: {e}', "error")

    except Exception as e:
        print_personalized(f'Error al crear el articulo: {e}', "error")

def create_colections():
    try:
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        input_nombre_col = verificador_de_inputs('Ingrese el nombre de la colección nueva: ', str, 'Debe ingresar un nombre válido.', lambda x: bool(x))

        tipos_disponibles = operacion_read_collection_types(imprimir=False)

        if not tipos_disponibles:
            raise error_de_operacion('No hay tipos de colecciones disponibles. Por favor, cree un tipo de colección antes de crear una colección.')

        print_for_titles("\n--- Seleccione el Tipo de Colección ---", "title", 50)
        for i, tipo in enumerate(tipos_disponibles, 1):
            print_personalized(f'  {i}. {tipo}', "info")
        print("-------------------------------------\n")

        opcion_tipo_num = verificador_de_inputs('Ingrese el número del tipo de colección: ', int, 'Debe ingresar un número de la lista.', lambda x: 1 <= x <= len(tipos_disponibles))

        if opcion_tipo_num is None:
            raise error_de_operacion('Número de tipo de colección no válido. Operación cancelada.')

        input_tipo_col = tipos_disponibles[opcion_tipo_num - 1]
        input_date_time = datetime.now().strftime('%Y-%m-%d')

        parametros = (input_nombre_col, input_tipo_col, input_date_time)

        with get_db_conection() as conexion:
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO colecciones(nombre_coleccion, tipo_coleccion, fecha_creacion) VALUES (?,?,?)', parametros)

        print(f'\nColección "{input_nombre_col}" creada exitosamente.')

    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")
    
    except error_de_operacion as e:
        print_personalized(f'\nError: {e}', "error")
        
    except Exception as e:
        print_personalized(f'Error al crear la coleccion: {e}', "error")

def create_types_collections():
    try:
        print_personalized('Escriba "menu o m" en cualquier momento para volver al menú principal.', "info")
        operacion_read_collection_types(imprimir=True)

        tipos_disponibles = operacion_read_collection_types(imprimir=False)

        input_nombre_tipo_coleccion = verificador_de_inputs('Ingresar un nombre descriptivo para un tipo de coleccion nueva: ', str.upper, 'Debe ingresar un nombre valido', lambda  x: bool(x))

        #es un for simplificado para convertir mayusculas o minusculas en la tabla y evitar duplicados
        tipos_disponibles_upper = [tipo.upper() for tipo in tipos_disponibles]

        if input_nombre_tipo_coleccion in tipos_disponibles_upper:
            raise error_de_operacion(f'El tipo de coleccion "{input_nombre_tipo_coleccion}" ya existe en la base de datos')
        
        with get_db_conection() as conexion:
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO tiposdecolecciones(nombre_tipo) VALUES(?)', (input_nombre_tipo_coleccion,))

        print_personalized(f'Tipo agregado exitosamente {input_nombre_tipo_coleccion}, a la base de datos ', "success")

    except volver_al_menu:
        print_personalized("\nOperación cancelada. Volviendo al menú principal.", "info")
        
    except error_de_operacion as e:
        print_personalized(f'\nError: {e}', "error")

    except Exception as e:
        print_personalized(f'Error en la creacion: {e}', "error")

if __name__ == '__main__':
    create_art_in_collections()
    create_colections()
    create_types_collections()
    
