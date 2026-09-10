# De la teoría a la práctica — guía rápida

Esta guía resume lo que **ya se puede hacer** en el repositorio y lo que **aún no**.

## Qué existe hoy

1. Gobernanza y políticas (`GOVERNANCE.md`, `AI_ETHICS.md`, `DATA_GOVERNANCE.md`, `SECURITY.md`).
2. Un prompt de ejemplo en estado **prueba** (no operativo): `prompts/formulario-intake-v1.0.0.yaml`.
3. Suite sintética: `evaluations/casos-prueba/intake-test-set.yaml`.
4. Harness **offline** y **model**: `evaluations/harness.py` (secretos solo por env).
5. Resultados de corrida en `evaluations/resultados/`.
6. CI smoke-test offline: `.github/workflows/eval-offline.yml`.
7. ADR-001 (MVP offline) y ADR-002 (modo model + secretos + slot de evaluación).
8. Model-card del slot `models/openai-compatible-eval/` (**propuesto**, no productivo).
9. Contrato provisional INT-001: `docs/arquitectura/contratos/INT-001-escuela.md`.
10. Separación de roles de revisión: `docs/arquitectura/roles-revision.md`.

## Primer comando útil (offline)

```bash
pip install -r requirements.txt
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode offline \
  --output evaluations/resultados
```

Interpretación:

- Exit 0 + umbrales OK → la **estructura** del prompt y de la suite es coherente.
- `apto_para_aprobacion_operativa: false` → **no** usar en producción ni marcar `aprobado`.

## Modo model (secretos fuera de Git)

```bash
export MS_IA_MODEL_API_KEY="…"        # nunca en Git
export MS_IA_MODEL_BASE_URL="https://…"
export MS_IA_MODEL_ID="…"

python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode model \
  --model-ref models/openai-compatible-eval \
  --output evaluations/resultados
```

Ver `infra/secretos-y-entorno.md` y la model-card del slot. Sin key/URL el modo model **falla de forma controlada**.  
El slot actual **no** es proveedor productivo autorizado.

## Cómo aportar un cambio práctico

1. Abrir Issue con la plantilla `Componente de IA`.
2. Rama `issue-N/descripcion-corta`.
3. Crear/editar prompt siguiendo `prompts/esquema-prompt.yaml`.
4. Añadir o extender suite en `evaluations/casos-prueba/`.
5. Correr el harness offline (y model si hay entorno) y archivar resultado si es relevante.
6. Abrir PR con la plantilla de gobernanza y roles de revisión.

## Qué falta (siguiente ola práctica)

| Prioridad | Entrega |
|---|---|
| Hecho (base) | Modo `model` del harness con secretos fuera de Git |
| Hecho (base) | Model-card del slot de evaluación (propuesto; falta autorización productiva) |
| Hecho (base) | Contrato **provisional** INT-001 con Escuela (falta confirmación bilateral) |
| Hecho (base) | Separación documentada de roles de revisión (excepción dual temporal) |
| P2 | Autorizar proveedor productivo (vendor + INT-002 + registro) |
| P2 | Validar INT-001 con responsables de `mecanica-social-escuela` |
| P2 | Segundo maintainer / teams para four-eyes real en CODEOWNERS |
| P3 | Agentes con permisos mínimos y pruebas de abuso |

Detalle de huecos intencionales: `docs/arquitectura/pendientes-intencionales.md`.

## Reglas de oro

- No inventar inventarios (agentes, 100+ casos, aprobaciones).
- No subir PII real ni secretos.
- Offline ≠ aprobación; model score ≠ aprobación.
- La IA no decide; la persona responsable sí.
