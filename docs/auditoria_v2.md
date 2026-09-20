# 📜 INFORME DE AUDITORÍA TÉCNICA (VERSIÓN 2.0)

Este documento registra el diagnóstico exhaustivo de la base de código, la calidad de las pruebas y el nivel de enforcement real de los microservicios en el repositorio de Mecánica Social IA.

---

## 📊 Matriz de Diagnóstico y Brecha Técnica

A continuación, se detalla la brecha identificada entre el prototipo simulado actual y la meta técnica requerida para la operación segura con datos institucionales reales:

| Dimensión Evaluada | Puntuación Actual | Meta Experto / ONG | Diagnóstico de la Brecha |
| :--- | :---: | :---: | :--- |
| **Flujo funcional de punta a punta** | **1 / 5** | **4 / 5** | Ningún flujo asíncrono impacta la base de datos real. El pipeline de la IA está desconectado. |
| **Calidad de pruebas (Tests)** | **2 / 5** | **4 / 5** | Falsa seguridad. Pytest solo verifica la respuesta HTTP 202 rápida y no la persistencia final. |
| **Seguridad y secretos** | **2 / 5** | **4 / 5** | Tokens criptográficos hardcodeados expuestos en texto plano e indexados en el historial de Git. |
| **Proceso GitHub (Ramas y CI)** | **2 / 5** | **4 / 5** | La rama principal `main` carece de políticas de restricción de fusiones en estado degradado o roto. |
| **Documentación y gobernanza** | **4 / 5** | **3 / 5** | Excesiva y desproporcionada (~21.000 palabras) en comparación con las ~350 líneas de código físico. |
| **Preparación para datos reales** | **1 / 5** | **4 / 5** | Almacenamiento de texto crudo sin cifrar, sin consentimiento explícito ni políticas de retención legal. |

---

## 🔴 Hallazgos Críticos Bloqueantes

### C1. Exposición Transversal de Tokens
* **Diagnóstico:** El token de la Escuela (`ms_ia_secure_token_int_001_env_secured`) se encuentra expuesto en texto plano en `README.md`, `docker-compose.yaml` y `ci.yml`. Está indexado en el historial de Git.
* **Mitigación:** Rotar el token, extraerlo hacia un archivo privado `.env` (excluido en `.gitignore`), proveer un `.env.example` y configurar secretos en GitHub Actions.

### C2. Inoperatividad del Almacenamiento Relacional
* **Diagnóstico:** El archivo `database.py` se encuentra implementado pero la API principal en `api.py` solo lo importa. No existe persistencia real ni actualizaciones de estado atómicas al procesar solicitudes.

### C3. Desconexión de la Inteligencia Artificial
* **Diagnóstico:** El pipeline de inferencia apunta a un endpoint local inexistente (`localhost:8000/v1/mock`), lo que provoca que el ciclo de vida asíncrono aborte y caiga siempre de forma zombi en el fallback degradado.

### C4. Código Muerto en INT-002
* **Diagnóstico:** La función despachadora de notificaciones `disparar_notificacion_int002` nunca es invocada de forma física por el servidor web durante el procesamiento en segundo plano.

### C5. Ausencia de Endpoint de Inspección
* **Diagnóstico:** No existe un canal `GET /v1/intake/{id}` para verificar el estado de los datos estructurados guardados, obligando a inspeccionar SQLite de forma puramente manual.

### C6. Main sin Reglas de Protección
* **Diagnóstico:** No hay barreras perimetrales que impidan fusiones directas con los checks del CI en color rojo.

---

## 🗺️ Hoja de Ruta Priorizada (Fase 0 y Fase 1)

1. **Fase 0: Higiene y Rotación:** Implementar exclusión estricta de variables de entorno mediante `.env`, rotar tokens vulnerados y congelar la expansión documental.
2. **Fase 1: Conexión Real de Extremo a Extremo:** Configurar el Lifespan de FastAPI, acoplar Ollama mediante la red del Codespace, codificar los inserts relacionales durables, inyectar el endpoint `GET` de inspección y escribir el test de punta a punta contra la base de datos real.
