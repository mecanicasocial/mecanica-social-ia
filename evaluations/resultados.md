# Resultados de evaluación

## 1. Propósito

Este documento define cómo se **registran, almacenan, interpretan y gobiernan** los resultados de evaluación de componentes de `mecanica-social-ia`.

Los resultados son **evidencia**, no certificación automática de uso institucional.

## 2. Ubicación

```text
evaluations/
├── resultados.md                 ← este documento
├── _plantilla-resultado.json     ← plantilla de esquema (no es corrida real)
└── resultados/                   ← objetivo: corridas reales versionadas
    └── <fecha>-<componente>-<version>-<modo>.json
```

La plantilla canónica actual es:

```text
evaluations/_plantilla-resultado.json
```

Cuando se archive la primera corrida real, conviene mover o copiar resultados bajo `evaluations/resultados/` para no mezclar plantillas con evidencia.

Nombre de archivo recomendado para corridas reales:

```text
YYYY-MM-DD-<componente-id>-v<version>-<modo>.json
```

Ejemplo (solo cuando exista una corrida real):

```text
2026-09-09-formulario-intake-v1.0.0-offline.json
```

## 3. Principios

1. **Sin PII ni secretos** en archivos versionados.
2. **Trazabilidad:** componente, versión, suite, modo, fecha, responsable de la corrida.
3. **Honestidad del alcance:** el modo `offline` no se presenta como prueba de desempeño del modelo.
4. **Separar resultado técnico y decisión institucional.**
5. **Reproducibilidad suficiente:** indicar casos y config no sensible.
6. **No inventar corridas.** Solo se archivan resultados de ejecuciones reales o se mantienen plantillas claramente marcadas.
7. **Retención:** en Git solo agregados y metadatos; logs crudos con datos operativos viven fuera del repositorio.

## 4. Esquema del resultado (JSON)

Campos mínimos:

```json
{
  "schema_version": "1.0.0",
  "resultado_id": "eval-YYYYMMDD-NNN",
  "fecha_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "componente": {
    "tipo": "prompt",
    "id": "formulario-intake",
    "version": "1.0.0",
    "ruta": "prompts/formulario-intake-v1.0.0.yaml",
    "nivel_riesgo_declarado": "medio"
  },
  "suite": {
    "id": "intake-test-set",
    "version": "0.1.0",
    "ruta": "evaluations/casos-prueba/intake-test-set.yaml",
    "n_casos": 0
  },
  "ejecucion": {
    "modo": "offline",
    "harness_ref": "evaluations/harness.md",
    "modelo_ref": null,
    "entorno": "local|ci|otro",
    "semilla": null,
    "ejecutado_por": "rol-o-handle",
    "notas": "Descripción breve del alcance real de la corrida."
  },
  "metricas": [
    {
      "id": "json_valido",
      "nombre": "JSON válido",
      "valor": null,
      "unidad": "porcentaje",
      "umbral": 100,
      "umbral_cumplido": "no_aplicable",
      "metodo": "pendiente",
      "n_casos": 0,
      "limitaciones": "Sin corrida real archivada."
    }
  ],
  "resumen": {
    "n_casos": 0,
    "n_pasados": 0,
    "n_fallidos": 0,
    "tasa_exito_primaria": null,
    "umbrales_obligatorios_ok": false,
    "alcance": "estructural|modelo|mixto|plantilla",
    "apto_para_aprobacion_operativa": false
  },
  "casos_detalle": [],
  "limitaciones": [
    "Plantilla o corrida sin evidencia de modelo."
  ],
  "decision_institucional": {
    "estado": "no_aplicable",
    "referencia": null,
    "notas": "La decisión vive en gobernanza (PR/registro); no la inventa el harness."
  }
}
```

### 4.1 `casos_detalle`

Por caso, solo metadatos no sensibles:

```json
{
  "caso_id": "caso-001",
  "tags": ["feliz"],
  "estado": "pass|fail|skip|error",
  "metricas_locales": {},
  "mensaje": "Razón breve sin copiar el input completo si pudiera ser sensible"
}
```

No reimprimir formularios reales ni salidas con datos personales.

### 4.2 Valores de `decision_institucional.estado`

Alineados al vocabulario de estados del repositorio (uso documental):

| Valor | Significado |
|---|---|
| `no_aplicable` | Solo evidencia técnica; sin acto de aprobación |
| `registrado` | Resultado archivado para revisión |
| `en_prueba` | Componente en evaluación |
| `informativo` | No bloquea ni habilita por sí solo |

Los estados de componente (`borrador`, `prueba`, `aprobado`, …) se actualizan en el artefacto del componente y en el registro de gobernanza, **no** se autoasignan aquí como “aprobado” por un score.

## 5. Interpretación

| Situación | Interpretación correcta |
|---|---|
| Umbrales OK en modo `model` con suite adecuada | Evidencia técnica favorable; falta revisión según riesgo |
| Umbrales OK solo en modo `offline` | Evidencia estructural de metadatos/casos; **no** desempeño del modelo |
| Umbrales fail | No promover; corregir o restringir |
| Sin archivo de resultado | No hay evidencia reproducible en el repo |
| Plantilla sin números reales | No citar como evaluación ejecutada |

## 6. Flujo de archivo de un resultado

```text
1. Ejecutar harness (o protocolo manual documentado)
2. Redactar/generar JSON según este esquema
3. Revisar que no haya PII/secretos
4. Guardar en evaluations/resultados/
5. Referenciar el archivo en el PR del componente
6. Completar revisiones de GOVERNANCE / DATA_GOVERNANCE / AI_ETHICS
7. Registrar decisión fuera del simple score
```

## 7. Resultados y experimentos

| Carpeta | Uso |
|---|---|
| `evaluations/resultados/` | Evidencia formal para criterios de aceptación |
| `experiments/*/results/` | Exploración; puede alimentar una evaluación posterior, no la sustituye |

Un éxito en experimento no es promoción automática.

## 8. Privacidad y seguridad

Antes de commitear un resultado, verificar:

- [ ] No hay correos, teléfonos, RUT u otros identificadores reales
- [ ] No hay tokens ni claves
- [ ] Los `mensaje` de error están redactados
- [ ] La clasificación de datos de la suite es sintética o autorizada
- [ ] Si hubo incidente de exposición, aplicar `SECURITY.md` (canal privado)

## 9. Estado actual del repositorio

- Existe la convención de carpetas, el esquema y el harness offline (P1).
- Las corridas en `evaluations/resultados/` provienen de ejecuciones reales del harness.
- El modo offline deja siempre `apto_para_aprobacion_operativa: false`.
- **No** se archivan corridas inventadas con tasas de éxito ficticias de modelo.

La plantilla versionada `evaluations/_plantilla-resultado.json` sirve para validar forma y para copiar estructura; no es evidencia.
## 10. Referencias

- `evaluations/harness.md`
- `evaluations/metricas.md`
- `evaluations/_plantilla-resultado.json`
- `evaluations/README.md`
- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `SECURITY.md`
