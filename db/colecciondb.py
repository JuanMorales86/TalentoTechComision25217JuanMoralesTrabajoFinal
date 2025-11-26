from .conexion import get_db_conection

def create_database():
    conexion = get_db_conection()
    if not(conexion):
        return
    cursor = conexion.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS colecciones (
                id_coleccion INTEGER PRIMARY KEY,
                nombre_coleccion TEXT NOT NULL,
                tipo_coleccion TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL
                )
''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articulos (
            id_articulo INTEGER PRIMARY KEY,
            id_coleccion INTEGER NOT NULL,
            codigo_art TEXT UNIQUE,
            nombre_art TEXT NOT NULL,
            descripcion_art TEXT NOT NULL,
            ano_lanzamiento_art INTEGER NOT NULL,
            visto_art INTEGER NOT NULL,
            valoracion_art INTEGER,
            FOREIGN KEY(id_coleccion) REFERENCES colecciones(id_coleccion)
            ON DELETE CASCADE)   
''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiposdecolecciones (
                id_tipo INTEGER PRIMARY KEY,
                nombre_tipo TEXT NOT NULL UNIQUE
                )
''')
    

    conexion.commit()
    conexion.close()
    print("Base de datos y tablas creadas correctamente.")

if __name__ == '__main__':
    create_database()
