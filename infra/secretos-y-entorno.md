# Secretos y variables de entorno

## Principio

**Ningún secreto se versiona en Git.** API keys, tokens, contraseñas y
credenciales viven solo en el entorno de ejecución o en un gestor
institucional de secretos.

Ver también: `SECURITY.md`, `DATA_GOVERNANCE.md`, ADR-002.

## Variables para modo `model` del harness

| Variable | Obligatoria | Descripción |
|---|---|---|
| `MS_IA_MODEL_API_KEY` | Sí (modo model) | Credencial del proveedor. Nunca se imprime ni se escribe en resultados. |
| `MS_IA_MODEL_BASE_URL` | No | Base URL del endpoint (p. ej. `https://api.ejemplo/v1`). Si falta, se usa `base_url` de `models/<id>/config.yaml` si es público y no sensible. |
| `MS_IA_MODEL_ID` | No | Identificador de modelo en el proveedor. Sobrescribe `model_id` del config. |
| `MS_IA_MODEL_API_KEY_HEADER` | No | Nombre del header de auth (default: `Authorization` con prefijo `Bearer`). |
| `MS_IA_MODEL_TIMEOUT_SEC` | No | Timeout HTTP en segundos (default: 60). |

## Configuración no sensible (sí versionable)

- `evaluations/config.example.yaml` — ejemplo de corrida.
- `models/<id>/config.yaml` — id, provider, parámetros públicos, nombre de la variable de entorno de la key (**no** el valor).

Copiar el ejemplo y ajustar en local **sin** commitear keys:

```bash
cp evaluations/config.example.yaml evaluations/config.local.yaml
# config.local.yaml debe permanecer fuera de Git (ver .gitignore si se añade)
```

## GitHub Actions

| Contexto | ¿Modo model? | Secretos |
|---|---|---|
| PR públicos / forks | **No** | No disponibles de forma segura |
| `eval-offline.yml` | Solo offline | Ninguno |
| Futuro job `model` (`workflow_dispatch`, rama protegida) | Opcional | GitHub Actions secrets / OIDC de la org |

Nunca echo de secretos en logs de CI.

## Rotación e incidentes

Si una key se filtra:

1. Revocar/rotar en el proveedor de inmediato.
2. Reportar por canal privado (`SECURITY.md`).
3. No pegar el valor completo en Issues/PR.

## Checklist rápido

- [ ] No hay keys en archivos del commit
- [ ] `MS_IA_MODEL_API_KEY` solo en shell/CI secrets
- [ ] Resultados en `evaluations/resultados/` sin PII ni headers de auth
- [ ] Model-card y `estado` del modelo revisados antes de uso no sintético
