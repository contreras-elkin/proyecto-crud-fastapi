import os
from dotenv import load_dotenv
from pathlib import Path

# BASE_DIR apunta a la raíz del proyecto en donde está ubicado .env para cargarlo de forma adecuada
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está definida en las variables de entorno")

