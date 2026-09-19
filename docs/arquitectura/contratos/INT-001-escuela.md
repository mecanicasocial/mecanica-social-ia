# 📜 CONTRATO DE INTEGRACIÓN BILATERAL: INT-001
## ESTADO DEL DOCUMENTO: PROVISIONAL (Fase MVP / Prototipo Experimental)

Este documento establece los acuerdos y especificaciones técnicas para la ingesta y extracción automatizada de formularios institucionales entre Mecánica Social Escuela y Mecánica Social IA.
### 📂 Metadatos de la Integración
* **Propósito:** Automatizar la extracción estructurada de datos de formularios libres usando IA.
* **Sistema Origen:** Mecánica Social Escuela (Emisor de solicitudes).
* **Sistema Destino:** Runtime de Mecánica Social IA (Procesador asíncrono).
* **Versión Contractual:** 2.2.0 (Fase MVP Local).
* **Clasificación de Datos:** Datos de Formación (Sintética, Pública o Autorizada).

### 📥 1. Perímetro Técnico de Entrada
La API valida estrictamente que la entrada JSON () contenga los siguientes campos obligatorios:
* `solicitud_id`: Cadena de texto (ID opaco generado por Escuela; libre de PII).
* `texto_formulario`: Cadena de texto libre con el contenido de la postulación.
* `programa_ref`: Cadena de texto de referencia del programa institucional.
* `locale`: Configuración regional obligatoria (ej. `es-CL`).
* `clasificacion_datos`: Tipo restrictivo (`sintetica`, `publica`, `autorizada`).
*Control Estructural:* Pydantic bloquea parámetros adicionales mediante `extra="forbid"`.

### 📤 2. Comportamiento Asíncrono y Respuesta HTTP
El Runtime opera en memoria de forma desacoplada para el MVP. Ante una petición legítima, la API responde un código `HTTP 202 Accepted` validado contra el esquema `int-001-intake-response.schema.json` con este payload:
```json
{
  "solicitud_id": "string",
  "status": "processing",
  "meta": {
    "componente_id": "formulario-intake",
    "componente_version": "1.0.0",
    "modelo_ref": "openai-compatible-eval",
    "requiere_revision_humana": true,
    "status_proceso": "accepted"
  }
}
```

### 📊 3. Perímetro Técnico de Extracción Final
Una vez concluida la inferencia en segundo plano por el modelo experimental, la salida estructurada se valida contra `int-001-output.schema.json` exigiendo estrictamente:
* `nombre`: Cadena de texto con el nombre extraído.
* `email`: Cadena de texto con el correo electrónico.
* `telefono`: Cadena de texto con el teléfono analizado.
* `interes`: Resumen textual del interés detectado en la postulación.

### 🔑 4. Autenticación, Seguridad y Errores
* **Autenticación Perimetral:** Uso obligatorio de la cabecera `X-API-Key` mapeada desde la variable de entorno `API_KEY_ESCUELA_TOKEN`.
* **Manejo de Errores Contractuales:**
  * `HTTP 401 Unauthorized`: Petición emitida sin cabecera de credenciales.
  * `HTTP 403 Forbidden`: Token inválido o corrupto.
  * `HTTP 422 Unprocessable Entity`: Datos inválidos o presencia de campos extras prohibidos.
  * `HTTP 429 Too Many Requests`: Límite de tráfico local excedido (Máximo 5 peticiones por minuto).
  * `HTTP 503 Service Unavailable`: Circuit Breaker local abierto ante caídas consecutivas de infraestructura.

### ⚠️ 5. Elementos que Requieren Confirmación de Escuela
Este acuerdo es estrictamente provisional. El Runtime no iniciará operaciones reales hasta que la Escuela ratifique de forma bilateral:
1. La autorización institucional y asignación de API Keys de producción.
2. El despliegue de colas de mensajería durables (ej. Redis/RabbitMQ) para evitar pérdidas de datos en caídas.
3. El endpoint oficial para recibir el Webhook callback e implementar firmas digitales HMAC o mTLS en la comunicación saliente.
4. La política de persistencia operacional: definir tiempos de retención y purga de PII extraída.
