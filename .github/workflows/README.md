# Workflows CI

## Activos

| Workflow | Propósito | Secretos |
|---|---|---|
| [eval-offline.yml](eval-offline.yml) | Smoke-test del harness en modo offline (estructura de prompt + suite) | Ninguno |

El job offline **no** llama a proveedores de modelos y **no** declara aprobación operativa.

## Pendiente

- Validación de enlaces markdown
- Secret scanning adicional al de la plataforma
- Job de modo `model` solo con `workflow_dispatch` / rama protegida y
  secretos de organización (`MS_IA_MODEL_*`). **Nunca** en PRs de forks.
  Detalle de huecos intencionales: `docs/arquitectura/pendientes-intencionales.md` (PEND-004).

## Referencias

- `infra/secretos-y-entorno.md`
- ADR-002
- `PRACTICO.md`
