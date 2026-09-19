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

### ⚠️ ADVERTENCIA DE INFRAESTRUCTURA: PROCESAMIENTO ASÍNCRONO NO DURABLE
De acuerdo con las restricciones validadas en la auditoría arquitectónica, se deja constancia explícita de lo siguiente:
1. El Runtime utiliza `BackgroundTasks` en memoria volátil local para procesar las solicitudes en segundo plano.
2. NO existe una cola de mensajería persistente o durable (como Redis, RabbitMQ, Celery, SQS o Kafka) implementada en esta fase.
3. Si el proceso del servidor experimenta un reinicio forzado, falla crítica o caída del sistema inmediatamente después de responder el código `HTTP 202`, la tarea encolada se perderá de forma permanente.
4. Este mecanismo es un control local válido única y estrictamente para la fase de MVP o prototipo de evaluación. Queda prohibido su uso en producción a gran escala sin antes acordar bilateralmente el despliegue de una cola persistente de grado industrial.

### ⚠️ ADVERTENCIA DE RESILIENCIA: CIRCUIT BREAKER LOCAL POR INSTANCIA
De acuerdo con los criterios de validación de la arquitectura de resiliencia, se hace explícito que:
1. La máquina de estados del `IA_CircuitBreaker` opera bajo un aislamiento estricto en la memoria RAM del proceso local.
2. Este disyuntor perimetral constituye un mecanismo local por instancia; NO es un sistema de control distribuido ni comparte su estado a través de la red.
3. En escenarios de escalamiento distribuido con múltiples réplicas o instancias activas en paralelo (ej. API-1 y API-2), cada contenedor evaluará de forma independiente sus umbrales de fallo sin sincronizar los cambios de estado (CLOSED/OPEN) de forma centralizada.
4. Se clasifica formalmente como una implementación correcta y suficiente para la fase de MVP local, requiriendo el uso de tecnologías de almacenamiento compartido (como Redis) en caso de una migración futura hacia una topología de producción distribuida masiva.

### ⚠️ ADVERTENCIA DE SEGURIDAD: RATE LIMITING LOCAL POR INSTANCIA
De acuerdo con los criterios de validación de la arquitectura de control de tráfico, se hace explícito que:
1. El componente `PerimetralRateLimiter` opera bajo un aislamiento estricto almacenando los consumos en un diccionario en memoria volátil (`historial_consumos`).
2. Este limitador perimetral constituye un mecanismo local por instancia; los contadores acumulados se perderán de forma permanente ante cualquier reinicio del proceso del servidor web FastAPI.
3. En escenarios de escalamiento distribuido con múltiples réplicas (ej. Instancia A e Instancia B), cada contenedor computará de forma independiente sus propias cuotas de tráfico (5 solicitudes por minuto) sin sincronizar los consumos de los clientes autenticados a través de la red.
4. Se clasifica formalmente como una implementación correcta y recomendada para la fase de MVP local, posponiendo la introducción de bases de datos en memoria (como Redis) hasta que se autorice formalmente una transición hacia una topología de producción distribuida masiva.
1. **Seguridad del Webhook Saliente:** Se declara formalmente que la comunicación técnica saliente actual IA -> Escuela transmite únicamente la cabecera `X-Event-Type`. Carece de API Keys de aplicación, firmas criptográficas HMAC, OAuth o certificados mutuos mTLS. Su uso operativo en producción queda estrictamente inhabilitado hasta que Mecánica Social Escuela defina y apruebe bilateralmente el protocolo de autenticación saliente correspondiente.

### 📊 6. Semántica de Validación Cruzada de Esquemas
Para garantizar la integridad total de la información en todo su ciclo de vida, el Runtime subdivide el Contrato INT-001 en dos flujos semánticos de validación independientes:
1. **Fase de Aceptación HTTP (Emisión Inmediata):** Validada estrictamente contra `int-001-intake-response.schema.json`. Regula el payload de respuesta de confirmación asíncrona entregado al cliente en milisegundos ante un código `HTTP 202 Accepted`.
2. **Fase de Extracción Operacional (Procesamiento IA):** Validada estrictamente contra `int-001-output.schema.json`. Regula la estructura definitiva generada por el LLM en segundo plano (`nombre`, `email`, `telefono`, `interes`, `meta`) que se transmite de forma asíncrona mediante el webhook callback.

#### 🔄 Diagrama de Flujo del Ciclo de Vida Contractual:
Escuela Request -> [POST /v1/intake] -> Valida Entrada Pydantic
                      │
                      ├──> [Aceptación HTTP] -> int-001-intake-response.schema.json -> HTTP 202 Accepted
                      │
                      └──> [BackgroundTask] -> Inferencia de IA -> int-001-output.schema.json -> Webhook
