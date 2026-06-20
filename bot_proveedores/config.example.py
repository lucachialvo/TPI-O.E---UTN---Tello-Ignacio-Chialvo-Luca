import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

DATA_DIR = "data"
USUARIOS_CSV = f"{DATA_DIR}/usuarios.csv"
SOLICITUDES_CSV = f"{DATA_DIR}/solicitudes_proveedor.csv"
PROVEEDORES_CSV = f"{DATA_DIR}/proveedores.csv"
