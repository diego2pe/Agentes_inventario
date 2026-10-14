import math

# REGLAS DE INVENTARIO

def calcular_demanda_diaria(ventas_ultimos_30_dias):
    """
    Calcula la demanda diaria promedio a partir de las
    ventas de los últimos 30 días.
    """
    return round(ventas_ultimos_30_dias / 30, 2)


def calcular_dias_hasta_agotamiento(stock_actual, demanda_diaria):
    """
    Calcula cuántos días aproximadamente puede mantenerse
    el stock actual considerando la demanda diaria.
    """
    if demanda_diaria <= 0:
        return None

    return round(stock_actual / demanda_diaria, 2)


def calcular_stock_seguridad(demanda_diaria):
    """
    Stock de seguridad:
        demanda diaria × 2
    """
    return round(demanda_diaria * 2, 2)


def calcular_stock_objetivo(demanda_diaria, tiempo_entrega_dias):
    """
    Stock objetivo:
        (demanda diaria × tiempo de entrega)
        + stock de seguridad
    """
    stock_seguridad = calcular_stock_seguridad(demanda_diaria)

    return round(
        (demanda_diaria * tiempo_entrega_dias)
        + stock_seguridad,
        2
    )


def calcular_cantidad_recomendada(
    stock_actual,
    stock_minimo,
    stock_maximo,
    demanda_diaria,
    tiempo_entrega_dias
):
    """
    Calcula la cantidad recomendada de reposición.

    Fórmula:
        max(stock objetivo, stock mínimo) - stock actual

    La cantidad:
        - nunca puede ser negativa;
        - se redondea hacia arriba;
        - no puede superar la capacidad disponible
          hasta el stock máximo.
    """

    stock_objetivo = calcular_stock_objetivo(
        demanda_diaria,
        tiempo_entrega_dias
    )

    objetivo_reposicion = max(stock_objetivo, stock_minimo)
    cantidad_teorica = objetivo_reposicion - stock_actual

    if cantidad_teorica <= 0:
        return 0

    cantidad_redondeada = math.ceil(cantidad_teorica)

    capacidad_hasta_maximo = stock_maximo - stock_actual

    if capacidad_hasta_maximo <= 0:
        return 0

    return min(
        cantidad_redondeada,
        capacidad_hasta_maximo
    )


def clasificar_riesgo(stock_actual, stock_minimo, dias_hasta_agotamiento):
    """
    Clasifica el nivel de riesgo del producto.

    Reglas:
        stock = 0                   -> SIN STOCK
        stock < stock mínimo        -> CRÍTICO
        días <= 2                   -> CRÍTICO
        2 < días <= 5               -> ALTO
        5 < días <= 7               -> MEDIO
        días > 7                    -> NORMAL

    Si el stock es igual al mínimo, se clasifica usando los días
    estimados hasta agotamiento.
    """

    if stock_actual == 0:
        return "SIN STOCK"

    if stock_actual < stock_minimo:
        return "CRÍTICO"

    if dias_hasta_agotamiento is None:
        return "NORMAL"

    if dias_hasta_agotamiento <= 2:
        return "CRÍTICO"

    if dias_hasta_agotamiento <= 5:
        return "ALTO"

    if dias_hasta_agotamiento <= 7:
        return "MEDIO"

    return "NORMAL"


def determinar_momento_reposicion(
    stock_actual,
    dias_hasta_agotamiento,
    tiempo_entrega_dias
):
    """
    Determina cuándo debería realizarse la reposición.

    Reglas:
        stock = 0
            -> INMEDIATA

        días hasta agotamiento <= tiempo de entrega
            -> INMEDIATA

        días hasta agotamiento <= tiempo de entrega + 2
            -> EN 1 DÍA

        caso contrario
            -> NO REQUIERE REPOSICIÓN INMEDIATA
    """

    if stock_actual == 0:
        return "INMEDIATA"

    if dias_hasta_agotamiento is None:
        return "NO REQUIERE REPOSICIÓN INMEDIATA"

    if dias_hasta_agotamiento <= tiempo_entrega_dias:
        return "INMEDIATA"

    if dias_hasta_agotamiento <= tiempo_entrega_dias + 2:
        return "EN 1 DÍA"

    return "NO REQUIERE REPOSICIÓN INMEDIATA"


def analizar_producto(producto):
    """
    Ejecuta todas las reglas de inventario para un producto
    y devuelve un resultado estructurado.

    El producto debe contener los datos provenientes del ERP.
    """

    stock_actual = int(producto["stock_actual"])
    stock_minimo = int(producto["stock_minimo"])
    stock_maximo = int(producto["stock_maximo"])
    ventas_30_dias = int(producto["ventas_ultimos_30_dias"])
    tiempo_entrega = int(producto["tiempo_entrega_dias"])

    # 1. Demanda

    demanda_diaria = calcular_demanda_diaria(
        ventas_30_dias
    )

    # 2. Días hasta agotamiento

    dias_hasta_agotamiento = calcular_dias_hasta_agotamiento(
        stock_actual,
        demanda_diaria
    )

    # 3. Nivel de riesgo

    nivel_riesgo = clasificar_riesgo(
        stock_actual,
        stock_minimo,
        dias_hasta_agotamiento
    )

    # 4. Stock de seguridad

    stock_seguridad = calcular_stock_seguridad(
        demanda_diaria
    )

    # 5. Stock objetivo

    stock_objetivo = calcular_stock_objetivo(
        demanda_diaria,
        tiempo_entrega
    )

    # 6. Cantidad recomendada

    cantidad_recomendada = calcular_cantidad_recomendada(
        stock_actual,
        stock_minimo,
        stock_maximo,
        demanda_diaria,
        tiempo_entrega
    )

    # 7. Momento de reposición

    momento_reposicion = determinar_momento_reposicion(
        stock_actual,
        dias_hasta_agotamiento,
        tiempo_entrega
    )

    # 8. Necesidad de reposición

    necesita_reposicion = cantidad_recomendada > 0

    # Resultado

    return {
        "producto_id": int(producto["id"]),
        "producto": producto["nombre"],

        "stock_actual": stock_actual,
        "stock_minimo": stock_minimo,
        "stock_maximo": stock_maximo,

        "ventas_ultimos_30_dias": ventas_30_dias,
        "demanda_diaria": demanda_diaria,
        "dias_hasta_agotamiento": dias_hasta_agotamiento,

        "tiempo_entrega_dias": tiempo_entrega,

        "stock_seguridad": stock_seguridad,
        "stock_objetivo": stock_objetivo,

        "nivel_riesgo": nivel_riesgo,
        "necesita_reposicion": necesita_reposicion,

        "momento_reposicion": momento_reposicion,
        "cantidad_recomendada": cantidad_recomendada,

        "precio_compra": float(producto["precio_compra"]),
        "proveedor": producto["proveedor"],
    }
