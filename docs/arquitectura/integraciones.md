# 🗺️ ÍNDICE MAESTRO DE INTEGRACIONES INSTITUCIONALES

Este documento registra el mapa oficial, el estado de madurez de la gobernanza y el nivel de enforcement técnico de las interfaces de datos bilaterales entre Mecánica Social IA y Mecánica Social Escuela.

---

## 📊 Ecosistema Contractual Vigente (Fase MVP Local)

El repositorio divide sus capacidades operacionales en dos contratos complementarios de datos, validados de forma matemática rígida mediante robots de prueba locales:

### 1. CONTRATO INT-001: Admisión e Intake Asíncrono
* **Tipo:** Interfaz de Entrada (Ingreso de solicitudes desde la Escuela hacia la IA).
* **Estado de Gobernanza:** `Provisional` — Contrato técnico y especificaciones descriptivas de 3671 bytes consolidadas.
* **Enforcement Técnico:** `Operativo Experimental` — Servidor FastAPI asíncrono implementado en el código, protegido localmente por `PerimetralRateLimiter` y `IA_CircuitBreaker` en memoria RAM. Cuenta con bloqueo duro e intolerante a fallas en entornos de producción ante la ausencia de `ESCUELA_WEBHOOK_URL`.

### 2. CONTRATO INT-002: Notificación de Resultados Estructurados
* **Tipo:** Interfaz de Salida (Devolución de perfiles purificados desde la IA hacia la Escuela).
* **Estado de Gobernanza:** `Propuesto` — Fase de especificación de arquitectura y diseño inicial; pendiente de ratificación institucional bilateral de endpoints, políticas de reintentos y llaves de cifrado criptográfico (HMAC/mTLS).
* **Enforcement Técnico:** `Código Físico Implementado` — La función despachadora `disparar_notificacion_int002` se encuentra acoplada físicamente al Runtime en `app/api.py`. Realiza una validación preventiva simétrica contra el JSON Schema `int-002-output.schema.json` y se encuentra integrada a la suite de pruebas automáticas.

---

## 🔄 Matriz de Trazabilidad de Contratos y Validadores

El ciclo de vida de los datos se encuentra blindado de extremo a extremo mediante el siguiente mapa físico de control cruzado:

| Código Contrato | Documento de Especificación | Esquema de Validación JSON (Aduana) | Payload Sintético de Simulación |
| :--- | :--- | :--- | :--- |
| **INT-001** | `docs/arquitectura/contratos/INT-001-escuela.md` | `data/schemas/int-001-intake-response.schema.json`<br>`data/schemas/int-001-output.schema.json` | `data/samples/int-001-solicitud-formacion.sample.json` |
| **INT-002** | `docs/arquitectura/contratos/INT-002-escuela-output.md` | `data/schemas/int-002-output.schema.json` | `data/samples/int-002-notificacion.sample.json` |

---

## 🏁 Certificación de Calidad y Robustez Operacional

* **Suite de Pruebas Unitarias:** Respaldada de forma reproducible por **12 pruebas automatizadas en verde (`100% passed`)** libres de advertencias, las cuales validan flujos exitosos, contingencias degradadas de fallback con `status_proceso: "degraded"`, barreras de red en desarrollo y simulaciones de error controlado.
* **Entorno de Microservicios:** Orquestado de forma local e independiente de internet mediante `docker-compose.yaml` bajo una red privada bridge aislada (`red-mecanica-social-ia`).
