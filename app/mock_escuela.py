import os
import json
import logging
from fastapi import FastAPI, Request, Response
import jsonschema

# Configuración básica de logs vistosos para la terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MOCK_ESCUELA")

app = FastAPI(title="Mock Receptor Mecánica Social Escuela")

@app.get("/health")
def health_check():
    return {"status": "ok", "componente": "mock-escuela-receptor"}

@app.post("/webhooks/escuela-intake")
async def receiver_intake_mock(request: Request):
    """Simula la confirmación de recepción del lead original (INT-001)"""
    payload = await request.json()
    logger.info(f"📥 [INT-001] Escuela recibio confirmacion asincrona: {json.dumps(payload)}")
    return Response(status_code=202)

@app.post("/webhooks/escuela-output")
async def receiver_output_notificacion(request: Request):
    """Simula el endpoint oficial de la Escuela que recibe los resultados de la IA (INT-002)"""
    payload = await request.json()
    logger.info("======================================================================")
    logger.info("📥 [INT-002] ¡NOTIFICACIÓN RECIBIDA EN LOS SERVIDORES DE LA ESCUELA!")
    logger.info("======================================================================")
    logger.info(f"Datos del Payload: {json.dumps(payload, indent=2)}")
    
    # Aduana de validación rígida del lado de la Escuela
    try:
        with open("data/schemas/int-002-output.schema.json", "r", encoding="utf-8") as f:
            schema_int002 = json.load(f)
        jsonschema.validate(instance=payload, schema=schema_int002)
        logger.info("🟢 [INT-002-VALIDADOR_ESCUELA] ÉXITO: El paquete cumple al 100% con el contrato.")
        return {"status": "success", "message": "Resultados indexados en base de datos escolar"}
    except jsonschema.exceptions.ValidationError as err:
        logger.error(f"🔴 [INT-002-VALIDADOR_ESCUELA] ERROR: Formato corrupto o invalido. {err.message}")
        return Response(content=json.dumps({"error": err.message}), status_code=400, media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
