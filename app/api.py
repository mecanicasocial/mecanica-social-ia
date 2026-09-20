import contextlib
from app.database import inicializar_base_de_datos
import random
import time
from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict
import yaml, logging, os, json, time, jsonschema, httpx
from dotenv import load_dotenv
from app.dependencies import verificar_api_key_escuela
from ms_ia.model_client import build_client_from_model_config

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [AUDIT_LOG] %(message)s")
logger = logging.getLogger("runtime_api")
class PerimetralRateLimiter:
    def __init__(self, requests_limit: int = 5, window_seconds: float = 60.0):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.historial_consumos: Dict[str, list] = {}
    def verificar_limite(self, id_cliente: str) -> bool:
        ahora = time.time()
        if id_cliente not in self.historial_consumos: self.historial_consumos[id_cliente] = []
        m = [t for t in self.historial_consumos[id_cliente] if (ahora - t) < self.window_seconds]
        self.historial_consumos[id_cliente] = m
        if len(m) >= self.requests_limit: return False
        self.historial_consumos[id_cliente].append(ahora)
        return True

limitador_trafico = PerimetralRateLimiter(5, 60.0)
class IA_CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()
    def registrar_exito(self):
        self.failure_count = 0
        if self.state != "CLOSED": self.state = "CLOSED"; self.last_state_change = time.time()
    def registrar_fallo(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold and self.state != "OPEN": self.state = "OPEN"; self.last_state_change = time.time()
    def evaluar_estado(self):
        ahora = time.time()
        if self.state == "OPEN" and (ahora - self.last_state_change >= self.recovery_timeout):
            self.state = "HALF-OPEN"; self.last_state_change = ahora
        return self.state

disyuntor_ia = IA_CircuitBreaker(3, 30.0)
app = FastAPI(title="Mecánica Social IA - API REST", version="2.2.0")
class SolicitudFormacionInput(BaseModel):
    solicitud_id: str = Field(..., description="ID opaco.")
    texto_formulario: str = Field(..., description="Texto libre.")
    programa_ref: str = Field(..., description="Referencia.")
    locale: str = Field(..., description="Locale.")
    clasificacion_datos: Literal["sintetica", "publica", "autorizada"] = Field(..., description="Datos.")
    model_config = {"extra": "forbid"}

class MetaSalida(BaseModel):
    componente_id: str = "formulario-intake"
    componente_version: str = "1.0.0"
    modelo_ref: Optional[str] = "openai-compatible-eval"
    requiere_revision_humana: bool = True
    status_proceso: str = "accepted"
    tiempo_respuesta_ms: Optional[int] = None

class ExtraccionFormacionOutput(BaseModel):
    solicitud_id: str = Field(..., description="ID recibido.")
    status: str = "processing"
    meta: MetaSalida = Field(default_factory=MetaSalida)
def emitir_log_sanitizado(payload: SolicitudFormacionInput, mensaje: str, tiempo_ms: Optional[int] = None):
    log = {"solicitud_id": payload.solicitud_id, "programa_ref": payload.programa_ref, "texto_formulario": "[REDACTED_PII]", "tiempo_respuesta_ms": tiempo_ms}
    logger.info(f"{mensaje} | Metadata: {log}")

def disparar_webhook_escuela(solicitud_id: str, payload_estructurado: dict):
    ambiente_actual = os.getenv("AMBIENTE", "development")
    url_callback_escuela = os.getenv("ESCUELA_WEBHOOK_URL")
    
    # CONTROL PERIMETRAL MANDATORIO DE AUDITORÍA
    if ambiente_actual == "production" and not url_callback_escuela:
        logger.critical("[SANEAMIENTO_SEGURIDAD] INTEGRACIÓN BLOQUEADA: ESCUELA_WEBHOOK_URL es obligatoria en produccion.")
        raise RuntimeError("ESCUELA_WEBHOOK_URL es obligatoria en produccion")
        
    if ambiente_actual != "production":
        logger.warning(f"[MOCK_DEVELOPMENT] Barrera activa para {solicitud_id}. Simulacion de Webhook local para impedir fugas.")
        logger.info(f"[MOCK_DEVELOPMENT] Datos: {json.dumps(payload_estructurado)}")
        return

    logger.info(f"[WEBHOOK_DISPATCHER] Despachando notificacion hacia {url_callback_escuela}")
    try:
        headers = {"X-Event-Type": "intake.processed"}
        response = httpx.post(url_callback_escuela, json=payload_estructurado, headers=headers, timeout=5.0)
        logger.info(f"[WEBHOOK_DISPATCHER] Respuesta Escuela HTTP {response.status_code}")
    except Exception as err:
        logger.error(f"[WEBHOOK_DISPATCHER] Error de entrega: {str(err)}")

def ejecutar_fallback_contingencia(payload: SolicitudFormacionInput, razon: str, tiempo_ms: Optional[int] = None) -> dict:
    return {"nombre": "DEGRADADO_A_COLA_HUMANA", "email": "NO_PROPORCIONADO", "telefono": "NO_PROPORCIONADO", "interes": f"PROCESAMIENTO_DEGRADADO: {razon}", "meta": {"componente_id": "formulario-intake", "componente_version": "1.0.0", "modelo_ref": "FALLBACK", "requiere_revision_humana": True, "tiempo_respuesta_ms": tiempo_ms, "status_proceso": "degraded"}}
def disparar_notificacion_int002(solicitud_id: str, resultado_ia: dict, meta_ia: dict):
    """Implementación física de red del Contrato INT-002 para notificar resultados a la Escuela."""
    ambiente_actual = os.getenv("AMBIENTE", "development")
    url_notificacion = os.getenv("ESCUELA_NOTIFICACION_URL")
    
    payload_notificacion = {
        "solicitud_id": solicitud_id,
        "resultado": resultado_ia,
        "meta": meta_ia
    }
    
    # Validamos preventivamente contra el nuevo JSON Schema de INT-002 antes de transmitir
    try:
        with open("data/schemas/int-002-output.schema.json", "r", encoding="utf-8") as f:
            schema_int002 = json.load(f)
        jsonschema.validate(instance=payload_notificacion, schema=schema_int002)
        logger.info(f"[INT-002-VALIDATOR] Payload de notificacion validado con exito para {solicitud_id}")
    except Exception as s_err:
        logger.error(f"[INT-002-VALIDATOR] Error de consistencia interna en el esquema de notificacion: {str(s_err)}")
        return

    # Bloqueo Perimetral Mandatorio de Auditoría en Producción
    if ambiente_actual == "production" and not url_notificacion:
        logger.critical("[INT-002-SEGURIDAD] INTEGRACIÓN BLOQUEADA: ESCUELA_NOTIFICACION_URL es obligatoria en produccion.")
        raise RuntimeError("ESCUELA_NOTIFICACION_URL es obligatoria en produccion")
        
    if ambiente_actual != "production":
        logger.warning(f"[MOCK_DEVELOPMENT] Barrera INT-002 activa para {solicitud_id}. Simulacion de Notificacion local.")
        logger.info(f"[MOCK_DEVELOPMENT] Payload INT-002: {json.dumps(payload_notificacion)}")
        return

    logger.info(f"[INT-002-DISPATCHER] Iniciando secuencia de despacho resiliente hacia {url_notificacion}")
    headers = {"X-Event-Type": "inference.completed"}
    max_reintentos = 3
    base_espera = 2.0

    for intento in range(max_reintentos + 1):
        try:
            response = httpx.post(url_notificacion, json=payload_notificacion, headers=headers, timeout=5.0)
            
            # Si el código es transitorio del servidor (500, 502, 503), forzamos una excepción para reintentar
            if response.status_code in [500, 502, 503]:
                raise httpx.HTTPStatusError(f"Error de servidor HTTP {response.status_code}", request=None, response=response)
                
            logger.info(f"[INT-002-DISPATCHER] Exito absoluto en Intento {intento}. Respuesta Escuela HTTP {response.status_code}")
            return
            
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            logger.warning(f"[INT-002-RETRY_GATE] Intento {intento} fallido con error: {str(err)}")
            if intento == max_reintentos:
                logger.error("[INT-002-DISPATCHER] Se agotaron todos los reintentos logicos. El paquete de notificacion se descarta.")
                return
                
            # Algoritmo matemático: Base * 2^intento + Jitter aleatorio (-500ms a +500ms)
            jitter = random.uniform(-0.5, 0.5)
            espera_calculada = max(0.1, (base_espera * (2 ** intento)) + jitter)
            logger.info(f"[INT-002-RETRY_GATE] Aplicando Backoff Exponencial. Esperando {espera_calculada:.2f} segundos antes del siguiente intento...")
            time.sleep(espera_calculada)


def ejecutar_pipeline_background(payload: SolicitudFormacionInput):
    start_time = time.perf_counter()
    try:
        with open("prompts/formulario-intake-v1.0.0.yaml", "r", encoding="utf-8") as f: cp = yaml.safe_load(f)
        with open("data/schemas/int-001-output.schema.json", "r", encoding="utf-8") as f: ss = json.load(f)
        model_cfg = {"provider": "openai-compatible", "api_key": os.getenv("MS_IA_MODEL_API_KEY", "fallback"), "base_url": "http://localhost:8000/v1/mock", "model_id": "openai-compatible-eval", "temperature": 0.0, "max_tokens": 512}
        client = build_client_from_model_config(model_cfg)
        res = client.complete(system_or_prompt=cp.get("prompt_text", ""), user_input=payload.texto_formulario, temperature=0.0, max_tokens=512)
        tiempo_ms = int((time.perf_counter() - start_time) * 1000)
        parsed = json.loads(getattr(res, "text", "")) if getattr(res, "text", "") else {}
        crudo = {"nombre": parsed.get("nombre") or "MOCK_EXTRAIDO", "email": parsed.get("email") or "NO_PR", "telefono": parsed.get("telefono") or "NO_PR", "interes": parsed.get("interes") or "Analizado."}
        disyuntor_ia.registrar_exito()
        final = {**crudo, "meta": {"componente_id": "formulario-intake", "componente_version": "1.0.0", "modelo_ref": "openai-compatible-eval", "requiere_revision_humana": True, "tiempo_respuesta_ms": tiempo_ms, "status_proceso": "completed"}}
        jsonschema.validate(instance=final, schema=ss)
        disparar_webhook_escuela(payload.solicitud_id, final)
    except Exception as exc:
        tiempo_ms = int((time.perf_counter() - start_time) * 1000); disyuntor_ia.registrar_fallo()
        resultado_fallback = ejecutar_fallback_contingencia(payload, str(exc), tiempo_ms)
        jsonschema.validate(instance=resultado_fallback, schema=ss)
        disparar_webhook_escuela(payload.solicitud_id, resultado_fallback)
@app.get("/health")
async def health_check(): return {"status": "healthy", "version": "2.2.0", "circuit_state": disyuntor_ia.state}
@app.get("/ready")
async def ready_check():
    if disyuntor_ia.evaluar_estado() == "OPEN": raise HTTPException(status_code=503, detail="Abierto.")
    return {"status": "ready"}
@app.post("/v1/intake", status_code=202, response_model=ExtraccionFormacionOutput)
async def process_intake(payload: SolicitudFormacionInput, background_tasks: BackgroundTasks, _token: str = Depends(verificar_api_key_escuela)):
    emitir_log_sanitizado(payload, "Interceptando solicitud HTTP")
    if not limitador_trafico.verificar_limite(_token):
        raise HTTPException(status_code=429, detail="Tasa de solicitudes excedida. Límite de infraestructura: Máximo 5 peticiones por minuto.")
    if disyuntor_ia.evaluar_estado() == "OPEN":
        raise HTTPException(status_code=503, detail="Servicio degradado.")
    background_tasks.add_task(ejecutar_pipeline_background, payload)
    return {"solicitud_id": payload.solicitud_id, "status": "processing", "meta": {"componente_id": "formulario-intake", "componente_version": "1.0.0", "modelo_ref": "openai-compatible-eval", "requiere_revision_humana": True, "status_proceso": "accepted"}}
