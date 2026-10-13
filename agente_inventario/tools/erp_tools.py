from crewai.tools import tool

from services.erp_client import obtener_analisis_inventario


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

        resultado = "INVENTARIO ACTUAL DEL ERP\n\n"

        for p in productos:

            resultado += f"""
                PRODUCTO: {p['nombre']}
                ID: {p['id']}
                Categoría: {p['categoria']}

                Stock actual: {p['stock_actual']}
                Stock mínimo: {p['stock_minimo']}
                Stock máximo: {p['stock_maximo']}

                Ventas últimos 30 días: {p['ventas_ultimos_30_dias']}
                Demanda diaria promedio: {p['demanda_diaria']}
                Días estimados hasta agotamiento: {p['dias_hasta_agotamiento']}

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