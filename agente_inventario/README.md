# SmartStock — gestión inteligente de inventarios

Aplicación académica para visualizar el estado del inventario y generar recomendaciones de reposición mediante un flujo multiagente. La interfaz está desarrollada con Streamlit; la API del ERP usa FastAPI; los agentes están coordinados con CrewAI y utilizan Google Gemini. Los datos se almacenan en MySQL.

## Arquitectura

1. El usuario inicia sesión en la aplicación Streamlit.
2. El dashboard presenta indicadores del inventario.
3. Para el análisis, CrewAI coordina los agentes Monitor, Analista y Comprador.
4. El Monitor obtiene los datos a través de la API privada FastAPI.
5. La API consulta MySQL y devuelve los datos del ERP.
6. Los agentes usan Gemini para interpretar la información y redactar una recomendación. La recomendación requiere revisión humana; la aplicación no ejecuta compras.

## Requisitos

- Python 3.11 o superior.
- Acceso a la base de datos MySQL configurada para el proyecto.
- Certificado CA de Aiven (`ca.pem`) en la raíz del repositorio si se usa la conexión Aiven definida en `config_erp/database.py`.
- Clave de API de Google Gemini.

## Instalación local en Windows / PowerShell

Desde la carpeta raíz del repositorio:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pip install uvicorn
Copy-Item .env.example config_erp\.env
```

Edita `config_erp\.env` y completa las variables indicadas en la sección siguiente. No compartas ni subas ese archivo.

## Variables de entorno

| Variable | Uso |
| --- | --- |
| `AIVEN_DB_PASSWORD` | Contraseña de acceso a MySQL. |
| `GEMINI_API_KEY` | Clave para consumir el modelo de Google Gemini. |
| `ERP_API_KEY` | Secreto compartido para proteger las solicitudes a la API privada del ERP. Configura el mismo valor en la API y en la aplicación Streamlit. |
| `ERP_API_BASE_URL` | URL base de la API del ERP. En local se usa `http://127.0.0.1:8000`; en producción, configura la URL pública de la API desplegada. |

La aplicación busca el archivo local de variables en `config_erp/.env`. En producción, configura los mismos nombres como secretos o variables de entorno en el servicio correspondiente.

La dirección, puerto, usuario y nombre de la base de datos están definidos actualmente en `config_erp/database.py`. Si cambian los datos del servidor, actualiza esa configuración. El certificado `ca.pem` debe corresponder al servidor MySQL configurado y permanecer en la raíz del proyecto.

## Preparar la base de datos

1. Crea o selecciona la base de datos MySQL correspondiente.
2. Ejecuta `erp_db.sql` para crear las tablas y datos iniciales del ERP, si aún no existen.
3. Ejecuta `migrations/001_usuarios.sql` en esa misma base para crear la tabla de usuarios.
4. Verifica que `config_erp/.env` y `ca.pem` estén configurados correctamente.

## Crear el primer administrador

Activa el entorno virtual y ejecuta:

```powershell
python .\scripts\crear_admin_inicial.py
```

El script solicitará el nombre, el usuario y una contraseña de al menos 12 caracteres. No hay registro público; las cuentas adicionales se administran desde el módulo de usuarios con una cuenta administradora.

## Ejecutar en local

Abre dos terminales en la raíz del repositorio y activa el entorno virtual en ambas.

Terminal 1 — API ERP:

```powershell
python -m uvicorn api_erp:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — aplicación Streamlit:

```powershell
streamlit run app.py
```

Streamlit abrirá la aplicación en el navegador. La API debe estar ejecutándose para que el módulo multiagente pueda consultar el ERP.

## Despliegue

La interfaz Streamlit y la API FastAPI se despliegan como servicios separados (por ejemplo, Streamlit Community Cloud y Render). Configura las variables de entorno requeridas en cada servicio y establece `ERP_API_BASE_URL` en la aplicación Streamlit con la URL pública de la API. Usa HTTPS para la API pública y configura la misma `ERP_API_KEY` en ambos servicios. No publiques contraseñas, claves API ni archivos `.env`.

## Seguridad y alcance

Las recomendaciones generadas son apoyo para el usuario y deben revisarse antes de tomar decisiones de compra. Este proyecto no registra órdenes ni efectúa pagos. Para un uso productivo, se recomienda revisar permisos de base de datos, límites de acceso, registros de auditoría, respaldos y manejo de datos personales.

## Tecnologías

Las versiones de las dependencias Python están fijadas en `requirements.txt`. El proyecto no requiere Docker ni Docker Compose.
