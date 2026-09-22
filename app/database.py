import os
import sqlite3
import logging

logger = logging.getLogger("RUNTIME_IA")

DB_PATH = "data/mecanica_social_ia.db"

def inicializar_base_de_datos():
    """Crea el archivo físico de SQLite y las tablas relacionales contractuales."""
    # Aseguramos que la carpeta data/ exista físicamente en el contenedor
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    try:
        # Habilitamos el soporte mandatorio para claves foráneas en SQLite
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Creamos la tabla de seguimiento para el Contrato INT-001
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_intake (
                solicitud_id TEXT PRIMARY KEY,
                programa_ref TEXT NOT NULL,
                texto_crudo TEXT NOT NULL,
                fecha_recepcion TEXT NOT NULL,
                status_actual TEXT NOT NULL
            );
        """)
        
        # 2. Creamos la tabla de sincronización para el Contrato INT-002
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados_inferencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre_extraido TEXT NOT NULL,
                email_extraido TEXT NOT NULL,
                telefono_extraido TEXT NOT NULL,
                interes_extraido TEXT NOT NULL,
                modelo_ref TEXT NOT NULL,
                tiempo_respuesta_ms INTEGER,
                fecha_notificacion TEXT NOT NULL,
                solicitud_id TEXT NOT NULL UNIQUE,
            FOREIGN KEY (solicitud_id) REFERENCES solicitudes_intake (solicitud_id) ON DELETE CASCADE
            );
        """)
        
        conexion.commit()
        logger.info(f"🟢 [DATABASE] Base de datos relacional inicializada con exito en {DB_PATH}")
        
    except Exception as err:
        conexion.rollback()
        logger.error(f"🔴 [DATABASE] Error critico al construir los esquemas de persistencia: {str(err)}")
        raise err
    finally:
        conexion.close()

if __name__ == "__main__":
    # Permite probar la inicialización de forma directa desde la terminal
    logging.basicConfig(level=logging.INFO)
    inicializar_base_de_datos()
