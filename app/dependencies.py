from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# 1. Definición del estándar del encabezado HTTP exigido por el contrato
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# 2. Token provisional para la fase técnica de prueba
API_KEY_PROVISIONAL_IA = "ms_ia_secure_token_int_001_prov"

async def verificar_api_key_escuela(api_key_solicitada: str = Security(api_key_header)) -> str:
    """
    Dependencia de seguridad que valida la autenticidad del emisor.
    Garantiza que solo peticiones legítimas firmadas por la Escuela consuman el runtime.
    """
    if not api_key_solicitada:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el encabezado de autenticación obligatorio: X-API-Key"
        )
    
    if api_key_solicitada != API_KEY_PROVISIONAL_IA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credencial inválida o no autorizada para consumir el Contrato INT-001."
        )
        
    return api_key_solicitada
