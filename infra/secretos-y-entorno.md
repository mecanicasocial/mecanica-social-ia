# 🔐 GOBERNANZA DE SECRETOS Y VARIABLES DE ENTORNO

Este documento establece el inventario oficial, el propósito y las restricciones operacionales de las variables de entorno utilizadas por el Runtime de Mecánica Social IA para gestionar los perímetros de seguridad y conectividad de red.

---

## 📋 Inventario de Variables de Configuración y Red

Las siguientes variables deben ser inyectadas en el contenedor del servidor web de forma obligatoria según el entorno de ejecución correspondiente:

### 1. `AMBIENTE`
* **Tipo:** Configuración Lógica.
* **Valores permitidos:** `development`, `production`.
* **Propósito:** Determina las barreras de seguridad activas. Si su valor es `production`, se deshabilitan todos los simuladores locales (Mocks) y se exige el cumplimiento estricto de las URLs de red reales.

### 2. `API_KEY_ESCUELA_TOKEN`
* **Tipo:** Secreto Criptográfico (Llave de entrada).
* **Valor sintético (Dev/Test):** `<API_KEY>`
* **Propósito:** Token perimetral utilizado para autenticar las peticiones entrantes desde la Escuela hacia el endpoint `POST /v1/intake` (Contrato INT-001). Su ausencia o descalce provoca un error `403 Forbidden`.

### 3. `MS_IA_MODEL_API_KEY`
* **Tipo:** Secreto Criptográfico (Llave de proveedor).
* **Valor sintético (Dev/Test):** `mock_local_secret_key`
* **Propósito:** Credencial utilizada por el cliente interno de IA (`ms_ia`) para autenticarse ante el proveedor de modelos. En desarrollo, valida la comunicación contra el simulador local.

### 4. `ESCUELA_WEBHOOK_URL`
* **Tipo:** Configuración de Red Saliente (Callback INT-001).
* **Valor sintético (Dev/Test):** `http://mock-provider-ia:8001/webhooks/escuela-intake`
* **Propósito:** Endpoint de la Escuela utilizado para despachar la confirmación asíncrona inmediata del lead.
* **Restricción de Producción:** Si `AMBIENTE=production` y esta variable está ausente, el Runtime interrumpe la transacción de inmediato lanzando un `RuntimeError` controlado. Se eliminó físicamente cualquier fallback a localhost.

### 5. `ESCUELA_NOTIFICACION_URL` (Inyectada para INT-002)
* **Tipo:** Configuración de Red Saliente (Callback INT-002).
* **Valor sintético (Dev/Test):** `http://mock-provider-ia:8001/webhooks/escuela-output`
* **Propósito:** Endpoint oficial de la Escuela utilizado por la función `disparar_notificacion_int002` para despachar los perfiles de alumnos extraídos y validados por la IA de forma asíncrona en segundo plano.
* **Restricción de Producción:** Si `AMBIENTE=production` y esta variable está ausente, el Runtime genera un log crítico de auditoría (`[INT-002-SEGURIDAD] INTEGRACIÓN BLOQUEADA`) y lanza un `RuntimeError` bloqueante, impidiendo cualquier fuga silenciosa de información hacia redes externas.

---

## 🐳 Inyección en Entornos de Microservicios (Docker Compose)

En la infraestructura de evaluación local, todas estas variables se inyectan de forma centralizada y segura a través del bloque `environment:` en el archivo `docker-compose.yaml`, operando bajo el aislamiento estricto de la red privada puente `red-mecanica-social-ia`.
