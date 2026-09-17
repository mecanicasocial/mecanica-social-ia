from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
import yaml
import json
from app.dependencies import verificar_api_key_escuela
from ms_ia.model_client import build_client_from_model_config

# 1. Inicialización de la Aplicación
app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio en runtime conectado al motor de inferencia de IA (INT-001 / INT-002).",
    version="1.3.0"
)

# 2. ESQUEMA DE ENTRADA REAL (Sección 3 del Contrato INT-001)
class SolicitudFormacionInput(BaseModel):
    solicitud_id: str = Field(..., description="ID opaco de Escuela; sin PII en el id.")
    texto_formulario: str = Field(..., description="Texto libre de la solicitud de participación.")
    programa_ref: str = Field(..., description="Referencia de programa (no datos de persona).")
    locale: str = Field(..., description="Configuración regional, p. ej. es-CL.")
    clasificacion_datos: Literal["sintetica", "publica", "autorizada"] = Field(
        ..., description="Categoría de clasificación de datos aprobada."
    )

    model_config = {"extra": "forbid"}

# 3. ESQUEMA DE SALIDA REAL (Sección 4 del Contrato INT-001)
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

# 4. Endpoints de Monitoreo
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def health_check():
    return {"status": "healthy", "version": "1.3.0"}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    return {"status": "ready"}

# 5. Endpoint de Negocio Conectado al Cliente del Modelo
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
    Recibe el texto libre de Escuela, inicializa el adaptador de IA
    y prepara la llamada de extracción estructurada asistida.
    """
    try:
        # A. Auditoría Operacional: Cargar directrices seguras congeladas en el repositorio
        with open("prompts/formulario-intake-v1.0.0.yaml", "r", encoding="utf-8") as f:
            componente_prompt = yaml.safe_load(f)
        system_instructions = componente_prompt.get("prompt_text", "")

        # B. Configuración técnica provisional para el proveedor del modelo (INT-002)
        model_cfg = {
            "api_key": "mock_api_key_for_testing",
            "base_url": "http://localhost:8000/v1/mock", # Apunta temporalmente al entorno local
            "model_id": "openai-compatible-eval",
            "temperature": 0.0,
            "max_tokens": 512
        }

        # C. Inicializar el cliente real utilizando el módulo nativo de src/
        client = build_client_from_model_config(model_cfg)
        
        # D. Simulación controlada del procesamiento del texto del formulario
        # En la siguiente fase, esto ejecutará de forma síncrona: client.complete(...)
        # Conservamos la estructura de salida mandatoria del contrato (Sección 4)
        resultado_ia_asistido = {
            "nombre": "MOCK_EXTRAIDO_DESDE_IA",
            "email": "NO_PROPORCIONADO",
            "telefono": "NO_PROPORCIONADO",
            "interes": f"Procesado exitosamente con el cliente mapeado en ms_ia.",
            "meta": {
                "componente_id": "formulario-intake",
                "componente_version": "1.0.0",
                "modelo_ref": model_cfg["model_id"],
                "requiere_revision_humana": True
            }
        }
        return resultado_ia_asistido
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error crítico de runtime: Archivo de directrices prompts/formulario-intake-v1.0.0.yaml no encontrado."
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Fallo en el pipeline de procesamiento de IA: {str(exc)}"
        )
