import os
from pathlib import Path

from crewai import LLM
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / "config_erp" / ".env")


def get_llm():
    """Crea la instancia de Gemini usando una clave cargada desde el entorno."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY no está configurada en config_erp/.env")

    # LiteLLM y el SDK de Google pueden consultar esta variable además del parámetro api_key.
    os.environ["GOOGLE_API_KEY"] = api_key

    return LLM(
        model="gemini/gemini-3.5-flash-lite",
        temperature=0.7,
        api_key=api_key,
    )


if __name__ == "__main__":
    llm = get_llm()
    print(f"LLM configurado: {llm.model}")
