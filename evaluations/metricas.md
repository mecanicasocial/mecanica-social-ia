# Métricas de evaluación

## 1. Propósito

Este catálogo define **métricas reutilizables** para evaluar componentes de `mecanica-social-ia`. Orienta qué medir, cómo interpretarlo y qué umbrales son solo **orientativos**, no aprobaciones automáticas.

Las métricas deben elegirse según el **propósito del componente**, el **nivel de riesgo** y el tipo de salida (texto libre, JSON, clasificación, ranking, etc.).

## 2. Principios de medición

1. **Adecuación al objetivo.** Medir lo que el componente promete (p. ej. extracción de campos), no una métrica genérica por costumbre.
2. **Umbral ≠ aprobación institucional.** Cumplir un porcentaje no reemplaza revisión humana ni controles de datos/ética.
3. **Separar calidad, seguridad y equidad.** Un buen score de exactitud no implica ausencia de sesgo o de fuga de datos.
4. **Declarar el método.** Automático, humano o mixto; con o sin modelo.
5. **Datos de prueba legítimos.** Preferir sintéticos; ver `DATA_GOVERNANCE.md`.
6. **Reportar cobertura.** Número de casos, etiquetas (feliz, edge, adversario) y limitaciones.
7. **No optimizar una sola métrica** si degrada seguridad, veracidad o equidad.

## 3. Metadatos mínimos de una métrica en un run

Cada métrica reportada debería indicar:

| Campo | Descripción |
|---|---|
| `id` | Identificador estable (`exactitud_extraccion`, `json_valido`, …) |
| `nombre` | Nombre legible |
| `valor` | Número o etiqueta de resultado |
| `unidad` | `ratio`, `porcentaje`, `conteo`, `booleano`, `escala_1_5`, etc. |
| `umbral` | Objetivo declarado (si existe) |
| `umbral_cumplido` | `true` / `false` / `no_aplicable` |
| `metodo` | Cómo se calculó |
| `n_casos` | Casos incluidos |
| `limitaciones` | Lo que la métrica no cubre |

## 4. Catálogo de métricas

### 4.1 Estructurales y de formato

| ID | Qué mide | Cuándo usarla | Cálculo orientativo | Umbral orientativo |
|---|---|---|---|---|
| `esquema_componente_valido` | Metadatos mínimos del YAML/manifiesto | Siempre en CI offline | Pass/fail por campos requeridos | 100% pass |
| `json_valido` | Salida parseable como JSON | Extracción estructurada | Casos con JSON válido / total | 100% |
| `campos_requeridos_presentes` | Claves obligatorias en la salida | JSON con schema | Casos completos / total | ≥ 95–100% según riesgo |
| `formato_salida` | Cumple plantilla (markdown, lista, etc.) | Contenidos con formato fijo | Reglas o evaluador | Según componente |

### 4.2 Exactitud y utilidad de tarea

| ID | Qué mide | Cuándo usarla | Cálculo orientativo | Umbral orientativo |
|---|---|---|---|---|
| `exactitud_extraccion` | Coincidencia de campos con *ground truth* | Prompts de parsing/intake | Campos correctos / campos esperados (macro o micro) | ≥ 95% solo con evaluación **con modelo** y casos suficientes |
| `exactitud_caso` | Caso completo correcto (todo o nada) | Tareas estrictas | Casos exactos / total | Según criticidad |
| `precision` | Acierto entre lo predicho positivo | Clasificación | TP / (TP+FP) | Definir por clase |
| `recall` | Cobertura de lo relevante | Clasificación / detección | TP / (TP+FN) | Definir por clase |
| `f1` | Balance precision/recall | Clasificación | Media armónica | Definir por clase |
| `coherencia_estructura` | Estructura consistente entre corridas o vs schema | Salidas estructuradas | Validación schema + reglas | 100% schema |
| `cumplimiento_instrucciones` | Respeta prohibiciones y pasos del prompt | Cualquier prompt | Checklist automático o humano | Alto; fallar si viola “NUNCA” críticos |
| `no_invencion` | No inventa datos no presentes en el input | Extracción, resúmenes factuales | Comparación input vs salida; revisión humana muestral | 100% en campos sensibles |
| `rouge_l` / `bleu` | Solapamiento n-gramas con referencia | Solo textos con referencia estable | Librerías estándar | **No** usar como métrica primaria en extracción JSON ni en contenidos institucionales sin referencia fija |

### 4.3 Robustez y casos límite

| ID | Qué mide | Cuándo usarla | Notas |
|---|---|---|---|
| `tasa_exito_edge` | Éxito en casos límite | Inputs incompletos, ruido, idiomas mixtos | Reportar separado del set “feliz” |
| `manejo_campos_faltantes` | Usa marcadores acordados (`NO_PROPORCIONADO`) | Intake / formularios | Debe coincidir con el contrato del prompt |
| `estabilidad` | Misma entrada → misma clase de salida | Con temperatura > 0 acotar | Varias semillas; no exigir bit-idéntico si el proveedor no lo garantiza |
| `regresion` | No empeora vs baseline versionado | Al subir MINOR/MAJOR | Comparar con resultado anterior archivado |

### 4.4 Seguridad y abuso

| ID | Qué mide | Cuándo usarla | Notas |
|---|---|---|---|
| `resistencia_prompt_injection` | No sigue instrucciones hostiles del input | Componentes expuestos a texto de terceros | Suite adversaria sintética |
| `no_filtracion_secretos` | No reproduce secretos de contexto | Si el contexto pudiera contenerlos | Nunca usar secretos reales en pruebas |
| `no_pii_en_logs_resultado` | El artefacto de resultado no guarda PII | Todos los runs versionados | Revisión automática de patrones + política |
| `uso_datos_prohibidos` | Respeta lista `datos_prohibidos` del componente | Componentes con PII potencial | Pass/fail de política |

### 4.5 Equidad e impacto

| ID | Qué mide | Cuándo usarla | Notas |
|---|---|---|---|
| `paridad_error_por_grupo` | Diferencias de error entre grupos de análisis | Riesgo medio/alto con impacto en personas | Grupos sintéticos o autorizados; no crear perfiles indebidos |
| `lenguaje_estereotipado` | Marcadores de estereotipo en salidas | Comunicación, evaluación formativa | Apoyo humano obligatorio |
| `cobertura_territorial_idioma` | Desempeño por variante de lenguaje/territorio | Contexto Chile / multiterritorial | Declarar limitaciones si no se midió |

Estas métricas **no autorizan** perfiles políticos ni evaluación de dignidad de personas (`AI_ETHICS.md`).

### 4.6 Evaluación humana

| ID | Qué mide | Escala sugerida | Cuándo |
|---|---|---|---|
| `juicio_utilidad` | Utilidad para la tarea institucional | 1–5 | Muestra de casos |
| `juicio_veracidad` | Exactitud factual percibida | 1–5 o pass/fail | Contenidos públicos |
| `juicio_tono_respetuoso` | Alineación con dignidad y claridad | 1–5 | Comunicación |
| `supervision_muestral` | % de salidas revisadas por humano en operación | % | Post-despliegue; no es métrica de harness pre-merge solamente |

La evaluación humana debe registrar revisor (rol), fecha, guía de rubrica y desacuerdos relevantes, **sin** pegar datos personales en el repo.

## 5. Métricas ligadas al ejemplo `formulario-intake`

El prompt documenta:

| Métrica declarada | Interpretación en este catálogo | Condición para tomarla en serio |
|---|---|---|
| `exactitud_extraccion` ≥ 95% | § 4.2 con *ground truth* por campo | Requiere modo **modelo** o fixtures de salida real + casos suficientes |
| `coherencia_estructura` 100% | `json_valido` + `campos_requeridos_presentes` | Puede medirse sobre salidas del modelo o sobre `expected` de la suite (esto último solo valida la suite, no el modelo) |

**Advertencia metodológica:** validar únicamente que el campo `expected` del YAML sea JSON válido **no** mide el comportamiento del modelo. Ese procedimiento solo audita la calidad de la suite o del ejemplo.

## 6. Umbrales y riesgo

| Riesgo del componente | Expectativa de medición |
|---|---|
| Bajo | Estructural + muestra pequeña; revisión humana antes de publicar |
| Medio | Exactitud/utilidad con suite documentada; fuentes; datos; umbrales explícitos |
| Alto | Lo anterior + seguridad + equidad + supervisión humana reforzada + autorización institucional |

Regla de coherencia (también en `DATA_GOVERNANCE.md`): un componente que trata de forma habitual datos personales identificables **no** debería gestionarse como riesgo bajo solo por tener buen score offline.

## 7. Agregación

Resumen típico de un run:

```text
n_casos
n_pasados / n_fallidos (según criterio primario)
metricas[] (lista del § 3)
tasa_exito_primaria
umbrales_global_ok: true|false
modo: offline|model|replay
```

Si hay varias métricas obligatorias, el run global es **fail** si **alguna** obligatoria no cumple umbral (salvo que el diseño del componente defina otra regla explícita).

## 8. Lo que no se reporta como métrica de éxito

- “El texto se lee bien” sin rúbrica.
- Opiniones generadas por el mismo modelo bajo evaluación sin control.
- Comparaciones con otros proveedores sin la misma suite y protocolo.
- Resultados obtenidos con datos no autorizados.

## 9. Extensión del catálogo

Para proponer una métrica nueva:

1. Asignar `id` estable en snake_case.
2. Definir propósito, método, limitaciones y tipo de componente.
3. Indicar si es automática, humana o mixta.
4. Documentar umbral solo como orientación.
5. Actualizar este archivo mediante PR y referencia en el componente que la use.

## 10. Referencias

- `evaluations/harness.md`
- `evaluations/resultados.md`
- `evaluations/README.md`
- `GOVERNANCE.md`
- `AI_ETHICS.md`
- `DATA_GOVERNANCE.md`
