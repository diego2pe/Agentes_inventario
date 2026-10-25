import time

from crewai import Task

from agents.monitor_agent import crear_agente_monitor
from agents.analista_agent import crear_agente_analista
from agents.comprador_agent import crear_agente_comprador
from config_erp.llm_config import get_llm


ULTIMA_EJECUCION = 0


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

            La herramienta obtiene los datos base del ERP y aplica las reglas
            determinísticas de inventario. Presenta únicamente los productos
            que devuelve la herramienta, conservando exactamente sus valores,
            nivel de riesgo y motivo de atención. No agregues productos ni
            recalcules métricas o cantidades. Si la herramienta indica que no
            hay alertas, informa que no hay productos que requieran atención.
            """,

            expected_output="""
            Lista fiel de los productos con alerta entregados por la
            herramienta, con datos de inventario, métricas, riesgo, proveedor
            y motivo. Si no hay alertas, indicarlo. No incluir órdenes.
            """,

            agent=monitor
        )
        inicio = time.perf_counter()
        resultado1 = t1.execute_sync()

        print("Monitor completado")

        # PAUSA ENTRE AGENTES

        print("Pausa de 5 segundos entre agentes...")

        time.sleep(5)

        # TAREA 2 - ANALISTA

        print("\nEjecutando Agente Analista...")

        t2 = Task(
            description=f"""
            Recibiste del Agente Monitor la lista de productos que cumplen
            las reglas de alerta, junto con sus datos y valores calculados.

            ==================================================
            PRODUCTOS Y RESULTADOS DEL MONITOR
            ==================================================

            {resultado1}

            ==================================================

            Arma un plan de reposición únicamente para los productos
            identificados por el Monitor. No agregues otros productos.

            IMPORTANTE:

            Los valores numéricos incluidos por el Monitor provienen de las
            reglas determinísticas de inventario.

            NO vuelvas a calcular ni modifiques:

            - demanda diaria
            - días hasta agotamiento
            - stock de seguridad
            - stock objetivo
            - cantidad recomendada
            - nivel de riesgo
            - momento de reposición

            Debes utilizar exactamente los valores proporcionados.

            Tu función es explicar la prioridad y preparar un plan para cada
            producto, conservando exactamente las cantidades, proveedor,
            precio y momento de reposición recibidos. También explica:

            - qué productos presentan riesgo
            - cuál es el nivel de riesgo de cada producto
            - cuáles necesitan reposición
            - por qué existe el riesgo
            - qué productos requieren atención prioritaria
            - qué información debe considerar el Agente Comprador

            Prepara el plan para el Agente Comprador.

            No ejecutes ninguna compra.
            No envíes ninguna orden.
            """,

            expected_output="""
            Plan de reposición estructurado únicamente para los productos
            indicados por el Monitor, que contenga:

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

            Convierte el plan de reposición del Agente Analista en una
            recomendación clara para el usuario. Limítate a los productos y
            valores incluidos en ese plan; no agregues productos.

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

            Explica brevemente el motivo de cada recomendación.
            Si el plan indica que no hay productos para reponer, informa que
            no hay recomendaciones pendientes.

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

            Utilizar exactamente los valores calculados
            por el sistema.

            No incluir confirmación de envío ni ejecución
            de compras.
            """,

            agent=comprador
        )

        resultado3 = t3.execute_sync()
        fin = time.perf_counter()
        tiempo_total = fin - inicio

        print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos", flush=True)
        print("Comprador completado", flush=True)

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
