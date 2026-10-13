import streamlit as st

from components.sidebar import render_sidebar
from components.styles import aplicar_estilos
from views.analisis import render_analisis
from views.dashboard import render_dashboard
from views.login import render_login
from views.usuarios import render_usuarios
from services.auth import cambiar_password, obtener_usuario_activo

st.set_page_config(
    page_title="IA Inventarios ERP",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilos()

username = st.session_state.get("usuario")
user = None
if username:
    try:
        user = obtener_usuario_activo(username)
    except Exception:
        st.error("No se pudo validar la sesión contra MySQL. Revisa la conexión y vuelve a intentarlo.")
        st.stop()
    if not user:
        st.session_state.pop("usuario", None)
        st.session_state.modulo = "Dashboard"

if not user:
    render_login()
    st.stop()

if user["cambio_clave_obligatorio"]:
    st.title("Actualiza tu contraseña")
    st.info("Por seguridad, debes cambiar la contraseña temporal antes de continuar.")
    with st.form("cambiar_clave_obligatoria"):
        nueva = st.text_input("Nueva contraseña", type="password")
        confirmar = st.text_input("Confirmar contraseña", type="password")
        submitted = st.form_submit_button("Guardar contraseña", type="primary")
    if submitted:
        if nueva != confirmar:
            st.error("Las contraseñas no coinciden.")
        else:
            try:
                cambiar_password(user["username"], nueva)
                st.success("Contraseña actualizada.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except Exception:
                st.error("No se pudo guardar la contraseña. Revisa la conexión a MySQL.")
    st.stop()

if "resultados" not in st.session_state:
    st.session_state.resultados = None
if "ejecutado" not in st.session_state:
    st.session_state.ejecutado = False
if "modulo" not in st.session_state:
    st.session_state.modulo = "Dashboard"
if user["rol"] != "admin" and st.session_state.modulo == "Usuarios":
    st.session_state.modulo = "Dashboard"

render_sidebar(user)

if st.session_state.modulo == "Dashboard":
    render_dashboard()
elif st.session_state.modulo == "Análisis Multi-Agente":
    render_analisis()
elif st.session_state.modulo == "Usuarios":
    render_usuarios(user)
