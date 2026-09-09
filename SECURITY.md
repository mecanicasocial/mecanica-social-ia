# Security Policy

## Propósito

Mecánica Social IA promueve el desarrollo y utilización segura de tecnologías de inteligencia artificial dentro de la ONG Mecánica Social y de los proyectos, programas y servicios que ésta desarrolla.

## Alcance

Esta política aplica a:

- Código fuente.
- Prompts institucionales.
- Automatizaciones.
- Asistentes virtuales.
- Bases de conocimiento.
- Integraciones externas.
- Documentación técnica.
- Configuraciones de seguridad.

## Principios de seguridad

- Seguridad por diseño.
- Privacidad por diseño.
- Mínimo privilegio.
- Gestión responsable de datos.
- Transparencia.
- Mejora continua.

## Reporte de vulnerabilidades

Si identifica una vulnerabilidad, exposición de datos, credencial filtrada, uso indebido de un componente de IA u otro riesgo de seguridad:

1. **No publique** la información en Issues, Pull Requests, Discussions ni otros canales públicos.
2. Reporte el hallazgo **por un canal privado** de los indicados abajo.
3. Incluya evidencia suficiente para reproducir y evaluar el problema.
4. Mantenga la confidencialidad hasta que el equipo confirme la resolución o autorice la divulgación.

### Canales de reporte (privados)

Use **uno** de los siguientes canales, en este orden de preferencia:

1. **GitHub Private Vulnerability Reporting** (preferido)  
   Abra un aviso privado en:  
   https://github.com/mecanicasocial/mecanica-social-ia/security/advisories/new  
   Si la opción no aparece habilitada, utilice el correo institucional.

2. **Correo institucional de gobernanza / seguridad**  
   - **Para:** `governance@mecanicasocial.org`  
   - **Asunto sugerido:** `[Seguridad] mecanica-social-ia — <título breve del hallazgo>`  
   - Este buzón es el canal institucional documentado para gobernanza y reportes sensibles del proyecto.

3. **Contacto de respaldo (solo si los canales anteriores no responden)**  
   Contacte de forma privada al responsable técnico del repositorio en GitHub: [@LeodanZapata](https://github.com/LeodanZapata), sin incluir secretos completos en mensajes públicos.

### Qué incluir en el reporte

Para agilizar la evaluación, incluya cuando sea posible:

- Descripción clara del problema y su impacto potencial.
- Componente afectado (por ejemplo: prompt, agente, documentación, integración, configuración o futuro código).
- Pasos para reproducir el hallazgo.
- Evidencia técnica (capturas, fragmentos redactados, fechas, URLs internas no sensibles).
- Versión, commit, rama o fecha en que se observó.
- Si hay datos personales, credenciales o secretos involucrados: **indíquelos sin pegar valores completos**; use redacciones (`sk-***`, últimos 4 caracteres, etc.).
- Su evaluación preliminar de severidad (baja, media, alta, crítica), si la tiene.
- Forma de contacto para seguimiento.

### Tiempos de respuesta esperados

El equipo institucional procurará:

| Etapa | Plazo orientativo |
| --- | --- |
| Acuse de recibo | hasta 3 días hábiles |
| Evaluación inicial y clasificación | hasta 7 días hábiles |
| Plan de mitigación o contención | según severidad e impacto |
| Cierre y aprendizaje documentado | al resolver el incidente |

Los plazos son orientativos y pueden extenderse en hallazgos complejos, dependencias externas o cuando se requiera coordinación con otras áreas de la ONG.

### Alcance de los reportes

Se aceptan, entre otros:

- Exposición de secretos, tokens o credenciales.
- Filtración o mal manejo de datos personales o confidenciales.
- Controles de acceso insuficientes en integraciones o automatizaciones.
- Prompt injection u otros abusos de componentes de IA con impacto en seguridad o privacidad.
- Suplantación, fraude o manipulación facilitada por componentes del repositorio.
- Configuraciones inseguras en workflows, agentes o infraestructura documentada aquí.

No use este canal para:

- Consultas generales de uso o soporte funcional (prefiera Issues públicos sin datos sensibles).
- Reportes de conducta comunitaria (vea `CODE_OF_CONDUCT.md`).
- Discusiones de producto sin riesgo de seguridad.

### Buena fe y divulgación responsable

- Se espera reporte de buena fe, sin explotar el hallazgo más allá de lo necesario para demostrarlo.
- No se solicitará acceso no autorizado a sistemas de terceros ni exfiltración de datos reales de personas.
- Coordine cualquier divulgación pública con el equipo antes de publicarla.
- Quien reporte de buena fe no será sancionado por informar un riesgo o vulnerabilidad.

## Información sensible

No debe almacenarse en este repositorio:

- Contraseñas.
- Tokens.
- Claves API.
- Credenciales de acceso.
- Datos personales sin autorización.
- Información protegida por acuerdos de confidencialidad.

## Inteligencia artificial responsable

Toda solución basada en IA deberá considerar:

- Riesgos de sesgo.
- Riesgos de privacidad.
- Calidad de resultados.
- Supervisión humana.
- Trazabilidad de decisiones.

La inteligencia artificial actúa como herramienta de apoyo y no reemplaza la responsabilidad profesional ni institucional de las personas.

## Gestión de incidentes

Los incidentes reportados serán:

1. Registrados.
2. Evaluados.
3. Priorizados según impacto.
4. Mitigados.
5. Documentados para aprendizaje institucional.

## Actualizaciones

Esta política podrá ser revisada y actualizada conforme evolucione la arquitectura tecnológica y organizacional de Mecánica Social IA.
