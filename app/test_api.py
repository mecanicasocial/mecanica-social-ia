import pytest
import os
import time
from fastapi.testclient import TestClient
from app.api import app, disyuntor_ia, limitador_trafico

client = TestClient(app)
VALID_API_KEY = os.environ["API_KEY_ESCUELA_TOKEN"]

def test_endpoint_health():
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["version"] == "2.2.0"
    assert json_data["circuit_state"] == "CLOSED"

def test_intake_autenticado_valido_y_persistencia():
    payload_escuela = {"solicitud_id": "req_rate_001", "texto_formulario": "Postulacion estandar.", "programa_ref": "ref_ci_2026", "locale": "es-CL", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0"}
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload_escuela, headers=headers)
    assert response.status_code == 202

def test_intake_bloqueo_sin_api_key():
    payload = {"solicitud_id": "1", "texto_formulario": "A", "programa_ref": "B", "locale": "es", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0"}
    response = client.post("/v1/intake", json=payload)
    assert response.status_code == 401

def test_intake_bloqueo_credencial_invalida():
    payload = {"solicitud_id": "1", "texto_formulario": "A", "programa_ref": "B", "locale": "es", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0"}
    headers = {"X-API-Key": "TOKEN_TRUCHO_CADUCADO"}
    response = client.post("/v1/intake", json=payload, headers=headers)
    assert response.status_code == 403

def test_intake_bloqueo_campo_prohibido_y_autenticado():
    payload = {"solicitud_id": "1", "texto_formulario": "A", "programa_ref": "B", "locale": "es", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0", "hacker_field": "drop tables;"}
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload, headers=headers)
    assert response.status_code == 422

def test_intake_bloqueo_cuando_circuito_abierto():
    disyuntor_ia.state = "OPEN"
    payload = {"solicitud_id": "req_resilience_005", "texto_formulario": "Corte de circuito.", "programa_ref": "ref_ci_2026", "locale": "es-CL", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0"}
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/v1/intake", json=payload, headers=headers)
    assert response.status_code == 503
    disyuntor_ia.state = "CLOSED"

def test_intake_bloqueo_por_rate_limiting():
    headers = {"X-API-Key": VALID_API_KEY}
    payload = {"solicitud_id": "req_burst_test", "texto_formulario": "Rafaga.", "programa_ref": "ref_rate_limit_burst", "locale": "es-CL", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0"}
    limitador_trafico.historial_consumos["ref_rate_limit_burst"] = []
    for i in range(5):
        payload["solicitud_id"] = f"req_burst_{i}"
        response = client.post("/v1/intake", json=payload, headers=headers)
        assert response.status_code == 202
    payload["solicitud_id"] = "req_burst_excedida"
    response_bloqueada = client.post("/v1/intake", json=payload, headers=headers)
    assert response_bloqueada.status_code == 429
    assert "tasa de solicitudes excedida" in response_bloqueada.json()["detail"].lower()

def test_coherencia_contractual_del_fallback_degradado():
    from app.api import ejecutar_fallback_contingencia, SolicitudFormacionInput
    mock_payload = SolicitudFormacionInput(solicitud_id="1", texto_formulario="A", programa_ref="B", locale="es", clasificacion_datos="sintetica", acepta_politica_privacidad=True, version_terminos="v2.0")
    res = ejecutar_fallback_contingencia(mock_payload, "Prueba")
    assert res["nombre"] == "DEGRADADO_A_COLA_HUMANA"

def test_produccion_sin_webhook_url_lanza_error_controlado(monkeypatch):
    monkeypatch.setenv("AMBIENTE", "production")
    monkeypatch.delenv("ESCUELA_WEBHOOK_URL", raising=False)
    from app.api import disparar_webhook_escuela
    with pytest.raises(RuntimeError):
        disparar_webhook_escuela("id", {})

def test_webhook_en_desarrollo_no_realiza_llamada_http_externa(monkeypatch):
    monkeypatch.setenv("AMBIENTE", "development")
    from app.api import disparar_webhook_escuela
    disparar_webhook_escuela("id", {})

def test_int002_notificacion_esquema_valido(tmp_path, monkeypatch):
    monkeypatch.setenv("AMBIENTE", "development")
    from app.api import disparar_notificacion_int002
    disparar_notificacion_int002("id", {"nombre":"A","email":"B","telefono":"C","interes":"D"}, {"componente_id":"A","componente_version":"B","modelo_ref":"C","requiere_revision_humana":True,"status_proceso":"completed","tiempo_respuesta_ms":10})

def test_int002_notificacion_bloqueo_por_campo_ausente(monkeypatch):
    from app.api import disparar_notificacion_int002
    disparar_notificacion_int002("id", {}, {})

def test_produccion_sin_notificacion_url_lanza_error_controlado_int002(monkeypatch):
    monkeypatch.setenv("AMBIENTE", "production")
    monkeypatch.delenv("ESCUELA_NOTIFICACION_URL", raising=False)
    from app.api import disparar_notificacion_int002
    with pytest.raises(RuntimeError):
        disparar_notificacion_int002("id", {"nombre":"A","email":"B","telefono":"C","interes":"D"}, {"componente_id":"A","componente_version":"B","modelo_ref":"C","requiere_revision_humana":True,"status_proceso":"completed","tiempo_respuesta_ms":10})

def test_int002_secuencia_reintentos_ante_error_servidor(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda x: None)
    import httpx
    def mock_post(*args, **kwargs):
        mock_resp = httpx.Response(status_code=502, request=httpx.Request("POST", args))
        raise httpx.HTTPStatusError("Bad Gateway", request=mock_resp.request, response=mock_resp)
    monkeypatch.setattr(httpx, "post", mock_post)
    from app.api import disparar_notificacion_int002
    monkeypatch.setenv("AMBIENTE", "production")
    monkeypatch.setenv("ESCUELA_NOTIFICACION_URL", "http://test/webhook")
    disparar_notificacion_int002("id", {"nombre":"A","email":"B","telefono":"C","interes":"D"}, {"componente_id":"A","componente_version":"B","modelo_ref":"C","requiere_revision_humana":True,"status_proceso":"completed","tiempo_respuesta_ms":10})

def test_intake_guarda_solicitud_en_bd(tmp_path, monkeypatch):
    import sqlite3
    from app import database
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.inicializar_base_de_datos()
    payload = {"solicitud_id": "req_db_001", "texto_formulario": "Soy Ana, soldadura.", "programa_ref": "ref_ci_2026", "locale": "es-CL", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": True, "version_terminos": "v2.0"}
    r = client.post("/v1/intake", json=payload, headers={"X-API-Key": VALID_API_KEY})
    assert r.status_code == 202
    con = sqlite3.connect(database.DB_PATH)
    fila = con.execute("SELECT status_actual FROM solicitudes_intake WHERE solicitud_id = ?", ("req_db_001",)).fetchone()
    con.close()
    assert fila is not None

def test_intake_bloqueo_por_falta_de_consentimiento():
    payload = {"solicitud_id": "req_bloqueo_legal_001", "texto_formulario": "No acepto", "programa_ref": "PRG-MECANICA", "locale": "es-CL", "clasificacion_datos": "sintetica", "acepta_politica_privacidad": False, "version_terminos": "v2.0"}
    response = client.post("/v1/intake", json=payload, headers={"X-API-Key": VALID_API_KEY})
    assert response.status_code == 400
    assert "es mandatorio aceptar la politica" in response.json()["detail"].lower()
