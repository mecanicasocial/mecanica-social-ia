# Harness de evaluación

## 1. Propósito

El harness es el **mecanismo reproducible** para ejecutar casos de prueba contra un componente de IA (prompt, modelo, agente u otro), calcular métricas y emitir un resultado trazable.

Este documento define el **contrato de diseño** del harness previsto en:

```text
evaluations/harness.py
```

La implementación en código es opcional hasta que exista un entorno autorizado; **la evaluación institucional no se considera cumplida solo por existir el script**. Debe haber casos, criterios, umbrales, registro de resultado y revisión humana según el riesgo.

## 2. Principios

1. **Evidencia antes de promoción.** Un componente no pasa a uso operativo solo porque una respuesta parezca plausible.
2. **Reproducibilidad.** Misma versión de componente, casos y configuración deben permitir comprender cómo se obtuvo el resultado.
3. **Separación de responsabilidades.** El harness ejecuta y mide; no aprueba institucionalmente.
4. **Sin secretos ni PII real.** Entradas de prueba preferentemente sintéticas; ver `DATA_GOVERNANCE.md` y `SECURITY.md`.
5. **Métricas adecuadas al propósito.** No imponer BLEU/ROUGE cuando el objetivo sea extracción estructurada, seguridad o equidad.
6. **Fallo seguro.** Si no hay modelo configurado, el harness puede validar estructura y casos en modo *offline*, pero no debe declarar “aprobado para producción” solo con ese modo.
7. **Trazabilidad.** Todo run deja un artefacto en `evaluations/resultados/` (o referencia equivalente) con metadatos mínimos.

## 3. Ubicación y relación con el repositorio

| Artefacto | Rol |
|---|---|
| `evaluations/harness.md` | Contrato y diseño (este documento) |
| `evaluations/harness.py` | Implementación de referencia (cuando exista) |
| `evaluations/metricas.md` | Catálogo de métricas y umbrales orientativos |
| `evaluations/resultados.md` | Formato y gobernanza de resultados |
| `evaluations/resultados/` | Salidas de corridas (agregadas, sin PII; carpeta al archivar la primera) |
| `evaluations/_plantilla-resultado.json` | Plantilla de esquema de resultado |
| `evaluations/casos-prueba.md` | Norma de suites |
| `evaluations/casos-prueba/` | Suites YAML reutilizables (cuando existan) |
| `prompts/*.yaml` | Metadatos, ejemplos y criterios del prompt |
| `experiments/` | Exploración; no sustituye evaluación formal |

**Nota (P0):** se eliminó el borrador mal ubicado `prompts/.evaluations/test-casos-intake.yaml` (Python con extensión `.yaml` que podía sugerir “aprobado para producción” sin medir el modelo). El harness canónico y los casos de prueba viven **solo** bajo `evaluations/`, nunca bajo `prompts/`.

## 4. Alcance funcional

El harness debe poder, en su forma objetivo:

1. Cargar la definición del componente (p. ej. prompt YAML).
2. Cargar una suite de casos de prueba.
3. Ejecutar cada caso en uno de estos modos:
   - **offline / estructural:** valida formato de casos, JSON esperado, campos obligatorios del componente; no llama a un modelo.
   - **modelo:** envía el prompt + input a un proveedor configurado **fuera del repositorio** (credenciales nunca en Git).
   - **replay:** compara salidas previamente capturadas (fixtures sintéticas) para regresión.
4. Calcular métricas declaradas en el componente o en la suite.
5. Contrastar umbrales de aceptación.
6. Emitir un resultado estructurado (ver `resultados.md`).
7. Devolver código de salida útil para CI: `0` si la corrida técnica terminó y los umbrales evaluables se cumplieron; distinto de `0` si falló la ejecución o umbrales.

## 5. Entradas

### 5.1 Componente

Ejemplo de invocación objetivo:

```text
python evaluations/harness.py \
  --component prompts/formulario-intake-v1.0.0.yaml \
  --suite evaluations/casos-prueba/intake-test-set.yaml \
  --mode offline \
  --output evaluations/resultados/
```

### 5.2 Suite de casos (YAML)

Campos mínimos recomendados:

```yaml
id: intake-test-set
version: 0.1.0
componente_objetivo: formulario-intake
descripcion: Casos sintéticos para extracción estructurada de solicitudes.
datos_clasificacion: sintetica
casos:
  - id: caso-001
    descripcion: Datos completos de ejemplo sintético
    input: |
      Texto sintético de formulario...
    expected:
      nombre: "..."
      email: "..."
      telefono: "..."
      interes: "..."
    tags: [feliz, json]
  - id: caso-002
    descripcion: Campo faltante
    input: |
      ...
    expected:
      email: "NO_PROPORCIONADO"
    tags: [edge]
```

Reglas:

- Sin datos personales reales.
- `expected` puede ser objeto, texto o criterios (`contains`, `json_schema`, `forbid_fields`).
- Cada caso tiene `id` estable entre versiones de la suite.

### 5.3 Configuración de ejecución (no sensible)

```yaml
# evaluations/config.example.yaml  (ejemplo; no credenciales)
mode: offline   # offline | model | replay
model_ref: null # p. ej. models/<nombre> cuando exista config
thresholds_override: {}
seed: null
max_cases: null
```

Las API keys se leen solo de variables de entorno o del gestor de secretos institucional, nunca del YAML versionado.

## 6. Flujo interno

```text
CLI / CI
   ↓
Cargar componente + suite + config
   ↓
Validar esquema y política de datos (sin PII en repo)
   ↓
Para cada caso:
   ├─ Construir entrada (prompt_text + input)
   ├─ Obtener salida (offline skip | modelo | fixture)
   ├─ Aplicar métricas del caso / suite / componente
   └─ Registrar detalle del caso
   ↓
Agregar métricas globales
   ↓
Comparar umbrales
   ↓
Escribir resultado en evaluations/resultados/
   ↓
Código de salida + resumen humano
```

## 7. Contrato de la implementación `harness.py`

### 7.1 Responsabilidades

| Módulo / área | Responsabilidad |
|---|---|
| Carga | Leer YAML/JSON de componente y suite |
| Ejecutores | Offline, modelo, replay |
| Métricas | Delegar en funciones documentadas en `metricas.md` |
| Reporte | Serializar resultado según `resultados.md` |
| CLI | Argumentos, códigos de salida, mensajes claros |

### 7.2 API interna orientativa

```text
load_component(path) -> Component
load_suite(path) -> Suite
run_case(component, case, mode, ctx) -> CaseResult
compute_metrics(case_result, definitions) -> dict
aggregate(results) -> Summary
write_result(summary, path) -> Path
main(argv) -> int
```

### 7.3 Lo que el harness **no** hace

- No otorga estado institucional `aprobado`.
- No sustituye revisión ética, de datos o de seguridad.
- No envía datos reales a proveedores no autorizados.
- No imprime secretos ni PII en logs.
- No inventa *ground truth* ni marca éxito si no hubo evaluación real del comportamiento del modelo cuando el modo lo requiere.

### 7.4 Modo offline (alcance honesto)

El modo offline puede verificar:

- que el YAML del componente es válido;
- que los ejemplos/casos tienen `input` y `expected`;
- que `expected` cumple formato (p. ej. JSON parseable);
- que campos de metadatos mínimos existen (id, version, nivel_riesgo, datos_prohibidos, etc.).

El modo offline **no** demuestra exactitud de extracción del modelo. Cualquier resumen debe etiquetarse:

```text
modo: offline
alcance: estructural
apto_para_aprobacion_operativa: false
```

## 8. Integración con el ciclo de gobernanza

```text
Desarrollo del componente
        ↓
Definición de casos y métricas
        ↓
Ejecución del harness (prueba)
        ↓
Resultado en evaluations/resultados/
        ↓
Revisión técnica / metodológica / ética / datos (según riesgo)
        ↓
Decisión: prueba | aprobado | restringido | rechazo
```

Umbrales de métricas son **insumo** de la decisión, no la decisión.

## 9. Criterios de aceptación del propio harness

Se considerará usable como herramienta de apoyo cuando:

1. Documentación (este archivo + métricas + resultados) esté alineada con `GOVERNANCE.md` y `DATA_GOVERNANCE.md`.
2. Exista al menos una suite sintética de ejemplo bajo `evaluations/casos-prueba/`.
3. La implementación, si existe, corra en modo offline sin red y sin secretos.
4. Los resultados generados cumplan el esquema de `resultados.md`.
5. Quede explícito en cada run el modo y si basta o no para promoción.

## 10. Estado

| Elemento | Estado |
|---|---|
| Diseño / contrato (`harness.md`) | Documentado |
| Implementación `harness.py` | Pendiente / no requerida para cerrar el diseño |
| Suites de casos | Estructura prevista; contenido inicial mínimo opcional |
| CI smoke-test (offline, sin secretos) | Pendiente de diseño/implementación |
| CI job **model** (inferencia con proveedor) | Pendiente **intencional** (PEND-004): solo con secrets de **organización** en el repo canónico; **no** en forks. Ver `docs/arquitectura/pendientes-intencionales.md` |

## 11. Referencias

- `evaluations/README.md`
- `evaluations/metricas.md`
- `evaluations/resultados.md`
- `docs/arquitectura/componentes.md`
- `docs/arquitectura/arquitectura-general.md`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `AI_ETHICS.md`
- `SECURITY.md`
