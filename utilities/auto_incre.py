from .print_estilo import print_personalized

def auto_incrementar_id(cursor):
    try:
        cursor.execute('SELECT codigo_art FROM articulos ORDER BY codigo_art DESC LIMIT 1')
        ultimo_codigo = cursor.fetchone()

        if ultimo_codigo:
            numero_actual = int(ultimo_codigo[0].split('_')[1])
            numero_nuevo = numero_actual + 1
            return f"COLE_{numero_nuevo:03d}"
        else:
            return "COLE_001"
    except Exception as e:
        print_personalized(f"Error al auto incrementar el ID: {e}", "error")
        return None
