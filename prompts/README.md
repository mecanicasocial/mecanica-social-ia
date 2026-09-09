# Prompts

Esta carpeta contiene los prompts versionados utilizados por
`mecanica-social-ia`.

prompts/
├── README.md                          ← Guía de uso
├── esquema-prompt.yaml                ← Template comentado
├── formulario-intake-v1.0.0.yaml      ← Ejemplo real, aprobado
├── resumidor-solicitudes-v0.1.0.yaml  ← Ejemplo en desarrollo
└── .evaluations/
    └── test-casos-intake.yaml         ← Casos de prueba

## Propósito

Mantener los prompts como artefactos versionables, trazables,
revisables y evaluables.

## Contenido

Aquí se almacenarán:

- Prompts en desarrollo.
- Prompts en evaluación.
- Prompts aprobados.
- Versiones históricas de prompts.
- Esquemas y convenciones para su definición.

## Versionado

Los prompts utilizarán versionado semántico:

`MAJOR.MINOR.PATCH`

Ejemplo:

`formulario-intake-v1.0.0.yaml`

## Estados

Los prompts podrán utilizar los siguientes estados:

- `draft`
- `testing`
- `approved`
- `deprecated`
- `archived`

## Reglas

- Cada prompt debe tener un identificador único.
- Cada versión debe ser trazable.
- Los cambios relevantes deben realizarse mediante Issue y Pull Request.
- Los prompts aprobados deben contar con evaluaciones.
- No incorporar datos personales, credenciales, tokens o información sensible.

## Evaluación

Las pruebas de los prompts se gestionarán en:

`evaluations/`

## Relación con otros componentes

Los prompts pueden ser utilizados por:

- `agents/`
- `experiments/`
- `evaluations/`
- `src/`

## Principio

Un prompt es un componente versionable del sistema y debe tratarse con
el mismo nivel de trazabilidad que el código.
