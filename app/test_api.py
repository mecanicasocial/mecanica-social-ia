import os
os.environ["AMBIENTE"] = "development"
os.environ["API_KEY_ESCUELA_TOKEN"] = "ms_ia_secure_token_int_001_env_secured"
os.environ["MS_IA_MODEL_API_KEY"] = "mock_local_secret_key"
from fastapi.testclient import TestClient
import os
import shutil
from dotenv import load_dotenv
from app.api import app, disyuntor_ia, limitador_trafico

load_dotenv()
client = TestClient(app)
VALID_API_KEY = os.getenv("API_KEY_ESCUELA_TOKEN", "ms_ia_secure_token_int_001_env_secured")
import os

def setup_function():
    disyuntor_ia.state = "CLOSED"
    disyuntor_ia.failure_count = 0
    limitador_trafico.historial_consumos = {}
    if os.path.exists("data/records"):
        shutil.rmtree("data/records")

def test_endpoint_health():
    """Valida el monitoreo de salud reflejando la versión con Rate Limiting 2.2.0."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["version"] == "2.2.0"
    assert json_data["circuit_state"] == "CLOSED"
def test_intake_autenticado_valido_y_persistencia():
    payload_escuela = {
        "solicitud_id": "req_rate_001",
        "texto_formulario": "Postulación estándar para control de tráfico.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_escuela, headers=headers)
    assert response.status_code == 202

def test_intake_bloqueo_sin_api_key():
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
    assert response.json()["detail"][0]["type"] == "extra_forbidden"

def test_intake_bloqueo_cuando_circuito_abierto():
    disyuntor_ia.state = "OPEN"
    payload = {
        "solicitud_id": "req_resilience_005",
        "texto_formulario": "Formulario emitido durante corte de circuito.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload, headers=headers)
    assert response.status_code == 503
def test_intake_bloqueo_por_rate_limiting():
    """Fuerza una ráfaga abusiva de 6 peticiones manteniendo el contador del disyuntor en cero."""
    headers = {"X-API-Key": VALID_API_KEY}
    payload = {
        "solicitud_id": "req_burst_test",
        "texto_formulario": "Petición consecutiva de ráfaga.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    
    # 1. Ejecutar las primeras 5 peticiones permitidas por la ventana de tráfico
    for i in range(5):
        disyuntor_ia.failure_count = 0  # Reseteamos para que el error de red local no abra el circuito
        payload["solicitud_id"] = f"req_burst_{i}"
        response = client.post("/v1/intake", json=payload, headers=headers)
        assert response.status_code == 202

    # 2. La sexta petición excede la cuota de tráfico perimetral y gatilla el HTTP 429 de inmediato
    payload["solicitud_id"] = "req_burst_excedida"
    response_bloqueada = client.post("/v1/intake", json=payload, headers=headers)
    assert response_bloqueada.status_code == 429
    assert "Tasa de solicitudes excedida" in response_bloqueada.json()["detail"]
