import pymysql
import os
from dotenv import load_dotenv

# Buscar el .env que está dentro de config_erp
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "config_erp", ".env")

load_dotenv(ENV_PATH)


def obtener_conexion():

    password = os.getenv("AIVEN_DB_PASSWORD")

    if not password:
        raise Exception("AIVEN_DB_PASSWORD no está configurada")

    return pymysql.connect(
        host="mysql-112ce839-angeloticlla-66f3.d.aivencloud.com",
        port=26634,
        user="avnadmin",
        password=password,
        database="defaultdb",
        ssl={
            "ca": os.path.join(
            BASE_DIR,
            "ca.pem"
            )
        },
        cursorclass=pymysql.cursors.DictCursor
    )