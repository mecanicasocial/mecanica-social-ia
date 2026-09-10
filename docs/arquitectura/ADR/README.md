# Architecture Decision Records (ADR)

Este directorio contiene las decisiones arquitectónicas relevantes de `mecanica-social-ia`.

## Cuándo crear un ADR

Se recomienda registrar una decisión cuando:

- afecta la estructura general;
- establece una regla que condicionará futuros desarrollos;
- cambia una integración relevante;
- modifica una estrategia de seguridad o gobernanza;
- introduce una tecnología estructural;
- genera consecuencias que conviene conservar para futuras revisiones.

## Convención

```text
ADR-NNN-titulo-corto.md
```

Ejemplo:

```text
ADR-001-arquitectura-inicial.md
```

## Estados

- `Propuesto`
- `Aceptado`
- `Rechazado`
- `Reemplazado`
- `Obsoleto`

## Estructura mínima

```markdown
# ADR-NNN — Título

## Estado

Propuesto

## Fecha

YYYY-MM-DD

## Contexto

## Decisión

## Alternativas consideradas

## Consecuencias

## Implicancias

## Referencias
```

Los ADR registran principalmente **por qué** se tomó una decisión. La documentación arquitectónica explica **cómo** está organizado el sistema.

## Índice

| ADR | Título | Estado |
|---|---|---|
| [ADR-001](ADR-001-arquitectura-inicial-y-mvp-evaluacion.md) | Arquitectura inicial y MVP de evaluación offline | Aceptado |
