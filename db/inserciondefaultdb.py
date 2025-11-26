from .conexion import get_db_conection
from utilities.auto_incre import auto_incrementar_id
from utilities.print_estilo import print_personalized


def database_insert_default():
    try:

        with get_db_conection() as conexion:
            cursor = conexion.cursor()

            tipos_de_coleccion = [("PELICULAS",), ("SERIES",), ("LIBROS",), ("COMICS",), ("REVISTAS",), ("VIDEO JUEGOS",)]

            cursor.executemany('''
                INSERT INTO tiposdecolecciones(nombre_tipo) VALUES (?)
        ''', tipos_de_coleccion)
            
            cursor.execute('''
                INSERT INTO colecciones(nombre_coleccion, tipo_coleccion, fecha_creacion) VALUES (?,?,?)
        ''', ("Peliculas de Terror", "PELICULAS", "2023-01-15"))
            
            id_nueva_coleccion = cursor.lastrowid #Obtener el ID de la coleccion recien creada

            cursor.execute('''
                INSERT INTO colecciones(nombre_coleccion, tipo_coleccion, fecha_creacion) VALUES (?,?,?)
        ''', ("Juegos de Accion", "VIDEO JUEGOS", "2023-01-15"))            
            
            id_nueva_coleccion2 = cursor.lastrowid 

            cursor.execute('''
                INSERT INTO colecciones(nombre_coleccion, tipo_coleccion, fecha_creacion) VALUES (?,?,?)
        ''', ("Juegos de ROL", "VIDEO JUEGOS", "2023-01-15"))            
            
            id_nueva_coleccion3 = cursor.lastrowid 

            
            id_incrementador1 = auto_incrementar_id(cursor)

            cursor.execute('''
                INSERT INTO articulos(id_coleccion,codigo_art, nombre_art, descripcion_art, ano_lanzamiento_art, visto_art, valoracion_art) VALUES (?,?,?,?,?,?,?)
        ''', (id_nueva_coleccion, id_incrementador1,"El Resplandor", "Una película de terror psicológico", 1980, False, 0))
            
            id_incrementador2 = auto_incrementar_id(cursor)

            cursor.execute('''
                INSERT INTO articulos(id_coleccion,codigo_art, nombre_art, descripcion_art, ano_lanzamiento_art,visto_art,valoracion_art) VALUES(?,?,?,?,?,?,?)
        ''', (id_nueva_coleccion, id_incrementador2 , "It", "Una película basada en la novela de Stephen King", 2017, True, 0))
            
            id_incrementador3 = auto_incrementar_id(cursor)
            
            cursor.execute('''
                INSERT INTO articulos(id_coleccion,codigo_art, nombre_art, descripcion_art, ano_lanzamiento_art,visto_art,valoracion_art) VALUES(?,?,?,?,?,?,?)
        ''', (id_nueva_coleccion3, id_incrementador3 , "Persona 5", "Video Juego de RPG", 2017, False, 5))
            
            id_incrementador4 = auto_incrementar_id(cursor)

            cursor.execute('''
                INSERT INTO articulos(id_coleccion,codigo_art, nombre_art, descripcion_art, ano_lanzamiento_art,visto_art,valoracion_art) VALUES(?,?,?,?,?,?,?)
        ''', (id_nueva_coleccion2, id_incrementador4 , "Battlefield 6", "Video Juego de First Person Shooter", 2025, True, 5))
            
            print("Datos por defecto insertados correctamente en la base de datos.")


    except Exception as e:
        print_personalized(f"Error al insertar datos por defecto: {e}", "error")


if __name__ == '__main__':
    database_insert_default()
