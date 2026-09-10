# ADR-001 — Arquitectura inicial de carpetas y MVP de evaluación offline

## Estado

Aceptado

## Fecha

2026-09-10

## Contexto

`mecanica-social-ia` nació como marco de gobernanza y arquitectura documental.
La auditoría del proceso identificó una brecha entre política y práctica:
prompts marcados como aprobados sin evidencia, harness solo en markdown y
plantillas GitHub no operativas.

Se necesita un primer paso **práctico y reversible** que:

1. Mantenga la separación de carpetas ya definida.
2. Haga ejecutable la evaluación estructural (offline).
3. Evite presentar el modo offline como aprobación operativa.

## Decisión

1. Conservar la estructura de primer nivel:
   `docs/`, `prompts/`, `models/`, `agents/`, `experiments/`, `evaluations/`,
   `infra/`, `data/`, `examples/`, `src/`.
2. El harness canónico vive en `evaluations/harness.py` y se alinea a
   `evaluations/harness.md`.
3. Las suites de casos viven en `evaluations/casos-prueba/`.
4. Las corridas se archivan en `evaluations/resultados/`.
5. El MVP implementa solo modo **offline** (validación estructural).
6. Todo resultado offline declara `apto_para_aprobacion_operativa: false`.
7. Los estados de componente en español preferidos son:
   `borrador`, `prueba`, `aprobado`, `restringido`, `obsoleto`, `suspendido`, `retirado`.
8. No se versionan PII reales ni secretos; las suites son sintéticas.

## Alternativas consideradas

- Esperar a tener proveedor de modelo y CI completa antes de cualquier código:
  retrasa la trazabilidad y perpetúa documentación sin evidencia.
- Evaluar “aprobado” solo con ejemplos embebidos en el prompt:
  confunde fixture con desempeño del modelo.
- Colocar scripts de prueba bajo `prompts/.evaluations/`:
  mezcla artefactos y ya produjo un falso positivo de aprobación.

## Consecuencias

- Se puede correr una smoke-test local/CI sin red ni secretos.
- Queda explícito qué falta para promoción (modo model + revisión de gobernanza).
- Aumenta ligeramente la superficie de código (Python + PyYAML).
- Habrá que añadir ADR posteriores para proveedor de modelo e integración con
  `mecanica-social-escuela` cuando existan contratos reales.

## Implicancias

- Actualizar inventarios y guías para no listar como existentes agentes,
  model cards o harness de 100+ casos hasta que existan.
- El primer prompt de ejemplo permanece en estado `prueba` con riesgo `medio`
  por tratamiento potencial de datos personales.

## Referencias

- `docs/arquitectura/arquitectura-general.md`
- `evaluations/harness.md`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
