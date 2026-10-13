from crewai import Agent
from tools.erp_tools import obtener_alertas_stock


def crear_agente_monitor(llm):
    return Agent(
        role="Monitor de Inventarios",
        goal=(
            "Supervisar el inventario del ERP e identificar los productos "
            "que requieren un análisis más detallado debido a su nivel de "
            "stock, demanda o proximidad al agotamiento."
        ),
        backstory=(
            "Eres un especialista en monitoreo de inventarios. "
            "Tu función es revisar la información actual del ERP, detectar "
            "productos que presentan señales de riesgo y entregar una lista "
            "clara al Agente Analista para que este realice el análisis "
            "correspondiente. No calculas cantidades de compra ni generas "
            "órdenes de compra."
        ),
        llm=llm,
        tools=[obtener_alertas_stock],
        verbose=True,
        allow_delegation=False
    )