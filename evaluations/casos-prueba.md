# Casos de prueba

## Propósito

Definir cómo se construyen y versionan las **suites de casos** que alimentan el harness de evaluación.

## Ubicación objetivo

```text
evaluations/casos-prueba/
├── intake-test-set.yaml
└── sesgo-detection-suite.yaml
```

Norma de diseño de suites. Suite inicial disponible: `evaluations/casos-prueba/intake-test-set.yaml` (sintéticos, sin PII real).

## Campos mínimos de una suite

```yaml
id: nombre-suite
version: 0.1.0
componente_objetivo: id-del-prompt-o-agente
descripcion: |
  Texto breve del propósito de la suite.
datos_clasificacion: sintetica   # sintetica | publica | autorizada
casos:
  - id: caso-001
    descripcion: Caso feliz sintético
    input: |
      Contenido de entrada inventado...
    expected:
      campo: valor
    tags: [feliz]
```

## Reglas

1. Cumplir `DATA_GOVERNANCE.md` y `SECURITY.md`.
2. `id` de caso estable entre versiones de la suite.
3. Preferir muchos casos pequeños y etiquetados (`feliz`, `edge`, `adversario`, `equidad`) sobre un único ejemplo narrativo.
4. No copiar formularios reales de beneficiarios o estudiantes.
5. Todo cambio de cobertura o de umbral implícito se refleja en un nuevo resultado bajo el esquema de `resultados.md`.

## Relación con el prompt de ejemplo

`prompts/formulario-intake-v1.0.0.yaml` está en estado `prueba` (alcance `ejemplo-no-operativo`, riesgo `medio`). La suite canónica es `evaluations/casos-prueba/intake-test-set.yaml`. Las corridas (offline o model) se archivan en `evaluations/resultados/` y **no** bastan por sí solas para promoción operativa. La evidencia no se archiva bajo `prompts/`.

## Referencias

- [harness.md](harness.md)
- [metricas.md](metricas.md)
- [resultados.md](resultados.md)
