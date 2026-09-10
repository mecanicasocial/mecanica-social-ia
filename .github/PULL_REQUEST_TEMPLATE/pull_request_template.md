## Resumen

<!-- Qué cambia y por qué -->

## Issue relacionada

Closes #

## Tipo de cambio

- [ ] Documentación / gobernanza
- [ ] Prompt
- [ ] Evaluación (suite, harness, resultado)
- [ ] Modelo / agente
- [ ] Código (`src/`, `infra/`)
- [ ] CI / plantillas
- [ ] Integración (INT-*)

## Riesgo del componente afectado

- [ ] N/A (docs menores)
- [ ] Bajo
- [ ] Medio
- [ ] Alto

## Checklist de gobernanza

- [ ] Propósito institucional claro
- [ ] Sin secretos, credenciales ni PII real
- [ ] Datos clasificados y minimizados
- [ ] Limitaciones documentadas
- [ ] Supervisión humana descrita si aplica
- [ ] Evaluación: suite y/o corrida según el cambio
- [ ] El modo offline **no** se presenta como aprobación operativa
- [ ] El score de modo `model` **no** se presenta como aprobación operativa
- [ ] README / docs alineados con lo que **existe** (sin inventarios fantasma)

## Revisiones por rol

Ver `docs/arquitectura/roles-revision.md` y `GOVERNANCE.md`.  
Si la misma persona ocupa varios roles, declarar **excepción de rol dual**
y, en riesgo alto, segundo participante en el registro de decisión.

- [ ] Técnica — revisor: @
- [ ] Metodológica (medio+) — revisor: @
- [ ] Ética (medio+/alto o impacto en personas) — revisor: @
- [ ] Datos / privacidad (PII o vendor) — revisor: @
- [ ] Seguridad (secretos, CI, INT-*) — revisor: @
- [ ] Área usuaria / aprobación institucional (si aplica) — @
- [ ] Registro en `docs/gobernanza/registros/` si la decisión es sensible

## Evidencia de evaluación (si aplica)

- Componente y versión:
- Suite:
- Resultado (`evaluations/resultados/...`):
- Modo harness: offline / model
- `model_ref` (si model):
- `apto_para_aprobacion_operativa`:

## Cómo probar

```bash
# Offline (sin secretos)
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode offline \
  --output evaluations/resultados

# Model (requiere env; ver infra/secretos-y-entorno.md)
# export MS_IA_MODEL_API_KEY=…
# export MS_IA_MODEL_BASE_URL=…
# export MS_IA_MODEL_ID=…
# python evaluations/harness.py \
#   --component prompts/formulario-intake-v1.0.0.yaml \
#   --suite evaluations/casos-prueba/intake-test-set.yaml \
#   --mode model \
#   --model-ref models/openai-compatible-eval \
#   --output evaluations/resultados
```
