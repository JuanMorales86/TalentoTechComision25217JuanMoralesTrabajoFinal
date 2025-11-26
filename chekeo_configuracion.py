import os
from db.colecciondb import create_database
from db.inserciondefaultdb import database_insert_default



def check_status_db():
    try:
        db_folder = os.path.join(os.path.dirname(__file__), 'db')#crear la ruta absoluta donde debria estar el archivo de db
        db_path = os.path.join(db_folder, "master_data.db")#aqui se crea la ruta completa del archivo db 

        if os.path.exists(db_path):
            print("La base de datos ya existe.")
            print("......Iniciando aplicación.")
        else:
            print("Primera ejecución detectada. Configurando la base de datos...")
            create_database()
            database_insert_default()
            print("¡Configuración inicial completada con éxito!")
    except Exception as e:
        print(f"Error durante la configuración inicial: {e}")
        exit()#si falla la configuracion, "falla" no tiene sentido seguir ejecutando la app

if __name__ == '__main__':
    check_status_db()