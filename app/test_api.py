from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

# Definimos el token de prueba alineado con dependencies.py
VALID_API_KEY = "ms_ia_secure_token_int_001_prov"

def test_endpoint_health():
    """Valida que el monitoreo de salud responda con éxito sin requerir credenciales."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.2.0"}

def test_intake_autenticado_valido():
    """Certifica que el pipeline procese la solicitud cuando se incluye la X-API-Key correcta."""
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
    assert json_data["meta"]["requiere_revision_humana"] is True

def test_intake_bloqueo_sin_api_key():
    """Verifica el bloqueo inmediato (HTTP 401) si la Escuela no envía credenciales."""
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
    """Verifica el rechazo estricto (HTTP 403) ante un token falso o malicioso."""
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
    """Valida que un cliente autenticado siga siendo bloqueado por el JSON Schema si envía campos extras."""
    payload_malicioso = {
        "solicitud_id": "req_attack_004",
        "texto_formulario": "Intento de elusión con token válido.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica",
        "admin": True
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_malicioso, headers=headers)
    assert response.status_code == 422
    
    # CORRECCIÓN DE AUDITORÍA: Accedemos al primer elemento [0] de la lista 'detail'
    assert response.json()["detail"][0]["type"] == "extra_forbidden"
