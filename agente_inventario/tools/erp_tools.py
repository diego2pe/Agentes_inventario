from crewai.tools import tool

from services.erp_client import obtener_analisis_inventario
from rules.inventory_rules import analizar_producto


@tool("Consultar Inventario ERP")
def obtener_alertas_stock(**kwargs) -> str:
    """
    Consulta el inventario actual del ERP y obtiene la información
    necesaria para identificar productos que requieren análisis.
    """

    try:
        datos = obtener_analisis_inventario()

        productos = datos.get("productos", [])

        if not productos:
            return "No hay productos registrados en el ERP."

        resultado = "PRODUCTOS QUE REQUIEREN ATENCIÓN\n\n"
        productos_con_alerta = []

        for p in productos:

            analisis = analizar_producto(p)

            # El Monitor recibe únicamente productos sin stock, con riesgo
            # distinto de NORMAL o con una cantidad de reposición positiva.
            if (
                analisis["nivel_riesgo"] == "NORMAL"
                and not analisis["necesita_reposicion"]
            ):
                continue

            productos_con_alerta.append((p, analisis))

        if not productos_con_alerta:
            return "No hay productos sin stock, con riesgo o que requieran reposición."

        for p, analisis in productos_con_alerta:

            resultado += f"""
                PRODUCTO: {p['nombre']}
                ID: {p['id']}
                Categoría: {p['categoria']}

                Stock actual: {p['stock_actual']}
                Stock mínimo: {p['stock_minimo']}
                Stock máximo: {p['stock_maximo']}

                Ventas últimos 30 días: {p['ventas_ultimos_30_dias']}
                Demanda diaria promedio: {analisis['demanda_diaria']}
                Días estimados hasta agotamiento: {analisis['dias_hasta_agotamiento']}
                Nivel de riesgo: {analisis['nivel_riesgo']}
                Necesita reposición: {analisis['necesita_reposicion']}
                Stock de seguridad: {analisis['stock_seguridad']}
                Stock objetivo: {analisis['stock_objetivo']}
                Cantidad recomendada: {analisis['cantidad_recomendada']}
                Momento de reposición: {analisis['momento_reposicion']}

                Proveedor: {p['proveedor']}
                Tiempo de entrega: {p['tiempo_entrega_dias']} días
                Precio de compra: S/ {p['precio_compra']}

                ----------------------------------------
                """

        return resultado

    except Exception as e:
        return f"Error procesando información del ERP: {str(e)}"


@tool("Enviar Recomendación de Compra")
def enviar_orden_whatsapp(mensaje: str) -> str:
    """
    Simula el envío de una recomendación de compra.
    
    Por ahora no realiza un envío real.
    """

    from datetime import datetime

    return f"""
RECOMENDACIÓN DE COMPRA GENERADA

Mensaje:
{mensaje}

Fecha:
{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
