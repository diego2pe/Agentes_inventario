"""Cliente HTTP para acceder a la API privada del ERP."""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config_erp" / ".env")


def obtener_analisis_inventario():
    api_key = os.getenv("ERP_API_KEY")
    if not api_key:
        raise RuntimeError("Falta configurar ERP_API_KEY en el entorno de la aplicación.")

    base_url = os.getenv("ERP_API_BASE_URL", "https://agente-inventario-zt0o.onrender.com/docs").rstrip("/")
    response = requests.get(
        f"{base_url}/api/inventario/analisis-riesgo",
        headers={"X-API-Key": api_key},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
