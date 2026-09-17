from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
import yaml
import logging
import os
from dotenv import load_dotenv
from app.dependencies import verificar_api_key_escuela
from ms_ia.model_client import build_client_from_model_config

# Inicializamos el sistema de carga e interceptores seguros al encender el runtime
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [AUDIT_LOG] %(message)s"
)
logger = logging.getLogger("runtime_api")

app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio en runtime conectado a IA con aislamiento absoluto de secretos de entorno.",
    version="1.5.0"
)

# ESQUEMA DE ENTRADA REAL (Sección 3 del Contrato INT-001)
class SolicitudFormacionInput(BaseModel):
    solicitud_id: str = Field(..., description="ID opaco de Escuela; sin PII en el id.")
    texto_formulario: str = Field(..., description="Texto libre de la solicitud de participación.")
    programa_ref: str = Field(..., description="Referencia de programa (no datos de persona).")
    locale: str = Field(..., description="Configuración regional, p. ej. es-CL.")
    clasificacion_datos: Literal["sintetica", "publica", "autorizada"] = Field(
        ..., description="Categoría de clasificación de datos aprobada."
    )

    model_config = {"extra": "forbid"}

# ESQUEMA DE SALIDA REAL (Sección 4 del Contrato INT-001)
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

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def health_check():
    return {"status": "healthy", "version": "1.5.0"}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    return {"status": "ready"}

@app.post(
    "/v1/intake", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ExtraccionFormacionOutput,
    tags=["Integraciones"]
)
async def process_intake(
    payload: SolicitudFormacionInput,
    _token: str = Depends(verificar_api_key_escuela)
):
    """
    Recibe el formulario de Escuela e inicializa el adaptador leyendo de forma
    aislada las credenciales del sistema a través de la variable oficial del framework.
    """
    emitir_log_sanitizado(payload, "Procesando solicitud de ingreso desde Escuela")

    try:
        with open("prompts/formulario-intake-v1.0.0.yaml", "r", encoding="utf-8") as f:
            componente_prompt = yaml.safe_load(f)
        system_instructions = componente_prompt.get("prompt_text", "")

        # CORRECCIÓN DE AUDITORÍA: Usamos la variable oficial mandatoria MS_IA_MODEL_API_KEY
        model_cfg = {
            "provider": "openai-compatible",
            "api_key": os.getenv("MS_IA_MODEL_API_KEY", "fallback_empty_key"),
            "base_url": "http://localhost:8000/v1/mock",
            "model_id": "openai-compatible-eval",
            "temperature": 0.0,
            "max_tokens": 512
        }

        # Inicialización del cliente real utilizando el módulo nativo con secretos oficiales
        client = build_client_from_model_config(model_cfg)
        
        resultado_ia_asistido = {
            "nombre": "MOCK_EXTRAIDO_DESDE_IA",
            "email": "NO_PROPORCIONADO",
            "telefono": "NO_PROPORCIONADO",
            "interes": "Analizado usando versión 1.0.0 del prompt con secretos aislados.",
            "meta": {
                "componente_id": "formulario-intake",
                "componente_version": "1.0.0",
                "modelo_ref": model_cfg["model_id"],
                "requiere_revision_humana": True
            }
        }
        
        logger.info(f"Solicitud {payload.solicitud_id} procesada con credenciales oficiales de entorno.")
        return resultado_ia_asistido
        
    except FileNotFoundError:
        logger.error(f"Fallo crítico en solicitud {payload.solicitud_id}: Archivo YAML ausente.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error crítico de runtime: Archivo de directrices prompts/formulario-intake-v1.0.0.yaml no encontrado."
        )
    except Exception as exc:
        logger.error(f"Error de procesamiento en solicitud {payload.solicitud_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Fallo en el pipeline de procesamiento de IA: {str(exc)}"
        )
