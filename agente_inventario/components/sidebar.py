import streamlit as st


def render_sidebar(user):
    with st.sidebar:
    
        st.markdown(
            """
            <div class="brand">
                <div class="brand-icon">SS</div>
                <div>
                    <div class="brand-name">SmartStock</div>
                    <div class="brand-subtitle">
                        Gestión de inventarios
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        st.markdown("<div class='sidebar-separator'></div>", unsafe_allow_html=True)
    
        st.markdown(
            "<div class='sidebar-section-title'>NAVEGACIÓN</div>",
            unsafe_allow_html=True
        )
    
        # NAVEGACIÓN
    
        if st.button(
            "Dashboard",
            use_container_width=True,
            type="primary" if st.session_state.modulo == "Dashboard" else "secondary"
        ):
            st.session_state.modulo = "Dashboard"
            st.rerun()
    
        if st.button(
            "Análisis Multi-Agente",
            use_container_width=True,
            type="primary"
            if st.session_state.modulo == "Análisis Multi-Agente"
            else "secondary"
        ):
            st.session_state.modulo = "Análisis Multi-Agente"
            st.rerun()
    
        if user["rol"] == "admin":
            if st.button(
                "Usuarios",
                use_container_width=True,
                type="primary" if st.session_state.modulo == "Usuarios" else "secondary",
            ):
                st.session_state.modulo = "Usuarios"
                st.rerun()

        st.caption(f"Sesión: {user['nombre']} · {user['rol']}")
        if st.button("Cerrar sesión", use_container_width=True):
            for key in ("usuario", "resultados", "ejecutado"):
                st.session_state.pop(key, None)
            st.session_state.modulo = "Dashboard"
            st.rerun()

        st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)
    
        # ESTADO ERP
    
        st.html(
            """
            <div class="erp-status-card">
    
                <div class="erp-status-title">
                    <span class="status-dot"></span>
                    ERP sincronizado
                </div>
    
                <div class="erp-status-text">
                    <strong>Sistema conectado</strong>
                    <br>
                    Datos disponibles para análisis
                </div>
    
            </div>
            """
        )
    
        st.html(
            """
            <div class="sidebar-footer-brand">
                <div class="mini-logo">SS</div>
                <div>
                    <div class="mini-brand-name">SmartStock</div>
                    <div class="mini-brand-text">MVP · Demo</div>
                </div>
            </div>
            """
        )

