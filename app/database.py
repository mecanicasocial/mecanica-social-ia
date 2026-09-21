import sqlite3
import os

DB_PATH = os.getenv("MS_IA_DB_PATH", "data/mecanica_social_ia.db")

def inicializar_base_de_datos():
    """Inicializa el esquema relacional de la base de datos de forma atómica y durable."""
    directorio = os.path.dirname(DB_PATH)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)
        
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Tabla Madre: Solicitudes de Ingreso
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_intake (
                solicitud_id TEXT PRIMARY KEY,
                programa_ref TEXT NOT NULL,
                texto_crudo TEXT NOT NULL,
                fecha_recepcion TEXT NOT NULL,
                status_actual TEXT NOT NULL
            );
        """)
        
        # 🛡️ TABLA REQUISITO AUDITORÍA (C6/A2): Gobernanza y Traza Legal de Consentimiento PII
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trazas_consentimiento (
                solicitud_id TEXT PRIMARY KEY,
                acepta_politica_privacidad INTEGER NOT NULL,
                version_terminos TEXT NOT NULL,
                fecha_registro TEXT NOT NULL,
                FOREIGN KEY (solicitud_id) REFERENCES solicitudes_intake (solicitud_id) ON DELETE CASCADE
            );
        """)
        
        # 2. Tabla Hija: Resultados de Inferencia de la IA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados_inferencia (
                solicitud_id TEXT PRIMARY KEY,
                nombre_extraido TEXT,
                email_extraido TEXT,
                telefono_extraido TEXT,
                interes_extraido TEXT,
                modelo_ref TEXT NOT NULL,
                tiempo_respuesta_ms INTEGER,
                fecha_notificacion TEXT NOT NULL,
                FOREIGN KEY (solicitud_id) REFERENCES solicitudes_intake (solicitud_id) ON DELETE CASCADE
            );
        """)
        conn.commit()
