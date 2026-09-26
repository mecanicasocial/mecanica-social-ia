import re
import logging
from src.ms_ia.model_client import IAClient

logger = logging.getLogger("IA-API")

PATRONES_INYECCION = [
    r"ignore\s+all\s+previous\s+instructions",
    r"system\s*:",
    r"disregard\s+above",
    r"you\s+are\s+now\s+a",
    r"eval\(",
    r"<script>"
]

def sanitizar_prompt(prompt_usuario: str) -> str:
    """
    Sanitiza y valida la entrada descartando patrones maliciosos.
    """
    if not prompt_usuario or not isinstance(prompt_usuario, str):
        raise ValueError("Entrada inválida o vacía.")

    prompt_limpio = prompt_usuario.strip()

    for patron in PATRONES_INYECCION:
        if re.search(patron, prompt_limpio, re.IGNORECASE):
            logger.warning(f"Intento de inyección detectado: {patron}")
            raise ValueError("Consulta bloqueada por políticas de seguridad.")

    return prompt_limpio

def procesar_consulta(prompt: str) -> dict:
    try:
        prompt_valido = sanitizar_prompt(prompt)
        cliente = IAClient()
        respuesta = cliente.generar_respuesta(prompt_valido)
        return {"status": "success", "respuesta": respuesta}
    except ValueError as e:
        return {"status": "error", "mensaje": str(e)}
    except Exception:
        return {"status": "error", "mensaje": "Fallo interno en el servicio de IA."}
