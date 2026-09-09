# Evaluations

Esta carpeta contiene los mecanismos, casos de prueba, métricas y
resultados utilizados para evaluar los componentes de
`mecanica-social-ia`.

## Propósito

Determinar de manera sistemática si prompts, modelos, agentes y otros
componentes cumplen los criterios definidos para su utilización.

## Componentes evaluables

Las evaluaciones podrán aplicarse a:

- Prompts.
- Modelos.
- Agentes.
- Flujos.
- Integraciones.
- Componentes de software.

## Tipos de evaluación

Según corresponda podrán utilizarse:

- Exactitud.
- Precisión.
- Recall.
- F1.
- Consistencia.
- Cumplimiento de instrucciones.
- Evaluación humana.
- Seguridad.
- Manejo de casos límite.
- Evaluaciones específicas del dominio.

## Estructura sugerida

```text
evaluations/
├── README.md
├── prompts/
├── models/
├── agents/
└── results/
Reglas

Las evaluaciones deben identificar:

Componente evaluado.
Versión.
Fecha.
Casos utilizados.
Criterios.
Métricas.
Resultado.
Umbral de aprobación.
Principio

Un componente no debe considerarse aprobado únicamente porque
funciona en un caso individual.

Debe existir evidencia suficiente y reproducible para respaldar
su comportamiento esperado.

---
