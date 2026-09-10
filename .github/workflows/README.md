# Workflows

## Activos

| Workflow | Propósito |
|---|---|
| `eval-offline.yml` | Smoke-test del harness offline (sin secretos, sin red de modelos) |

## Pendiente

- Validación de enlaces markdown
- Secret scanning adicional al de la plataforma
- Job de modo `model` solo con `workflow_dispatch` / rama protegida y
  secretos de organización (`MS_IA_MODEL_*`). **Nunca** en PRs de forks.

## Referencias

- `infra/secretos-y-entorno.md`
- ADR-002
