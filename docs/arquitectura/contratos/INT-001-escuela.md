# INT-001 — Contrato con `mecanica-social-escuela`

## Estado

**Provisional / propuesto** — pendiente de confirmación bilateral con el
equipo de `mecanica-social-escuela`.  
Este documento **no** inventa endpoints productivos ni aprueba intercambio
de datos reales.

| Campo | Valor |
|---|---|
| ID | INT-001 |
| Origen | Mecánica Social Escuela |
| Destino | Mecánica Social IA |
| Versión contrato | 0.1.0-provisional |
| Fecha | 2026-09-10 |
| Responsable IA (provisional) | `@LeodanZapata` |
| Responsable Escuela | **Por confirmar** |

## 1. Propósito (propuesto)

Permitir que procesos de formación (p. ej. solicitudes de participación /
intake) usen capacidades de IA de este repositorio de forma **asistida**,
con supervisión humana, sin que la IA decida derechos de acceso.

Caso ancla alineado al prompt de prueba:

- Componente IA: `prompts/formulario-intake-v1.0.0.yaml` (estado `prueba`)
- Extracción estructurada de solicitudes sintéticas de formación

## 2. Dirección del flujo (objetivo, no implementado)

```text
Escuela (origen de necesidad / formularios)
        │  payload mínimo autorizado
        ▼
mecanica-social-ia (evaluación / asistencia)
        │  resultado versionado + revisión humana
        ▼
Escuela (consumo del resultado asistido)
```

**Aclaración:** el diagrama de API en documentación histórica es
**aspiracional**. No existe cliente ni OpenAPI implementados en `src/`
hacia Escuela a la fecha de este contrato.

## 3. Entrada (propuesta de negocio — sintética)

Categoría de datos: **solicitud de participación en formación**
(campos alineados al intake).

Esquema de referencia (sintético):

- `data/schemas/int-001-solicitud-formacion.schema.json`
- Muestra: `data/samples/int-001-solicitud-formacion.sample.json`

Campos de negocio propuestos:

| Campo | Tipo | Notas |
|---|---|---|
| `solicitud_id` | string | ID opaco de Escuela; sin PII en el id |
| `texto_formulario` | string | Texto libre de la solicitud |
| `programa_ref` | string | Referencia de programa (no datos de persona) |
| `locale` | string | p. ej. `es-CL` |
| `clasificacion_datos` | enum | `sintetica` \| `autorizada` \| … |

### Datos prohibidos en este contrato provisional

- Menores de edad / datos de estudiantes sin base legal y autorización
- Salud, vulnerabilidad sensible, datos bancarios
- Identificadores oficiales salvo autorización expresa
- Credenciales y secretos

## 4. Salida (propuesta)

Objeto estructurado (JSON) con al menos:

```json
{
  "nombre": "...",
  "email": "...",
  "telefono": "...",
  "interes": "...",
  "meta": {
    "componente_id": "formulario-intake",
    "componente_version": "1.0.0",
    "modelo_ref": null,
    "requiere_revision_humana": true
  }
}
```

Campos faltantes: marcador `NO_PROPORCIONADO` (contrato del prompt).

**Toda salida hacia Escuela requiere revisión humana** antes de usarse
en decisiones o comunicaciones a personas.

## 5. Autenticación y autorización

| Tema | Estado |
|---|---|
| Mecanismo | **Por definir** con Escuela (OIDC, mTLS, token de servicio, etc.) |
| Secretos | Fuera de Git (`infra/secretos-y-entorno.md`, `SECURITY.md`) |
| Mínimo privilegio | Solo la operación de asistencia acordada |
| Entornos | dev / test / prod separados cuando existan |

No se documentan URLs ni credenciales reales aquí.

## 6. Errores y resiliencia (orientativo)

- Timeouts y reintentos limitados
- Respuestas no JSON → error controlado, sin reintento ciego infinito
- Indisponibilidad del modelo → no inventar resultado; degradar a cola humana
- Versionado: cambios breaking de schema = minor/major acordado + aviso

## 7. Evaluación

- Suites sintéticas en `evaluations/casos-prueba/`
- Harness offline y model (`evaluations/harness.py`)
- Umbrales = insumo; **no** aprueban el contrato ni el componente
- Riesgo del caso ancla: **medio** (PII potencial en uso real)

## 8. Supuestos explícitos (marcar al validar)

1. Escuela es la dueña del dato de origen y de la relación con la persona.
2. IA no publica ni notifica directamente a beneficiarios en v0.
3. No hay API REST publicada hoy; el primer paso puede ser **batch manual**
   o copia humana de textos sintéticos/autorizados.
4. Cualquier campo o endpoint real debe confirmarse en Issue conjunta y
   actualizar este documento + fila INT-001 en `integraciones.md`.

## 9. Criterios para pasar de provisional → validado

- [ ] Confirmación escrita de responsables Escuela + IA
- [ ] Schema de entrada/salida acordado (sin campos inventados)
- [ ] Mecanismo de auth definido (sin secretos en Git)
- [ ] Clasificación de datos y retención
- [ ] Prueba con datos sintéticos archivada
- [ ] Revisión de seguridad y datos
- [ ] ADR de integración si el flujo se vuelve estructural

## 10. Referencias

- `docs/arquitectura/integraciones.md`
- `DATA_GOVERNANCE.md`
- `prompts/formulario-intake-v1.0.0.yaml`
- `evaluations/casos-prueba/intake-test-set.yaml`
- ADR-001, ADR-002
