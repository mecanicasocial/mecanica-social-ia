Este es especialmente importante.
# Data

Esta carpeta contiene esquemas, muestras y definiciones relacionadas
con los datos utilizados por `mecanica-social-ia`.

## Propósito

Definir cómo se estructuran, documentan y utilizan los datos dentro
del proyecto.

## Estructura sugerida

```text
data/
├── README.md
├── schemas/
├── samples/
└── policies/
Restricción fundamental

No almacenar directamente en este repositorio:

Datos personales.
Información confidencial.
Información sensible.
Credenciales.
Bases de datos reales.
Información cuya publicación no esté autorizada.
Samples

Las muestras utilizadas para desarrollo y pruebas deberán ser,
preferentemente:

Sintéticas.
Anonimizadas.
Públicamente disponibles.
Expresamente autorizadas.
Schemas

Los esquemas deberán permitir describir la estructura esperada
de los datos utilizados por los componentes del sistema.

Policies

Las políticas deberán documentar las condiciones de acceso,
utilización y tratamiento de los datos.

Principio

Los datos utilizados por los sistemas de IA deben ser trazables,
adecuados para el propósito y tratados de acuerdo con las reglas
de seguridad y gobernanza definidas para el proyecto.


---

# 8. `examples/README.md`

```markdown
# Examples

Esta carpeta contiene ejemplos simples destinados a demostrar el
funcionamiento y utilización de los componentes de
`mecanica-social-ia`.

## Propósito

Facilitar la comprensión del sistema mediante ejemplos pequeños,
claros y reproducibles.

## Contenido

Podrá incluir:

- Ejemplos de utilización de prompts.
- Ejemplos de agentes.
- Ejemplos de configuración.
- Ejemplos de integración.
- Casos de uso demostrativos.

## Reglas

Los ejemplos deben:

- Ser simples.
- Ser reproducibles.
- Estar documentados.
- Evitar datos personales o sensibles.
- No contener credenciales reales.
- Indicar las dependencias necesarias.

## Importante

Los ejemplos no necesariamente representan configuraciones
productivas.

Cuando corresponda, deberán indicar expresamente sus limitaciones.

## Relación con otros componentes

Los ejemplos podrán utilizar elementos de:

- `prompts/`
- `models/`
- `agents/`
- `src/`

