from fastapi import Depends, FastAPI
from config_erp.database import obtener_conexion
from config_erp.api_security import validar_api_key

app = FastAPI(title="API ERP - Gestión Inteligente de Inventarios")


@app.get("/api/inventario/analisis-riesgo")
def analizar_riesgo_inventario(_api_key: None = Depends(validar_api_key)):
    """
    Consulta la información actual del inventario y las ventas
    de los últimos 30 días.

    La API entrega los datos necesarios para que los agentes
    Monitor, Analista y Comprador puedan realizar sus funciones.
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

                # Regla 1:
                # Demanda diaria promedio
                demanda_diaria = round(
                    ventas_30_dias / 30,
                    2
                )

                # Regla 2:
                # Días estimados hasta agotamiento
                if demanda_diaria > 0:
                    dias_hasta_agotamiento = round(
                        stock_actual / demanda_diaria,
                        2
                    )
                else:
                    dias_hasta_agotamiento = None

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
                    "demanda_diaria": demanda_diaria,
                    "dias_hasta_agotamiento": dias_hasta_agotamiento
                }

                productos.append(producto)

            return {
                "total_productos": len(productos),
                "periodo_analisis": "Últimos 30 días",
                "productos": productos
            }

    finally:
        conexion.close()