import time
import re
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Fake LLM Server - OpenAI Compatible")

@app.post("/v1/chat/completions")
async def chat_completions(payload: dict):
    # Simulación de costo de cómputo real solicitado por auditoría
    time.sleep(1.0)
    
    messages = payload.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Missing messages content")
        
    prompt_text = messages[-1].get("content", "")
    
    # 🕵️ REGLAS DETERMINISTAS INTELIGENTES BASADAS EN EXPRESIONES REGULARES
    if re.search(r"Ana", prompt_text, re.IGNORECASE):
        resultado = {
            "nombre": "Ana",
            "email": "ana@test.cl",
            "telefono": "+56911111111",
            "interes": "Soldadura"
        }
    elif re.search(r"Juan", prompt_text, re.IGNORECASE):
        resultado = {
            "nombre": "Juan Herrera",
            "email": "juan.herrera@email.cl",
            "telefono": "56911112222",
            "interes": "Mecanica Social Aplicada con IA"
        }
    else:
        resultado = {
            "nombre": "DEGRADADO_A_COLA_HUMANA",
            "email": "NO_PROPORCIONADO",
            "telefono": "NO_PROPORCIONADO",
            "interes": "PROCESAMIENTO_GENERICO: Requiere clasificacion manual"
        }
        
    return {
        "choices": [{
            "message": {
                "content": json_response(resultado)
            }
        }],
        "model": "fake-llm-advanced-7b"
    }

def json_response(data: dict) -> str:
    import json
    return json.dumps(data)
