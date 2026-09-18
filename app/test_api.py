from fastapi.testclient import TestClient
import os
import shutil
from dotenv import load_dotenv
from app.api import app, disyuntor_ia

load_dotenv()
client = TestClient(app)
VALID_API_KEY = os.getenv("API_KEY_ESCUELA_TOKEN", "fallback_empty_for_testing")

def setup_function():
    disyuntor_ia.state = "CLOSED"
    disyuntor_ia.failure_count = 0
    if os.path.exists("data/records"):
        shutil.rmtree("data/records")

def test_endpoint_health():
    """Valida el monitoreo de salud reflejando la versión de webhooks 2.1.0."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["version"] == "2.1.0"
    assert json_data["circuit_state"] == "CLOSED"
def test_intake_autenticado_valido_y_persistencia():
    """Certifica que el endpoint acepte la solicitud y el worker genere el archivo en disco."""
    payload_escuela = {
        "solicitud_id": "req_webhook_001",
        "texto_formulario": "Postulación asíncrona para validar persistencia y callbacks.",
        "programa_ref": "ref_ci_2026",
        "locale": "es-CL",
        "clasificacion_datos": "sintetica"
    }
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_escuela, headers=headers)
    
    assert response.status_code == 202
    json_data = response.json()
    assert json_data["status"] == "processing"
    
    ruta_esperada = "data/records/req_webhook_001.json"
    assert os.path.exists(ruta_esperada), "El archivo de persistencia no fue generado por el worker."
    
    with open(ruta_esperada, "r", encoding="utf-8") as f:
        registro_guardado = f.read()
    assert "formulario-intake" in registro_guardado
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
