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
- [ ] README / docs alineados con lo que **existe** (sin inventarios fantasma)

## Evidencia de evaluación (si aplica)

- Componente y versión:
- Suite:
- Resultado (`evaluations/resultados/...`):
- `apto_para_aprobacion_operativa`:

## Cómo probar

```bash
# Ejemplo MVP offline
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode offline \
  --output evaluations/resultados
```
