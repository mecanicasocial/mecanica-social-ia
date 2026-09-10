# Gobernanza de datos de Mecánica Social IA

## Propósito

Esta política define cómo se clasifican, autorizan, documentan, utilizan, conservan, comparten, evalúan y retiran los datos en el ciclo de vida de los componentes de Mecánica Social IA.

Su finalidad es asegurar que el tratamiento de datos:

- respete la dignidad, autonomía y derechos de las personas;
- se limite a finalidades legítimas, necesarias y documentadas;
- minimice la exposición de información personal, sensible o confidencial;
- sea trazable, reversible y auditable en lo esencial;
- no convierta este repositorio en un almacén de datos operativos reales;
- permita supervisión humana efectiva y rendición de cuentas.

La inteligencia artificial es una herramienta de apoyo. El tratamiento de datos y las decisiones derivadas siguen siendo responsabilidad de personas y órganos institucionales competentes.

## Alcance

Se aplica a:

- Datos utilizados para diseñar, probar, evaluar o operar prompts, agentes, modelos, flujos e integraciones.
- Metadatos, esquemas, muestras, catálogos y políticas de datos del repositorio.
- Entradas y salidas de componentes de IA con relevancia institucional.
- Transferencias a proveedores de modelos, servicios en la nube u otros sistemas (incluido, cuando exista, el intercambio con `mecanica-social-escuela` u otros repositorios del ecosistema).
- Registros, logs y evidencias de evaluación en la medida en que puedan contener o revelar información personal o confidencial.
- Documentación que describa fuentes, finalidades, restricciones y responsables de datos.

No sustituye:

- normas legales aplicables;
- políticas institucionales generales de la ONG Mecánica Social aún no publicadas en este repositorio;
- contratos, convenios o bases de legitimación específicos de cada programa;
- la política de seguridad (`SECURITY.md`) ni la de ética de IA (`AI_ETHICS.md`).

## Principios de gobernanza de datos

1. **Finalidad legítima y explícita.** Todo uso de datos debe tener un propósito institucional documentado.
2. **Necesidad y minimización.** Solo se tratan los datos indispensables para ese propósito.
3. **Autorización previa.** No se tratan datos personales, sensibles o confidenciales sin base legítima y autorización correspondiente.
4. **Proporcionalidad al riesgo.** A mayor sensibilidad o impacto, mayores controles y revisión.
5. **Calidad adecuada al uso.** Los datos deben ser pertinentes, actualizados en lo posible y suficientes para el propósito, sin pretender exhaustividad innecesaria.
6. **Separación de entornos y artefactos.** Se distinguen metadatos, esquemas, muestras, datos operativos, secretos, código y documentación.
7. **No almacenamiento indebido en Git.** Este repositorio no es un repositorio de datos personales reales, bases operativas ni secretos.
8. **Limitación de conservación.** Los datos se conservan solo el tiempo necesario para la finalidad y los controles aplicables.
9. **Acceso con mínimo privilegio.** El acceso se limita a roles y personas autorizadas.
10. **Transparencia razonable.** Cuando sea relevante, se informa el uso de datos y de asistencia de IA de forma comprensible.
11. **Trazabilidad.** Fuentes, versiones, finalidades, restricciones y decisiones relevantes quedan documentadas.
12. **Seguridad y confidencialidad.** Controles proporcionales durante el ciclo de vida, incluido el tránsito hacia servicios externos.
13. **Equidad y no discriminación.** Se revisan riesgos de sesgo, exclusión o impactos desproporcionados asociados a los datos o a su uso.
14. **Supervisión humana y rendición de cuentas.** Existe persona o área responsable identificable; la IA no es titular de la responsabilidad.
15. **Preferencia por datos sintéticos, públicos o anonimizados** en diseño, pruebas y demostraciones.

## Clasificación de datos

Todo componente que trate o documente datos deberá clasificar la información involucrada antes del desarrollo relevante y, en todo caso, antes de la aprobación operativa.

### Categorías

| Categoría | Descripción | Ejemplos orientativos | Tratamiento en este repositorio |
|---|---|---|---|
| Pública | Información cuya divulgación está autorizada o es de dominio público legítimo | Materiales públicos institucionales, normas publicadas | Permitida con atribución y licencia compatibles |
| Interna | Información organizacional no sensible destinada a uso interno | Procedimientos internos no confidenciales, plantillas | Solo metadatos o extractos autorizados; no datos operativos masivos |
| Personal | Datos que identifican o permiten identificar a una persona | Nombre, correo, teléfono, identificadores de participante | **Prohibida** su publicación en el repositorio salvo autorización expresa, minimización extrema y controles documentados; preferir sintéticos |
| Sensible / de especial protección | Datos cuyo mal uso puede generar alto daño o discriminación | Salud, ideología, situación de vulnerabilidad, datos de niñas/niños, entre otros según norma aplicable | **Prohibida** en el repositorio y en herramientas no autorizadas; requiere evaluación reforzada fuera de Git |
| Confidencial | Información protegida por acuerdo, secreto profesional o reserva institucional | Credenciales, contratos reservados, información de terceros bajo NDA | **Prohibida** en el repositorio |
| Sintética / de prueba | Datos artificiales o fuertemente anonimizados para desarrollo y evaluación | Casos inventados en YAML de prueba | Preferida para prompts, experiments, evaluations y examples |
| Secreto técnico | Credenciales y material de autenticación | API keys, tokens, contraseñas | **Nunca** en Git; ver `SECURITY.md` |

La clasificación debe registrarse en la documentación del componente (por ejemplo, metadatos del prompt, manifiesto del agente, contrato de integración o ficha de experimento).

### Relación con el nivel de riesgo del componente

La clasificación de datos **informa** el nivel de riesgo del componente (bajo / medio / alto) definido en el `README.md` y en `GOVERNANCE.md`, sin reemplazarlo:

- Datos solo públicos o sintéticos, uso interno de borradores → suele ser riesgo bajo, sin perjuicio de revisión humana antes de publicar.
- Datos personales no sensibles, análisis o comunicación con impacto moderado → riesgo medio o superior.
- Datos sensibles, perfiles de personas o comunidades, decisiones con efecto sobre derechos o acceso a beneficios → riesgo alto; requiere evaluación específica, controles reforzados y autorización institucional.

Un componente no debe etiquetarse como riesgo bajo si trata de forma habitual datos personales de beneficiarios, estudiantes u otras personas identificables.

## Roles y responsabilidades

### Autoría del componente

- Identificar datos utilizados, generados o inferidos.
- Declarar categoría, finalidad, origen y restricciones.
- Evitar incorporar datos reales no autorizados.
- Preparar muestras sintéticas o autorizadas para pruebas.
- Documentar limitaciones de calidad y cobertura.

### Área responsable del uso

- Confirmar la necesidad institucional y la base de autorización.
- Definir quién puede acceder a resultados que contengan datos.
- Asegurar supervisión humana y canales de corrección.
- Suspender el uso si cambia la finalidad, el proveedor o el riesgo.

### Revisión de datos y privacidad

Evalúa, conforme a `GOVERNANCE.md`:

- finalidad y compatibilidad de usos posteriores;
- necesidad y minimización;
- base de autorización;
- calidad y sesgos plausibles en la fuente;
- clasificación;
- acceso, retención y eliminación;
- anonimización o seudonimización;
- transferencias a servicios externos y ubicación del tratamiento cuando sea relevante;
- claridad de datos permitidos y prohibidos en el componente.

### Revisión de seguridad

Complementa la revisión de datos respecto de exposición, control de acceso, secretos, logs e incidentes (`SECURITY.md`).

### Revisión ética y de derechos

Evalúa impactos sobre dignidad, discriminación, transparencia y participación cuando el tratamiento de datos pueda afectar personas o comunidades (`AI_ETHICS.md`).

### Aprobación institucional

Decide si el beneficio justifica el riesgo residual y si los controles de datos son suficientes para el propósito y contexto autorizados.

La autoría no implica aprobación. En cambios sensibles, quien tenga conflicto de interés relevante deberá abstenerse de la decisión final, de acuerdo con `GOVERNANCE.md`.

## Lo que no debe almacenarse en este repositorio

Queda prohibido versionar en `mecanica-social-ia`:

- contraseñas, tokens, claves API, certificados privados u otros secretos;
- bases de datos operativas o extracciones masivas de personas;
- datos personales reales de beneficiarios, estudiantes, donantes, personal o comunidades, salvo decisión institucional excepcional documentada (no es el diseño por defecto);
- datos sensibles o de especial protección;
- información confidencial de terceros o bajo acuerdo de reserva;
- logs crudos que contengan PII o secretos;
- respaldos, dumps o archivos de producción;
- material cuya licencia o autorización no permita su publicación.

En su lugar, el repositorio puede contener:

- esquemas y diccionarios de datos (`data/schemas/` cuando existan);
- muestras sintéticas o públicas autorizadas (`data/samples/`);
- políticas y procedimientos de datos (`data/policies/` y este documento);
- metadatos de prompts, modelos, agentes y evaluaciones;
- descripciones de fuentes y restricciones sin pegar contenidos protegidos.

## Ciclo de vida de los datos en componentes de IA

```text
Necesidad institucional
        ↓
Definición de finalidad y datos mínimos
        ↓
Clasificación y base de autorización
        ↓
Diseño (prompt / agente / flujo / integración)
        ↓
Pruebas con datos sintéticos o autorizados
        ↓
Revisión de datos, ética y seguridad (según riesgo)
        ↓
Aprobación de propósito y contexto
        ↓
Uso controlado y supervisión humana
        ↓
Conservación limitada / agregación / eliminación
        ↓
Reevaluación, restricción, suspensión o retiro
```

Ningún conjunto de datos ni resultado de IA se considera autorizado para un nuevo propósito solo porque existió una aprobación anterior.

## Requisitos mínimos por componente

Todo prompt, modelo, agente, experimento, evaluación o integración que involucre datos deberá documentar, en la medida aplicable:

1. Identificador y versión del componente.
2. Finalidad del tratamiento.
3. Categorías de datos involucrados (entrada, salida, inferidos).
4. Datos permitidos y datos prohibidos.
5. Origen o fuente (y si es pública, interna, sintética o de terceros).
6. Base de autorización o supuesto pendiente de confirmación (explícito).
7. Personas o grupos potencialmente afectados.
8. Nivel de riesgo del componente.
9. Proveedores o sistemas externos a los que podrían transferirse datos.
10. Medidas de minimización, seudonimización o redacción.
11. Requisitos de supervisión humana sobre salidas.
12. Retención prevista de entradas/salidas/logs fuera del repositorio.
13. Procedimiento de contención si se filtra o se usa indebidamente un dato.
14. Limitaciones de calidad, cobertura geográfica, idioma u otros sesgos conocidos.

Cuando falte información sobre un sistema externo (por ejemplo, contrato aún no definido con `mecanica-social-escuela`), debe marcarse el **supuesto** y el estado del contrato como propuesto o provisional, sin inventar APIs, campos o acuerdos.

## Datos en diseño, pruebas y evaluación

1. Preferir datos sintéticos construidos para el caso de uso.
2. Si se usan datos reales, deben estar autorizados, minimizados y, cuando sea posible, anonimizados o seudonimizados.
3. Las carpetas `experiments/`, `evaluations/`, `examples/` y `prompts/` no son lugar para PII real.
4. Los conjuntos de prueba deben versionarse como artefactos de evaluación (metadatos + casos sintéticos), no como extracciones de producción.
5. Está prohibido usar datos de personas menores de edad o datos sensibles en demos, capturas o casos de prueba del repositorio.
6. Un resultado de evaluación no debe publicarse si expone datos personales; se publican métricas agregadas y conclusiones no identificadoras.

## Inferencias, perfiles y resultados generados

1. Las salidas de IA que describan, clasifiquen o prioricen personas o comunidades se tratan con el mismo rigor que los datos de entrada, o mayor si el impacto lo exige.
2. No se permite crear perfiles políticos individuales sin base legítima, ni evaluar dignidad, merecimiento o valor de una persona.
3. Las inferencias no verificadas deben etiquetarse como tales y no presentarse como hechos institucionales.
4. No se reutilizarán resultados para finalidades incompatibles sin nueva evaluación de datos, ética y riesgo.
5. La automatización de decisiones de alto impacto sobre derechos o acceso a beneficios no se implementará sin evaluación específica, controles reforzados, autorización institucional y supervisión humana efectiva.

## Transferencias y proveedores externos

Antes de enviar datos a un modelo, API, nube u otro sistema:

1. Confirmar que el envío es necesario para la finalidad.
2. Verificar que el servicio está autorizado institucionalmente para ese tipo de dato.
3. Aplicar minimización y redacción de campos innecesarios.
4. Documentar proveedor, finalidad, categorías de datos, restricciones y responsable.
5. Considerar retención del proveedor, registro de prompts y políticas de entrenamiento del proveedor cuando sean relevantes y conocidas.
6. No enviar secretos ni datos sensibles a herramientas no aprobadas.
7. Registrar el contrato de integración según `docs/arquitectura/integraciones.md` cuando la interfaz sea estable o vaya a usarse de forma reiterada.

Las credenciales se gestionan fuera del repositorio.

## Conservación, eliminación y salida de servicio

1. Definir retención de entradas, salidas y logs en los sistemas operativos autorizados (no en Git por defecto).
2. Eliminar o agregar datos cuando deje de ser necesaria la identificación.
3. Al suspender o retirar un componente, revisar qué datos derivados deben borrarse, bloquearse o conservarse por obligación legal o de auditoría.
4. Los metadatos y la documentación de trazabilidad pueden conservarse sin PII para aprendizaje institucional.

## Calidad, sesgo y limitación de fuentes

Quien proponga un componente deberá:

- indicar sesgos o huecos conocidos de la fuente (territorio, idioma, género, cobertura temporal, etc.);
- evitar presentar muestras parciales como censo o verdad completa;
- no inventar fuentes, citas ni estadísticas;
- documentar cuando el modelo pueda completar campos faltantes de forma indebida (y prohibirlo en el prompt o flujo cuando corresponda);
- incorporar pruebas de equidad o casos límite cuando el riesgo sea medio o alto.

## Registro y trazabilidad

Las decisiones relevantes sobre datos deberán poder relacionarse con:

- Issue y Pull Request cuando el cambio viva en el repositorio;
- versión del componente;
- clasificación de datos y de riesgo;
- participantes en la revisión de datos/privacidad;
- restricciones y controles exigidos;
- fecha o condición de reevaluación.

No se registrarán en Issues públicos secretos, PII ni evidencia sensible; para incidentes aplica `SECURITY.md`.

## Incidentes relacionados con datos

Se consideran incidentes de datos, entre otros:

- publicación accidental de PII, datos sensibles o confidenciales en el repositorio o canales públicos;
- uso de datos reales en herramientas no autorizadas;
- transferencia no autorizada a terceros;
- reidentificación de personas a partir de conjuntos que se creían anonimizados;
- uso de datos fuera de la finalidad aprobada;
- negativa o imposibilidad de ejercer supervisión humana sobre resultados que afectan personas.

Acciones mínimas:

1. Contener la exposición (incluyendo rotación de secretos si aplica).
2. No amplificar el dato en Issues públicos.
3. Reportar por canal privado según `SECURITY.md`.
4. Evaluar impacto en personas y obligaciones de comunicación institucional.
5. Corregir el componente, la documentación y los controles.
6. Documentar el aprendizaje sin reexponer la información.

## Evaluación mínima de datos (checklist)

Antes de aprobar un componente, responder:

1. ¿Cuál es la finalidad exacta del tratamiento?
2. ¿Qué datos son estrictamente necesarios?
3. ¿Qué categoría de clasificación tienen?
4. ¿Cuál es la base de autorización o qué falta por confirmar?
5. ¿Quiénes son las personas afectadas?
6. ¿Se puede cumplir el objetivo con datos sintéticos o agregados?
7. ¿Qué datos están explícitamente prohibidos en el componente?
8. ¿A qué sistemas externos podrían transferirse?
9. ¿Cómo se evita que el modelo invente o complete datos personales?
10. ¿Qué supervisión humana se ejerce sobre las salidas?
11. ¿Cuánto tiempo se conservan entradas, salidas y logs fuera de Git?
12. ¿Cómo se suspende el uso si cambia el riesgo o el proveedor?
13. ¿El nivel de riesgo del componente es coherente con la clasificación de datos?
14. ¿La documentación permite auditar lo anterior sin exponer PII?

Si alguna respuesta es “no sé” en un componente de riesgo medio o alto, no corresponde aprobación operativa hasta aclararla o documentar la restricción.

## Relación con la estructura del repositorio

| Ubicación | Rol respecto de datos |
|---|---|
| `DATA_GOVERNANCE.md` | Política institucional de datos del sistema de IA |
| `data/` | Esquemas, muestras autorizadas y políticas operativas de datos |
| `docs/arquitectura/` | Decisiones y límites arquitectónicos; no datos reales |
| `prompts/`, `agents/`, `models/` | Metadatos de datos permitidos/prohibidos y limitaciones |
| `experiments/`, `evaluations/`, `examples/` | Pruebas y demos con datos sintéticos o autorizados |
| `infra/`, `src/` | Ejecución e integración sin secretos ni PII en Git |
| `SECURITY.md` | Incidentes, secretos y controles de seguridad |
| `AI_ETHICS.md` | Requisitos éticos del tratamiento y de los resultados |
| `GOVERNANCE.md` | Flujo de aprobación y roles de revisión |

## Cumplimiento y mejoras

El incumplimiento de esta política puede motivar el rechazo del cambio, la restricción, suspensión o retiro del componente, y la gestión del hecho como incidente cuando exista exposición o riesgo para personas.

Esta política deberá revisarse cuando:

- cambien los usos del repositorio o del ecosistema digital;
- se incorpore una integración estable con datos personales;
- ocurra un incidente relevante de datos;
- cambien normas aplicables o políticas institucionales de la ONG;
- la experiencia de evaluación muestre controles insuficientes o excesivos.

## Relación con otras políticas

Esta política se complementa con:

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `GOVERNANCE.md`
- `AI_ETHICS.md`
- `SECURITY.md`
- `docs/arquitectura/integraciones.md`
- `docs/arquitectura/gobernanza.md` y `docs/arquitectura/gobernanza-rapida.md` (guías de proceso; en caso de conflicto sobre el fondo normativo, prevalecen las políticas de la raíz del repositorio)
- `data/README.md`

## Estado del documento

- **Estado:** vigente como política base del repositorio
- **Ámbito:** `mecanica-social-ia`
- **Responsable de custodia documental:** equipo de gobernanza del repositorio (ver `CODEOWNERS` y `NOTICE`)
- **Notas:** no inventa contratos de datos con `mecanica-social-escuela` ni declara cumplimientos legales específicos no confirmados; las bases de legitimación concretas deben documentarse por caso de uso

## Historial

| Fecha | Cambio |
|---|---|
| 2026-09-09 | Creación inicial de `DATA_GOVERNANCE.md` para cubrir la referencia existente en `README.md` y `GOVERNANCE.md` |
