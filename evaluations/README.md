# Evaluations

Marco de evaluación de `mecanica-social-ia`: diseño, suites sintéticas, harness y resultados.

## Principio

Un componente **no** se aprueba solo porque una respuesta parezca plausible.
El harness **mide**; la gobernanza **decide**.

## Inventario actual (práctico)

| Elemento | Estado |
|---|---|
| `harness.md`, `metricas.md`, `resultados.md`, `casos-prueba.md` | Documentados |
| `harness.py` | Offline + **model** (secretos por env) |
| `config.example.yaml` | Ejemplo no sensible |
| `casos-prueba/intake-test-set.yaml` | Suite sintética v0.1.0 |
| `resultados/` | Corridas archivadas |
| `_plantilla-resultado.json` | Plantilla (no es evidencia) |
| CI smoke offline | `.github/workflows/eval-offline.yml` |
| Modo `replay` | Pendiente |
| Suites de sesgo / 100+ casos | No existen aún |

## Cómo ejecutar (offline)

```bash
pip install -r requirements.txt
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode offline \
  --output evaluations/resultados
```

El modo offline valida estructura del componente y de la suite.
Siempre deja `apto_para_aprobacion_operativa: false`.

## Cómo ejecutar (model)

Requiere variables de entorno (nunca en Git). Ver `infra/secretos-y-entorno.md`.

```bash
export MS_IA_MODEL_API_KEY=…
export MS_IA_MODEL_BASE_URL=…
export MS_IA_MODEL_ID=…
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode model \
  --model-ref models/openai-compatible-eval \
  --output evaluations/resultados
```

Métricas adicionales sobre salidas del modelo: `json_valido`,
`campos_requeridos_presentes`, `exactitud_extraccion`, `no_invencion`.
Tampoco aprueba uso operativo.

## Estructura

```text
evaluations/
├── README.md
├── harness.md
├── harness.py
├── config.example.yaml
├── metricas.md
├── resultados.md
├── casos-prueba.md
├── _plantilla-resultado.json
├── casos-prueba/
│   └── intake-test-set.yaml
└── resultados/
    └── YYYY-MM-DD-<id>-v<ver>-{offline|model}.json
```

## Documentos de diseño

| Documento | Contenido |
|---|---|
| [harness.md](harness.md) | Contrato de diseño (modos, entradas, límites) |
| [metricas.md](metricas.md) | Catálogo de métricas y umbrales orientativos |
| [resultados.md](resultados.md) | Esquema y gobernanza de resultados |
| [casos-prueba.md](casos-prueba.md) | Norma para suites sintéticas |
| [_plantilla-resultado.json](_plantilla-resultado.json) | Plantilla de esquema (no es corrida real) |

## Flujo resumido

```text
Componente + suite sintética
        ↓
Harness (offline o model)
        ↓
Resultado en evaluations/resultados/
        ↓
Revisión humana / gobernanza
        ↓
Estado del componente (prueba, aprobado, …)
```

## Relación con otros directorios

| Ruta | Relación |
|---|---|
| `prompts/` | Metadatos y ejemplos; no archiva evidencia formal |
| `experiments/` | Exploración; no sustituye evaluación formal |
| `models/` | Slot de evaluación y model-cards |
| `PRACTICO.md` | Guía rápida del MVP |
| `DATA_GOVERNANCE.md` / `GOVERNANCE.md` | Datos y decisión institucional |

## Referencias

- `docs/arquitectura/ADR/ADR-001-arquitectura-inicial-y-mvp-evaluacion.md`
- `docs/arquitectura/ADR/ADR-002-modo-model-secretos-y-proveedor.md`
- `models/openai-compatible-eval/model-card.md`
- `infra/secretos-y-entorno.md`
- `PRACTICO.md`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `SECURITY.md`
