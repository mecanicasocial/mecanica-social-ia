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
| INT-001 | Mecánica Social Escuela | Mecánica Social IA | Por definir | Por definir | Propuesto |
| INT-002 | Mecánica Social IA | Proveedor de modelo | Inferencia IA | Por definir | Propuesto |

Estas filas son referencias iniciales y no presuponen integraciones implementadas.

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
