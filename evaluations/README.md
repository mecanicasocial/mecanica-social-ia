# Evaluations

Marco de evaluación de `mecanica-social-ia`: diseño, suites sintéticas, harness y resultados.

## Principio

Un componente **no** se aprueba solo porque una respuesta parezca plausible.
El harness **mide**; la gobernanza **decide**.

## Inventario actual (práctico)

| Elemento | Estado |
|---|---|
| `harness.md`, `metricas.md`, `resultados.md`, `casos-prueba.md` | Documentados |
| `harness.py` | **MVP offline implementado** |
| `casos-prueba/intake-test-set.yaml` | Suite sintética v0.1.0 (6 casos) |
| `resultados/` | Corridas offline reales |
| `_plantilla-resultado.json` | Plantilla (no es evidencia) |
| Modo `model` / `replay` | Pendiente |
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

## Estructura

```text
evaluations/
├── README.md
├── harness.md
├── harness.py
├── metricas.md
├── resultados.md
├── casos-prueba.md
├── _plantilla-resultado.json
├── casos-prueba/
│   └── intake-test-set.yaml
└── resultados/
    └── YYYY-MM-DD-<id>-v<ver>-offline.json
```

## Referencias

- `docs/arquitectura/ADR/ADR-001-arquitectura-inicial-y-mvp-evaluacion.md`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `SECURITY.md`
