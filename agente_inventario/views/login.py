import streamlit as st

from services.auth import autenticar


def render_login():
    _, panel, _ = st.columns([1, 1.1, 1])
    with panel:
        st.markdown("## Iniciar sesión")
        st.caption("Acceso privado al sistema de inventarios")
        with st.form("login_form"):
            username = st.text_input("Usuario", autocomplete="username")
            password = st.text_input("Contraseña", type="password", autocomplete="current-password")
            submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
        if submitted:
            if not username.strip() or not password:
                st.error("Ingresa tu usuario y contraseña.")
                return
            try:
                user = autenticar(username, password)
            except Exception:
                st.error("No se pudo conectar con el servicio de usuarios. Revisa la conexión a MySQL.")
                return
            if not user:
                st.error("Usuario o contraseña incorrectos, o la cuenta está desactivada.")
                return
            st.session_state["usuario"] = user["username"]
            st.rerun()
