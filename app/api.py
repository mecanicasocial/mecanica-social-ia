import json
import contextlib
import random
import time
from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict
import yaml, logging, os, json, jsonschema, httpx
from dotenv import load_dotenv
from app.dependencies import verificar_api_key_escuela
import app.database as db_mod

load_dotenv()

from cryptography.fernet import Fernet
import os
from cryptography.fernet import Fernet
import os
from cryptography.fernet import Fernet
SECRET_CRYPTO_KEY = os.getenv("MS_IA_CRYPTO_KEY")
if not SECRET_CRYPTO_KEY:
    raise RuntimeError("Configuración Insegura: Falta la clave de cifrado MS_IA_CRYPTO_KEY inyectada.")
if isinstance(SECRET_CRYPTO_KEY, str):
    SECRET_CRYPTO_KEY = SECRET_CRYPTO_KEY.encode()
cs = Fernet(SECRET_CRYPTO_KEY)
RESET = "\033[0m"
ROJO = "\033[31m"
VERDE = "\033[32m"
CIAN = "\033[36m"
MAGENTA = "\033[35m"

class ColorFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        if "[SANEAMIENTO_SEGURIDAD]" in msg or "[INT-002-SEGURIDAD]" in msg or "CRITICAL" in record.levelname:
            return f"{ROJO}{msg}{RESET}"
        elif "INT-001" in msg or "PIPELINE" in msg or "PERIMETRAL" in msg:
            return f"{CIAN}{msg}{RESET}"
        elif "INT-002" in msg or "RETRY_GATE" in msg or "DATABASE" in msg:
            return f"{MAGENTA}{msg}{RESET}"
        elif "VALIDACIÓN EXITOSA" in msg or "Exito" in msg:
            return f"{VERDE}{msg}{RESET}"
        return msg
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger = logging.getLogger("runtime_api")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

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

@contextlib.asynccontextmanager
async def lifespan(app_fastapi: FastAPI):
    try:
        db_mod.inicializar_base_de_datos()
    except Exception as e:
        logger.error(f"[LIFESPAN_CRITICAL] No se pudo inicializar el almacenamiento: {str(e)}")
    yield
    logger.info("[LIFESPAN] Apagando Runtime de IA de forma segura.")

app = FastAPI(title="Mecánica Social IA - API REST", version="2.2.0", lifespan=lifespan)
class SolicitudFormacionInput(BaseModel):
    solicitud_id: str = Field(..., description="ID opaco.")
    texto_formulario: str = Field(..., description="Texto libre.")
    programa_ref: str = Field(..., description="Referencia.")
    locale: str = Field(..., description="Locale.")
    clasificacion_datos: Literal["sintetica", "publica", "autorizada"] = Field(..., description="Datos.")
    acepta_politica_privacidad: bool = Field(..., description="Consentimiento legal mandatorio.")
    version_terminos: str = Field(..., description="Version terminos.")
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
    if ambiente_actual == "production" and not url_callback_escuela:
        logger.critical("[SANEAMIENTO_SEGURIDAD] INTEGRACIÓN BLOQUEADA: ESCUELA_WEBHOOK_URL es obligatoria.")
        raise RuntimeError("ESCUELA_WEBHOOK_URL es obligatoria en produccion")
    if ambiente_actual != "production":
        logger.warning(f"[MOCK_DEVELOPMENT] Barrera activa para {solicitud_id}. Simulacion de Webhook local.")
        return
    try:
        headers = {"X-Event-Type": "intake.processed"}
        httpx.post(url_callback_escuela, json=payload_estructurado, headers=headers, timeout=5.0)
    except Exception as err:
        logger.error(f"[WEBHOOK_DISPATCHER] Error de entrega: {str(err)}")

def ejecutar_fallback_contingencia(payload: SolicitudFormacionInput, razon: str, tiempo_ms: Optional[int] = None) -> dict:
    return {"nombre": "DEGRADADO_A_COLA_HUMANA", "email": "NO_PROPORCIONADO", "telefono": "NO_PROPORCIONADO", "interes": f"PROCESAMIENTO_DEGRADADO: {razon}", "meta": {"componente_id": "formulario-intake", "componente_version": "1.0.0", "modelo_ref": "FALLBACK", "requiere_revision_humana": True, "tiempo_respuesta_ms": tiempo_ms, "status_proceso": "degraded"}}

def disparar_notificacion_int002(solicitud_id: str, resultado_ia: dict, meta_ia: dict):
    ambiente_actual = os.getenv("AMBIENTE", "development")
    url_notificacion = os.getenv("ESCUELA_NOTIFICACION_URL")
    payload_notificacion = {"solicitud_id": solicitud_id, "resultado": resultado_ia, "meta": meta_ia}
    try:
        with open("data/schemas/int-002-output.schema.json", "r", encoding="utf-8") as f:
            schema_int002 = json.load(f)
        jsonschema.validate(instance=payload_notificacion, schema=schema_int002)
    except Exception as s_err:
        logger.error(f"[INT-002-VALIDATOR] Error de esquema: {str(s_err)}")
        return
    if ambiente_actual == "production" and not url_notificacion:
        raise RuntimeError("ESCUELA_NOTIFICACION_URL es obligatoria en produccion")
    if ambiente_actual != "production":
        logger.warning(f"[MOCK_DEVELOPMENT] Barrera INT-002 activa para {solicitud_id}.")
        return
    headers = {"X-Event-Type": "inference.completed"}
    max_reintentos = 3
    base_espera = 2.0
    for intento in range(max_reintentos + 1):
        try:
            response = httpx.post(url_notificacion, json=payload_notificacion, headers=headers, timeout=5.0)
            if response.status_code in [500, 502, 503]:
                raise httpx.HTTPStatusError("Falla transitoria", request=None, response=response)
            return
        except Exception as err:
            logger.warning(f"[INT-002-RETRY_GATE] Intento {intento} fallido con error: Simulación HTTP")
            if intento == max_reintentos: return
            time.sleep(max(0.1, (base_espera * (2 ** intento)) + random.uniform(-0.5, 0.5)))
def ejecutar_pipeline_background(payload: SolicitudFormacionInput):
    import sqlite3
    logger.info(f"[PIPELINE-BACKGROUND] Inicializando extraccion asincrona para {payload.solicitud_id}")
    try:
        if disyuntor_ia.evaluar_estado() == "OPEN":
            raise RuntimeError("Circuito de IA abierto de forma preventiva.")
                # Conexión real al cliente OpenAI compatible
        from ms_ia.model_client import OpenAICompatibleClient
        base_url_ia = os.getenv("MS_IA_MODEL_BASE_URL", "http://127.0.0.1:8001")
        api_key_ia = os.getenv("MS_IA_MODEL_API_KEY", "mock_key")
        model_id_ia = os.getenv("MS_IA_MODEL_ID", "fake-llm-advanced-7b")
        client_ia = OpenAICompatibleClient(base_url=base_url_ia, api_key=api_key_ia, model_id=model_id_ia, timeout_sec=float(os.getenv("MODEL_TIMEOUT_SECONDS", "30.0")))
        t_inicio = time.time()
        resultado_ia = client_ia.complete(system_or_prompt="Extrae campos JSON", user_input=payload.texto_formulario)
        tiempo_ms = int((time.time() - t_inicio) * 1000)
        texto_ia = getattr(resultado_ia, "text", "") or ""
        parsed = json.loads(texto_ia) if texto_ia else {}
        final = {
            "nombre": parsed.get("nombre") or "NO_PR",
            "email": parsed.get("email") or "NO_PR",
            "telefono": parsed.get("telefono") or "NO_PR",
            "interes": parsed.get("interes") or "NO_PR",
            "meta": {"componente_id": "formulario-intake", "componente_version": "1.0.0",
                     "modelo_ref": model_id_ia, "requiere_revision_humana": True,
                     "tiempo_respuesta_ms": tiempo_ms, "status_proceso": "completed"},
        }
        disyuntor_ia.registrar_exito()
    except Exception as e:
        disyuntor_ia.registrar_fallo()
        logger.error(f"🔴 [PIPELINE-EXC] Aborto por error: {str(e)}")
        final = ejecutar_fallback_contingencia(payload, str(e), 5)
    try:
        fecha_notif = time.strftime("%Y-%m-%d %H:%M:%S")
        status_final = final["meta"].get("status_proceso", "completed")
        with sqlite3.connect(db_mod.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("UPDATE solicitudes_intake SET status_actual = ? WHERE solicitud_id = ?;", (status_final, payload.solicitud_id))
            cursor.execute("""
                INSERT INTO resultados_inferencia (solicitud_id, nombre_extraido, email_extraido, telefono_extraido, interes_extraido, modelo_ref, tiempo_respuesta_ms, fecha_notificacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(solicitud_id) DO UPDATE SET nombre_extraido=excluded.nombre_extraido, email_extraido=excluded.email_extraido, telefono_extraido=excluded.telefono_extraido, interes_extraido=excluded.interes_extraido, modelo_ref=excluded.modelo_ref, tiempo_respuesta_ms=excluded.tiempo_respuesta_ms, fecha_notificacion=excluded.fecha_notificacion;
            """, (payload.solicitud_id, final.get("nombre", "NO_PR"), final.get("email", "NO_PR"), final.get("telefono", "NO_PR"), final.get("interes", "NO_PR"), final["meta"].get("modelo_ref", "FALLBACK"), final["meta"].get("tiempo_respuesta_ms", 0), fecha_notif))
            conn.commit()
        logger.info(f"🟢 [DATABASE-BACKGROUND] Sincronizacion exitosa para {payload.solicitud_id}. Estado: {status_final}")
    except Exception as db_err2:
        logger.error(f"🔴 [DATABASE-BACKGROUND] Error al persistir resultados: {str(db_err2)}")
    disparar_webhook_escuela(payload.solicitud_id, final)
    resultado_puro = {k: v for k, v in final.items() if k != "meta"}
    disparar_notificacion_int002(payload.solicitud_id, resultado_puro, final["meta"])
@app.get("/v1/intake/{solicitud_id}")
def obtener_registro_intake(solicitud_id: str, autenticado: bool = Depends(verificar_api_key_escuela)):
    import sqlite3
    with sqlite3.connect(db_mod.DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT solicitud_id, programa_ref, fecha_recepcion, status_actual FROM solicitudes_intake WHERE solicitud_id = ?;", (solicitud_id,))
        fila_madre = cursor.fetchone()
        if not fila_madre:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        cursor.execute("SELECT nombre_extraido, email_extraido, telefono_extraido, interes_extraido, modelo_ref, tiempo_respuesta_ms, fecha_notificacion FROM resultados_inferencia WHERE solicitud_id = ?;", (solicitud_id,))
        fila_hija = cursor.fetchone()
        return {**dict(fila_madre), "extraccion_estructurada_ia": dict(fila_hija) if fila_hija else None}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.2.0", "circuit_state": disyuntor_ia.evaluar_estado()}

@app.post("/v1/intake", response_model=ExtraccionFormacionOutput, status_code=status.HTTP_202_ACCEPTED)
def registrar_solicitud_intake(payload: SolicitudFormacionInput, background_tasks: BackgroundTasks, autenticado: bool = Depends(verificar_api_key_escuela)):
    emitir_log_sanitizado(payload, "Interceptando solicitud HTTP")
    
    # 🔞 REGLA DE PRODUCTO: Declaración y control perimetral de edad y datos sensibles (Ley 21.719)
    texto_analizar = payload.texto_formulario.lower()
    
    if any(p in texto_analizar for p in ["menor de edad", "tengo 16", "tengo 17", "tengo 15"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingesta rechazada: El programa de formación está reservado exclusivamente para mayores de edad."
        )
        
    if any(p in texto_analizar for p in ["rut ", "r.u.t", "clave", "patologia", "medico"]):
        logger.warning("⚠️ [DATA-GOVERNANCE] Alerta: Se detectó potencial PII sensible no autorizada en el formulario libre.")
    if disyuntor_ia.evaluar_estado() == "OPEN":
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Circuito de Inteligencia Artificial abierto de forma preventiva.")
    if not limitador_trafico.verificar_limite(autenticado):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Tasa de solicitudes excedida")
    import sqlite3
    try:
        fecha_actual = time.strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(db_mod.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("""
                INSERT INTO solicitudes_intake (solicitud_id, programa_ref, texto_crudo, fecha_recepcion, status_actual) VALUES (?, ?, ?, ?, ?) ON CONFLICT(solicitud_id) DO UPDATE SET programa_ref=excluded.programa_ref, texto_crudo=excluded.texto_crudo, status_actual=excluded.status_actual;
            """, (payload.solicitud_id, payload.programa_ref, cs.encrypt(payload.texto_formulario.encode()).decode(), fecha_actual, "processing"))
            conn.commit()
        logger.info(f"🟢 [DATABASE-POST-INTAKE] Solicitud {payload.solicitud_id} registrada con exito en estado: processing")
    except Exception as db_err:
        logger.error(f"🔴 [DATABASE-POST-INTAKE] Error critico de persistencia: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno: No se pudo registrar la solicitud en el almacenamiento duradero de la ONG."
        )
    background_tasks.add_task(ejecutar_pipeline_background, payload)
    return ExtraccionFormacionOutput(solicitud_id=payload.solicitud_id)
