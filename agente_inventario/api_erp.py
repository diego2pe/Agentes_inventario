from fastapi import Depends, FastAPI
from config_erp.database import obtener_conexion
from config_erp.api_security import validar_api_key

app = FastAPI(title="API ERP - Gestión Inteligente de Inventarios")


@app.get("/api/inventario/analisis-riesgo")
def analizar_riesgo_inventario(_api_key: None = Depends(validar_api_key)):
    """
    Consulta únicamente los datos almacenados en el inventario,
    proveedores y ventas de los últimos 30 días. Los cálculos de
    demanda y riesgo se realizan en las reglas del sistema.

    La API no calcula demanda, riesgo ni cantidades de reposición;
    devuelve los campos base para que el sistema aplique sus reglas.
    """

    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:

            sql = """
                SELECT
                    p.id,
                    p.nombre,
                    p.categoria,
                    p.stock_actual,
                    p.stock_minimo,
                    p.stock_maximo,
                    p.precio_compra,

                    pr.id AS proveedor_id,
                    pr.nombre AS proveedor,
                    pr.tiempo_entrega_dias,

                    COALESCE(SUM(v.cantidad), 0) AS ventas_ultimos_30_dias

                FROM productos p

                INNER JOIN proveedores pr
                    ON p.proveedor_id = pr.id

                LEFT JOIN ventas v
                    ON p.id = v.producto_id
                    AND v.fecha >= NOW() - INTERVAL 30 DAY

                GROUP BY
                    p.id,
                    p.nombre,
                    p.categoria,
                    p.stock_actual,
                    p.stock_minimo,
                    p.stock_maximo,
                    p.precio_compra,
                    pr.id,
                    pr.nombre,
                    pr.tiempo_entrega_dias

                ORDER BY p.id;
            """

            cursor.execute(sql)

            productos_db = cursor.fetchall()

            productos = []

            for p in productos_db:

                # Convertimos los valores de la BD a tipos
                # compatibles con JSON.
                stock_actual = int(p["stock_actual"])
                stock_minimo = int(p["stock_minimo"])
                stock_maximo = int(p["stock_maximo"])

                ventas_30_dias = int(p["ventas_ultimos_30_dias"])

                producto = {
                    "id": int(p["id"]),
                    "nombre": p["nombre"],
                    "categoria": p["categoria"],

                    "stock_actual": stock_actual,
                    "stock_minimo": stock_minimo,
                    "stock_maximo": stock_maximo,

                    "precio_compra": float(p["precio_compra"]),

                    "proveedor_id": int(p["proveedor_id"]),
                    "proveedor": p["proveedor"],
                    "tiempo_entrega_dias": int(
                        p["tiempo_entrega_dias"]
                    ),

                    "ventas_ultimos_30_dias": ventas_30_dias,
                }

                productos.append(producto)

            return {
                "total_productos": len(productos),
                "periodo_analisis": "Últimos 30 días",
                "productos": productos
            }

    finally:
        conexion.close()
