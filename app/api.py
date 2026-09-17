from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Literal

# 1. Inicialización de la Aplicación
app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio en runtime alineado estrictamente al Contrato INT-001.",
    version="1.1.0"
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

    class Config:
        extra = "forbid"  # Bloquea inyecciones de datos no documentados en la entrada

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
    return {"status": "healthy", "version": "1.1.0"}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    return {"status": "ready"}

# 5. Endpoint de Negocio Corregido y Alineado
@app.post(
    "/v1/intake", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ExtraccionFormacionOutput,
    tags=["Integraciones"]
)
async def process_intake(payload: SolicitudFormacionInput):
    """
    Recibe el bloque de texto libre y metadatos de Escuela (Sección 3).
    Devuelve la estructura JSON procesada esperada por el contrato (Sección 4).
    """
    try:
        # Simulación del comportamiento del componente IA (Mock trazable según Section 4)
        # En la siguiente fase aquí se llamará al cliente del modelo con payload.texto_formulario
        resultado_asistido = {
            "nombre": "MOCK_EXTRAIDO_DESDE_IA",
            "email": "NO_PROPORCIONADO",
            "telefono": "NO_PROPORCIONADO",
            "interes": f"Analizado a partir de: {payload.texto_formulario[:30]}...",
            "meta": {
                "componente_id": "formulario-intake",
                "componente_version": "1.0.0",
                "modelo_ref": "openai-compatible-eval",
                "requiere_revision_humana": True
            }
        }
        return resultado_asistido
        
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Fallo en el pipeline de procesamiento de IA: {str(exc)}"
        )
