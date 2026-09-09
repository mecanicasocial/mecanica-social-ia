# Arquitectura general — Mecánica Social IA

## 1. Propósito

Este documento define la arquitectura general del repositorio `mecanica-social-ia`: una organización clara, trazable y escalable para los componentes de inteligencia artificial de Mecánica Social.

La arquitectura facilita la comprensión del proyecto, la evolución controlada, la evaluación, la seguridad, la gobernanza y la incorporación de nuevos componentes.

## 2. Principios arquitectónicos

1. **Trazabilidad:** los cambios relevantes deben relacionarse con Issues, branches, commits, Pull Requests y documentación.
2. **Separación de responsabilidades:** cada componente tiene una función definida.
3. **Versionamiento:** prompts, configuraciones y componentes relevantes deben tener versiones identificables.
4. **Evaluación antes de promoción:** los componentes destinados a uso operativo deben contar con evidencia adecuada a su propósito.
5. **Seguridad por diseño:** no se almacenan credenciales, tokens ni claves API en el repositorio.
6. **Privacidad y minimización:** se utiliza la menor cantidad de datos necesaria para cada propósito.
7. **Supervisión humana:** la IA apoya procesos y decisiones; no sustituye automáticamente la responsabilidad humana.
8. **Reproducibilidad:** experimentos y evaluaciones deben registrar las condiciones necesarias para comprender sus resultados.
9. **Evolución documentada:** las decisiones arquitectónicas relevantes se registran mediante ADR.

## 3. Estructura general

```text
mecanica-social-ia/
├── docs/
│   └── arquitectura/
│       ├── README.md
│       ├── arquitectura-general.md
│       ├── componentes.md
│       ├── integraciones.md
│       ├── gobernanza.md
│       └── adr/
├── prompts/
├── models/
├── agents/
├── experiments/
├── evaluations/
├── infra/
├── data/
├── examples/
└── src/
```

La estructura representa la separación conceptual de componentes. No implica que todos deban estar implementados desde el inicio.

## 4. Capas

### `docs/arquitectura/`
Documentación de arquitectura, componentes, integraciones, gobernanza y decisiones. No contiene código, datos reales ni secretos.

### `prompts/`
Prompts versionados, documentados y trazables.

### `models/`
Configuraciones, referencias y documentación de modelos. No contiene credenciales ni pesos salvo decisión técnica, legal y de infraestructura explícita.

### `agents/`
Definiciones de agentes, instrucciones, modelos, herramientas, entradas, salidas y permisos.

### `experiments/`
Pruebas controladas para explorar prompts, modelos, agentes, flujos o configuraciones.

### `evaluations/`
Casos de prueba, criterios, métricas y resultados que aportan evidencia sobre el comportamiento de los componentes.

### `infra/`
Configuraciones, automatizaciones y elementos necesarios para ejecutar o desplegar el sistema.

### `data/`
Esquemas, muestras controladas, políticas y documentación de datos. No debe convertirse en repositorio de datos personales o sensibles reales sin autorización y controles.

### `examples/`
Demostraciones simples y reproducibles.

### `src/`
Código fuente y lógica compartida del sistema.

## 5. Flujo de desarrollo

```text
Necesidad
   ↓
Issue
   ↓
Branch
   ↓
Diseño / desarrollo
   ↓
Commit
   ↓
Pull Request
   ↓
Revisión
   ↓
Pruebas / evaluación
   ↓
Merge
   ↓
Documentación
   ↓
Release o promoción

┌─────────────────────────────────────────────┐
│ CICLO DE VIDA DE UN COMPONENTE DE IA        │
└─────────────────────────────────────────────┘

ENTRADA: Necesidad institucional
    ↓
PROPUESTA: Define caso de uso + área responsable
    ↓
ANÁLISIS: Classifica riesgo (bajo/medio/alto)
    ↓
DESARROLLO: Crea prompt/modelo/agente
    ↓
PRUEBAS: Ejecuta test cases + evaluación
    ↓
REVISIÓN: ✓ Técnica ✓ Metodológica ✓ Ética ✓ Datos
    ↓
APROBACIÓN: Decisión formal (sí/restricción/no)
    ↓
IMPLEMENTACIÓN CONTROLADA: Monitoreo en producción
    ↓
SEGUIMIENTO: Métricas + incidentes
```

El nivel de control debe ser proporcional al riesgo e impacto del cambio.

## 6. Relación entre componentes

```text
                 ┌──────────────┐
                 │    Datos     │
                 └──────┬───────┘
                        │
                        ▼
┌───────────┐     ┌──────────────┐     ┌─────────────┐
│  Prompts  │────►│    Agentes   │────►│  Resultados │
└─────┬─────┘     └──────┬───────┘     └──────┬──────┘
      │                  │                    │
      └──────────────►┌──▼─────────┐           │
                      │   Modelos  │           │
                      └─────┬──────┘           │
                            ▼                  ▼
                     ┌──────────────────────────┐
                     │       Evaluaciones       │
                     └──────────────────────────┘
```

`infra/` proporciona el entorno de ejecución y `src/` la lógica de software que integra los componentes cuando corresponda.

## 7. Seguridad y gobernanza

Los controles de seguridad, privacidad, ética y gobernanza son transversales. Como mínimo:

- no almacenar secretos en Git;
- minimizar datos personales;
- documentar fuentes y condiciones de uso de datos;
- registrar limitaciones conocidas;
- evaluar componentes relevantes antes del uso operativo;
- mantener supervisión humana en procesos de riesgo;
- registrar decisiones arquitectónicas significativas.

## 8. ADR

Las decisiones que modifiquen relaciones importantes entre componentes, integraciones, seguridad, gobernanza o tecnologías estructurales deben evaluarse para su registro en:

```text
docs/arquitectura/adr/
```

## 9. Estados de madurez

Debe distinguirse entre:

- **Propuesto:** definido pero no implementado.
- **En desarrollo:** implementación en construcción.
- **Experimental:** en evaluación.
- **Validado:** cuenta con evidencia suficiente para su propósito.
- **Operativo:** autorizado para el entorno correspondiente.
- **Deprecado:** no debe utilizarse para nuevos desarrollos.
- **Archivado:** se conserva principalmente por trazabilidad.

## 10. Referencias

- [Componentes](componentes.md)
- [Integraciones](integraciones.md)
- [Gobernanza](gobernanza.md)
- [Decisiones arquitectónicas](adr/)
