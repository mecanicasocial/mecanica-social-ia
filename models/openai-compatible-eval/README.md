# openai-compatible-eval

Slot de modelo para **evaluación sintética** del harness (modo `model`).

| Campo | Valor |
|---|---|
| Estado | `propuesto` — no productivo |
| Config | `config.yaml` (sin secretos) |
| Card | `model-card.md` |
| Cliente | `src/ms_ia/model_client.py` |

## Uso

```bash
export MS_IA_MODEL_API_KEY="…"          # nunca en Git
export MS_IA_MODEL_BASE_URL="https://…" # endpoint chat/completions
export MS_IA_MODEL_ID="…"               # id del modelo en el vendor

python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode model \
  --model-ref models/openai-compatible-eval \
  --output evaluations/resultados
```

Ver `infra/secretos-y-entorno.md` y ADR-002.
