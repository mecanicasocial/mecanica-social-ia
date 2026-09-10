# Model card — `<id>`

## Estado

`propuesto` | `solo_evaluacion` | `autorizado` | `restringido` | `retirado`

## Identificación

| Campo | Valor |
|---|---|
| id (repo) | |
| Proveedor | |
| model_id (vendor) | |
| Versiones evaluadas | |
| Interfaz | openai-compatible chat/completions |
| Responsable técnico | |
| Fecha | |

## Propósito y capacidades

- Propósito institucional autorizado:
- Tareas evaluadas:
- Fuera de alcance:

## Datos

- Datos de entrenamiento (resumen del vendor / desconocido):
- ¿El vendor retiene prompts/completions? :
- ¿Se usa para entrenar el modelo del vendor? :
- Ubicación de tratamiento (si se conoce):
- Datos permitidos en inferencia (este repo):
- Datos prohibidos:

## Limitaciones conocidas

-

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Invención de datos | Suite + métrica `no_invencion`; supervisión humana |
| Fuga de PII | Solo sintéticos hasta autorización; secretos fuera de Git |
| Cambio silencioso de versión | Fijar `model_id`; re-evaluar ante cambio |

## Licencia, costo y cuotas

- Licencia de uso:
- Costo estimado:
- Límites de tasa:

## Evaluación

- Suite:
- Resultado (`evaluations/resultados/`):
- `apto_para_aprobacion_operativa` del harness: siempre insumo, no decisión

## Autorización institucional

- [ ] Model-card completa
- [ ] Revisión de datos/privacidad
- [ ] Revisión de seguridad
- [ ] Registro de decisión en `docs/gobernanza/registros/`
- [ ] INT-002 actualizado si aplica

**Sin esos checks, el modelo no se considera autorizado para uso operativo.**
