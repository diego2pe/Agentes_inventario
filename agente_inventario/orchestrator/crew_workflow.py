import time

from crewai import Task

from agents.monitor_agent import crear_agente_monitor
from agents.analista_agent import crear_agente_analista
from agents.comprador_agent import crear_agente_comprador
from config_erp.llm_config import get_llm
from rules.inventory_rules import analizar_producto
from services.erp_client import obtener_analisis_inventario


ULTIMA_EJECUCION = 0


def obtener_datos_erp():
    """
    Obtiene los productos directamente desde la API del ERP.
    """
    datos = obtener_analisis_inventario()
    return datos.get("productos", [])


def ejecutar_orquestacion():
    global ULTIMA_EJECUCION

    try:

        # CONTROL DE EJECUCIÓN

        tiempo_actual = time.time()
        tiempo_desde_ultima = tiempo_actual - ULTIMA_EJECUCION

        if tiempo_desde_ultima < 20:
            espera = 20 - tiempo_desde_ultima

            print(
                f"Esperando {espera:.1f} segundos "
                "para evitar límites de RPM..."
            )

            time.sleep(espera)

        ULTIMA_EJECUCION = time.time()

        # CONFIGURAR LLM

        llm = get_llm()

        print(f"Usando LLM: {llm.model}")

        # CREAR AGENTES

        monitor = crear_agente_monitor(llm)
        analista = crear_agente_analista(llm)
        comprador = crear_agente_comprador(llm)

        # TAREA 1 - MONITOR

        print("\nEjecutando Agente Monitor...")

        t1 = Task(
            description="""
            Consulta la herramienta "Consultar Inventario ERP".

            Revisa la información actual de todos los productos del ERP.

            Identifica los productos que requieren un análisis más detallado
            considerando principalmente:

            - stock actual
            - stock mínimo
            - ventas de los últimos 30 días
            - demanda diaria promedio
            - días estimados hasta el agotamiento
            - tiempo de entrega del proveedor

            No calcules cantidades de compra.

            Tu función en esta etapa es identificar y entregar al Agente
            Analista los productos que presentan señales de riesgo o que
            requieren atención.

            Presenta un informe claro indicando el producto y los datos
            relevantes que justifican que deba ser analizado.
            """,

            expected_output="""
            Informe de monitoreo del inventario que contenga:

            - Productos que requieren análisis
            - Stock actual
            - Demanda diaria
            - Días estimados hasta agotamiento
            - Tiempo de entrega
            - Motivo por el cual el producto requiere análisis

            No incluir órdenes de compra.
            """,

            agent=monitor
        )

        resultado1 = t1.execute_sync()

        print("Monitor completado")

        # OBTENER DATOS ESTRUCTURADOS DEL ERP

        print("\nObteniendo datos estructurados del ERP...")

        productos_erp = obtener_datos_erp()

        if not productos_erp:
            raise Exception(
                "El ERP no devolvió productos para analizar."
            )

        print(
            f"Productos obtenidos desde ERP: "
            f"{len(productos_erp)}"
        )

        # APLICAR REGLAS DETERMINÍSTICAS

        print("\nAplicando reglas determinísticas de inventario...")

        analisis_reglas = []

        for producto in productos_erp:

            resultado_regla = analizar_producto(producto)

            analisis_reglas.append(resultado_regla)

            print(
                f"  {resultado_regla['producto']} -> "
                f"{resultado_regla['nivel_riesgo']} | "
                f"Cantidad: "
                f"{resultado_regla['cantidad_recomendada']} | "
                f"Momento: "
                f"{resultado_regla['momento_reposicion']}"
            )

        print("Reglas de inventario aplicadas correctamente.")

        # PREPARAR INFORMACIÓN PARA EL ANALISTA

        datos_para_analista = ""

        for resultado in analisis_reglas:

            datos_para_analista += f"""
                PRODUCTO: {resultado['producto']}

                Stock actual: {resultado['stock_actual']}
                Stock mínimo: {resultado['stock_minimo']}
                Stock máximo: {resultado['stock_maximo']}

                Ventas últimos 30 días: {resultado['ventas_ultimos_30_dias']}
                Demanda diaria: {resultado['demanda_diaria']}
                Días hasta agotamiento: {resultado['dias_hasta_agotamiento']}

                Tiempo de entrega: {resultado['tiempo_entrega_dias']} días

                Stock de seguridad: {resultado['stock_seguridad']}
                Stock objetivo: {resultado['stock_objetivo']}

                Nivel de riesgo: {resultado['nivel_riesgo']}
                Necesita reposición: {resultado['necesita_reposicion']}

                Momento de reposición: {resultado['momento_reposicion']}
                Cantidad recomendada: {resultado['cantidad_recomendada']}

                Proveedor: {resultado['proveedor']}
                Precio de compra: S/ {resultado['precio_compra']}

                ----------------------------------------
                """

        # PAUSA ENTRE AGENTES

        print("Pausa de 5 segundos entre agentes...")

        time.sleep(5)

        # TAREA 2 - ANALISTA

        print("\nEjecutando Agente Analista...")

        t2 = Task(
            description=f"""
            Recibiste el informe del Agente Monitor y los resultados
            calculados por el sistema de reglas de inventario.

            ==================================================
            INFORME DEL MONITOR
            ==================================================

            {resultado1}

            ==================================================
            RESULTADOS CALCULADOS POR EL SISTEMA
            ==================================================

            {datos_para_analista}

            ==================================================

            Analiza los productos identificados por el Monitor.

            IMPORTANTE:

            Los valores numéricos proporcionados en "RESULTADOS
            CALCULADOS POR EL SISTEMA" ya fueron calculados por
            el motor determinístico de reglas de inventario.

            NO vuelvas a calcular:

            - demanda diaria
            - días hasta agotamiento
            - stock de seguridad
            - stock objetivo
            - cantidad recomendada
            - nivel de riesgo
            - momento de reposición

            Debes utilizar exactamente los valores proporcionados.

            Tu función es interpretar los resultados y explicar:

            - qué productos presentan riesgo
            - cuál es el nivel de riesgo de cada producto
            - cuáles necesitan reposición
            - por qué existe el riesgo
            - qué productos requieren atención prioritaria
            - qué información debe considerar el Agente Comprador

            Prepara un análisis claro para el Agente Comprador.

            No ejecutes ninguna compra.
            No envíes ninguna orden.
            """,

            expected_output="""
            Análisis de inventario estructurado que contenga:

            - Producto
            - Nivel de riesgo
            - Stock actual
            - Demanda diaria
            - Días hasta agotamiento
            - Tiempo de entrega
            - Necesidad de reposición
            - Cantidad recomendada calculada por el sistema
            - Momento de reposición calculado por el sistema
            - Justificación del riesgo
            - Observaciones relevantes para compras

            No modificar los valores calculados por el sistema.
            No ejecutar compras.
            """,

            agent=analista
        )

        resultado2 = t2.execute_sync()

        print("Analista completado")


        # PAUSA ENTRE AGENTES

        print("Pausa de 5 segundos entre agentes...")

        time.sleep(5)

        # TAREA 3 - COMPRADOR

        print("\nEjecutando Agente Comprador...")

        t3 = Task(
            description=f"""
            Recibiste el análisis elaborado por el Agente Analista.

            ==================================================
            ANÁLISIS DEL ANALISTA
            ==================================================

            {resultado2}

            ==================================================

            Genera una RECOMENDACIÓN DE COMPRA utilizando los
            resultados calculados por el sistema.

            Para cada producto relevante presenta:

            - Producto
            - Proveedor
            - Nivel de riesgo
            - Cuándo se recomienda realizar la reposición
            - Cantidad recomendada
            - Precio de compra
            - Justificación de la recomendación

            IMPORTANTE:

            La cantidad recomendada y el momento de reposición
            ya fueron calculados por el sistema de reglas.

            NO vuelvas a calcular esos valores.

            Utiliza exactamente los valores proporcionados
            por el Agente Analista.

            Si un producto no requiere reposición inmediata,
            indícalo claramente.

            Explica brevemente el motivo de cada recomendación.

            IMPORTANTE:

            No generes una orden de compra real.
            No envíes mensajes por WhatsApp.
            No ejecutes ninguna compra.

            El resultado es solamente una RECOMENDACIÓN que
            posteriormente será revisada y aprobada por un
            responsable humano.
            """,

            expected_output="""
            Recomendación de compra estructurada que contenga:

            - Producto
            - Proveedor
            - Nivel de riesgo
            - Cuándo reponer
            - Cantidad recomendada
            - Precio de compra
            - Justificación

            Incluir también los productos que no requieren
            reposición inmediata.

            Utilizar exactamente los valores calculados
            por el sistema.

            No incluir confirmación de envío ni ejecución
            de compras.
            """,

            agent=comprador
        )

        resultado3 = t3.execute_sync()

        print("Comprador completado")

        # RESULTADOS
     
        return {
            "monitor": (
                "**MONITOREO DEL INVENTARIO**\n\n"
                f"{str(resultado1)}"
            ),

            "analista": (
                "**ANÁLISIS DE INVENTARIO**\n\n"
                f"{str(resultado2)}"
            ),

            "final": (
                "**RECOMENDACIONES DE COMPRA**\n\n"
                f"{str(resultado3)}"
            )
        }

    except Exception as e:

        print(f"Error en la orquestación: {e}")

        return {
            "monitor": f"Error en Monitor: {str(e)}",
            "analista": "No se pudo completar el análisis.",
            "final": "No se pudo generar la recomendación de compra."
        }