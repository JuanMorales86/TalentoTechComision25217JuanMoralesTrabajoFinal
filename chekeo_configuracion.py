import os
from db.colecciondb import create_database
from db.inserciondefaultdb import database_insert_default
from utilities.print_estilo import print_personalized



def check_status_db():
    try:
        db_folder = os.path.join(os.path.dirname(__file__), 'db')#creo la ruta absoluta donde debria estar el archivo de db
        db_path = os.path.join(db_folder, "master_data.db")#se crea la ruta completa del archivo db (algo de node parecido para buscar carpetas desde la raiz desde cualquier maquina q se instale)

        if os.path.exists(db_path):
            print_personalized('\n----------------------------------', "warning")
            print_personalized("La base de datos ya existe.", "success")
            print_personalized("......Iniciando aplicación.", "warning")
        else:
            print_personalized('\n----------------------------------', "warning")
            print_personalized("Primera ejecución detectada. Configurando la base de datos...", "warning")
            create_database()
            database_insert_default()
            print_personalized("¡Configuración inicial completada con éxito!", "success")
            print_personalized('......Iniciando aplicación', "warning")
    except Exception as e:
        print_personalized(f"Error durante la configuración inicial: {e}", "error")
        exit()#si falla la configuracion. "FALLA" no tiene sentido seguir ejecutando la appp

if __name__ == '__main__':
    check_status_db()