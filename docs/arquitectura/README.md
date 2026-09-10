# Arquitectura inicial — mecanica-social-ia

Propósito
- Documentar la arquitectura inicial del repositorio `mecanica-social-ia`.
- Servir como guía para desarrolladores y colaboradores sobre dónde ubicar prompts, agentes, modelos, experimentos, evaluaciones, integraciones y documentación.
- Proveer convenciones mínimas, artefactos y checklist para avanzar ordenadamente desde esta Issue fundacional.

Resumen ejecutivo
`mecanica-social-ia` es el componente de IA del proyecto Mecánica Social. Su objetivo es ofrecer una estructura ordenada, trazable y reproducible para:
- Desarrollo y versionado de prompts.
- Definición e integración de agentes.
- Gestión de configuraciones y modelos.
- Ejecución y registro de experimentos y evaluaciones.
- Gobernanza y seguridad en el uso de modelos.

Alcance de este README
- Explicar la visión general y los componentes principales.
- Proponer una estructura de carpetas inicial.
- Indicar convenciones y plantillas básicas para prompts, agents y experiments.
- Enumerar próximos pasos y criterios mínimos de aceptación.

Componentes principales (visión rápida)
- docs/arquitectura/: Documentación de arquitectura y decisiones (ADRs).
- docs/arquitectura/pendientes-intencionales.md: Huecos dejados a propósito (vendor, INT-001/002, CODEOWNERS multi-persona, CI model).
- prompts/: Registro versionado de prompts y metadatos.
- models/: Configs, model-cards y referencias a pesos/servicios.
- agents/: Implementaciones y manifiestos de agentes.
- experiments/: Notebooks y scripts reproducibles con resultados.
- evaluations/: Harness de evaluación, métricas y scripts de agregación.
- infra/: Scripts de despliegue y configuración de infraestructura (opcional).
- data/: Descriptores y políticas de acceso (NO datos sensibles directamente).
- examples/: Pequeños demos y ejemplos de uso.
- src/ o packages/: Código compartido y librerías internas.
- .github/: Workflows CI, ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE, CODEOWNERS.

Estructura propuesta (resumen)
- docs/
  - arquitectura/
    - README.md
    - arquitectura-general.md
    - componentes.md
    - integraciones.md
    - gobernanza.md
    - adr/ (architecture decision records)
- prompts/
- models/
- agents/
- experiments/
- evaluations/
- infra/
- data/
- examples/
- src/

Convenciones y buenas prácticas
- Branches: issue-<número>/descripcion o feat/<area>/descripcion (ej. issue-1/arquitectura-general).
- Commits: tipo(scope): breve-descripción — p.ej. feat(arquitectura): añadir README inicial.
- PRs: Título claro y referencia a la Issue (ej. "ISSUE #1 — Definir arquitectura general"). Incluir checklist de criterios de aceptación.
- ADRs: Registrar decisiones arquitectónicas importantes en docs/arquitectura/adr/*.md (fecha, contexto, decisión, consecuencias).

Estrategia para prompts
- Formato: YAML por prompt con metadatos y test-cases.
- Ubicación: prompts/<id>-v<versión>.yaml
- Metadatos mínimos: id, versión, autor, fecha, tags, prompt_text, examples, tests.
- Ejemplo (esquema):
```yaml
id: user-intake-v1
version: 0.1.0
author: tu-nombre
date: 2026-09-06
tags: [intake, form]
prompt_text: |
  Por favor, resume el siguiente formulario en 3 puntos principales...
examples:
  - input: "..."
    expected: "..."
tests:
  - type: exact_match
    input: "Prueba..."
    expected: "Respuesta esperada..."
```

Estrategia para agents y modelos
- Agents: cada agent tiene un manifiesto agents/<agent-name>/agent.yaml que declara entradas, salidas, permisos y recursos necesarios.
- Models: models/<model-name>/config.yaml con provider, version, token_limits, licencia, model-card.md.
- Separar definiciones (metadata) de implementaciones (src/ o agents/).

Experimentos y evaluaciones
- Experiments: experiments/<nombre>/ con notebook, run.sh y environment.yml. Guardar resultados en experiments/<nombre>/results/.
- Evaluations: evaluations/harness.py o similar que ejecute prompts contra modelos y calcule métricas reproducibles (BLEU, ROUGE, exactitud, evaluación humana, etc.).
- CI: incluir job de smoke-test para ejecutar un experimento pequeño en PRs si procede.

Seguridad, datos y gobernanza
- No versionar datos sensibles ni PII. Usar placeholders y scripts de descarga con permisos.
- Mantener model-cards y registro de evaluaciones antes de aceptar modelos en producción.
- Revisiones obligatorias para cambios en prompts/models: PR + checklist + aprobación por persona de gobernanza.
- Revisar licencias de modelos y dependencias antes de integrarlos.

Plantillas y artefactos mínimos a crear
- docs/arquitectura/arquitectura-general.md (diagrama y flujo de datos)
- docs/arquitectura/componentes.md (responsables y contratos)
- docs/arquitectura/integraciones.md (contratos con mecanica-social-escuela)
- docs/arquitectura/gobernanza.md (políticas)
- prompts/README.md (esquema y cómo versionar)
- agents/README.md (manifiesto)
- experiments/sample-experiment/ (notebook + run script)
- evaluations/harness.py (script de ejemplo)
- .github/ISSUE_TEMPLATE.md y PULL_REQUEST_TEMPLATE.md con checklist para modelos/prompts

Checklist mínimo para cerrar la Issue #1
- [ ] Arquitectura general definida y documentada (docs/arquitectura/arquitectura-general.md)
- [ ] Estructura de carpetas creada y documentada (README y README en cada subcarpeta)
- [ ] Principales componentes identificados y responsables asignados (componentes.md)
- [ ] Relación técnica con mecanica-social-escuela documentada (integraciones.md)
- [ ] Dependencias principales listadas (docs/arquitectura/)
- [ ] Riesgos técnicos iniciales identificados y mitigaciones propuestas (gobernanza.md)

Próximos pasos (inmediatos)
1. ~~Añadir este README y estructura de carpetas.~~
2. ~~Completar arquitectura-general.md y componentes.~~
3. ~~P1: harness offline ejecutable + suite intake (ver PRACTICO.md y ADR-001).~~
4. P2+: modo model (PEND-004), vendor (PEND-001), INT-001 (PEND-002).

Referencias y notas
- Registrar decisiones importantes en docs/arquitectura/adr/.
- Mantener un CHANGELOG para cambios significativos de arquitectura.
- Para cualquier integración con `mecanica-social-escuela`, definir contrato de datos y API en docs/arquitectura/integraciones.md.
- Lo que queda pendiente **a propósito** (sin inventar vendor, contrato Escuela, segundo maintainer ni job CI model) está en [pendientes-intencionales.md](pendientes-intencionales.md).

Contacto
- Owner técnico (asignar en la Issue): @LeodanZapata
- Persona gobernanza (recomendado): [elegir responsable]

(Plantilla inicial: ampliar en docs/arquitectura/arquitectura-general.md y componentes.md según avance)

## Actualización 2026-09 (ola práctica)

Documentos adicionales:

- [`roles-revision.md`](roles-revision.md) — separación de roles de revisión
- [`contratos/INT-001-escuela.md`](contratos/INT-001-escuela.md) — contrato provisional con Escuela
- [`ADR/ADR-002-modo-model-secretos-y-proveedor.md`](ADR/ADR-002-modo-model-secretos-y-proveedor.md) — modo model y secretos
- Inventario de integraciones: [`integraciones.md`](integraciones.md)

Estado honesto: harness offline+model; model-card de evaluación **propuesta** (no productiva); INT-001 provisional.

