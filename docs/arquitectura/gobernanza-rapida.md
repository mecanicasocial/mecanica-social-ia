# Guía Rápida de Gobernanza - Mecánica Social IA

*Para decisiones ágiles sin perder rigor ético y técnico*

---

## **Flujo en 5 minutos**

### **Paso 1: Clasifica tu componente**

Responde estas 3 preguntas:
┌─────────────────────────────────────────────────────────┐ │ P1: ¿Usa datos personales o sensibles? │ │ P2: ¿Toma decisiones que afecten derechos/acceso? │ │ P3: ¿Se comunica el resultado al público? │ └─────────────────────────────────────────────────────────┘

Puntuación: 0 "SÍ" → RIESGO BAJO 1-2 "SÍ" → RIESGO MEDIO 3 "SÍ" → RIESGO ALTO


### **Paso 2: Sigue el flujo según riesgo**

RIESGO BAJO RIESGO MEDIO RIESGO ALTO ═════════════════ ════════════════ ═════════════════════════ ✓ Lluvia de ideas ✓ Análisis documental ✓ Decisiones sobre derechos ✓ Corrección estilo ✓ Evaluación formativa ✓ Datos sensibles ✓ Organización info ✓ Comunicación pública ✓ Perfiles de personas ✓ Borradores internos ✓ Sistemas internos ✓ Automatización de decisiones

Revisor: Revisores: Revisores: @LeodanZapata @LeodanZapata @LeodanZapata (técnica) (técnica + metodología) (técnica + metodología + ética + datos)

Tiempo: Tiempo: Tiempo: 1 día 3 días 5 días

Checklist: Checklist: Checklist: □ Funciona □ Cumple checklist BAJO □ Cumple checklist MEDIO □ Documentado □ Fuentes verificables □ Evaluación ética □ Pruebas ejecutadas □ Aprobación formal □ Datos validados □ Supervisión humana clara


---

## **Checklist RÁPIDA por Tipo de Componente**

### **Nuevo Prompt (cualquier versión)**

```yaml
tipo: prompt
archivo: prompts/mi-prompt-v0.1.0.yaml

RIESGO BAJO (Ej: lluvia de ideas)
  ☐ ¿Tiene prompt_text claro?
  ☐ ¿Está documentado qué hace?
  ☐ ¿Evita datos sensibles?
  
RIESGO MEDIO (Ej: análisis documental)
  ☐ Cumple checklist BAJO
  ☐ ¿Tiene ejemplos de entrada/salida?
  ☐ ¿Están las fuentes documentadas?
  ☐ ¿Se ejecutó y probó?
  ☐ ¿Limita hallazgaciones sobre personas?
  
RIESGO ALTO (Ej: decisiones sobre beneficiarios)
  ☐ Cumple checklist MEDIO
  ☐ ¿Tiene supervisión humana definida?
  ☐ ¿Podría discriminar por género/edad/territorio?
  ☐ ¿Se documentó evaluación de sesgo?
  ☐ ¿Está aprobado por @LeodanZapata?

Nuevo Modelo o Integración

tipo: modelo
archivo: models/nuevo-modelo/config.yaml

SIEMPRE (todos los modelos son RIESGO MEDIO+)
  ☐ ¿Existe model-card.md?
  ☐ ¿Está documentada licencia y costo?
  ☐ ¿Se incluyen limitaciones conocidas?
  ☐ ¿Se testó con datos de prueba?
  ☐ ¿Se validó contra privacidad?
  ☐ ¿Está aprobado por @LeodanZapata?

Preguntas Éticas Rápidas (14 preguntas de AI_ETHICS.md)
Usa esto como test mínimo de 2 minutos:
□ ¿Respeta la dignidad de personas? 
  → No inventa valores sobre quiénes son

□ ¿Hay alternativa sin IA? 
  → Si sí, ¿por qué usar IA?

□ ¿Quién se beneficia? ¿Quién podría dañarse?
  → Si hay daño potencial, contrólalo

□ ¿Supervisa una persona el resultado?
  → Nunca decisiones solo-IA

□ ¿Se comunica que se usó IA?
  → Transparencia: "Generado con IA"

□ ¿Se verifica la información?
  → No inventar fuentes

□ ¿Podría tener sesgo contra un grupo?
  → Verifica género, edad, territorio, idioma

□ ¿Cómo puede alguien impugnar un resultado?
  → Debe haber proceso de revisión

Si respondes "NO" o "NO SÉ" a cualquiera → Requiere revisión ética

Tiempos de Respuesta
Situación	Tiempo	Responsable
PR con typo o formato	1 día	@LeodanZapata
Nuevo prompt BAJO	1 día	@LeodanZapata
Nuevo prompt MEDIO	3 días	@LeodanZapata
Nuevo prompt ALTO	5 días + aprobación	@LeodanZapata
Cambio en política	5 días	@LeodanZapata
Incidente de seguridad	24h	@LeodanZapata
Bug crítico en producción	4h	@LeodanZapata
Plantilla de PR Mínima
## Descripción
[Qué hace este cambio en 2 líneas]

## Tipo de cambio
- [ ] Nuevo prompt (especificar riesgo: bajo/medio/alto)
- [ ] Nuevo modelo o integración
- [ ] Cambio en gobernanza/política
- [ ] Corrección (bug fix)
- [ ] Documentación

## Riesgo clasificado
- [ ] BAJO
- [ ] MEDIO
- [ ] ALTO

## Checklist
- [ ] Cumple los puntos de la checklist de riesgo
- [ ] No expone credenciales, tokens, datos sensibles
- [ ] Respeta los principios de AI_ETHICS.md
- [ ] Está documentado o viene con ejemplo

## Para @LeodanZapata
[Preguntas o consideraciones especiales]
Ejemplos Rápidos

✅ Ejemplo 1: Prompt BAJO (se aprueba en 1 día)
Nombre: resumidor-lluvia-ideas-v0.1.0.yaml
Caso: Resumir notas de una sesión de lluvia de ideas en 3 puntos
Riesgo: BAJO (no usa datos personales, es interno, revisión manual garantizada)

Contenido:
  prompt_text: "Resume en 3 puntos principales la siguiente lluvia de ideas..."
  ejemplo: 
    entrada: "Los facilitadores dijeron... todos sugirieron..."
    salida: "1. Punto clave\n2. Oportunidad\n3. Riesgo identificado"

Aprobación: @LeodanZapata valida en 1 día
Decisión: ✓ APROBADO

🟡 Ejemplo 2: Prompt MEDIO (se aprueba en 3 días)
Nombre: analizador-solicitudes-capacitacion-v0.2.0.yaml
Caso: Extraer datos estructurados de formularios de solicitud
Riesgo: MEDIO (toca datos de beneficiarios, comunicación pública de resultados)

Contenido:
  prompt_text: "Extrae nombre, email, teléfono, interés..."
  ejemplos: [5+ casos de prueba]
  criterios_aceptacion:
    - "JSON válido en 100% de casos"
    - "Extrae 4/4 campos en 95%+ de casos"
    - "No inventa información"
  datos_permitidos: [nombre, email, teléfono, interés]
  datos_prohibidos: [datos bancarios, dirección exacta]

Pruebas: evaluations/harness.py en modo offline (estructura OK; no aprueba producción)
  + corrida con modelo cuando exista proveedor autorizado
Revisión: @LeodanZapata verifica técnica + metodología
Decisión: solo tras evidencia y gobernanza (offline ≠ aprobado operativo)

🔴 Ejemplo 3: Prompt ALTO (se aprueba en 5+ días)
Nombre: seleccionador-beneficiarios-v1.0.0.yaml
Caso: Recomendar quién debería recibir beca basado en perfil
Riesgo: ALTO (afecta derechos, usa datos sensibles, decisión automática)

Contenido:
  prompt_text: "Evalúa elegibilidad de beneficiario..."
  datos_prohibidos: [género, edad, raza, orientación, situación familiar]
  evaluacion_sesgos: [test de equidad por género, edad, territorio]
  supervison_humana: "REQUIERE revisión de 100% de recomendaciones"

Pruebas:
  - Funciona: ✓
  - Sesgos: ✓ sin diferencia injustificada
  - Fuentes: ✓ criterios documentados
  - Ética: ✓ supervisión humana clara

Revisión:
  ☐ @LeodanZapata (técnica)
  ☐ @LeodanZapata (metodología)
  ☐ @LeodanZapata (ética)

Aprobación formal: @LeodanZapata firma documento
Decisión: ✓ APROBADO para piloto en 1 región, 30 días de monitoreo

Contacto y Dudas
Pregunta	Contacto
¿Es BAJO o MEDIO?	Pregunta en el PR a @LeodanZapata
¿Falla el test ético?	Documenta en issue y abre discusión
¿Tengo emergencia?	@LeodanZapata responde en 4 horas
¿Quiero aportar?	Lee CONTRIBUTING.md primero
Última actualización: 2026-09-10
Responsable: @LeodanZapata
Próxima revisión: tras primer piloto o incidente
Ver también: PRACTICO.md (MVP ejecutable)


