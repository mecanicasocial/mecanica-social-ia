import os
os.environ["MS_IA_CRYPTO_KEY"] = "P_t2bZU5Pw1s3Ez_W4Xw8mXNA4QpqCNPNqx4UgLlMRo="
os.environ["API_KEY_ESCUELA_TOKEN"] = "ms_ia_secure_token_int_001_env_secured"
import os
os.environ["MS_IA_CRYPTO_KEY"] = "3uHkeA9mF_kj5zUZH4bDsOfs0TUG-7asVhGsy_U2InI="
os.environ["API_KEY_ESCUELA_TOKEN"] = "ms_ia_secure_token_int_001_env_secured"
import os
os.environ["AMBIENTE"] = "development"
os.environ["API_KEY_ESCUELA_TOKEN"] = "token-solo-para-pruebas"
os.environ["MS_IA_MODEL_API_KEY"] = "clave-solo-para-pruebas"

import pytest
import os
import sqlite3
import socket
import threading
import time
import uvicorn
from app import database
from app import api

@pytest.fixture(scope="session")
def llm_falso():
    """FIXTURE SESIÓN: Levanta el servidor compatible con OpenAI en un puerto libre asignado por el OS."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        puerto = s.getsockname()[1]
        
    server = uvicorn.Server(uvicorn.Config("app.fake_llm:app", host="127.0.0.1", port=puerto, log_level="error"))
    hilo = threading.Thread(target=server.run, daemon=True)
    hilo.start()
    
    while not server.started:
        time.sleep(0.05)
        
    yield f"http://127.0.0.1:{puerto}/v1"
    server.should_exit = True
    hilo.join(timeout=5)

@pytest.fixture(autouse=True)
def estado_limpio(tmp_path, monkeypatch, llm_falso):
    """FIXTURE AUTOMÁTICA: Garantiza aislamiento de BD, redirige el cliente al puerto libre y resetea el ámbito global."""
    # 1. Aislamiento absoluto de Base de Datos
    ruta_temporal = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DB_PATH", ruta_temporal)
    database.inicializar_base_de_datos()
    
    # 2. Redirección dinámica del Backend hacia el servidor simulado de sesión
    monkeypatch.setenv("MS_IA_MODEL_BASE_URL", llm_falso)
    
    # 3. Limpieza imperativa de memoria interna contra contaminación cruzada
    api.disyuntor_ia.state = "CLOSED"
    api.disyuntor_ia.failure_count = 0
    api.limitador_trafico.historial_consumos = {}
    yield
