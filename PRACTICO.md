# De la teoría a la práctica — guía rápida

Esta guía resume lo que **ya se puede hacer** en el repositorio y lo que **aún no**.

## Qué existe hoy (P1 — MVP de evaluación ejecutable)

1. Gobernanza y políticas (`GOVERNANCE.md`, `AI_ETHICS.md`, `DATA_GOVERNANCE.md`, `SECURITY.md`).
2. Un prompt de ejemplo en estado **prueba** (no operativo): `prompts/formulario-intake-v1.0.0.yaml`.
3. Suite sintética: `evaluations/casos-prueba/intake-test-set.yaml`.
4. Harness **offline**: `evaluations/harness.py`.
5. Resultados de corrida estructural en `evaluations/resultados/`.
6. CI smoke-test: `.github/workflows/eval-offline.yml` (sin secretos ni red de modelo).
7. ADR-001: `docs/arquitectura/ADR/ADR-001-arquitectura-inicial-y-mvp-evaluacion.md`.

## Primer comando útil

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

## Cómo aportar un cambio práctico

1. Abrir Issue con la plantilla `Componente de IA`.
2. Rama `issue-N/descripcion-corta`.
3. Crear/editar prompt siguiendo `prompts/esquema-prompt.yaml`.
4. Añadir o extender suite en `evaluations/casos-prueba/`.
5. Correr el harness offline y archivar resultado si es relevante.
6. Abrir PR con la plantilla de gobernanza.

## Qué falta (siguiente ola; no es P1)

| Prioridad | Entrega | Nota |
|---|---|---|
| P2 | Modo `model` del harness | Secrets fuera de Git; ver PEND-004 |
| P2 | Model-card del proveedor autorizado | PEND-001 |
| P2 | Contrato INT-001 con `mecanica-social-escuela` | PEND-002 |
| P3 | Separación de roles de revisión / segundo maintainer | PEND-003 |
| P3 | Agentes con permisos mínimos y pruebas de abuso | — |

Detalle de huecos intencionales: `docs/arquitectura/pendientes-intencionales.md`.

## Reglas de oro

- No inventar inventarios (agentes, 100+ casos, aprobaciones).
- No subir PII real ni secretos.
- Offline ≠ aprobación operativa.
- La IA no decide; la persona responsable sí.
