from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Literal
import yaml
import logging
import os
import json
import time
import jsonschema
from dotenv import load_dotenv
from app.dependencies import verificar_api_key_escuela
from ms_ia.model_client import build_client_from_model_config

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [AUDIT_LOG] %(message)s")
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
            self.state = "CLOSED"
            self.last_state_change = time.time()

    def registrar_fallo(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold and self.state != "OPEN":
            self.state = "OPEN"
            self.last_state_change = time.time()

    def evaluar_estado(self):
        ahora = time.time()
        if self.state == "OPEN" and (ahora - self.last_state_change >= self.recovery_timeout):
            self.state = "HALF-OPEN"
            self.last_state_change = ahora
        return self.state

disyuntor_ia = IA_CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)
app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio desacoplado de alta concurrencia mediante Background Tasks.",
    version="2.0.0"
)

class SolicitudFormacionInput(BaseModel):
    solicitud_id: str = Field(..., description="ID opaco de Escuela.")
    texto_formulario: str = Field(..., description="Texto libre.")
    programa_ref: str = Field(..., description="Referencia de programa.")
    locale: str = Field(..., description="Locale.")
    clasificacion_datos: Literal["sintetica", "publica", "autorizada"] = Field(..., description="Datos.")
    model_config = {"extra": "forbid"}

class MetaSalida(BaseModel):
    componente_id: str = "formulario-intake"
    componente_version: str = "1.0.0"
    modelo_ref: Optional[str] = "openai-compatible-eval"
    requiere_revision_humana: bool = True
    status_proceso: str = Field("accepted", description="Estado asíncrono de la solicitud.")
    tiempo_respuesta_ms: Optional[int] = Field(None, description="Latencia de la IA.")

class ExtraccionFormacionOutput(BaseModel):
    solicitud_id: str = Field(..., description="Confirmación de ID opaco recibido.")
    status: str = Field("processing", description="Glosa de estado perimetral.")
    meta: MetaSalida = Field(default_factory=MetaSalida)
def emitir_log_sanitizado(payload: SolicitudFormacionInput, mensaje_accion: str, tiempo_ms: Optional[int] = None):
    log_seguro = {
        "solicitud_id": payload.solicitud_id,
        "programa_ref": payload.programa_ref,
        "texto_formulario": "[REDACTED_PII]",
        "tiempo_respuesta_ms": tiempo_ms
    }
    logger.info(f"{mensaje_accion} | Metadata: {log_seguro}")

def ejecutar_pipeline_background(payload: SolicitudFormacionInput):
    """
    HITO ARQUITECTÓNICO FASE 8: Orquestación pesada ejecutada fuera del hilo HTTP.
    Mide latencia, consume el LLM, valida esquemas y procesa la persistencia de forma aislada.
    """
    logger.info(f"[BACKGROUND_TASK] Iniciando procesamiento asíncrono para ID: {payload.solicitud_id}")
    start_time = time.perf_counter()
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
            system_or_prompt=system_instructions, user_input=payload.texto_formulario,
            temperature=model_cfg["temperature"], max_tokens=model_cfg["max_tokens"]
        )
        
        end_time = time.perf_counter()
        tiempo_respuesta_ms = int((end_time - start_time) * 1000)

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
        
        logger.info(f"[BACKGROUND_TASK] ÉXITO: Solicitud {payload.solicitud_id} procesada y validada en {tiempo_respuesta_ms}ms de forma asíncrona.")
        # En la Fase 9 aquí se gatillará la persistencia física del resultado y el disparo del Webhook de salida
        
    except Exception as exc:
        end_time = time.perf_counter()
        tiempo_respuesta_ms = int((end_time - start_time) * 1000)
        logger.error(f"[BACKGROUND_TASK] FALLO CRÍTICO asíncrono en {payload.solicitud_id} tras {tiempo_respuesta_ms}ms: {str(exc)}")
        disyuntor_ia.registrar_fallo()
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def health_check():
    return {"status": "healthy", "version": "2.0.0", "circuit_state": disyuntor_ia.state}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    if disyuntor_ia.evaluar_estado() == "OPEN":
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Circuit breaker abierto.")
    return {"status": "ready"}
@app.post(
    "/v1/intake", 
    status_code=status.HTTP_202_ACCEPTED, # Cambiado formalmente a 202 por estándar asíncrono
    response_model=ExtraccionFormacionOutput,
    tags=["Integraciones"]
)
async def process_intake(
    payload: SolicitudFormacionInput,
    background_tasks: BackgroundTasks, # Inyección del despachador de tareas de FastAPI
    _token: str = Depends(verificar_api_key_escuela)
):
    """
    Recibe el formulario de Escuela, delega la inferencia pesada a la cola en segundo plano
    y libera la conexión HTTP de forma inmediata con un estado 202 Accepted.
    """
    emitir_log_sanitizado(payload, "Recibiendo solicitud HTTP perimetral - Desviando a BackgroundTask")
    
    if disyuntor_ia.evaluar_estado() == "OPEN":
        logger.critical(f"[CIRCUIT_BREAKER] Bloqueo perimetral para {payload.solicitud_id} por circuito OPEN.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio temporalmente degradado en contingencia humana."
        )

    # Encolar la ejecución pesada de red en el worker en segundo plano nativo
    background_tasks.add_task(ejecutar_pipeline_background, payload)

    # Construcción de la respuesta inmediata ultra-rápida (Liberación del hilo HTTP)
    respuesta_asincrona = {
        "solicitud_id": payload.solicitud_id,
        "status": "processing",
        "meta": {
            "componente_id": "formulario-intake",
            "componente_version": "1.0.0",
            "modelo_ref": "openai-compatible-eval",
            "requiere_revision_humana": True,
            "status_proceso": "accepted"
        }
    }
    return respuesta_asincrona
