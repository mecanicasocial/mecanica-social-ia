# Componentes de la arquitectura

## 1. Propósito

Este documento define la responsabilidad de cada componente principal de `mecanica-social-ia` y sus límites básicos.

| Componente | Responsabilidad | Estado inicial |
|---|---|---|
| `docs/arquitectura/` | Arquitectura y documentación | Base |
| `prompts/` | Prompts versionados | Base |
| `models/` | Configuración y documentación de modelos | Base |
| `agents/` | Definición de agentes | Base |
| `experiments/` | Experimentación controlada | Base |
| `evaluations/` | Evaluación y evidencia | Base |
| `infra/` | Infraestructura y automatización | Base |
| `data/` | Esquemas, muestras y políticas | Base |
| `examples/` | Ejemplos reproducibles | Base |
| `src/` | Código fuente compartido | Base |

"Base" indica que el componente pertenece a la arquitectura; no significa que exista una implementación productiva.

## 2. `docs/arquitectura/`

Explica cómo está organizado el sistema, sus componentes, integraciones, gobernanza y decisiones.

## 3. `prompts/`

Gestiona instrucciones utilizadas por modelos o agentes.

Estructura sugerida:

```text
prompts/
├── README.md
├── esquema-prompt.yaml
├── <nombre>-v<version>.yaml
└── ...
```

Cada prompt relevante debe tener identificador y versión. No debe contener credenciales, tokens ni información personal innecesaria.

## 4. `models/`

Documenta y configura los modelos utilizados: proveedor, versión, capacidades, limitaciones, configuración no sensible y referencias.

Inventario inicial: `models/openai-compatible-eval/` (estado **propuesto**, solo evaluación; ADR-002). Plantillas en `models/_plantillas/`.

No debe contener API keys, tokens, credenciales ni secretos. Ver `infra/secretos-y-entorno.md`.

## 5. `agents/`

Define agentes que combinan instrucciones, modelos, herramientas, entradas, salidas y permisos.

```text
agents/
└── nombre-del-agente/
    ├── README.md
    └── agent.yaml
```

Debe aplicarse el principio de mínimo privilegio y existir evaluación antes de promover un agente a uso operativo.

## 6. `experiments/`

Registra experimentos controlados: objetivo, hipótesis, fecha, responsable, modelo, prompt, datos, configuración, resultados, conclusiones y limitaciones.

```text
experiments/
└── EXP-001-nombre/
    ├── README.md
    ├── config.yaml
    └── results/
```

## 7. `evaluations/`

Conserva casos de prueba, criterios, métricas y resultados para prompts, modelos, agentes, flujos, integraciones o código.

Las métricas deben ser apropiadas al objetivo; pueden incluir exactitud, precisión, recall, F1, consistencia, cumplimiento de instrucciones, evaluación humana, seguridad y casos límite.

```text
evaluations/
├── README.md
├── harness.md              # contrato de evaluations/harness.py
├── harness.py              # MVP offline (P1)
├── metricas.md
├── resultados.md
├── casos-prueba.md
├── _plantilla-resultado.json
├── casos-prueba/
│   └── intake-test-set.yaml
└── resultados/
```

Documentación normativa del marco: `evaluations/README.md`, `evaluations/harness.md`, `evaluations/metricas.md`, `evaluations/resultados.md`. Guía práctica: `PRACTICO.md`.
## 8. `infra/`

Gestiona contenedores, scripts, automatizaciones, configuración de entornos, despliegues y observabilidad cuando corresponda. Los secretos se mantienen fuera del repositorio.

## 9. `data/`

Define datos mediante esquemas, muestras y políticas.

```text
data/
├── README.md
├── schemas/
├── samples/
└── policies/
```

Prioridades: minimización, autorización, trazabilidad, protección y uso de datos sintéticos o anonimizados cuando sea posible.

## 10. `examples/`

Contiene demostraciones sencillas. Los ejemplos no deben confundirse con configuraciones productivas.

## 11. `src/`

Incluye `src/ms_ia/model_client.py` (cliente OpenAI-compatible para el harness modo `model`).

Contiene código compartido: clientes de IA, utilidades, procesadores, integraciones y lógica común. Debe mantenerse separado de secretos y datos.

## 12. Regla de separación

- explica arquitectura → `docs/`
- instrucción para modelo → `prompts/`
- configuración de modelo → `models/`
- definición de agente → `agents/`
- prueba de hipótesis → `experiments/`
- evidencia o medición → `evaluations/`
- ejecución/despliegue → `infra/`
- datos autorizados de prueba → `data/`
- demostración → `examples/`
- código → `src/`
