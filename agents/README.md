# Agents

Esta carpeta contiene los agentes de inteligencia artificial
desarrollados para `mecanica-social-ia`.

## Propósito

Organizar agentes que integren instrucciones, modelos, herramientas,
reglas y flujos de trabajo para resolver tareas específicas.

## Contenido

Cada agente podrá contener:

- Manifiesto del agente.
- Configuración.
- Instrucciones.
- Herramientas requeridas.
- Entradas y salidas.
- Permisos.
- Dependencias.
- Documentación específica.

## Estructura sugerida

```text
agents/
└── nombre-del-agente/
    ├── README.md
    └── agent.yaml
Manifiesto

Cada agente deberá declarar, cuando corresponda:

Identificador.
Versión.
Propósito.
Entradas.
Salidas.
Modelo utilizado.
Prompts utilizados.
Herramientas.
Permisos.
Dependencias.
Seguridad

Los agentes deberán operar bajo el principio de mínimo privilegio.

No deberán incorporar directamente:

Contraseñas.
API keys.
Tokens.
Credenciales.
Datos sensibles innecesarios.
Evaluación

Los agentes deberán contar con pruebas apropiadas antes de considerarse
aptos para uso productivo.

Relación con otros componentes

Los agentes pueden utilizar:

prompts/
models/
data/
src/

y pueden ser evaluados mediante:

evaluations/

---
