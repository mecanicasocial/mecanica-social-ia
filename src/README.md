# Source Code

Esta carpeta contiene el código fuente compartido de
`mecanica-social-ia`.

## Propósito

Centralizar las implementaciones de software necesarias para ejecutar,
integrar y evaluar los componentes del proyecto.

## Contenido

Podrá incluir:

- Librerías internas.
- Clientes de servicios de IA.
- Utilidades.
- Procesadores.
- Integraciones.
- Lógica común.
- Interfaces internas.

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

Los cambios relevantes deberán pasar por:

```text
Issue
↓
Branch
↓
Commit
↓
Pull Request
↓
Review
↓
Merge

Principio

El código fuente debe ser mantenible, reutilizable, trazable y
suficientemente documentado para permitir su evolución.

---

# Así quedará el repositorio

Después de crear estos archivos, la **estructura física inicial** será:

```text
mecanica-social-ia/
│
├── docs/
│   └── arquitectura/
│       ├── README.md
│       ├── arquitectura-general.md
│       ├── componentes.md
│       ├── integraciones.md
│       ├── gobernanza.md
│       └── adr/
│
├── prompts/
│   └── README.md
│
├── models/
│   └── README.md
│
├── agents/
│   └── README.md
│
├── experiments/
│   └── README.md
│
├── evaluations/
│   └── README.md
│
├── infra/
│   └── README.md
│
├── data/
│   └── README.md
│
├── examples/
│   └── README.md
│
└── src/
    └── README.md
