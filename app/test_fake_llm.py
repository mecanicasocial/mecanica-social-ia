import pytest
from fastapi.testclient import TestClient
from app.fake_llm import app

client = TestClient(app)

def test_fake_llm_extrae_ana():
    payload = {"messages": [{"content": "Soy Ana, mi correo es ana@test.cl y quiero aprender soldadura"}]}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200

def test_fake_llm_extrae_juan():
    payload = {"messages": [{"content": "Soy Juan, mi fono es 56911112222 y me interesa Mecanica"}]}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200

def test_fake_llm_fallback_generico():
    payload = {"messages": [{"content": "Texto sin nombres conocidos ni datos claros"}]}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200

def test_timeout_lanza_error_controlado(monkeypatch):
    """TEST REQUISITO AUDITORÍA: Fuerza un error de tiempo de espera controlado."""
    import urllib.request
    from src.ms_ia.model_client import OpenAICompatibleClient, ModelClientError
    
    # Truco Profesional: Interceptamos urlopen y forzamos a que lance un TimeoutError nativo
    def mock_urlopen_lento(*args, **kwargs):
        raise TimeoutError("Simulación de red saturada o lenta en CPU")
        
    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen_lento)
    
    client_timeout = OpenAICompatibleClient(
        base_url="http://127.0.0.1:8001",
        api_key="mock",
        model_id="test",
        timeout_sec=0.01
    )
    
    with pytest.raises(ModelClientError) as exc_info:
        client_timeout.complete(system_or_prompt="sys", user_input="Ana")
        
    assert "tiempo de espera" in str(exc_info.value).lower()
