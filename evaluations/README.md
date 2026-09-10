# Evaluations

Marco de evaluación de `mecanica-social-ia`: diseño, suites sintéticas, harness y resultados.

## Principio

Un componente **no** se aprueba solo porque una respuesta parezca plausible.
El harness **mide**; la gobernanza **decide**.

## Inventario actual (P1 — MVP ejecutable offline)

| Elemento | Estado |
|---|---|
| `harness.md`, `metricas.md`, `resultados.md`, `casos-prueba.md` | Documentados |
| `harness.py` | **MVP offline implementado** |
| `casos-prueba/intake-test-set.yaml` | Suite sintética v0.1.0 (6 casos) |
| `resultados/` | Corridas offline reales |
| `_plantilla-resultado.json` | Plantilla (no es evidencia) |
| CI smoke offline | `.github/workflows/eval-offline.yml` |
| Modo `model` / `replay` | Pendiente (PEND-004 para job model) |
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
Harness offline (estructural)
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
| `PRACTICO.md` | Guía rápida del MVP |
| `DATA_GOVERNANCE.md` / `GOVERNANCE.md` | Datos y decisión institucional |

## Referencias

- `docs/arquitectura/ADR/ADR-001-arquitectura-inicial-y-mvp-evaluacion.md`
- `PRACTICO.md`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `SECURITY.md`
