# Models

Esta carpeta contiene la configuración, documentación y referencias
de los modelos de inteligencia artificial utilizados por
`mecanica-social-ia`.

## Propósito

Mantener trazabilidad sobre los modelos utilizados, sus versiones,
proveedores, capacidades, restricciones y condiciones de uso.

## Inventario real

| id | Estado | Card | Notas |
|---|---|---|---|
| `openai-compatible-eval` | `propuesto` / solo evaluación | [model-card.md](openai-compatible-eval/model-card.md) | Slot para harness modo `model`. **No** autorizado para producción ni PII real. |
| `_plantillas/` | n/a | plantillas | `config.example.yaml`, `model-card.example.md` |

No listar providers fantasma. Un modelo pasa a `autorizado` solo con
registro de gobernanza + revisiones de datos/seguridad (ver
`docs/arquitectura/roles-revision.md`).

## Estructura por modelo

```text
models/<id>/
  config.yaml      # sin secretos
  model-card.md
  README.md        # opcional
```

## Importante

Los pesos de modelos no deben almacenarse directamente en este
repositorio salvo que exista una decisión técnica y de licenciamiento
que lo justifique.

Las credenciales, API keys, tokens y secretos **nunca** deben
almacenarse en esta carpeta. Ver `infra/secretos-y-entorno.md` y ADR-002.

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
- `src/ms_ia/` (cliente de inferencia)

## Principio

La configuración de un modelo debe permitir identificar qué modelo,
qué versión y qué parámetros fueron utilizados en una ejecución.
