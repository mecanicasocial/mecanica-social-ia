# Experiments

Esta carpeta contiene experimentos controlados relacionados con
modelos, prompts, agentes y componentes de `mecanica-social-ia`.

## Propósito

Permitir investigar, probar y comparar alternativas de manera
reproducible y trazable.

## Cada experimento debería registrar

- Objetivo.
- Hipótesis o pregunta.
- Fecha.
- Autor.
- Modelo utilizado.
- Versión del prompt.
- Datos utilizados.
- Configuración.
- Resultados.
- Conclusiones.
- Limitaciones.

## Estructura sugerida

```text
experiments/
└── nombre-experimento/
    ├── README.md
    ├── run.sh
    ├── config.yaml
    └── results/
Datos

No almacenar datos personales, confidenciales o sensibles.

Para experimentación se deberán utilizar preferentemente datos
sintéticos, anonimizados o expresamente autorizados.

Reproducibilidad

Siempre que sea técnicamente posible, un experimento debe poder
repetirse utilizando la misma configuración y versiones.

Relación con otros componentes

Los experimentos pueden utilizar:

prompts/
models/
agents/
data/

Los resultados relevantes pueden alimentar:

evaluations/

Principio

Un experimento debe permitir comprender qué se probó, cómo se probó
y qué resultado se obtuvo.

---
