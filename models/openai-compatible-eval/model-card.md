# Model card — `openai-compatible-eval`

## Estado

`propuesto` / **solo evaluación sintética**.  
**No** es el proveedor productivo autorizado de Mecánica Social.  
Cualquier uso con datos personales reales o en procesos operativos requiere
autorización institucional explícita (registro en `docs/gobernanza/registros/`)
y actualización de INT-002.

## Identificación

| Campo | Valor |
|---|---|
| id (repo) | `openai-compatible-eval` |
| Proveedor | Compatible con API estilo OpenAI (vendor concreto: **por autorizar**) |
| model_id (vendor) | Via `MS_IA_MODEL_ID` / config local — no fijado en Git hasta autorización |
| Interfaz | HTTP `chat/completions` (`src/ms_ia/model_client.py`) |
| Responsable técnico | `@LeodanZapata` (provisional; ver roles de revisión) |
| Fecha | 2026-09-10 |
| ADR | ADR-002 |

## Propósito y capacidades

- **Propósito:** permitir corridas del harness en modo `model` sobre suites
  sintéticas (`evaluations/casos-prueba/`) para medir extracción estructurada
  y regresiones, sin versionar secretos.
- **Capacidades esperadas:** completar chat; devolver texto/JSON según prompt.
- **Fuera de alcance:** decisiones sobre personas, datos de menores, producción
  educativa, automatización sin supervisión humana.

## Datos

- **Entrenamiento del vendor:** desconocido hasta elegir proveedor concreto;
  documentar en esta card al autorizar.
- **Retención de prompts:** asumir que el vendor **puede** retener o inspeccionar
  tráfico salvo contrato contrario; por eso solo sintéticos.
- **Training con datos MS:** prohibido enviar datos reales hasta política y
  contrato con el vendor.
- **Inferencia permitida hoy:** únicamente textos sintéticos de evaluación.
- **Prohibido:** PII real, salud, datos de vulnerabilidad, credenciales,
  identificadores oficiales.

## Limitaciones conocidas

- El `model_id` y el endpoint no están fijados institucionalmente.
- La calidad depende del vendor/modelo elegido en el entorno.
- No hay garantía de determinismo entre versiones del vendor.
- El harness en modo model **no** otorga `aprobado` operativo.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Uso productivo prematuro | `estado: propuesto`; docs y PRACTICO lo declaran |
| Filtración de API key | Solo env (`MS_IA_MODEL_API_KEY`); ver `infra/secretos-y-entorno.md` |
| Envío de PII | Suites sintéticas; `datos_prohibidos_en_inferencia` en config |
| Invención de campos | Métrica `no_invencion` + revisión humana |
| Vendor no evaluado | Bloqueo de autorización hasta card + INT-002 + registro |

## Licencia, costo y cuotas

- Dependen del vendor finalmente autorizado (por definir).
- No hay compromiso de presupuesto en este slot.

## Evaluación

- Suite canónica prevista: `evaluations/casos-prueba/intake-test-set.yaml`
- Componente: `prompts/formulario-intake-v1.0.0.yaml`
- Resultados: `evaluations/resultados/*-model.json` cuando existan corridas
- Interpretación: umbrales = insumo; decisión = gobernanza

## Autorización institucional

- [x] Model-card inicial (este documento)
- [ ] Vendor y `model_id` concretos elegidos
- [ ] Revisión de datos/privacidad del vendor
- [ ] Revisión de seguridad / DPA si aplica
- [ ] Registro de decisión de autorización
- [ ] INT-002 actualizado a estado validado/operativo

Hasta completar los ítems pendientes, este modelo **no** se considera
proveedor autorizado para uso operativo.
