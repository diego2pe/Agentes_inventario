"""Autenticación y administración de cuentas para la interfaz Streamlit."""

import base64
import hashlib
import hmac
import os
import re
import secrets

from config_erp.database import obtener_conexion

ITERACIONES = 600_000
_ROLES = {"admin", "usuario"}


def _normalizar_username(username: str) -> str:
    username = username.strip().lower()
    if not re.fullmatch(r"[a-z0-9._-]{3,80}", username):
        raise ValueError("El usuario debe tener 3–80 caracteres: letras, números, punto, guion o guion bajo.")
    return username


def _hash_password(password: str) -> str:
    if len(password) < 12:
        raise ValueError("La contraseña debe tener al menos 12 caracteres.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERACIONES)
    return "pbkdf2_sha256${}${}${}".format(
        ITERACIONES,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def _verificar_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iteration_text, salt_text, digest_text = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iteration_text)
        salt = base64.b64decode(salt_text, validate=True)
        expected = base64.b64decode(digest_text, validate=True)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def autenticar(username: str, password: str):
    username = username.strip().lower()
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, username, password_hash, rol, activo, cambio_clave_obligatorio "
                "FROM usuarios WHERE username = %s LIMIT 1",
                (username,),
            )
            row = cursor.fetchone()
        if not row or not row["activo"] or not _verificar_password(password, row["password_hash"]):
            return None
        return {
            "id": row["id"],
            "nombre": row["nombre"],
            "username": row["username"],
            "rol": row["rol"],
            "cambio_clave_obligatorio": bool(row["cambio_clave_obligatorio"]),
        }
    finally:
        conexion.close()


def obtener_usuario_activo(username: str):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, username, rol, cambio_clave_obligatorio "
                "FROM usuarios WHERE username = %s AND activo = 1 LIMIT 1",
                (username,),
            )
            row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "nombre": row["nombre"],
            "username": row["username"],
            "rol": row["rol"],
            "cambio_clave_obligatorio": bool(row["cambio_clave_obligatorio"]),
        }
    finally:
        conexion.close()


def crear_usuario(nombre: str, username: str, password: str, rol: str = "usuario"):
    nombre = nombre.strip()
    username = _normalizar_username(username)
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if rol not in _ROLES:
        raise ValueError("Rol no válido.")
    password_hash = _hash_password(password)
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (nombre, username, password_hash, rol, cambio_clave_obligatorio) "
                "VALUES (%s, %s, %s, %s, 1)",
                (nombre, username, password_hash, rol),
            )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def cambiar_password(username: str, password: str):
    password_hash = _hash_password(password)
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET password_hash = %s, cambio_clave_obligatorio = 0 WHERE username = %s AND activo = 1",
                (password_hash, username),
            )
        conexion.commit()
        return cursor.rowcount == 1
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def listar_usuarios():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, username, rol, activo, creado_en "
                "FROM usuarios ORDER BY creado_en DESC, id DESC"
            )
            return cursor.fetchall()
    finally:
        conexion.close()


def cambiar_estado_usuario(user_id: int, activo: bool, username_actual: str):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT username, rol, activo FROM usuarios WHERE id = %s FOR UPDATE", (user_id,))
            target = cursor.fetchone()
            if not target:
                raise ValueError("No se encontró la cuenta.")
            if target["username"] == username_actual:
                raise ValueError("No puedes desactivar tu propia cuenta.")
            if not activo and target["activo"] and target["rol"] == "admin":
                cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE activo = 1 AND rol = 'admin'")
                if cursor.fetchone()["total"] <= 1:
                    raise ValueError("Debe permanecer al menos un administrador activo.")
            cursor.execute("UPDATE usuarios SET activo = %s WHERE id = %s", (int(activo), user_id))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def crear_primer_admin(nombre: str, username: str, password: str):
    """Inicialización por consola: solo permite crear el admin si no existe ninguno."""
    nombre = nombre.strip()
    username = _normalizar_username(username)
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    password_hash = _hash_password(password)
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE activo = 1 AND rol = 'admin' FOR UPDATE")
            if cursor.fetchone()["total"]:
                raise ValueError("Ya existe un administrador activo.")
            cursor.execute(
                "INSERT INTO usuarios (nombre, username, password_hash, rol, cambio_clave_obligatorio) "
                "VALUES (%s, %s, %s, 'admin', 0)",
                (nombre, username, password_hash),
            )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
