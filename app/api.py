from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 1. Inicialización de la Aplicación con metadatos de Gobernanza
app = FastAPI(
    title="Mecánica Social IA - API REST",
    description="Servicio en runtime para el procesamiento y clasificación de formularios (Contrato INT-001).",
    version="1.0.0"
)

# 2. Esquema de Entrada Estricto basado en el Contrato INT-001 (Pydantic actúa como JSON Schema)
class SolicitudFormacionInput(BaseModel):
    nombre: str = Field(..., description="Nombre completo del postulante de origen.")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico de contacto validado.")
    telefono: Optional[str] = Field(None, description="Teléfono en formato string (multiformato).")
    interes: str = Field(..., description="Glosa o texto libre con el interés expresado por el curso.")

    class Config:
        # Bloquea la inserción de llaves desconocidas o inyecciones de datos en la entrada
        extra = "forbid"

# 3. Endpoints Operacionales Base
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def health_check():
    """Verifica que el servicio esté vivo internamente."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/ready", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
async def ready_check():
    """Verifica que el runtime esté listo para aceptar conexiones (Base del Circuit Breaker)."""
    # En fases posteriores, aquí se verificará la conexión activa con el proveedor de IA (INT-002)
    return {"status": "ready"}

# 4. Endpoint de Negocio Principal (Contrato INT-001)
@app.post("/v1/intake", status_code=status.HTTP_201_CREATED, tags=["Integraciones"])
async def process_intake(payload: SolicitudFormacionInput):
    """
    Recibe la solicitud de formación provisional remitida por Escuela.
    Ejecuta validación estricta de esquemas antes del procesamiento del modelo.
    """
    try:
        # El validador de Pydantic ya filtró los datos en el argumento 'payload'
        # Por ahora, simulamos una respuesta exitosa mockeada según el diseño operativo provisional
        resultado_procesado = {
            "caso_id": "api_mock_trazable",
            "datos_extraidos": payload.dict(),
            "estado_interno": "SPECIFIED",
            "requiere_revision_humana": True  # Exigencia explícita de gobernanza del contrato
        }
        return resultado_procesado
        
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error en la consistencia de datos del contrato: {str(exc)}"
        )
