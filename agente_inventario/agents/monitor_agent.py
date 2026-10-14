from crewai import Agent
from tools.erp_tools import obtener_alertas_stock


def crear_agente_monitor(llm):
    return Agent(
        role="Monitor de Inventarios",
        goal=(
            "Consultar los productos del ERP mediante la herramienta "
            "disponible y reportar solo aquellos que, según las reglas "
            "determinísticas del sistema, están sin stock, tienen riesgo "
            "o requieren reposición."
        ),
        backstory=(
            "Eres un especialista en monitoreo de inventarios. "
            "Usas la herramienta Consultar Inventario ERP, que obtiene los "
            "datos actuales y aplica las reglas determinísticas de inventario. "
            "Debes conservar exactamente los productos, valores y motivos "
            "devueltos por la herramienta, sin inventar ni recalcular datos. "
            "Entregas esa lista al Agente Analista. No armas el plan de compra "
            "ni generas órdenes de compra."
        ),
        llm=llm,
        tools=[obtener_alertas_stock],
        verbose=True,
        allow_delegation=False
    )
