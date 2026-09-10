# Prompts

Prompts versionados de `mecanica-social-ia`.

## Inventario actual

| Archivo | Estado | Notas |
|---|---|---|
| `esquema-prompt.yaml` | plantilla | Metadatos mínimos |
| `formulario-intake-v1.0.0.yaml` | **prueba** | Riesgo medio; sin aprobación operativa |

No existe aún `resumidor-solicitudes`. No hay scripts de evaluación bajo `prompts/`.

## Convención de nombre

```text
<id>-v<MAJOR.MINOR.PATCH>.yaml
```

## Estados preferidos (español)

- `borrador`
- `prueba`
- `aprobado`
- `restringido`
- `obsoleto`
- `suspendido`
- `retirado`

Un prompt **no** pasa a `aprobado` solo por parecer plausible ni por una corrida offline.

## Evaluación

Las suites y el harness viven en `evaluations/`:

```bash
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode offline \
  --output evaluations/resultados
```

## Reglas

- Identificador y versión trazables.
- Cambios relevantes vía Issue y Pull Request.
- Sin datos personales reales, credenciales ni secretos.
- Ver `esquema-prompt.yaml` al crear uno nuevo.
