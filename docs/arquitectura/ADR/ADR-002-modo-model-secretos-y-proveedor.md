# ADR-002 — Modo `model` del harness, secretos fuera de Git y proveedor de evaluación

## Estado

Aceptado

## Fecha

2026-09-10

## Contexto

El MVP (ADR-001) solo valida estructura en modo `offline`. Las métricas de
exactitud del prompt `formulario-intake` requieren salidas reales de un modelo.
A la vez, `SECURITY.md`, `DATA_GOVERNANCE.md` e `infra/` prohíben versionar
API keys, tokens o credenciales.

Hace falta:

1. Un modo `model` del harness reproducible.
2. Una convención de secretos **solo** por entorno / gestor institucional.
3. Un slot de model-card versionado **sin** declarar proveedor productivo
   autorizado hasta decisión institucional expresa.

## Decisión

1. Extender `evaluations/harness.py` con modo `model` además de `offline`.
2. Las credenciales se leen **exclusivamente** de variables de entorno
   (p. ej. `MS_IA_MODEL_API_KEY`). Nunca de YAML, JSON ni archivos en Git.
3. La configuración no sensible vive en:
   - `evaluations/config.example.yaml` (ejemplo versionado);
   - `models/<id>/config.yaml` (parámetros públicos del modelo).
4. El cliente de inferencia vive en `src/ms_ia/` (interfaz + adaptador
   HTTP compatible con API estilo OpenAI chat/completions).
5. El primer slot documentado es
   `models/openai-compatible-eval/` con estado **`propuesto`** /
   solo evaluación. **No** está autorizado para uso operativo ni para
   datos personales reales.
6. Toda corrida `model` declara `apto_para_aprobacion_operativa: false`
   hasta revisión de gobernanza. Cumplir umbrales no aprueba el componente.
7. CI pública (PRs/forks) no ejecuta modo `model` ni inyecta secretos.
   Un job opcional queda documentado como pendiente / `workflow_dispatch`
   solo con secretos de organización.
8. Autorizar un proveedor **productivo** requiere: model-card completa,
   actualización de INT-002, revisión de datos/seguridad y decisión en
   registro de gobernanza (no solo merge de código).

## Alternativas consideradas

- Embebir API keys en `config.yaml` local ignorado por git: frágil y fácil
  de filtrar; se rechaza.
- Esperar proveedor productivo antes de cualquier modo model: retrasa la
  medición de exactitud sobre suites sintéticas.
- SDK propietario obligatorio: acopla el repo a un vendor; se prefiere
  HTTP OpenAI-compatible con stdlib.

## Consecuencias

- Se puede medir `exactitud_extraccion`, `json_valido`,
  `campos_requeridos_presentes` y `no_invencion` sobre salidas de modelo
  con datos sintéticos, sin secretos en Git.
- Queda explícito que el slot actual **no** es proveedor institucional
  autorizado para producción.
- Aumenta superficie de código (`src/ms_ia`, harness).
- Quien ejecute modo model debe configurar entorno local o secretos de org.

## Implicancias

- Actualizar `evaluations/harness.md`, `PRACTICO.md`, `models/README.md`,
  `infra/README.md` y workflows README.
- Completar INT-002 cuando exista proveedor productivo autorizado.
- No enviar PII real al endpoint de evaluación.

## Referencias

- `evaluations/harness.md`
- `evaluations/harness.py`
- `models/openai-compatible-eval/`
- `infra/secretos-y-entorno.md`
- `SECURITY.md`
- `DATA_GOVERNANCE.md`
- ADR-001
