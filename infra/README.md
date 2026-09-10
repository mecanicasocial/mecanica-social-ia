# Infrastructure

Esta carpeta contiene los elementos relacionados con la infraestructura
necesaria para ejecutar y desplegar los componentes de
`mecanica-social-ia`.

## Propósito

Organizar configuraciones y recursos necesarios para los entornos
de desarrollo, prueba y producción.

## Contenido

| Artefacto | Rol |
|---|---|
| `README.md` | Este índice |
| `secretos-y-entorno.md` | Convención de variables de entorno y secretos (ADR-002) |

Podrá incluir además:

- Configuración de despliegue.
- Scripts de infraestructura.
- Contenedores.
- Automatizaciones de entorno.

## Entornos

Cuando corresponda se distinguirán:

- Development.
- Testing.
- Production.

## Seguridad

Nunca almacenar directamente:

- Contraseñas.
- API keys.
- Tokens.
- Credenciales.
- Secretos.

Los secretos deberán administrarse mediante mecanismos seguros
de gestión de configuración. Detalle operativo:

→ [`secretos-y-entorno.md`](secretos-y-entorno.md)

## CI actual

El smoke-test offline vive en `.github/workflows/eval-offline.yml`
(sin secretos). El job de inferencia con modelo es pendiente intencional
(PEND-004): ver `docs/arquitectura/pendientes-intencionales.md`.

## Principio

La infraestructura debe ser reproducible, documentada y separada
de las credenciales y secretos de operación.
