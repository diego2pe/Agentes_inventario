import streamlit as st

from rules.inventory_rules import analizar_producto
from services.erp_client import obtener_analisis_inventario


def render_dashboard():
    
    # OBTENER DATOS DEL ERP
    
    productos = []
    api_conectada = False

    try:
        datos_dashboard = obtener_analisis_inventario()
        productos = datos_dashboard.get("productos", [])
        api_conectada = True
    except Exception:
        productos = []
        api_conectada = False
    
    # PROCESAR DATOS
    
    analisis_productos = []
    
    for producto in productos:
    
        resultado = analizar_producto(producto)
    
        analisis_productos.append(resultado)
    
    # KPIs
    
    total_productos = len(analisis_productos)
    
    productos_sin_stock = sum(
        1
        for p in analisis_productos
        if p["stock_actual"] == 0
    )
    
    productos_criticos = sum(
        1
        for p in analisis_productos
        if p["nivel_riesgo"] == "CRÍTICO"
    )
    
    productos_reposicion = sum(
        1
        for p in analisis_productos
        if p["necesita_reposicion"]
    )
    
    recomendaciones = sum(
        1
        for p in analisis_productos
        if p["cantidad_recomendada"] > 0
    )
    
    # ENCABEZADO
    
    st.html(
        """
        <div class="dashboard-header">
    
            <div>
                <div class="dashboard-title">
                    Dashboard
                </div>
    
                <div class="dashboard-subtitle">
                    Estado general del inventario · datos del ERP
                </div>
            </div>
    
            <div class="dashboard-status">
                <span class="status-dot"></span>
                ERP sincronizado
            </div>
    
        </div>
        """
    )
    
    # TARJETAS KPI
    
    st.markdown(
        "<div class='kpi-grid'>",
        unsafe_allow_html=True
    )
    
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    
    with kpi1:
    
        st.html(
            f"""
            <div class="kpi-card blue">
    
                <div class="kpi-label">
                    Productos monitoreados
                </div>
    
                <div class="kpi-value">
                    {total_productos}
                </div>
    
                <div class="kpi-description">
                    catálogo del ERP
                </div>
    
            </div>
            """
        )
    
    
    with kpi2:
    
        st.html(
            f"""
            <div class="kpi-card red">
    
                <div class="kpi-label">
                    Nivel crítico
                </div>
    
                <div class="kpi-value">
                    {productos_criticos}
                </div>
    
                <div class="kpi-description">
                    riesgo crítico o sin stock
                </div>
    
            </div>
            """
        )
    
    
    with kpi3:
    
        st.html(
            f"""
            <div class="kpi-card orange">
    
                <div class="kpi-label">
                    Sin stock
                </div>
    
                <div class="kpi-value">
                    {productos_sin_stock}
                </div>
    
                <div class="kpi-description">
                    stock actual en cero
                </div>
    
            </div>
            """
        )
    
    
    with kpi4:
    
        st.html(
            f"""
            <div class="kpi-card cyan">
    
                <div class="kpi-label">
                    Requieren reposición
                </div>
    
                <div class="kpi-value">
                    {productos_reposicion}
                </div>
    
                <div class="kpi-description">
                    según reglas de inventario
                </div>
    
            </div>
            """
        )
    
    
    with kpi5:
    
         st.html(
            f"""
            <div class="kpi-card green">
    
                <div class="kpi-label">
                    Recomendaciones
                </div>
    
                <div class="kpi-value">
                    {recomendaciones}
                </div>
    
                <div class="kpi-description">
                    generadas por el sistema
                </div>
    
            </div>
            """
        )
    
    # DISTRIBUCIÓN DEL INVENTARIO
    
    normales = sum(
        1
        for p in analisis_productos
        if p["nivel_riesgo"] == "NORMAL"
    )
    
    medios = sum(
        1
        for p in analisis_productos
        if p["nivel_riesgo"] == "MEDIO"
    )
    
    altos = sum(
        1
        for p in analisis_productos
        if p["nivel_riesgo"] == "ALTO"
    )
    
    criticos = sum(
        1
        for p in analisis_productos
        if p["nivel_riesgo"] == "CRÍTICO"
    )
    
    sin_stock = sum(
        1
        for p in analisis_productos
        if p["nivel_riesgo"] == "SIN STOCK"
    )
    
    
    st.html(
        """
        <div class="dashboard-section-title">
            Distribución del estado del inventario
        </div>
        """
    )
    
    
    col_grafico, col_ventas = st.columns(2)
    
    # PANEL DISTRIBUCIÓN
    
    with col_grafico:
    
        total = max(total_productos, 1)
    
        normal_deg = normales / total * 360
        medio_deg = medios / total * 360
        alto_deg = altos / total * 360
        critico_deg = criticos / total * 360
    
        inicio_medio = normal_deg
        inicio_alto = normal_deg + medio_deg
        inicio_critico = normal_deg + medio_deg + alto_deg
        inicio_stock = inicio_critico + critico_deg
    
        st.html(
            f"""
            <div class="dashboard-panel inventory-panel">
    
                <div class="panel-title">
                    Distribución del inventario
                </div>
    
                <div class="panel-subtitle">
                    Estado actual de los productos
                </div>
    
                <div class="inventory-content">
    
                    <div
                        class="inventory-donut"
                        style="
                            background:
                            conic-gradient(
                                #22c55e 0deg {normal_deg}deg,
                                #f59e0b {inicio_medio}deg {inicio_alto}deg,
                                #f97316 {inicio_alto}deg {inicio_critico}deg,
                                #ef4444 {inicio_critico}deg {inicio_stock}deg,
                                #64748b {inicio_stock}deg 360deg
                            );
                        "
                    >
    
                        <div class="donut-center">
    
                            <div class="donut-number">
                                {total_productos}
                            </div>
    
                            <div class="donut-label">
                                productos
                            </div>
    
                        </div>
    
                    </div>
    
    
                    <div class="inventory-legend">
    
                        <div class="legend-item">
                            <span class="legend-dot green"></span>
                            <span>Óptimo</span>
                            <strong>{normales}</strong>
                        </div>
    
                        <div class="legend-item">
                            <span class="legend-dot yellow"></span>
                            <span>Medio</span>
                            <strong>{medios}</strong>
                        </div>
    
                        <div class="legend-item">
                            <span class="legend-dot orange"></span>
                            <span>Alto</span>
                            <strong>{altos}</strong>
                        </div>
    
                        <div class="legend-item">
                            <span class="legend-dot red"></span>
                            <span>Crítico</span>
                            <strong>{criticos}</strong>
                        </div>
    
                        <div class="legend-item">
                            <span class="legend-dot gray"></span>
                            <span>Sin stock</span>
                            <strong>{sin_stock}</strong>
                        </div>
    
                    </div>
    
                </div>
    
            </div>
            """
        )
    
    # PANEL DEMANDA
    
    with col_ventas:
    
        productos_demanda_grafico = sorted(
            analisis_productos,
            key=lambda x: x["ventas_ultimos_30_dias"],
            reverse=True
        )
    
        max_ventas = max(
            [
                p["ventas_ultimos_30_dias"]
                for p in productos_demanda_grafico
            ],
            default=1
        )
    
    
        barras_html = ""
    
        for producto in productos_demanda_grafico:
    
            ventas = producto["ventas_ultimos_30_dias"]
    
            porcentaje = (
                ventas / max_ventas * 100
                if max_ventas > 0
                else 0
            )
    
            nombre = producto["producto"]
    
            barras_html += f"""
            <div class="sales-row">
    
                <div class="sales-header">
    
                    <span class="sales-name">
                        {nombre}
                    </span>
    
                    <span class="sales-value">
                        {ventas} u.
                    </span>
    
                </div>
    
                <div class="sales-bar-background">
    
                    <div
                        class="sales-bar"
                        style="width: {porcentaje}%"
                    ></div>
    
                </div>
    
            </div>
            """
    
    
        st.html(
            f"""
            <div class="dashboard-panel sales-panel">
    
                <div class="panel-title">
                    Evolución de ventas recientes
                </div>
    
                <div class="panel-subtitle">
                    Ventas registradas en los últimos 30 días
                </div>
    
                <div class="sales-chart">
    
                    {barras_html}
    
                </div>
    
            </div>
            """
        )
    
    # PRODUCTOS CRÍTICOS
    
    col_criticos, col_demanda = st.columns(2)
    
    
    with col_criticos:
    
        productos_riesgo = [
            p
            for p in analisis_productos
            if p["necesita_reposicion"]
        ]
    
        # Ordenar primero por gravedad
        prioridad_riesgo = {
            "SIN STOCK": 1,
            "CRÍTICO": 2,
            "ALTO": 3,
            "MEDIO": 4,
            "NORMAL": 5
        }
    
        productos_riesgo = sorted(
            productos_riesgo,
            key=lambda x: prioridad_riesgo.get(
                x["nivel_riesgo"],
                99
            )
        )
    
    
        filas_criticos = ""
    
        for producto in productos_riesgo[:5]:
    
            riesgo = producto["nivel_riesgo"]
    
            if riesgo == "SIN STOCK":
                clase = "risk-critical"
    
            elif riesgo == "CRÍTICO":
                clase = "risk-critical"
    
            elif riesgo == "ALTO":
                clase = "risk-high"
    
            else:
                clase = "risk-medium"
    
    
            filas_criticos += f"""
            <div class="product-row">
    
                <div class="product-name">
                    {producto["producto"]}
                </div>
    
                <div class="product-stock">
    
                    Stock:
                    <strong>
                        {producto["stock_actual"]}
                    </strong>
    
                </div>
    
                <div class="risk-badge {clase}">
                    {riesgo}
                </div>
    
            </div>
            """
    
    
        if not filas_criticos:
    
            filas_criticos = """
            <div class="empty-state">
                No existen productos que requieran reposición.
            </div>
            """
    
    
        st.html(
            f"""
            <div class="dashboard-panel bottom-panel">
    
                <div class="panel-header-row">
    
                    <div>
    
                        <div class="panel-title">
                            Productos críticos
                        </div>
    
                        <div class="panel-subtitle">
                            Productos que requieren atención
                        </div>
    
                    </div>
    
                    <div class="panel-link">
                        Ver todos →
                    </div>
    
                </div>
    
                <div class="critical-table-header">
    
                    <span>PRODUCTO</span>
                    <span>STOCK</span>
                    <span>NIVEL</span>
    
                </div>
    
                {filas_criticos}
    
            </div>
            """
        )
    
    # PRODUCTOS CON MAYOR DEMANDA
    
    with col_demanda:
    
        productos_demanda = sorted(
            analisis_productos,
            key=lambda x: x["ventas_ultimos_30_dias"],
            reverse=True
        )
    
    
        filas_demanda = ""
    
        for posicion, producto in enumerate(
            productos_demanda[:5],
            start=1
        ):
    
            filas_demanda += f"""
            <div class="demand-row">
    
                <div class="demand-position">
                    {posicion}
                </div>
    
                <div class="demand-product">
                    {producto["producto"]}
                </div>
    
                <div class="demand-value">
                    {producto["ventas_ultimos_30_dias"]} u.
                    <span>/ 30 días</span>
                </div>
    
            </div>
            """
    
    
        st.html(
            f"""
            <div class="dashboard-panel bottom-panel">
    
                <div class="panel-header-row">
    
                    <div>
    
                        <div class="panel-title">
                            Productos con mayor demanda
                        </div>
    
                        <div class="panel-subtitle">
                            Productos con mayores ventas registradas
                        </div>
    
                    </div>
    
                    <div class="panel-link">
                        Ver todos →
                    </div>
    
                </div>
    
                {filas_demanda}
    
            </div>
            """
        )
    
    # ESTADO ERP
    
    if api_conectada:
    
        st.html(
            f"""
            <div class="dashboard-footer-status">
    
                <span class="status-dot"></span>
    
                <strong>
                    ERP sincronizado
                </strong>
    
                <span>
                    {total_productos} productos disponibles
                </span>
    
            </div>
            """
        )
    
    else:
    
        st.html(
            """
            <div class="dashboard-footer-status error">
    
                <span class="status-dot-error"></span>
    
                <strong>
                    ERP desconectado
                </strong>
    
                <span>
                    No se pudo obtener información del ERP.
                </span>
    
            </div>
            """
        )
    
    # PIE
    
    st.html(
        """
        <div class="smartstock-footer">
            SmartStock · Sistema multi-agente de IA
            para la gestión inteligente de inventarios
        </div>
        """
    )
    
    return

