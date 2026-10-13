import streamlit as st

from orchestrator.crew_workflow import ejecutar_orquestacion


def render_analisis():
    
    # ENCABEZADO
    
    st.html(
        """
        <div class="analysis-header">
    
            <div>
    
                <div class="analysis-title">
                    Análisis Multi-Agente
                </div>
    
                <div class="analysis-subtitle">
                    Flujo secuencial: Monitor → Analista → Comprador
                </div>
    
            </div>
    
            <div class="analysis-status">
                <span class="status-dot"></span>
                ERP conectado
            </div>
    
        </div>
        """
    )
    
    # CONSULTA
    
    col_consulta, col_info = st.columns(
        [0.9, 1.7]
    )
    
    
    with col_consulta:
    
        st.html(
            """
            <div class="analysis-query-card">
    
                <div class="query-label">
                    CONSULTA
                </div>
    
                <div class="query-title">
                    ¿Qué productos tienen riesgo de quedarse
                    sin stock y qué debería comprar?
                </div>
    
            </div>
            """
        )
    
    
        ejecutar = st.button(
            "Ejecutar análisis",
            use_container_width=True,
            type="primary"
        )
    
    
    with col_info:
    
        st.html(
            """
            <div class="analysis-info-card">
    
                <div class="info-icon">
                    IA
                </div>
    
                <div>
    
                    <div class="info-title">
                        Análisis inteligente del inventario
                    </div>
    
                    <div class="info-text">
                        Los tres agentes colaboran sobre los datos
                        actuales del ERP para detectar riesgos y
                        generar recomendaciones de reposición.
                    </div>
    
                </div>
    
            </div>
            """
        )
    
    # LÍNEA DE AGENTES
    
    st.html(
        """
        <div class="analysis-section-title">
            Línea de agentes
        </div>
    
        <div class="analysis-section-subtitle">
            Cada salida alimenta la etapa siguiente.
        </div>
        """
    )
    
    
    # Estado inicial
    estado_monitor = "Pendiente"
    estado_analista = "Pendiente"
    estado_comprador = "Pendiente"
    
    clase_monitor = "agent-pending"
    clase_analista = "agent-pending"
    clase_comprador = "agent-pending"
    
    
    if st.session_state.ejecutado:
    
        estado_monitor = "Completado"
        estado_analista = "Completado"
        estado_comprador = "Completado"
    
        clase_monitor = "agent-completed"
        clase_analista = "agent-completed"
        clase_comprador = "agent-completed"
    
    
    st.html(
        f"""
        <div class="agent-flow">
    
            <div class="flow-agent {clase_monitor}">
    
                <div class="flow-icon">
                    🔎
                </div>
    
                <div class="flow-content">
    
                    <div class="flow-number">
                        AGENTE 01
                    </div>
    
                    <div class="flow-name">
                        Monitor
                    </div>
    
                    <div class="flow-status">
                        {estado_monitor}
                    </div>
    
                </div>
    
            </div>
    
    
            <div class="flow-arrow">
                →
            </div>
    
    
            <div class="flow-agent {clase_analista}">
    
                <div class="flow-icon">
                    📊
                </div>
    
                <div class="flow-content">
    
                    <div class="flow-number">
                        AGENTE 02
                    </div>
    
                    <div class="flow-name">
                        Analista
                    </div>
    
                    <div class="flow-status">
                        {estado_analista}
                    </div>
    
                </div>
    
            </div>
    
    
            <div class="flow-arrow">
                →
            </div>
    
    
            <div class="flow-agent {clase_comprador}">
    
                <div class="flow-icon">
                    🛒
                </div>
    
                <div class="flow-content">
    
                    <div class="flow-number">
                        AGENTE 03
                    </div>
    
                    <div class="flow-name">
                        Comprador
                    </div>
    
                    <div class="flow-status">
                        {estado_comprador}
                    </div>
    
                </div>
    
            </div>
    
        </div>
        """
    )
    
    
    # EJECUTAR ORQUESTACIÓN
    
    if ejecutar:
    
        st.session_state.ejecutado = False
        st.session_state.resultados = None
    
        with st.spinner(
            "Ejecutando Monitor → Analista → Comprador..."
        ):
    
            resultados = ejecutar_orquestacion()
    
        st.session_state.resultados = resultados
        st.session_state.ejecutado = True
    
        st.rerun()
    
    # RESULTADOS
    
    if st.session_state.resultados:
    
        st.html(
            """
            <div class="analysis-results-header">
    
                <div class="analysis-section-title">
                    Resultados del análisis
                </div>
    
                <div class="analysis-section-subtitle">
                    Información generada por los tres agentes
                    para revisión del responsable.
                </div>
    
            </div>
            """
        )
    
    
        resultado = st.session_state.resultados
    
    
        tab_monitor, tab_analista, tab_comprador = st.tabs(
            [
                "Monitor",
                "Analista",
                "Comprador"
            ]
        )
    
    
        # MONITOR
    
        with tab_monitor:
    
            st.html(
                """
                <div class="result-agent-header monitor">
    
                    <div class="result-agent-icon">
                        🔎
                    </div>
    
                    <div>
    
                        <div class="result-agent-number">
                            AGENTE 01
                        </div>
    
                        <div class="result-agent-name">
                            Monitor de Inventarios
                        </div>
    
                    </div>
    
                </div>
                """
            )
    
            st.markdown(
                resultado["monitor"]
            )
    
        # ANALISTA
    
        with tab_analista:
    
            st.html(
                """
                <div class="result-agent-header analyst">
    
                    <div class="result-agent-icon">
                        📊
                    </div>
    
                    <div>
    
                        <div class="result-agent-number">
                            AGENTE 02
                        </div>
    
                        <div class="result-agent-name">
                            Analista de Inventarios
                        </div>
    
                    </div>
    
                </div>
                """
            )
    
            st.markdown(
                resultado["analista"]
            )
    
        # COMPRADOR
    
        with tab_comprador:
    
            st.html(
                """
                <div class="result-agent-header buyer">
    
                    <div class="result-agent-icon">
                        🛒
                    </div>
    
                    <div>
    
                        <div class="result-agent-number">
                            AGENTE 03
                        </div>
    
                        <div class="result-agent-name">
                            Agente Comprador
                        </div>
    
                    </div>
    
                </div>
                """
            )
    
            st.markdown(
                resultado["final"]
            )
    
        # REVISIÓN HUMANA
    
        st.html(
            """
            <div class="human-review-card">
    
                <div class="human-review-icon">
                    👤
                </div>
    
                <div>
    
                    <div class="human-review-title">
                        Revisión humana requerida
                    </div>
    
                    <div class="human-review-text">
                        Las recomendaciones generadas por el
                        Agente Comprador son propuestas de
                        reposición. No se ejecutan compras
                        automáticamente y deben ser revisadas
                        y aprobadas por un responsable.
                    </div>
    
                </div>
    
            </div>
            """
        )

