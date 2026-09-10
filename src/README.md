# Source Code

Esta carpeta contiene el código fuente compartido de
`mecanica-social-ia`.

## Propósito

Centralizar las implementaciones de software necesarias para ejecutar,
integrar y evaluar los componentes del proyecto.

## Inventario real

```text
src/
├── README.md
└── ms_ia/
    ├── __init__.py
    └── model_client.py   # cliente OpenAI-compatible (secretos por env)
```

## Principios

El código debe:

- Mantener una estructura clara.
- Ser documentado cuando sea necesario.
- Contar con pruebas apropiadas.
- Evitar credenciales y secretos.
- Mantener separación entre configuración y código.
- Ser versionado mediante Git.

## Relación con otros componentes

El código puede interactuar con:

- `prompts/`
- `models/`
- `agents/`
- `data/`
- `evaluations/`
- `infra/`

## Calidad

Los cambios relevantes deberán pasar por Issue → Branch → PR → Review → Merge,
con roles según `docs/arquitectura/roles-revision.md`.

## Principio

El código fuente debe ser mantenible, reutilizable, trazable y
suficientemente documentado para permitir su evolución.
