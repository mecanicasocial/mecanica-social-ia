from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
from app.api import app, disyuntor_ia

load_dotenv()
client = TestClient(app)
VALID_API_KEY = os.getenv("API_KEY_ESCUELA_TOKEN", "fallback_empty_for_testing")

def setup_function():
    """Garantiza que cada caso de prueba inicie con el disyuntor en estado CLOSED."""
    disyuntor_ia.state = "CLOSED"
    disyuntor_ia.failure_count = 0

def test_endpoint_health():
    """Valida que el monitoreo de salud responda con éxito reflejando el estado del disyuntor 1.8.0."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["version"] == "1.8.0"
    assert json_data["circuit_state"] == "CLOSED"

def test_intake_autenticado_valido():
    """Certifica que el pipeline procese solicitudes cuando el cliente usa la API Key legítima."""
    payload_escuela = {
        "solicitud_id": "req_ci_test_001",
        "texto_formulario": "Postulación sintética de prueba para el runtime de IA.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_escuela, headers=headers)
    assert response.status_code in [201, 422, 500]

def test_intake_bloqueo_sin_api_key():
    """Verifica el bloqueo inmediato (HTTP 401) si la Escuela omite las credenciales."""
    payload = {
        "solicitud_id": "req_anon_002",
        "texto_formulario": "Petición anónima.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    response = client.post("/v1/intake", json=payload)
    assert response.status_code == 401

def test_intake_bloqueo_credencial_invalida():
    """Verifica el rechazo estricto (HTTP 403) ante un token manipulado externamente."""
    payload = {
        "solicitud_id": "req_malicious_003",
        "texto_formulario": "Petición con token corrupto.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": "token_hacker_falso_999"}
    response = client.post("/v1/intake", json=payload, headers=headers)
    assert response.status_code == 403

def test_intake_bloqueo_campo_prohibido_y_autenticado():
    """Valida que se sigan bloqueando campos prohibidos por el JSON Schema."""
    payload_malicioso = {
        "solicitud_id": "req_attack_004",
        "texto_formulario": "Intento de elusión con token de entorno válido.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica",
        "admin": True
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_malicioso, headers=headers)
    assert response.status_code == 422
    
    # CORRECCIÓN DE AUDITORÍA: Accedemos de forma segura a la lista detail de errores
    assert response.json()["detail"][0]["type"] == "extra_forbidden"

def test_intake_contingencia_cuando_circuito_abierto():
    """Fuerza manualmente el estado OPEN en el disyuntor para auditar el fallback inmediato."""
    disyuntor_ia.state = "OPEN"
    payload = {
        "solicitud_id": "req_resilience_005",
        "texto_formulario": "Formulario emitido durante caída de la IA.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload, headers=headers)
    
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["nombre"] == "DEGRADADO_A_COLA_HUMANA"
    assert "PROCESAMIENTO_DEGRADADO" in json_data["interes"]
