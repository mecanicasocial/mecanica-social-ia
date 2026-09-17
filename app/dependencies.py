from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env local de forma segura al inicializar
load_dotenv()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Extraemos la credencial directamente desde las variables del sistema
# Si no se encuentra configurada, degradamos a None por seguridad de auditoría
API_KEY_REAL_IA = os.getenv("API_KEY_ESCUELA_TOKEN")

async def verificar_api_key_escuela(api_key_solicitada: str = Security(api_key_header)) -> str:
    """
    Dependencia de seguridad perimetral que extrae y valida dinámicamente la API Key
    desde las variables de entorno locales, eliminando credenciales quemadas en código.
    """
    if not api_key_solicitada:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el encabezado de autenticación obligatorio: X-API-Key"
        )
    
    # Si la variable de entorno está ausente o la firma es inválida, se bloquea el acceso
    if not API_KEY_REAL_IA or api_key_solicitada != API_KEY_REAL_IA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credencial inválida o no autorizada para consumir el Contrato INT-001."
        )
        
    return api_key_solicitada
