# Pendientes intencionales (no inventados)

## 1. Propósito

Registrar de forma explícita lo que **queda pendiente a propósito** en `mecanica-social-ia`.

Estos huecos **no son omisiones accidentales** ni invitaciones a inventar contratos, proveedores, owners o automatizaciones. Se mantienen abiertos hasta que exista autorización, confirmación bilateral o condiciones de seguridad adecuadas.

## 2. Principio

Si falta un acuerdo, un vendor, un segundo maintainer o un secreto de organización:

- se documenta el pendiente;
- se deja el estado en “propuesto / pendiente”;
- **no** se inventan APIs, campos, actas, handles de Teams ni workflows con secretos.

## 3. Inventario

| ID | Pendiente | Por qué es intencional | Estado en repo | Desbloqueo (criterio verificable) | Referencias |
|---|---|---|---|---|---|
| PEND-001 | Vendor productivo + **INT-002** validado | Requiere **autorización institucional** (proveedor, datos en tránsito, evaluación y adopción) | Solo slot de **evaluación** `models/openai-compatible-eval/` (propuesto); INT-002 no productiva | Autorización institucional + registro del proveedor + evidencia de evaluación + INT-002 al menos en **Validada** | `integraciones.md`, `models/README.md`, ADR-002, `DATA_GOVERNANCE.md` |
| PEND-002 | **INT-001** confirmado con Escuela | Requiere **confirmación bilateral** con `mecanica-social-escuela` (contrato, datos, responsabilidades) | Contrato **provisional** + schema/muestra sintéticos; falta confirmación Escuela | Confirmación bilateral documentada (sin inventar API productiva) + actualización del inventario | `integraciones.md`, `contratos/INT-001-escuela.md`, `DATA_GOVERNANCE.md` |
| PEND-003 | Teams / segundo maintainer en `CODEOWNERS` | **Four-eyes real** con más de una persona (roles de `GOVERNANCE.md` no colapsados en un solo actor) | `CODEOWNERS` y `NOTICE` solo con `@LeodanZapata`; roles documentados en `roles-revision.md` | Segundo maintainer o Team de GitHub real en `CODEOWNERS` / roles, sin inventar handles | `CODEOWNERS`, `NOTICE`, `roles-revision.md`, `GOVERNANCE.md` |
| PEND-004 | CI job **model** | Solo con **secrets de organización** en el repo canónico; **no** en forks | Harness local soporta modo `model`; CI solo smoke offline (`eval-offline.yml`); **no** hay job model | Workflow model en repo canónico, secrets de org, guards anti-fork; separado del smoke offline | `evaluations/harness.md`, `.github/workflows/`, `infra/secretos-y-entorno.md`, ADR-002, `SECURITY.md` |

## 4. Detalle

### PEND-001 — Vendor productivo + INT-002 validado

- **Qué hay hoy:** slot de evaluación `models/openai-compatible-eval/` (estado propuesto), cliente `src/ms_ia/model_client.py` y modo `model` del harness con secretos por entorno (ADR-002).
- **Qué no hay hoy:** proveedor **productivo** autorizado, ni INT-002 Validada/Operativa.
- **Por qué no se completa aquí:** la adopción de un proveedor y el envío de datos a terceros exigen autorización institucional y controles de datos (`DATA_GOVERNANCE.md`).
- **Qué sí puede existir antes del desbloqueo:** slot y model-card de evaluación; corridas model con secretos locales; evaluaciones sintéticas offline.

### PEND-002 — INT-001 confirmado con Escuela

- **Qué hay hoy:** contrato **provisional** `contratos/INT-001-escuela.md` y schema/muestra sintéticos bajo `data/`.
- **Qué no hay hoy:** confirmación bilateral, API productiva ni acuerdo de datos operativos con Escuela.
- **Por qué no se completa aquí:** el contrato definitivo es bilateral; inventar la API productiva rompería la política de no presuponer campos no confirmados.
- **Qué sí puede existir antes del desbloqueo:** contrato provisional; schema sintético; diagrama conceptual Escuela ↔ IA.

### PEND-003 — Teams / segundo maintainer en CODEOWNERS

- **Qué hay hoy:** un único owner en `CODEOWNERS` y roles concentrados en `@LeodanZapata`; separación de roles documentada en `docs/arquitectura/roles-revision.md` (excepción dual temporal).
- **Por qué es intencional el gap:** el four-eyes de `GOVERNANCE.md` requiere **personas distintas** cuando el riesgo lo exige; no se inventan cuentas ni Teams.
- **Qué sí puede existir antes del desbloqueo:** políticas y matriz de roles; CODEOWNERS funcional con el owner actual; registros de decisión en `docs/gobernanza/registros/`.

### PEND-004 — CI job model

- **Qué hay hoy:** smoke offline en `.github/workflows/eval-offline.yml`; harness local con modo `model` (secretos por env, ADR-002).
- **Qué no hay:** job CI de inferencia con proveedor.
- **Distinción:**
  - **Smoke / offline:** implementado; sin secretos ni red.
  - **Modo model local:** disponible con `MS_IA_MODEL_*`; no es CI.
  - **Job model CI:** implica credenciales de proveedor → solo secrets de **organización**, en el repositorio canónico, **nunca** expuestos a forks no confiables.
- **Por qué no se inventa el job model aquí:** sin secrets de org y sin política de guards, un job model sería inseguro o simbólico.
- **Desbloqueo mínimo:** secretos configurados en la org; condición de ejecución que excluya forks; separación explícita del job offline.

## 5. Relación con estados de integración

En `integraciones.md`, **Propuesto** para INT-001 e INT-002 significa, en este contexto:

- la fila existe como referencia;
- **no** hay contrato implementado ni validado;
- el avance está **bloqueado a propósito** por PEND-002 y PEND-001 respectivamente.

No equivale a “se puede inventar el detalle para rellenar la tabla”.

## 6. Qué no hacer

- No inventar nombre de vendor, modelo productivo ni precios.
- No inventar endpoints, esquemas ni acuerdos con Escuela.
- No añadir handles ficticios a `CODEOWNERS` o Teams.
- No crear un job CI `model` que lea secretos en PRs de forks.
- No marcar INT-001 / INT-002 como Validada u Operativa sin evidencia y autorización.

## 7. Cuándo crear un ADR

Al desbloquear cada pendiente estructural, registrar la decisión en `docs/arquitectura/ADR/` cuando:

- se adopte un proveedor productivo (PEND-001);
- se confirme el contrato con Escuela (PEND-002);
- se defina el modelo de ownership multi-persona (PEND-003);
- se fije la política de CI model / secrets / forks (PEND-004).

## 8. Referencias

- `docs/arquitectura/integraciones.md`
- `docs/arquitectura/gobernanza.md`
- `docs/arquitectura/ADR/README.md`
- `models/README.md`
- `CODEOWNERS`
- `NOTICE`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `SECURITY.md`
- `evaluations/harness.md`
- `infra/README.md`
- `.github/workflows/README.md`
- `docs/arquitectura/roles-revision.md`
- `docs/arquitectura/contratos/INT-001-escuela.md`
- `infra/secretos-y-entorno.md`
