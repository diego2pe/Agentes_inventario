"""Autenticación sencilla entre Streamlit y la API privada del ERP."""

import hmac
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Header, HTTPException

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config_erp" / ".env")


def validar_api_key(x_api_key: str | None = Header(default=None)):
    expected = os.getenv("ERP_API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="API key is not configured")
    if not x_api_key or not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="Unauthorized")
