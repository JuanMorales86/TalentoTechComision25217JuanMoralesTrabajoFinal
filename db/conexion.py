import sqlite3
import os

def get_db_conection():
    try:

        db_path = os.path.join(os.path.dirname(__file__), "master_data.db")# esto asegura que la base de datos se cree en la misma carpeta que el archivo conexion.py y evita problemas de rutas relativas. ya que se me estaba creando de nuevo el archivo de db y me daba error, cuando lo llamaba fuera de la carpeta db.

        conexion = sqlite3.connect(db_path)# Conectar a la base de datos SQLite

        conexion.execute("PRAGMA foreign_keys = ON;")# habilitar claves foraneas
        
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar ala base de datos: {e}")
        return None 