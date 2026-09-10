# Prompts

Esta carpeta contiene los prompts versionados utilizados por
`mecanica-social-ia`.

```text
prompts/
├── README.md                          ← Guía de uso
└── formulario-intake-v1.0.0.yaml      ← Ejemplo de formato (estado: prueba; no operativo)
```

> **Nota:** `esquema-prompt.yaml` y otros prompts citados en documentación
> histórica son aspiracionales hasta que existan en este directorio.
> No hay harness ni suites de prueba bajo `prompts/`.

## Propósito

Mantener los prompts como artefactos versionables, trazables,
revisables y evaluables.

## Contenido

Aquí se almacenarán:

- Prompts en desarrollo.
- Prompts en evaluación / prueba.
- Prompts aprobados (solo con evidencia formal).
- Versiones históricas de prompts.
- Esquemas y convenciones para su definición (cuando existan).

## Versionado

Los prompts utilizarán versionado semántico:

`MAJOR.MINOR.PATCH`

Ejemplo:

`formulario-intake-v1.0.0.yaml`

## Estados

Los prompts usan el vocabulario institucional de estados de componente
(ver `README.md` raíz y `evaluations/resultados.md`):

| Estado | Significado |
|---|---|
| `borrador` | En definición; no listo para evaluación formal |
| `prueba` | En evaluación o ejemplo no operativo |
| `aprobado` | Autorizado para un uso definido, con evidencia y revisión |
| `restringido` | Uso limitado o condicionado |
| `obsoleto` / `suspendido` / `retirado` | Fuera de uso activo |

Mapeo orientativo si aparece vocabulario en inglés en borradores antiguos:
`draft`→`borrador`, `testing`→`prueba`, `approved`→`aprobado`,
`deprecated`→`obsoleto`, `archived`→`retirado`.

**Regla:** `aprobado` exige evidencia formal bajo `evaluations/` (suite,
corrida con modo declarado y revisión según riesgo). Un ejemplo embebido
en el YAML del prompt **no** basta.

## Ejemplo actual: `formulario-intake-v1.0.0.yaml`

| Campo | Valor actual |
|---|---|
| `estado` | `prueba` |
| `alcance` | `ejemplo-no-operativo` |
| `nivel_riesgo` | `medio` (PII de beneficiarios) |
| Evidencia formal | Pendiente en `evaluations/` |

No utilizar este archivo como componente productivo ni presentarlo como
autorizado institucionalmente.

## Reglas

- Cada prompt debe tener un identificador único.
- Cada versión debe ser trazable.
- Los cambios relevantes deben realizarse mediante Issue y Pull Request.
- Los prompts `aprobado` deben contar con evaluaciones formales archivadas.
- No incorporar datos personales reales, credenciales, tokens o información sensible.
- No colocar scripts de harness ni suites bajo `prompts/`.

## Evaluación (única ubicación de evidencia)

Las pruebas, el harness, las suites y los resultados de los prompts se
gestionan **solo** en:

```text
evaluations/
├── harness.md / harness.py   ← contrato e implementación
├── casos-prueba/             ← suites YAML sintéticas
├── resultados/               ← corridas archivadas
└── metricas.md, resultados.md, casos-prueba.md
```

| Qué | Dónde |
|---|---|
| Metadatos, `prompt_text`, ejemplos ilustrativos | `prompts/*.yaml` |
| Suites reutilizables, harness, métricas, resultados | `evaluations/` |

Cualquier borrador histórico bajo `prompts/.evaluations/` se eliminó en
P0 por estar mal ubicado (Python con extensión `.yaml`) y por poder
sugerir “aprobado para producción” sin medir el modelo. El harness
canónico se define en `evaluations/harness.md`.

## Relación con otros componentes

Los prompts pueden ser utilizados por:

- `agents/`
- `experiments/`
- `evaluations/`
- `src/`

## Principio

Un prompt es un componente versionable del sistema y debe tratarse con
el mismo nivel de trazabilidad que el código. La gobernanza decide el
estado; el harness solo mide.
