# Workflows CI

Aún no hay workflows YAML en este directorio.

## Pendiente intencional

| Job | Estado | Nota |
|---|---|---|
| Smoke / offline | Pendiente de diseño | Sin secretos ni red |
| **model** (inferencia) | Pendiente **a propósito** (PEND-004) | Solo con secrets de **organización** en el repo canónico; **no** ejecutar con secretos en forks |

Detalle: `docs/arquitectura/pendientes-intencionales.md`.

No añadir un job `model` hasta contar con secrets de org y guards anti-fork documentados/aceptados.
