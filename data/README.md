Este es especialmente importante.
# Data

Esta carpeta contiene esquemas, muestras y definiciones relacionadas
con los datos utilizados por `mecanica-social-ia`.

La política institucional de datos del sistema de IA está en
[`DATA_GOVERNANCE.md`](../DATA_GOVERNANCE.md). Esta carpeta no sustituye
esa política: materializa esquemas, muestras autorizadas y políticas
operativas coherentes con ella.

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

## Principio

Los datos utilizados por los sistemas de IA deben ser trazables,
adecuados para el propósito y tratados de acuerdo con las reglas
de seguridad y gobernanza definidas para el proyecto.

## Referencias

- [`DATA_GOVERNANCE.md`](../DATA_GOVERNANCE.md)
- [`SECURITY.md`](../SECURITY.md)
- [`AI_ETHICS.md`](../AI_ETHICS.md)
- [`GOVERNANCE.md`](../GOVERNANCE.md)
- [`docs/arquitectura/integraciones.md`](../docs/arquitectura/integraciones.md)

