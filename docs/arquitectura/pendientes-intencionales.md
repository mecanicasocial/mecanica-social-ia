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
| PEND-001 | Vendor productivo + **INT-002** validado | Requiere **autorización institucional** (proveedor, datos en tránsito, evaluación y adopción) | Sin vendor en `models/`; INT-002 en estado **Propuesto** | Autorización institucional + registro del proveedor + evidencia de evaluación + INT-002 al menos en **Validada** | `integraciones.md`, `models/README.md`, `DATA_GOVERNANCE.md` |
| PEND-002 | **INT-001** confirmado con Escuela | Requiere **confirmación bilateral** con `mecanica-social-escuela` (contrato, datos, responsabilidades) | INT-001 en estado **Propuesto**; propósito y datos “Por definir” | Confirmación bilateral documentada (sin inventar API) + actualización del inventario de integraciones | `integraciones.md`, `DATA_GOVERNANCE.md` |
| PEND-003 | Teams / segundo maintainer en `CODEOWNERS` | **Four-eyes real** con más de una persona (roles de `GOVERNANCE.md` no colapsados en un solo actor) | `CODEOWNERS` y `NOTICE` solo con `@LeodanZapata` | Segundo maintainer o Team de GitHub real en `CODEOWNERS` / roles, sin inventar handles | `CODEOWNERS`, `NOTICE`, `GOVERNANCE.md` |
| PEND-004 | CI job **model** | Solo con **secrets de organización** en el repo canónico; **no** en forks | Existe smoke offline (`eval-offline.yml`); **no** hay job model | Workflow model en repo canónico, secrets de org, guards anti-fork; separado del smoke offline | `evaluations/harness.md`, `.github/workflows/`, `infra/README.md`, `SECURITY.md` |

## 4. Detalle

### PEND-001 — Vendor productivo + INT-002 validado

- **Qué no hay hoy:** carpeta de proveedor en `models/`, `config.yaml` / model-card productivos, cliente de inferencia operativo, ni INT-002 más allá de “Propuesto”.
- **Por qué no se completa aquí:** la adopción de un proveedor y el envío de datos a terceros exigen autorización institucional y controles de datos (`DATA_GOVERNANCE.md`).
- **Qué sí puede existir antes del desbloqueo:** documentación de *cómo* se documentaría un proveedor; evaluaciones sintéticas offline; ejemplos no productivos sin secretos.

### PEND-002 — INT-001 confirmado con Escuela

- **Qué no hay hoy:** interfaz, entradas/salidas, autenticación ni acuerdo de datos con Escuela.
- **Por qué no se completa aquí:** el contrato es bilateral; inventarlo rompería la política de no presuponer APIs ni campos no confirmados.
- **Qué sí puede existir antes del desbloqueo:** diagrama conceptual Escuela ↔ IA; plantilla de contrato de integración; estado **Propuesto** en el inventario.

### PEND-003 — Teams / segundo maintainer en CODEOWNERS

- **Qué hay hoy:** un único owner en `CODEOWNERS` y los tres roles de `NOTICE` concentrados en `@LeodanZapata`.
- **Por qué es intencional el gap:** el four-eyes de `GOVERNANCE.md` (revisión técnica / metodológica / ética / independiente) requiere **personas distintas** cuando el riesgo lo exige; no se inventan cuentas ni Teams.
- **Qué sí puede existir antes del desbloqueo:** políticas de roles; CODEOWNERS funcional con el owner actual; comentario de que el segundo maintainer está pendiente.

### PEND-004 — CI job model

- **Qué hay hoy:** smoke offline en `.github/workflows/eval-offline.yml` (sin secretos ni red de modelo).
- **Qué no hay:** job de inferencia con proveedor.
- **Distinción:**
  - **Smoke / offline:** implementado en P1; sin secretos ni red.
  - **Job model:** implica credenciales de proveedor → solo secrets de **organización**, en el repositorio canónico, **nunca** expuestos a forks no confiables.
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
