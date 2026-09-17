from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
import yaml
from app.dependencies import verificar_api_key_escuela

# 1. Inicialización de la Aplicación
app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio en runtime alineado estrictamente al Contrato INT-001 y protegido con API Key.",
    version="1.2.0"
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
    modelo_ref: Optional[str] = None
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
    return {"status": "healthy", "version": "1.2.0"}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    return {"status": "ready"}

# 5. Endpoint de Negocio Protegido (Inyección de verificar_api_key_escuela)
@app.post(
    "/v1/intake", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ExtraccionFormacionOutput,
    tags=["Integraciones"]
)
async def process_intake(
    payload: SolicitudFormacionInput,
    _token: str = Depends(verificar_api_key_escuela)  # Guardia de Seguridad Activo
):
    """
    Recibe el bloque de texto libre de Escuela (Sección 3).
    Requiere autenticación obligatoria X-API-Key en las cabeceras HTTP.
    """
    try:
        # Auditoría Operacional: Cargamos el Prompt seguro v1.0.0 congelado en el repositorio
        with open("prompts/formulario-intake-v1.0.0.yaml", "r", encoding="utf-8") as f:
            componente_prompt = yaml.safe_load(f)
            
        system_instructions = componente_prompt.get("prompt_text", "")
        
        # Pipeline de Procesamiento Sintético Asistido
        resultado_ia_asistido = {
            "nombre": "MOCK_EXTRAIDO_DESDE_IA",
            "email": "NO_PROPORCIONADO",
            "telefono": "NO_PROPORCIONADO",
            "interes": "Analizado usando versión 1.0.0 del prompt.",
            "meta": {
                "componente_id": "formulario-intake",
                "componente_version": "1.0.0",
                "modelo_ref": "openai-compatible-eval",
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
