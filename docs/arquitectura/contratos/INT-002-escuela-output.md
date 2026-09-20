# 📜 CONTRATO DE INTEGRACIÓN BILATERAL: INT-002
## ESTADO DEL DOCUMENTO: PROPUESTO (Fase de Diseño Arquitectónico)

Este documento establece los acuerdos preliminares y las especificaciones técnicas para la devolución automatizada de resultados de inferencia estructurada desde Mecánica Social IA hacia Mecánica Social Escuela.

### 📂 Metadatos de la Integración
* **Propósito:** Sincronizar los perfiles de alumnos extraídos y validados por la IA en el sistema de gestión escolar.
* **Sistema Origen:** Runtime de Mecánica Social IA (Emisor de eventos procesados).
* **Sistema Destino:** Mecánica Social Escuela (Receptor de resultados finales).
* **Versión Contractual:** 1.0.0 (Fase de Diseño).
* **Clasificación de Datos:** Datos de Formación (Sintética, Pública o Autorizada).

### 📥 1. Perímetro Técnico de Entrada (Payload del Evento)
El contrato define de forma estricta que la Escuela recibirá una petición HTTP POST en su endpoint callback con un JSON que contiene:
* `solicitud_id`: Cadena de texto (ID único correlativo que amarra con INT-001).
* `resultado`: Objeto estructurado que contiene los campos extraídos:
  * `nombre`: Cadena de texto.
  * `email`: Cadena de texto (Formato email válido).
  * `telefono`: Cadena de texto.
  * `interes`: Cadena de texto.
* `meta`: Objeto de metadatos de auditoría:
  * `componente_id`: Cadena de texto.
  * `componente_version`: Cadena de texto.
  * `modelo_ref`: Cadena de texto.
  * `requiere_revision_humana`: Booleano.
  * `tiempo_respuesta_ms`: Entero.
  * `status_proceso`: Cadena restrictiva (`completed`, `degraded`).

### 📤 2. Respuestas Esperadas (Sistemas de la Escuela)
Para dar por cerrada la transacción de forma corta y exitosa, el servidor de la Escuela deberá responder:
* `HTTP 200 OK` o `HTTP 204 No Content`: Evento procesado e indexado correctamente en su base de datos.
* `HTTP 400 Bad Request`: Error de validación estructural en el esquema de destino.

### ⚠️ 3. Elementos que Requieren Confirmación de Escuela
Este contrato se encuentra en estado **Propuesto**. No se escribirá código de servidor para INT-002 hasta que las autoridades institucionales ratifiquen de forma bilateral:
1. El endpoint URL productivo oficial de la Escuela para recibir estas notificaciones.
2. El mecanismo mandatorio de autenticación saliente segura (exigencia estricta de auditoría: firmas HMAC o mTLS corporativo).
3. Las políticas de reintentos (Retry Policies) en caso de que el servidor escolar experimente intermitencias de red.
