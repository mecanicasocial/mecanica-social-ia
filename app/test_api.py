from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
from app.api import app

# Cargamos el archivo .env de forma explícita para la suite de pruebas automatizadas
load_dotenv()

client = TestClient(app)

# Extraemos la credencial real declarada en el entorno seguro del disco local
VALID_API_KEY = os.getenv("API_KEY_ESCUELA_TOKEN", "fallback_empty_for_testing")

def test_endpoint_health():
    """Valida que el monitoreo de salud responda con éxito reflejando la versión 1.5.0."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.5.0"}

def test_intake_autenticado_valido():
    """Certifica que el pipeline procese solicitudes cuando el cliente usa la API Key de entorno legítima."""
    payload_escuela = {
        "solicitud_id": "req_ci_test_001",
        "texto_formulario": "Postulación sintética de prueba para el runtime de IA.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_escuela, headers=headers)
    
    assert response.status_code == 201
    json_data = response.json()
    assert "nombre" in json_data
    assert json_data["meta"]["modelo_ref"] == "openai-compatible-eval"

def test_intake_bloqueo_sin_api_key():
    """Verifica el bloqueo inmediato (HTTP 401) si la Escuela omite las credenciales en el request."""
    payload = {
        "solicitud_id": "req_anon_002",
        "texto_formulario": "Petición anónima.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    response = client.post("/v1/intake", json=payload)
    assert response.status_code == 401
    assert "Falta el encabezado de autenticación obligatorio" in response.json()["detail"]

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
    assert "Credencial inválida o no autorizada" in response.json()["detail"]

def test_intake_bloqueo_campo_prohibido_y_autenticado():
    """Valida que un cliente con token válido de entorno siga siendo bloqueado por el JSON Schema si envía extras."""
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
    
    # CORRECCIÓN: Accedemos de forma precisa a la posición cero de la lista de errores detail
    assert response.json()["detail"][0]["type"] == "extra_forbidden"
