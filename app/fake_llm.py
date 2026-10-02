import json
from fastapi import FastAPI, Request

app = FastAPI()

def mock_llm_inference(texto_motivacion: str) -> str:
    """
    Función pura de simulación determinista para el pipeline interno.
    Mantiene los nombres de campos originales y añade las 3 calificaciones fijas.
    """
    mock_output = {
        "nombre": "Juan Pérez Mock",
        "email": "juan.perez@example.com",
        "telefono": "+56912345678",
        "interes": "Políticas Públicas",
        "alineacion_mision": 3,
        "disponibilidad_tiempo": 4,
        "impacto_territorial": 2
    }
    return json.dumps(mock_output)

@app.post("/v1/chat/completions")
async def mock_chat_completions(request: Request):
    """
    Endpoint de simulación HTTP requerido por app/test_fake_llm.py.
    Retorna la estructura compatible con OpenAI inyectando los datos extendidos.
    """
    body = await request.json()
    messages = body.get("messages", [])
    texto_usuario = messages[-1].get("content", "") if messages else ""

    # Obtenemos el JSON estructurado de nuestra función pura
    contenido_estructurado = mock_llm_inference(texto_usuario)

    return {
        "id": "chatcmpl-mock-123",
        "model": "fake-llm-v1",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": contenido_estructurado
                },
                "finish_reason": "stop"
            }
        ]
    }
