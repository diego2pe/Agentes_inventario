from config_erp.database import obtener_conexion

try:
    conexion = obtener_conexion()

    print("CONEXIÓN EXITOSA A AIVEN")

    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM productos")
        resultado = cursor.fetchone()

        print("Cantidad de productos:", resultado["total"])

    conexion.close()

except Exception as e:
    print("ERROR DE CONEXIÓN:")
    print(e)