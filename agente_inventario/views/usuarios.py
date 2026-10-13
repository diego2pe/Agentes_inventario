import streamlit as st
import pymysql

from services.auth import cambiar_estado_usuario, crear_usuario, listar_usuarios


def render_usuarios(user):
    if not user or user["rol"] != "admin":
        st.error("No tienes permiso para administrar usuarios.")
        return

    st.title("Administración de usuarios")
    st.caption("Las cuentas se crean desde aquí; no hay registro público.")

    with st.expander("Crear usuario", expanded=True):
        with st.form("crear_usuario_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre completo")
            username = col2.text_input("Nombre de usuario")
            col3, col4 = st.columns(2)
            rol_label = col3.selectbox("Rol", ["Usuario", "Administrador"])
            password = col4.text_input("Contraseña temporal", type="password")
            confirmar = st.text_input("Confirmar contraseña temporal", type="password")
            submitted = st.form_submit_button("Crear cuenta", type="primary")
        if submitted:
            if password != confirmar:
                st.error("Las contraseñas no coinciden.")
            else:
                try:
                    crear_usuario(nombre, username, password, "admin" if rol_label == "Administrador" else "usuario")
                    st.success("Cuenta creada. El usuario deberá cambiar su contraseña al ingresar.")
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
                except pymysql.err.IntegrityError as exc:
                    if exc.args and exc.args[0] == 1062:
                        st.error("Ese nombre de usuario ya está registrado.")
                    elif exc.args and exc.args[0] == 1146:
                        st.error("Falta aplicar migrations/001_usuarios.sql en MySQL.")
                    else:
                        st.error("MySQL rechazó la creación de la cuenta.")
                except Exception:
                    st.error("No se pudo crear la cuenta. Revisa la conexión y la migración de usuarios.")

    st.subheader("Cuentas existentes")
    try:
        users = listar_usuarios()
    except Exception:
        st.error("No se pudo consultar la tabla de usuarios. Verifica que aplicaste la migración SQL.")
        return

    if not users:
        st.info("Aún no hay cuentas.")
        return

    for account in users:
        col_info, col_action = st.columns([4, 1])
        state = "Activa" if account["activo"] else "Desactivada"
        col_info.write(f"**{account['nombre']}** · `{account['username']}` · {account['rol']} · {state}")
        if account["username"] == user["username"]:
            col_action.caption("Tu cuenta")
        else:
            label = "Desactivar" if account["activo"] else "Activar"
            if col_action.button(label, key=f"estado_usuario_{account['id']}"):
                try:
                    cambiar_estado_usuario(account["id"], not bool(account["activo"]), user["username"])
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))
