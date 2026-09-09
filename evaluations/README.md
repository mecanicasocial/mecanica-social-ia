# Evaluations

Esta carpeta contiene el **marco de evaluación** de `mecanica-social-ia`: diseño del harness, catálogo de métricas, formato de resultados, normas de casos de prueba y evidencia versionada.

## Propósito

Determinar de manera sistemática si prompts, modelos, agentes y otros componentes cumplen los criterios definidos para su utilización.

**Principio:** un componente no se considera aprobado solo porque funciona en un caso individual o porque produce una respuesta plausible. Debe existir evidencia suficiente, reproducible y revisada según el riesgo.

## Documentos de este marco (markdown)

| Documento | Contenido |
|---|---|
| [harness.md](harness.md) | Contrato de diseño de `evaluations/harness.py` (modos, entradas, límites) |
| [metricas.md](metricas.md) | Catálogo de métricas, umbrales orientativos y uso según riesgo |
| [resultados.md](resultados.md) | Esquema, interpretación y gobernanza de resultados |
| [casos-prueba.md](casos-prueba.md) | Norma para suites de casos sintéticos |
| [_plantilla-resultado.json](_plantilla-resultado.json) | Plantilla de artefacto de resultado (no es una corrida real) |

La implementación en código `harness.py` se alinea a `harness.md` cuando se desarrolle; **este marco documental es la fuente de verdad de diseño** hasta entonces.

## Estructura

```text
evaluations/
├── README.md
├── harness.md
├── metricas.md
├── resultados.md
├── casos-prueba.md
├── _plantilla-resultado.json
├── harness.py                 (implementación de referencia; pendiente)
├── casos-prueba/              (suites YAML; pendiente de contenido sintético)
└── resultados/                (corridas reales; crear al archivar la primera)
```

Estructura adicional por tipo de componente (cuando crezca el acervo): `prompts/`, `models/`, `agents/` bajo `evaluations/`.

## Componentes evaluables

- Prompts
- Modelos
- Agentes
- Flujos
- Integraciones
- Componentes de software

## Tipos de evaluación

- Exactitud y extracción estructurada
- Precisión, recall, F1
- Consistencia y cumplimiento de instrucciones
- Evaluación humana con rúbrica
- Seguridad (p. ej. inyección de prompt)
- Equidad y casos límite
- Evaluaciones de dominio

Detalle: [metricas.md](metricas.md).

## Reglas de evidencia

Toda evaluación registrada debe poder identificar:

1. Componente evaluado y versión
2. Fecha (UTC)
3. Suite o casos utilizados
4. Modo de ejecución (`offline` | `model` | `replay` | `manual`)
5. Criterios y métricas
6. Resultado y umbrales
7. Limitaciones y alcance real
8. Si es o no insumo suficiente para revisión de promoción

## Flujo resumido

```text
Componente + suite sintética
        ↓
Harness (según harness.md)
        ↓
Métricas (según metricas.md)
        ↓
Resultado (según resultados.md)
        ↓
Revisión humana / gobernanza
        ↓
Estado del componente (prueba, aprobado, restringido, …)
```

El harness **mide**; la gobernanza **decide**.

## Relación con otros directorios

| Ruta | Relación |
|---|---|
| `prompts/` | Define criterios y ejemplos; no archiva evidencia formal |
| `experiments/` | Exploración; puede alimentar una evaluación posterior |
| `models/` | Model cards y config; evaluación antes de uso operativo |
| `agents/` | Manifiestos; pruebas antes de promoción |
| `data/` | Esquemas y muestras; sin PII real en Git |
| `DATA_GOVERNANCE.md` | Clasificación y prohibiciones de datos |
| `GOVERNANCE.md` | Aprobación y roles de revisión |

## Estado actual

| Elemento | Estado |
|---|---|
| Diseño harness / métricas / resultados | Documentado en markdown |
| `harness.py` | Pendiente de implementación alineada al contrato |
| Suites YAML en `casos-prueba/` | Pendientes (norma en `casos-prueba.md`) |
| Corridas reales en `resultados/` | Ninguna archivada (sin inventar evidencia) |
| Plantilla de resultado | Disponible en `_plantilla-resultado.json` |

## Referencias

- [docs/arquitectura/componentes.md](../docs/arquitectura/componentes.md)
- [docs/arquitectura/arquitectura-general.md](../docs/arquitectura/arquitectura-general.md)
- [GOVERNANCE.md](../GOVERNANCE.md)
- [AI_ETHICS.md](../AI_ETHICS.md)
- [DATA_GOVERNANCE.md](../DATA_GOVERNANCE.md)
- [SECURITY.md](../SECURITY.md)
