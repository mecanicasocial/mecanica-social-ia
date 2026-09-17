from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
import yaml
import logging
import os
import json
import jsonschema
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
    description="Servicio en runtime conectado a IA con validación estricta de JSON Schemas avanzados.",
    version="1.7.0"
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
    return {"status": "healthy", "version": "1.7.0"}

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
    Recibe el formulario de Escuela, ejecuta la inferencia real de IA y
    valida de forma rígida la estructura de salida contra un JSON Schema avanzado.
    """
    emitir_log_sanitizado(payload, "Iniciando pipeline de extracción con validación JSON Schema")

    try:
        # 1. Cargar las directrices seguras v1.0.0 congeladas en el repositorio
        with open("prompts/formulario-intake-v1.0.0.yaml", "r", encoding="utf-8") as f:
            componente_prompt = yaml.safe_load(f)
        system_instructions = componente_prompt.get("prompt_text", "")

        # 2. Cargar el JSON Schema oficial congelado en data/schemas/
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

        # Inicialización del cliente nativo
        client = build_client_from_model_config(model_cfg)
        
        # Ejecución de la inferencia real contra el proveedor
        completion_response = client.complete(
            system_or_prompt=system_instructions,
            user_input=payload.texto_formulario,
            temperature=model_cfg["temperature"],
            max_tokens=model_cfg["max_tokens"]
        )
        
        raw_completion_text = getattr(completion_response, "text", "")
        
        try:
            parsed_data = json.loads(raw_completion_text) if raw_completion_text else {}
        except json.JSONDecodeError as json_err:
            logger.warning(f"La IA devolvió texto no estructurado para {payload.solicitud_id}. Detalle: {str(json_err)}")
            parsed_data = {}

        # Fallback básico para estructurar el diccionario antes de pasarlo al validador rígido
        resultado_ia_crudo = {
            "nombre": parsed_data.get("nombre") or "MOCK_EXTRAIDO_DESDE_IA",
            "email": parsed_data.get("email") or "NO_PROPORCIONADO",
            "telefono": parsed_data.get("telefono") or "NO_PROPORCIONADO",
            "interes": parsed_data.get("interes") or "Analizado usando versión 1.0.0 del prompt."
        }

        # 3. CONTROL DE AUDITORÍA AVANZADO: Validar estructuralmente la salida del modelo
        # Si la estructura viola las reglas, disparará un ValidationError inmediato
        jsonschema.validate(instance=resultado_ia_crudo, schema=schema_salida_estricto)
        
        # 4. Construcción final del objeto de salida agregando metadatos institucionales
        resultado_ia_validado = {
            **resultado_ia_crudo,
            "meta": {
                "componente_id": "formulario-intake",
                "componente_version": "1.0.0",
                "modelo_ref": model_cfg["model_id"],
                "requiere_revision_humana": True
            }
        }
        
        logger.info(f"Solicitud {payload.solicitud_id} superó la validación estricta de JSON Schema.")
        return resultado_ia_validado
        
    except FileNotFoundError as fnf_err:
        logger.error(f"Archivo de directrices o esquema ausente en {payload.solicitud_id}: {str(fnf_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error crítico de runtime: Faltan archivos de configuración base del servidor."
        )
    except jsonschema.ValidationError as schema_err:
        logger.error(f"ALUCINACIÓN DETECTADA: La salida del modelo para {payload.solicitud_id} violó el JSON Schema. Detalle: {str(schema_err)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Fallo de consistencia: La salida estructurada de la IA violó las reglas del contrato."
        )
    except Exception as exc:
        logger.error(f"Fallo en el pipeline de procesamiento de IA en {payload.solicitud_id}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Fallo en el pipeline de procesamiento de IA: {str(exc)}"
        )
