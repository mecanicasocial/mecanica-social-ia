import pytest
import os
from app import database

@pytest.fixture(autouse=True)
def bd_temporal(tmp_path, monkeypatch):
    """FIXTURE GLOBAL REQUISITO AUDITORÍA: Garantiza el aislamiento absoluto de la BD en cada test."""
    # Redireccionamos la ruta a una base de datos temporal en memoria/disco aislado de Pytest
    ruta_temporal = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DB_PATH", ruta_temporal)
    
    # Forzamos la inicialización física del esquema limpio antes de correr el test
    database.inicializar_base_de_datos()
    yield
