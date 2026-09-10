# Workflows CI

## Activos

| Workflow | Propósito | Secretos |
|---|---|---|
| [eval-offline.yml](eval-offline.yml) | Smoke-test del harness en modo offline (estructura de prompt + suite) | Ninguno |

El job offline **no** llama a proveedores de modelos y **no** declara aprobación operativa.

## Pendiente intencional

| Job | Estado | Nota |
|---|---|---|
| **model** (inferencia) | Pendiente **a propósito** (PEND-004) | Solo con secrets de **organización** en el repo canónico; **no** ejecutar con secretos en forks |

Detalle: `docs/arquitectura/pendientes-intencionales.md`.

No añadir un job `model` hasta contar con secrets de org y guards anti-fork documentados/aceptados.
