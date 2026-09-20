# 📜 DECISIÓN ARQUITECTÓNICA (ADR-003): POLÍTICA DE REINTENTOS ASÍNCRONOS

## ESTADO DEL DOCUMENTO: PROPUESTO (Fase de Diseño Técnico)

Este documento define la estrategia, límites y algoritmos de tolerancia a fallos para mitigar intermitencias de red transitorias durante la ejecución del Contrato INT-002.

### 🔍 Contexto y Problema Técnico
La comunicación saliente desde Mecánica Social IA hacia Mecánica Social Escuela opera en segundo plano de forma no durable (`BackgroundTasks` en memoria RAM). Si el servidor destino de la Escuela experimenta una caída momentánea (HTTP 502/503) o pérdida transitoria de paquetes, la petición HTTP POST fallará. Al no contar con una cola persistente, se requiere un mecanismo inmediato de recuperación automatizada a nivel de cliente de red.

### 🛡️ Decisión de Diseño: Backoff Exponencial con Jitter
Se establece la implementación de una política de reintentos basada en la librería estándar de red, configurando los siguientes parámetros de control perimetral:

1. **Límite de Reintentos:** Máximo **3 intentos adicionales** (4 llamados en total antes de desistir).
2. **Algoritmo de Espera Exponencial:** La demora entre llamados se duplicará progresivamente siguiendo la fórmula:
   \[\text{Espera} = \text{Base} \times 2^{\text{intento}}\]
   * Intento 1: Espera de 2 segundos.
   * Intento 2: Espera de 4 segundos.
   * Intento 3: Espera de 8 segundos.
3. **Inyección de Jitter (Ruido Aleatorio):** Se añadirá un factor de desalineación aleatoria de ± 500 ms a cada intervalo. Esto rompe la sincronización de hilos e impide que múltiples procesos reintenten ráfagas simultáneas contra la infraestructura de la Escuela (evitando un ataque accidental de denegación de servicio o *Thundering Herd*).
4. **Códigos HTTP Interceptados:** La política gatillará reintentos únicamente ante errores de timeout de red, fallas de conexión TCP o códigos de error HTTP transitorios del servidor (`500 Internal Error`, `502 Bad Gateway`, `503 Service Unavailable`). **Nunca** se reintentará ante errores del cliente (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`).

### 📊 Impacto Operacional en el MVP Local
* **Tolerancia a fallos:** El Runtime mitiga de forma autónoma cortes de red de hasta 14 segundos en total.
* **Gobernanza:** Este diseño permanece catalogado como **Propuesto** hasta su ratificación bilateral en las mesas de trabajo técnicas con Mecánica Social Escuela.
