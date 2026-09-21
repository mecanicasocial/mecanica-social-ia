import os
import hmac
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verificar_api_key_escuela(api_key_recibida: str = Security(api_key_header)) -> bool:
    """Valida criptográficamente la API Key de la Escuela mediante compare_digest contra Timing Attacks."""
    api_key_real = os.getenv("API_KEY_ESCUELA_TOKEN", "ms_ia_secure_token_int_001_env_secured")
    
    if not api_key_recibida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta la cabecera de autenticación X-API-Key perimetral."
        )
        
    # 🛡️ REMEDIACIÓN AUDITORÍA: Comparación en tiempo constante para mitigación de ataques de canal lateral
    if not hmac.compare_digest(api_key_recibida, api_key_real):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credencial perimetral inválida o caducada para Mecánica Social IA."
        )
    return api_key_recibida