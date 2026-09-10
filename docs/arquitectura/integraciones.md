# Integraciones

## 1. Propósito

Este documento establece cómo se diseñan y documentan las integraciones de `mecanica-social-ia` con otros sistemas, servicios, repositorios y componentes de Mecánica Social.

## 2. Principios

1. **Mínimo privilegio.**
2. **Separación de credenciales.**
3. **Trazabilidad.**
4. **Minimización de datos.**
5. **Validación de entradas y salidas.**
6. **Manejo controlado de errores.**
7. **Versionamiento de interfaces.**
8. **Controles proporcionales al riesgo.**

## 3. Relación con `mecanica-social-escuela`

```text
mecanica-social-escuela
        │
        │ necesidades / casos de uso
        ▼
mecanica-social-ia
        │
        │ capacidades de IA
        ▼
resultados / servicios
```

La implementación concreta deberá definir interfaz, entradas, salidas, autenticación, autorización, errores, versionamiento, datos y responsabilidades.

Existe un contrato **provisional** en `contratos/INT-001-escuela.md` (schema/muestra sintéticos). La confirmación **bilateral** con Escuela sigue pendiente (PEND-002); no inventar API productiva ni elevar el estado a Validada/Operativa sin esa confirmación. Ver `pendientes-intencionales.md`.

No debe asumirse que ambos repositorios deben compartir código directamente.

## 4. Proveedores de modelos

Toda integración con un proveedor externo debería documentar:

- proveedor;
- modelo y versión;
- interfaz;
- finalidad;
- datos enviados y recibidos;
- tratamiento de datos cuando sea relevante;
- autenticación;
- restricciones;
- estrategia ante cambios de versión;
- evaluación correspondiente.

Las credenciales se mantienen fuera del repositorio.

La adopción de un **vendor productivo** y la validación de **INT-002** requieren autorización institucional (PEND-001). No hay proveedor productivo versionado en `models/` hasta ese desbloqueo; ver `pendientes-intencionales.md`.

## 5. Contrato de integración

Una integración estable debería registrar:

```text
Identificador
Propósito
Sistema origen
Sistema destino
Entrada
Salida
Autenticación
Autorización
Errores
Versionado
Datos involucrados
Responsable
Evaluación
```

## 6. Datos en tránsito

Antes de intercambiar información debe determinarse qué datos son necesarios, si contienen información personal o sensible, la autorización para tratarlos, conservación, acceso y protección durante la transmisión.

## 7. Fallos y resiliencia

Cuando corresponda deben considerarse:

- timeouts;
- reintentos controlados;
- límites de uso;
- respuestas inválidas;
- indisponibilidad;
- cambios de API;
- incompatibilidad de versiones;
- registro de errores;
- recuperación.

## 8. Observabilidad

Las integraciones relevantes deberían permitir identificar cuándo ocurrió una operación, qué componente la inició, qué versión participó, qué integración se utilizó y el resultado general.

Los registros no deben exponer secretos ni datos personales innecesarios.

## 9. Inventario inicial

| ID | Sistema origen | Sistema destino | Propósito | Datos | Estado |
|---|---|---|---|---|---|
| INT-001 | Mecánica Social Escuela | Mecánica Social IA | Asistencia en solicitudes de formación (intake) | Texto de solicitud; schema sintético provisional | **Provisional** — ver contrato |
| INT-002 | Mecánica Social IA | Proveedor de modelo | Inferencia para evaluación / futuro uso autorizado | Solo sintéticos hasta autorización | Propuesto (slot `openai-compatible-eval`) |

Estas filas no presuponen integraciones productivas implementadas.

### Contratos versionados

| ID | Documento | Notas |
|---|---|---|
| INT-001 | [`contratos/INT-001-escuela.md`](contratos/INT-001-escuela.md) | Provisional; falta confirmación con Escuela |
| INT-002 | Model-card + `models/openai-compatible-eval/` + ADR-002 | Vendor productivo aún no autorizado |

Schema/muestra sintéticos INT-001:

- `data/schemas/int-001-solicitud-formacion.schema.json`
- `data/samples/int-001-solicitud-formacion.sample.json`

### Notas de bloqueo intencional

- **INT-001** está en estado **Provisional** (contrato y schema sintéticos documentados) hasta **confirmación bilateral** con Escuela. No inventar API productiva ni campos no acordados. Ver `pendientes-intencionales.md` (PEND-002).
- **INT-002** permanece en **Propuesto** hasta **autorización institucional** de vendor productivo, evaluación y validación de la integración. Ver `pendientes-intencionales.md` (PEND-001).

## 10. Cambios

Los cambios relevantes deben gestionarse mediante:

```text
Issue → Branch → Implementación → Evaluación → Pull Request → Revisión → Merge
```

Si modifican una decisión arquitectónica importante, debe considerarse un ADR.

## 11. Estados

Toda integración debe marcarse como:

- Propuesta
- En desarrollo
- Validada
- Operativa
- Deprecada
- Archivada
