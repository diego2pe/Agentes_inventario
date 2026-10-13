from getpass import getpass
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from services.auth import crear_primer_admin


def main():
    print("Crear el primer usuario administrador de SmartStock")
    nombre = input("Nombre completo: ").strip()
    username = input("Nombre de usuario: ").strip()
    password = getpass("Contraseña (mínimo 12 caracteres): ")
    confirmar = getpass("Confirma la contraseña: ")
    if password != confirmar:
        raise SystemExit("Las contraseñas no coinciden.")
    try:
        crear_primer_admin(nombre, username, password)
    except Exception as exc:
        raise SystemExit(f"No se pudo crear el administrador: {exc}")
    print("Administrador creado correctamente.")


if __name__ == "__main__":
    main()
