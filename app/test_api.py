from fastapi.testclient import TestClient
from app.api import app

# Inicializamos el cliente robótico de pruebas sobre la aplicación real
client = TestClient(app)

def test_endpoint_health():
    """Valida de forma automática que el monitoreo de salud responda con éxito."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.1.0"}

def test_intake_contrato_valido():
    """Certifica que el pipeline procese correctamente una entrada alineada a la Sección 3."""
    payload_escuela = {
        "solicitud_id": "req_ci_test_001",
        "texto_formulario": "Postulación sintética de prueba para el runtime de IA.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    response = client.post("/v1/intake", json=payload_escuela)
    
    # Exigimos la confirmación del código de éxito 201 Created
    assert response.status_code == 201
    
    # Auditamos que la salida contenga la estructura mandatoria de la Sección 4
    json_data = response.json()
    assert "nombre" in json_data
    assert "email" in json_data
    
    # Validación corregida para la estructura real
    assert json_data["meta"]["requiere_revision_humana"] is True

def test_intake_bloqueo_campo_prohibido():
    """Valida mecánicamente que el escudo Pydantic detenga solicitudes mutadas con campos extras."""
    payload_malicioso = {
        "solicitud_id": "req_attack_002",
        "texto_formulario": "Intento de elusión de directrices corporativas.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica",
        "admin": True  # Campo prohibido por el contrato
    }
    response = client.post("/v1/intake", json=payload_malicioso)
    
    # El sistema debe arrojar forzosamente un código 422 Unprocessable Content
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "extra_forbidden"
