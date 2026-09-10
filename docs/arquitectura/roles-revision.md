# Roles de revisión — separación de deberes

## Propósito

Operacionalizar los roles de `GOVERNANCE.md` evitando que la **misma
persona en el mismo acto** sea a la vez única autoría y única aprobación
en cambios de riesgo medio/alto.

## Roles (norma)

| Rol | Qué firma | Independencia |
|---|---|---|
| Autoría | Propósito, pruebas, limitaciones | No aprueba solo |
| Revisión técnica | Funciona, reproducible, seguro a nivel código | Distinta de autoría cuando sea posible |
| Revisión metodológica | Pertinencia, métricas, validez de evidencia | Riesgo medio+ |
| Revisión ética y derechos | Dignidad, sesgo, supervisión humana | Medio+/alto o impacto en personas |
| Revisión de datos y privacidad | Finalidad, minimización, transferencias | Datos personales o proveedores |
| Revisión de seguridad | Secretos, acceso, integraciones, CI | Secretos, INT-*, workflows |
| Área responsable del uso | Contexto autorizado, monitoreo | No sustituible por el modelo |
| Aprobación institucional | Beneficio vs riesgo, controles | No la otorga el harness |

## Asignación actual (transitoria)

Hasta contar con más personas o equipos GitHub:

| Rol | Titular actual | Suplente / cuatro ojos |
|---|---|---|
| Autoría | Quien abre el PR | — |
| Técnica | `@LeodanZapata` | Segundo revisor humano (área usuaria o par) en riesgo medio+ |
| Metodológica | `@LeodanZapata` *(dual)* | Acta con evidencia de suite/resultado |
| Ética | `@LeodanZapata` *(dual)* | Obligatorio declarar conflicto si es autor del mismo cambio |
| Datos/privacidad | `@LeodanZapata` *(dual)* | Idem |
| Seguridad | `@LeodanZapata` *(dual)* | Canal `SECURITY.md` si el hallazgo es suyo |
| Área usuaria | Por componente (p. ej. Formación) | Confirmar en el PR |
| Aprobación institucional | Registro en `docs/gobernanza/registros/` | **No** checkbox único del autor |

### Excepción documentada de rol dual

- **Quién:** `@LeodanZapata`
- **Qué:** concentra titulares de gobernanza en etapa temprana del repo.
- **Límite:** en riesgo **alto**, o cambios de secretos/integraciones/datos
  personales, el autor **no** puede ser el único en el registro de decisión:
  se exige al menos un segundo participante (área usuaria, dirección o par
  institucional) identificado en el registro.
- **Revisión de esta excepción:** en el próximo onboarding de un segundo
  maintainer o al autorizar proveedor productivo (INT-002).

## Matriz por tipo de cambio

| Cambio | Técnica | Metod. | Ética | Datos | Seguridad | Aprob. inst. |
|---|---|---|---|---|---|---|
| Docs menores / typos | ✓ | — | — | — | — | — |
| Prompt riesgo bajo | ✓ | — | checklist corto | — | — | — |
| Prompt riesgo medio | ✓ | ✓ | recomendada | si PII | si hay vendor | registro si se pide `aprobado` |
| Prompt riesgo alto | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Model-card / proveedor | ✓ | ✓ | según datos | ✓ | ✓ | ✓ para `autorizado` |
| INT-001 / INT-002 | ✓ | ✓ | según datos | ✓ | ✓ | ✓ |
| Workflows / secretos CI | ✓ | — | — | — | ✓ | según impacto |
| GOVERNANCE / políticas | ✓ | ✓ | ✓ | según tema | según tema | ✓ |

## CODEOWNERS y equipos (evolución)

Hoy `CODEOWNERS` apunta a `@LeodanZapata` en todas las rutas (etapa temprana).

Objetivo cuando existan handles o teams:

```text
/prompts/     @team-ia-tecnica @team-ia-metodologica
/models/      @team-ia-tecnica @team-ia-datos
/evaluations/ @team-ia-tecnica @team-ia-metodologica
GOVERNANCE.md AI_ETHICS.md DATA_GOVERNANCE.md SECURITY.md  @team-ia-gobernanza
```

No se inventan teams inexistentes en este documento.

## Pull Request

La plantilla de PR exige declarar revisores por rol (aunque el handle
coincida, los **checks son actos distintos** y el registro de decisión
debe listar participantes).

Labels recomendados (cuando se habiliten):

- `riesgo:bajo` | `riesgo:medio` | `riesgo:alto`
- `revision:etica` | `revision:datos` | `revision:seguridad`

## Registro de decisiones

Plantilla: `docs/gobernanza/registros/_plantilla-decision.md`  
Cada aprobación sensible deja un archivo datado **sin PII**.

## Relación con el harness

El harness (`offline` o `model`) **nunca** sustituye un rol de revisión ni
pone `apto_para_aprobacion_operativa: true`.

## Referencias

- `GOVERNANCE.md`
- `DATA_GOVERNANCE.md`
- `CODEOWNERS`
- `NOTICE`
- `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`
- `PRACTICO.md`
