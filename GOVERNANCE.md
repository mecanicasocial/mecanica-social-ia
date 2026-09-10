# Gobernanza de Mecánica Social IA

## Propósito

Esta política define cómo se proponen, revisan, aprueban, mantienen, suspenden y retiran los componentes de Mecánica Social IA.

La gobernanza busca asegurar:

- Coherencia con la misión institucional.
- Responsabilidad humana.
- Calidad metodológica y técnica.
- Uso ético de la inteligencia artificial.
- Protección de datos y seguridad.
- Transparencia y trazabilidad.
- Participación de las áreas afectadas.
- Mejora continua.

## Alcance

Se aplica a:

- Prompts.
- Asistentes.
- Modelos.
- Flujos automatizados.
- Integraciones.
- Conjuntos de evaluación.
- Bases de conocimiento.
- Documentación.
- Datos utilizados para diseño, prueba o funcionamiento.
- Resultados destinados a uso institucional.

## Principios de gobernanza

1. Ningún sistema de IA es responsable de una decisión.
2. Toda solución deberá tener una persona o área responsable.
3. El nivel de control será proporcional al riesgo.
4. La aprobación será específica para un propósito y contexto.
5. Una aprobación no se extenderá automáticamente a otros usos.
6. Las personas afectadas deberán ser consideradas durante la evaluación.
7. Las decisiones relevantes deberán quedar documentadas.
8. Los conflictos de interés deberán declararse.
9. Los riesgos graves podrán justificar la suspensión inmediata.
10. Toda solución podrá ser revisada, restringida o retirada.

## Funciones

La separación operativa de estos roles (matriz, excepción dual temporal,
registros y plantilla de PR) se detalla en
`docs/arquitectura/roles-revision.md`.


### Autoría

Responsable de:

- Crear o modificar el componente.
- Documentar el propósito.
- Identificar fuentes, datos y dependencias.
- Incorporar pruebas.
- Declarar limitaciones y riesgos conocidos.
- Responder a las observaciones de revisión.

La autoría no implica aprobación.

### Revisión técnica

Evalúa:

- Funcionamiento.
- Reproducibilidad.
- Dependencias.
- Control de versiones.
- Seguridad técnica.
- Mantenibilidad.
- Posibles fallos o usos indebidos.

### Revisión metodológica

Evalúa:

- Pertinencia del caso de uso.
- Coherencia con los objetivos.
- Calidad de criterios y fuentes.
- Validez de pruebas y evaluaciones.
- Adecuación al área usuaria.
- Claridad de las limitaciones.

### Revisión ética y de derechos

Evalúa:

- Dignidad y autonomía.
- Riesgos de discriminación.
- Equidad.
- Transparencia.
- Supervisión humana.
- Impactos sobre personas y comunidades.
- Proporcionalidad del uso.

### Revisión de datos y privacidad

Evalúa:

- Finalidad.
- Necesidad de los datos.
- Base de autorización.
- Minimización.
- Calidad.
- Clasificación.
- Acceso.
- Retención.
- Anonimización o seudonimización.
- Transferencias a servicios externos.

### Revisión de seguridad

Evalúa:

- Credenciales y secretos.
- Control de acceso.
- Exposición de información.
- Dependencias externas.
- Amenazas.
- Registro de eventos.
- Gestión de incidentes.
- Medidas de mitigación.

### Área responsable del uso

Deberá:

- Definir el contexto autorizado.
- Designar supervisión humana.
- Capacitar a las personas usuarias.
- Monitorizar resultados.
- Informar errores e incidentes.
- Mantener la documentación actualizada.
- Suspender el uso cuando existan riesgos no controlados.

### Aprobación institucional

Determina si el beneficio previsto justifica los riesgos y si existen controles suficientes.

La aprobación deberá identificar:

- Componente y versión.
- Propósito autorizado.
- Área responsable.
- Personas usuarias.
- Nivel de riesgo.
- Datos autorizados.
- Controles obligatorios.
- Fecha o condición de revisión.
- Condiciones de suspensión o retiro.

## Niveles de decisión

### Cambios menores

Ejemplos:

- Correcciones ortográficas.
- Enlaces.
- Formato.
- Clarificaciones sin cambio funcional.

Podrán aprobarse mediante revisión ordinaria del repositorio.

### Cambios funcionales

Ejemplos:

- Modificación de instrucciones.
- Nuevas fuentes.
- Nuevas salidas.
- Cambios en criterios de evaluación.
- Incorporación de herramientas externas.

Requieren revisión técnica y metodológica.

### Cambios sensibles

Ejemplos:

- Nuevos datos personales.
- Usos que puedan afectar derechos.
- Automatización de decisiones.
- Perfiles de personas o comunidades.
- Integraciones con sistemas institucionales.
- Cambios en controles de seguridad.

Requieren revisión técnica, metodológica, ética, de datos, seguridad y aprobación institucional expresa.

## Flujo de aprobación

1. Definición de la necesidad.
2. Identificación del área responsable.
3. Descripción del caso de uso.
4. Identificación de personas afectadas.
5. Clasificación de datos.
6. Clasificación de riesgo.
7. Desarrollo del componente.
8. Preparación de pruebas.
9. Revisión técnica y metodológica.
10. Revisión ética, de datos y seguridad cuando corresponda.
11. Corrección de observaciones.
12. Decisión de aprobación, restricción o rechazo.
13. Implementación controlada.
14. Seguimiento y reevaluación.

## Criterios de aprobación

Un componente podrá aprobarse si:

- Su propósito es legítimo y está claramente definido.
- Es coherente con la misión y los principios institucionales.
- Sus beneficios esperados están documentados.
- Utiliza únicamente datos autorizados.
- Ha superado las pruebas aplicables.
- Sus limitaciones son conocidas.
- Existe supervisión humana efectiva.
- Los riesgos cuentan con medidas de mitigación.
- Hay una persona o área responsable.
- Existe un procedimiento de suspensión y revisión.

## Causas de suspensión

Un componente podrá suspenderse cuando:

- Produzca daños o resultados discriminatorios.
- Exponga información.
- Use datos no autorizados.
- Cambie una dependencia crítica.
- Deje de cumplir requisitos normativos o institucionales.
- Presente errores reiterados.
- No pueda mantenerse la supervisión humana.
- Sea utilizado fuera de su propósito autorizado.
- Existan incidentes sin resolver.
- No cuente con una persona responsable activa.

## Registro de decisiones

Las decisiones relevantes deberán documentar:

- Fecha.
- Componente y versión.
- Participantes en la revisión.
- Evidencia examinada.
- Riesgos detectados.
- Medidas exigidas.
- Decisión.
- Responsable.
- Próxima revisión.

## Conflictos de interés

Las personas que participen en la revisión deberán declarar intereses que puedan afectar su independencia.

Cuando exista un conflicto significativo, la persona deberá abstenerse de la decisión y solicitar una revisión independiente.

## Participación y consulta

Cuando una solución pueda afectar significativamente a un área, colectivo o comunidad, la evaluación deberá incorporar la participación de representantes pertinentes antes de la aprobación.

La consulta no podrá sustituirse por opiniones generadas artificialmente.

## Revisión de esta política

Esta política deberá revisarse cuando:

- Cambien los usos del repositorio.
- Aparezcan nuevos riesgos.
- Se incorporen nuevas tecnologías.
- Ocurra un incidente relevante.
- Cambien las políticas institucionales o normas aplicables.

## Relación con otras políticas

Esta política se complementa con:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `AI_ETHICS.md`
- `DATA_GOVERNANCE.md`
- `SECURITY.md`
