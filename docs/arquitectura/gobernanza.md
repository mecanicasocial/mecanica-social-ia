## **Flujo en 5 minutos**

### **Paso 1: Clasifica tu componente**

Responde estas 3 preguntas:
┌────────────────────────────────────────────────────────────────────────┐ │ CICLO DE VIDA DE UN COMPONENTE DE IA │ └────────────────────────────────────────────────────────────────────────┘

┌─ NECESIDAD ──────────────────────────────────────────────────────────┐ │ Una persona/área identifica una necesidad institucional que podría │ │ resolverse con IA │ │ Ejemplo: "Necesitamos procesar formularios de solicitud de │ │ capacitación más rápido" │ └──────────────────────────────────────────────────────────────────────┘ ↓ (ISSUE #XX) ↓ ┌─ PROPUESTA ───────────────────────────────────────────────────────────┐ │ Define: │ │ • Caso de uso específico │ │ • Área responsable y personas afectadas │ │ • Datos que se utilizarán (permitidos y prohibidos) │ │ • Beneficio esperado │ │ • Riesgos iniciales identificados │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ CLASIFICACIÓN DE RIESGO ─────────────────────────────────────────────┐ │ ┌──────────────────────────────────────────────────────────────────┐ │ │ │ BAJO: MEDIO: ALTO: │ │ │ │ • Lluvia de ideas • Análisis • Decisiones que │ │ │ │ • Corrección de estilo documental afecten derechos │ │ │ │ • Organización de info • Evaluación • Datos sensibles │ │ │ │ • Borradores internos • Comunicación • Perfiles │ │ │ │ pública • Automatización │ │ │ │ Requiere: Revisión manual Requiere: Requiere: │ │ │ │ antes de publicar • Fuentes • Evaluación │ │ │ │ • Tests • Aprobación │ │ │ │ • Datos validados expresa │ │ │ │ • Aprobación • Controles │ │ │ │ reforzados │ │ │ └──────────────────────────────────────────────────────────────────┘ │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ DESARROLLO ──────────────────────────────────────────────────────────┐ │ Construcción del componente: │ │ • Redacción del prompt (versión inicial) │ │ • Configuración del modelo (parámetros, proveedor) │ │ • Definición de test cases │ │ • Documentación técnica │ │ │ │ Ubicación: prompts/, models/, agents/ con metadata YAML │ │ Rama: issue-XX/descripcion-corta │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ PRUEBAS ─────────────────────────────────────────────────────────────┐ │ ┌──────────────────────────────────────────────────────────────────┐ │ │ │ TÉCNICAS METODOLÓGICAS ÉTICAS │ │ │ │ • ¿Funciona? • ¿Resuelve la • ¿Respeta │ │ │ │ • ¿Formato correcto? necesidad? dignidad? │ │ │ │ • ¿Maneja errores? • ¿Tiene • ¿Hay sesgo? │ │ │ │ • ¿Performance limitaciones? • ¿Derechos │ │ │ │ aceptable? • ¿Fuentes protegidos? │ │ │ │ verificables? │ │ │ │ • ¿Casos de │ │ │ │ uso claros? │ │ │ └──────────────────────────────────────────────────────────────────┘ │ │ │ │ Herramientas: evaluations/harness.py, casos de prueba en YAML │ │ Criterio: ≥95% en métrica primaria │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ REVISIÓN FORMAL ─────────────────────────────────────────────────────┐ │ Según nivel de riesgo: │ │ │ │ BAJO: 1 revisor técnico │ │ MEDIO: • 1 revisor técnico │ │ • 1 revisor metodológico │ │ ALTO: • 1 revisor técnico │ │ • 1 revisor metodológico │ │ • 1 revisor ético │ │ • 1 revisor de datos/privacidad │ │ • Aprobación formal de gobernanza │ │ │ │ Responsable: @LeodanZapata (todas las áreas) │ │ Ubicación: Pull Request con checklist de gobernanza │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ APROBACIÓN INSTITUCIONAL ────────────────────────────────────────────┐ │ Decisión formal: │ │ │ │ ✓ APROBADO: Autorizado para producción con controles especificados │ │ ⊠ RESTRINGIDO: Permitido en contextos específicos con supervisión │ │ ✗ RECHAZADO: No se implementa (documentar razones) │ │ │ │ Produce: Documento de aprobación con: │ │ - Componente y versión │ │ - Propósito autorizado │ │ - Área responsable │ │ - Nivel de riesgo │ │ - Controles obligatorios │ │ - Próxima revisión │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ IMPLEMENTACIÓN CONTROLADA ───────────────────────────────────────────┐ │ Lanzamiento gradual con monitoreo: │ │ │ │ 1. Beta interna: Equipo responsable + evaluadores │ │ 2. Piloto: Área usuaria, monitoreo diario, 10-20% de carga │ │ 3. Producción: Implementación completa con alertas │ │ │ │ Métricas a monitorear: │ │ - Tasa de error/acierto │ │ - Casos de uso real vs. esperado │ │ - Feedback de usuarios │ │ - Incidentes reportados │ │ - Sesgo, discriminación, impactos adversos │ └──────────────────────────────────────────────────────────────────────┘ ↓ ┌─ SEGUIMIENTO Y MEJORA ────────────────────────────────────────────────┐ │ Monitoreo continuo: │ │ │ │ • Registro de errores y casos edge │ │ • Feedback de usuarios (satisfacción, problemas) │ │ • Evaluación de sesgos (¿afecta a grupos específicos?) │ │ • Cambios en contexto o requisitos │ │ • Incidentes de seguridad o privacidad │ │ │ │ Cadencia: Diaria (logs), Semanal (reporte), Trimestral (revisión) │ │ Responsable: Área usuaria con apoyo técnico │ └────────────────────────────���─────────────────────────────────────────┘ ↓ ┌─ ACTUALIZACIÓN O RETIRO ──────────────────────────────────────────────┐ │ Según evidencia: │ │ │ │ ACTUALIZAR: │ │ • Mejoras en calidad/performance │ │ • Adaptación a nuevos contextos │ │ • Corrección de sesgos detectados │ │ • Migración a nuevo modelo/proveedor │ │ │ │ RESTRINGIR: │ │ • Impacto negativo identificado │ │ • Cambio en modelo no mitigable │ │ • Vulnerabilidad de seguridad controlada │ │ │ │ SUSPENDER: │ │ • Riesgo inmediato incontrolable │ │ • Exposición de datos o seguridad crítica │ │ • Decisión institucional urgente │ │ │ │ RETIRAR: │ │ • Componente obsoleto sin usuarios │ │ • Conflicto con política institucional │ │ • Licencia o dependencias incompatibles │ └──────────────────────────────────────────────────────────────────────┘

---

## Componentes Principales

### **1. Sistema de Prompts Versionado**

```text
prompts/
├── README.md
├── esquema-prompt.yaml
└── formulario-intake-v1.0.0.yaml   # estado: prueba (riesgo medio)
```

`resumidor-solicitudes` y carpetas `.evaluaciones` bajo prompts **no existen**.
Las suites viven en `evaluations/casos-prueba/`.


**Responsabilidad**: @LeodanZapata (técnica, metodológica, ética)

**Convenciones**:
- Nombre: `<id-descriptivo>-v<semver>.yaml`
- Metadatos: id, versión, estado, autor, clasificación de riesgo
- Contenido: prompt_text, ejemplos, criterios de evaluación

---

### **2. Sistema de Modelos y Configuraciones**

Estado actual:

```text
models/
├── README.md
├── _plantillas/
└── openai-compatible-eval/   # propuesto / solo evaluación (ADR-002)
    ├── config.yaml
    └── model-card.md
```

Proveedor **productivo** autorizado: aún no. Ver model-card y roles de revisión.


**Responsabilidad**: @LeodanZapata (elige modelos, valida licencias)

**Contenido mínimo de model-card.md**:
- Propósito y capacidades
- Datos de entrenamiento
- Limitaciones conocidas
- Riesgos identificados
- Costo y performance
- Política de retención de datos del proveedor

---

### **3. Sistema de Evaluaciones**

Estado actual:

```text
evaluations/
├── harness.py                 # offline + model (secretos por env)
├── config.example.yaml
├── casos-prueba/intake-test-set.yaml
└── resultados/*-{offline|model}.json
```

Aún no hay suites de 100+ casos ni métricas tipo BLEU como primarias.


**Responsabilidad**: @LeodanZapata (define métricas, valida pruebas) — ver roles-revision.md

**Ejecución**: ver `PRACTICO.md` / `evaluations/README.md`

---

### **4. Sistema de Agentes Automatizados**

Estado actual: solo `agents/README.md`. No hay agentes implementados.
Los nombres `asistente-formacion` / `orquestador-proyectos` son **ejemplos futuros**, no inventario real.


**Responsabilidad**: @LeodanZapata (verifica seguridad y permisos)

**Información en agent.yaml**:
- Propósito
- Prompts que utiliza
- APIs externas
- Permisos requeridos
- Limitaciones de uso

---

### **5. Gobernanza y Políticas**

Raíz del repo/ ├── GOVERNANCE.md [Proceso de aprobación formal] ├── AI_ETHICS.md [14 requisitos éticos] ├── SECURITY.md [Políticas de seguridad] ├── CODE_OF_CONDUCT.md [Reglas de participación] ├── CONTRIBUTING.md [Cómo aportar] ├── LICENSE.md [Multi-licencia: CC-BY/Apache-2.0] ├── CODEOWNERS [Responsables por área] └── NOTICE [Atribución legal]


**Responsabilidad**: @LeodanZapata (custodio de políticas)

---

## Relación con Mecánica Social Escuela


**Responsabilidad**: @LeodanZapata (custodio de políticas)

---

## Relación con Mecánica Social Escuela

mecanica-social-escuela mecanica-social-ia (Plataforma educativa) (Sistema de IA) │ │ │ │ Programas ◄──────────────────────► Prompts Contenido ◄──────────────────────► Modelos Evaluación ◄────────────────────► Agentes │ │ └─────────────────────────────────────┘ (API Contract)


**Flujo de datos de mecanica-social-escuela → mecanica-social-ia**
(**objetivo no implementado**; contrato provisional INT-001):

1. Escuela aporta necesidad / textos de solicitud según contrato acordado
2. IA asiste (p. ej. extracción estructurada) solo con datos autorizados o sintéticos
3. Resultado versionado + **revisión humana** antes de uso en Escuela
4. No existe API productiva documentada aún — ver `contratos/INT-001-escuela.md`

**Restricciones críticas**:
- Nunca acceder a datos personales de estudiantes sin autorización
- Todo resultado pasa revisión humana antes de devolverse
- Versionar todos los cambios de prompts/modelos que afecten escuela

---

## Flujos de Decisión Rápida

### **¿Cómo sé si mi componente necesita revisión ética?**
¿Afecta datos personales? → SÍ → Revisión ética ¿Afecta derechos de personas? → SÍ → Revisión ética ¿Toma decisiones automáticas? → SÍ → Revisión ética ¿Crea perfiles de personas? → SÍ → Revisión ética ¿Comunica resultado a público? → SÍ → Revisión ética ¿Es solo interno/borradores? → NO → Revisión técnica básica


### **¿En qué rama trabajo?**

Nueva característica o fix → branch: issue-XX/descripcion-corta → ejemplo: issue-15/mejorar-prompt-intake

Pequeña corrección → branch: fix/descripcion → ejemplo: fix/typo-governance

Experimento no oficial → branch: exp/descripcion → ejemplo: exp/probar-claude-3.5


### **¿Cuándo abro Pull Request?**

Cambios en archivos críticos → Siempre (LICENSE, GOVERNANCE, etc.) Nuevo prompt ≥ v0.1.0 → Siempre (con evaluación) Cambios en modelos → Siempre (actualizar model-cards) Correcciones menores (typos) → Sí (revisión ligera) Experimentos privados → No (branch exp/ es temporal)


---

## Principios Rectores

1. **Supervisión humana siempre**: Ningún resultado de IA se publica sin revisión
2. **Trazabilidad completa**: Todo cambio está documentado, versionado y reversible
3. **Riesgo proporcional**: Control mayor = mayor riesgo
4. **Transparencia sobre capacidades**: Documentamos qué sí hace, qué no, y por qué
5. **Datos nunca se publican**: El repositorio tiene código y documentación, no datos sensibles
6. **Ética integrada**: No es un checklist final, es parte del diseño desde el inicio

---

## Próximos Pasos

1. ✅ **Licencia definida** (LICENSE.md)
2. ✅ **Responsables asignados** (@LeodanZapata)
3. ✅ **Primer prompt ejemplo en prueba** (formulario-intake-v1.0.0.yaml; riesgo medio)
4. ✅ **Harness offline MVP** (evaluations/harness.py + suite intake)
5. ✅ **Modo model del harness** (secretos por env; ADR-002) — vendor productivo aún no autorizado
6. ✅ **Contrato provisional INT-001** (`docs/arquitectura/contratos/INT-001-escuela.md`) — falta confirmación Escuela
7. ✅ **Model-card de evaluación** + **roles de revisión** documentados
8. ⏳ **Autorizar proveedor productivo** (INT-002 + registro de decisión)
9. ⏳ **Validar INT-001** con responsables de mecanica-social-escuela
10. ⏳ **Segundo maintainer / teams** para four-eyes en CODEOWNERS

---

## Contacto y Dudas

- **Gobernanza**: @LeodanZapata
- **Seguridad**: @LeodanZapata
- **Ética**: @LeodanZapata

Para contribuciones: Ver `CONTRIBUTING.md`
Para incidentes: Ver `SECURITY.md` y `CODE_OF_CONDUCT.md`

