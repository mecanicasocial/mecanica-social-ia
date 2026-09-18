from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
import yaml
import logging
import os
import json
import time
import jsonschema
from app.dependencies import verificar_api_key_escuela
from ms_ia.model_client import build_client_from_model_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [AUDIT_LOG] %(message)s"
)
logger = logging.getLogger("runtime_api")

class IA_CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()

    def registrar_exito(self):
        self.failure_count = 0
        if self.state != "CLOSED":
            logger.info(f"[CIRCUIT_BREAKER] Recuperado. Cambiando a CLOSED.")
            self.state = "CLOSED"
            self.last_state_change = time.time()

    def registrar_fallo(self):
        self.failure_count += 1
        logger.warning(f"[CIRCUIT_BREAKER] Fallo registrado ({self.failure_count}/{self.failure_threshold}).")
        if self.failure_count >= self.failure_threshold and self.state != "OPEN":
            logger.critical(f"[CIRCUIT_BREAKER] ¡SALTANDO DISYUNTOR! Cambiando a OPEN.")
            self.state = "OPEN"
            self.last_state_change = time.time()

    def evaluar_estado(self):
        ahora = time.time()
        if self.state == "OPEN":
            if ahora - self.last_state_change >= self.recovery_timeout:
                logger.warning("[CIRCUIT_BREAKER] Enfriamiento cumplido. Cambiando a HALF-OPEN.")
                self.state = "HALF-OPEN"
                self.last_state_change = ahora
        return self.state

disyuntor_ia = IA_CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)

app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio conectado a IA blindado con un Circuit Breaker (Disyuntor).",
    version="1.8.0"
)

class SolicitudFormacionInput(BaseModel):
    solicitud_id: str = Field(..., description="ID opaco de Escuela; sin PII en el id.")
    texto_formulario: str = Field(..., description="Texto libre de la solicitud de participación.")
    programa_ref: str = Field(..., description="Referencia de programa (no datos de persona).")
    locale: str = Field(..., description="Configuración regional, p. ej. es-CL.")
    clasificacion_datos: Literal["sintetica", "publica", "autorizada"] = Field(
        ..., description="Categoría de clasificación de datos aprobada."
    )
    model_config = {"extra": "forbid"}

class MetaSalida(BaseModel):
    componente_id: str = "formulario-intake"
    componente_version: str = "1.0.0"
    modelo_ref: Optional[str] = "openai-compatible-eval"
    requiere_revision_humana: bool = True

class ExtraccionFormacionOutput(BaseModel):
    nombre: str = Field(..., description="Nombre extraído por el componente de IA.")
    email: str = Field(..., description="Correo electrónico extraído o marcador.")
    telefono: str = Field(..., description="Teléfono extraído o marcador.")
    interes: str = Field(..., description="Interés analizado por el modelo.")
    meta: MetaSalida = Field(default_factory=MetaSalida)

def emitir_log_sanitizado(payload: SolicitudFormacionInput, mensaje_accion: str):
    log_seguro = {
        "solicitud_id": payload.solicitud_id,
        "programa_ref": payload.programa_ref,
        "locale": payload.locale,
        "clasificacion_datos": payload.clasificacion_datos,
        "texto_formulario": "[REDACTED_PII]"
    }
    logger.info(f"{mensaje_accion} | Metadata Institucional: {log_seguro}")

def ejecutar_fallback_contingencia(payload: SolicitudFormacionInput, razon: str) -> dict:
    logger.info(f"Estructurando payload seguro de degradación para la cola humana. Motivo: {razon}")
    return {
        "nombre": "DEGRADADO_A_COLA_HUMANA",
        "email": "NO_PROPORCIONADO",
        "telefono": "NO_PROPORCIONADO",
        "interes": "PROCESAMIENTO_DEGRADADO: El motor de IA experimentó una indisponibilidad temporal. El formulario requiere extracción manual por personal calificado.",
        "meta": {
            "componente_id": "formulario-intake",
            "componente_version": "1.0.0",
            "modelo_ref": f"FALLBACK_DEGRADATION_{razon}",
            "requiere_revision_humana": True
        }
    }

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def health_check():
    return {"status": "healthy", "version": "1.8.0", "circuit_state": disyuntor_ia.state}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    if disyuntor_ia.evaluar_estado() == "OPEN":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio parcialmente degradado: El motor de IA no está aceptando conexiones."
        )
    return {"status": "ready"}

@app.post("/v1/intake", status_code=status.HTTP_201_CREATED, response_model=ExtraccionFormacionOutput, tags=["Integraciones"])
async def process_intake(payload: SolicitudFormacionInput, _token: str = Depends(verificar_api_key_escuela)):
    emitir_log_sanitizado(payload, "Evaluando estado del disyuntor perimetral")
    
    if disyuntor_ia.evaluar_estado() == "OPEN":
        logger.critical(f"[CIRCUIT_BREAKER] Solicitud {payload.solicitud_id} desviada de inmediato a CONTINGENCIA por circuito OPEN.")
        return ejecutar_fallback_contingencia(payload, razon="CIRCUIT_BREAKER_OPEN")

    try:
        with open("prompts/formulario-intake-v1.0.0.yaml", "r", encoding="utf-8") as f:
            componente_prompt = yaml.safe_load(f)
        system_instructions = componente_prompt.get("prompt_text", "")

        with open("data/schemas/int-001-output.schema.json", "r", encoding="utf-8") as f:
            schema_salida_estricto = json.load(f)

        model_cfg = {
            "provider": "openai-compatible",
            "api_key": os.getenv("MS_IA_MODEL_API_KEY", "fallback_empty_key"),
            "base_url": "http://localhost:8000/v1/mock",
            "model_id": "openai-compatible-eval",
            "temperature": 0.0,
            "max_tokens": 512
        }

        client = build_client_from_model_config(model_cfg)
        
        completion_response = client.complete(
            system_or_prompt=system_instructions,
            user_input=payload.texto_formulario,
            temperature=model_cfg["temperature"],
            max_tokens=model_cfg["max_tokens"]
        )
        
        raw_completion_text = getattr(completion_response, "text", "")
        parsed_data = json.loads(raw_completion_text) if raw_completion_text else {}

        resultado_ia_crudo = {
            "nombre": parsed_data.get("nombre") or "MOCK_EXTRAIDO_DESDE_IA",
            "email": parsed_data.get("email") or "NO_PROPORCIONADO",
            "telefono": parsed_data.get("telefono") or "NO_PROPORCIONADO",
            "interes": parsed_data.get("interes") or "Analizado usando versión 1.0.0 del prompt."
        }

        jsonschema.validate(instance=resultado_ia_crudo, schema=schema_salida_estricto)
        disyuntor_ia.registrar_exito()
        
        return {
            **resultado_ia_crudo,
            "meta": {
                "componente_id": "formulario-intake",
                "componente_version": "1.0.0",
                "modelo_ref": model_cfg["model_id"],
                "requiere_revision_humana": True
            }
        }
        
    except (jsonschema.ValidationError, FileNotFoundError) as contractual_err:
        logger.error(f"Fallo contractual controlado para {payload.solicitud_id}: {str(contractual_err)}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(contractual_err))
        
    except Exception as network_or_quota_err:
        logger.error(f"[CIRCUIT_BREAKER] Excepción de infraestructura detectada en {payload.solicitud_id}: {str(network_or_quota_err)}")
        disyuntor_ia.registrar_fallo()
        logger.warning(f"Gatillando Fallback operativo inmediato en {payload.solicitud_id}.")
        return ejecutar_fallback_contingencia(payload, razon=f"IA_PROVIDER_EXCEPTION")
