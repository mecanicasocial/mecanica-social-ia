# Infrastructure

Esta carpeta contiene los elementos relacionados con la infraestructura
necesaria para ejecutar y desplegar los componentes de
`mecanica-social-ia`.

## Propósito

Organizar configuraciones y recursos necesarios para los entornos
de desarrollo, prueba y producción.

## Contenido

Podrá incluir:

- Configuración de despliegue.
- Scripts de infraestructura.
- Configuración de servicios.
- Automatizaciones.
- Contenedores.
- Configuración de entornos.

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
de gestión de configuración.

## Principio

La infraestructura debe ser reproducible, documentada y separada
de las credenciales y secretos de operación.
