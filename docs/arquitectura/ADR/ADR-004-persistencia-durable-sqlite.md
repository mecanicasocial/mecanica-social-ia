# 📜 DECISIÓN ARQUITECTÓNICA (ADR-004): PERSISTENCIA DURABLE MEDIANTE SQLITE

## ESTADO DEL DOCUMENTO: PROPUESTO (Fase de Diseño Arquitectónico)

Este documento define la estrategia, modelado de esquemas relacionales y límites operacionales para incorporar almacenamiento persistente en el Runtime de Mecánica Social IA.

### 🔍 Contexto y Justificación Técnica
El procesamiento asíncrono actual gestionado por `BackgroundTasks` en `app/api.py` opera de forma no durable en memoria RAM. Ante apagados forzados, reinicios del contenedor o fallas críticas del sistema, las tareas encoladas y el registro histórico se pierden. Para transicionar hacia un estándar empresarial mitigando la fragilidad del MVP, se requiere una base de datos relacional local que no agregue complejidad de red en la fase actual de prototipo.

Se selecciona **SQLite** debido a que:
1. No requiere un servidor independiente (vive como un único archivo físico en el disco).
2. Es nativo en la librería estándar de Python (`import sqlite3`), manteniendo el contenedor ligero.
3. Soporta operaciones transaccionales ACID ideales para auditoría.

### 📊 Modelado Preliminar del Esquema de Datos (Tablas)

Para dar soporte estricto a las interfaces contractuales de los Contratos **INT-001** e **INT-002**, se diseñan dos tablas relacionales iniciales:

#### 1. Tabla `solicitudes_intake` (Seguimiento de INT-001)
* `solicitud_id`: TEXT (PRIMARY KEY) -> Identificador único correlativo.
* `programa_ref`: TEXT -> Código de referencia institucional.
* `texto_crudo`: TEXT -> Formulario original sanitizado (con PII protegida).
* `fecha_recepcion`: TEXT -> Estampa de tiempo legible (`YYYY-MM-DD HH:MM:SS`).
* `status_actual`: TEXT -> Restrictivo (`processing`, `completed`, `degraded`).

#### 2. Tabla `resultados_inferencia` (Sincronización de INT-002)
* `id`: INTEGER (PRIMARY KEY AUTOINCREMENT)
* `solicitud_id`: TEXT (FOREIGN KEY apuntando a `solicitudes_intake.solicitud_id`)
* `nombre_extraido`: TEXT -> Datos purificados por la IA.
* `email_extraido`: TEXT
* `telefono_extraido`: TEXT
* `interes_extraido`: TEXT
* `modelo_ref`: TEXT -> Referencia del LLM utilizado o `FALLBACK`.
* `tiempo_respuesta_ms`: INTEGER
* `fecha_notificacion`: TEXT -> Estampa de tiempo de despacho hacia la Escuela.

### 🐳 Persistencia Física en la Infraestructura
El archivo de la base de datos se almacenará de forma obligatoria en la ruta física **`data/mecanica_social_ia.db`**. Gracias a la configuración de volumes declarada en el archivo `docker-compose.yaml`, este archivo persistirá en el disco duro de la máquina anfitriona (Codespace) incluso si los contenedores son destruidos, recreados o actualizados en su totalidad, garantizando la durabilidad absoluta de los datos.
