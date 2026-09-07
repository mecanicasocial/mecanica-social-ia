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

# 4. `experiments/README.md`

```markdown
# Experiments

Esta carpeta contiene experimentos controlados relacionados con
modelos, prompts, agentes y componentes de `mecanica-social-ia`.

## Propósito

Permitir investigar, probar y comparar alternativas de manera
reproducible y trazable.

## Cada experimento debería registrar

- Objetivo.
- Hipótesis o pregunta.
- Fecha.
- Autor.
- Modelo utilizado.
- Versión del prompt.
- Datos utilizados.
- Configuración.
- Resultados.
- Conclusiones.
- Limitaciones.

## Estructura sugerida

```text
experiments/
└── nombre-experimento/
    ├── README.md
    ├── run.sh
    ├── config.yaml
    └── results/
Datos

No almacenar datos personales, confidenciales o sensibles.

Para experimentación se deberán utilizar preferentemente datos
sintéticos, anonimizados o expresamente autorizados.

Reproducibilidad

Siempre que sea técnicamente posible, un experimento debe poder
repetirse utilizando la misma configuración y versiones.

Relación con otros componentes

Los experimentos pueden utilizar:

prompts/
models/
agents/
data/

Los resultados relevantes pueden alimentar:

evaluations/

Principio

Un experimento debe permitir comprender qué se probó, cómo se probó
y qué resultado se obtuvo.

---

# 5. `evaluations/README.md`

```markdown
# Evaluations

Esta carpeta contiene los mecanismos, casos de prueba, métricas y
resultados utilizados para evaluar los componentes de
`mecanica-social-ia`.

## Propósito

Determinar de manera sistemática si prompts, modelos, agentes y otros
componentes cumplen los criterios definidos para su utilización.

## Componentes evaluables

Las evaluaciones podrán aplicarse a:

- Prompts.
- Modelos.
- Agentes.
- Flujos.
- Integraciones.
- Componentes de software.

## Tipos de evaluación

Según corresponda podrán utilizarse:

- Exactitud.
- Precisión.
- Recall.
- F1.
- Consistencia.
- Cumplimiento de instrucciones.
- Evaluación humana.
- Seguridad.
- Manejo de casos límite.
- Evaluaciones específicas del dominio.

## Estructura sugerida

```text
evaluations/
├── README.md
├── prompts/
├── models/
├── agents/
└── results/
Reglas

Las evaluaciones deben identificar:

Componente evaluado.
Versión.
Fecha.
Casos utilizados.
Criterios.
Métricas.
Resultado.
Umbral de aprobación.
Principio

Un componente no debe considerarse aprobado únicamente porque
funciona en un caso individual.

Debe existir evidencia suficiente y reproducible para respaldar
su comportamiento esperado.

---

# 6. `infra/README.md`

```markdown
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
