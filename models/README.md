# Models

Esta carpeta contiene la configuración, documentación y referencias
de los modelos de inteligencia artificial utilizados por
`mecanica-social-ia`.

## Propósito

Mantener trazabilidad sobre los modelos utilizados, sus versiones,
proveedores, capacidades, restricciones y condiciones de uso.

## Contenido

Aquí podrán almacenarse:

- Configuraciones de modelos.
- Referencias a proveedores.
- Versiones utilizadas.
- Model cards.
- Parámetros relevantes.
- Restricciones y limitaciones conocidas.
- Información sobre licencias.

## Importante

Los pesos de modelos no deben almacenarse directamente en este
repositorio salvo que exista una decisión técnica y de licenciamiento
que lo justifique.

Las credenciales, API keys, tokens y secretos nunca deben almacenarse
en esta carpeta.

## Evaluación

Todo modelo destinado a un uso relevante deberá contar con evidencia
de evaluación antes de ser incorporado a procesos productivos.

Las evaluaciones se gestionarán en:

`evaluations/`

## Relación con otros componentes

Los modelos pueden ser utilizados por:

- `agents/`
- `experiments/`
- `evaluations/`
- `src/`

## Principio

La configuración de un modelo debe permitir identificar qué modelo,
qué versión y qué parámetros fueron utilizados en una ejecución.
