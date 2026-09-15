# Registro de decisión — `2026-09-15-formulario-intake-prueba`

## Metadatos

| Campo | Valor |
|---|---|
| Fecha (UTC) | 2026-09-15 |
| Componente | `formulario-intake` |
| Versión | `1.0.0` |
| Tipo de cambio | funcional |
| Nivel de riesgo | medio |
| Issue / PR | Issue #13 / PR pendiente |

## Participantes por rol

| Rol | Persona / cargo | ¿Se abstiene? |
|---|---|---|
| Autoría | `@LeodanZapata` | No |
| Revisión técnica | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión metodológica | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión ética | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión de datos | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión de seguridad | `@LeodanZapata` *(dual transitorio)* | No |
| Área usuaria | Por confirmar en PR | — |
| Aprobación institucional | No aplica en esta etapa | — |

## Evidencia examinada

- Suite: `evaluations/casos-prueba/intake-test-set.yaml`
- Resultado harness: `evaluations/resultados/2026-09-15-formulario-intake-v1.0.0-offline.json`
- Modo harness: `offline`
- `apto_para_aprobacion_operativa`: `false`
- Model-card: `models/openai-compatible-eval/model-card.md`

## Riesgos y medidas

- La evaluación offline valida estructura de componente y suite, pero no comportamiento de un modelo.
- La exactitud de extracción, `no_invencion` y resistencia a prompt injection sobre salidas de modelo permanecen pendientes.
- No existe proveedor ni `model_id` autorizado para ejecutar evaluación en modo `model`.
- Se mantienen prohibidos PII real, datos de menores, salud, credenciales e identificadores oficiales.
- La evidencia actual no constituye aprobación operativa.

## Decisión

- [x] prueba
- [ ] aprobado (propósito y contexto limitados)
- [ ] restringido
- [ ] rechazo
- [ ] suspensión

Condiciones:

Mantener `formulario-intake` en estado `prueba`. La evidencia actual permite validar la suite y la ejecución estructural reproducible, pero no permite concluir desempeño de un modelo ni autorización operativa.

Próxima revisión:

Después de disponer de un proveedor/modelo autorizado para evaluación sintética y ejecutar el modo `model`, o ante cambios relevantes en el componente, suite o gobernanza.

## Notas

Sin PII real ni secretos en este archivo.
EOFcat docs/gobernanza/registros/2026-09-15-formulario-intake-prueba.md
cat > docs/gobernanza/registros/2026-09-15-formulario-intake-prueba.md <<'EOF'
# Registro de decisión — `2026-09-15-formulario-intake-prueba`

## Metadatos

| Campo | Valor |
|---|---|
| Fecha (UTC) | 2026-09-15 |
| Componente | `formulario-intake` |
| Versión | `1.0.0` |
| Tipo de cambio | funcional |
| Nivel de riesgo | medio |
| Issue / PR | Issue #13 / PR pendiente |

## Participantes por rol

| Rol | Persona / cargo | ¿Se abstiene? |
|---|---|---|
| Autoría | `@LeodanZapata` | No |
| Revisión técnica | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión metodológica | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión ética | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión de datos | `@LeodanZapata` *(dual transitorio)* | No |
| Revisión de seguridad | `@LeodanZapata` *(dual transitorio)* | No |
| Área usuaria | Por confirmar en PR | — |
| Aprobación institucional | No aplica en esta etapa | — |

## Evidencia examinada

- Suite: `evaluations/casos-prueba/intake-test-set.yaml`
- Resultado harness: `evaluations/resultados/2026-09-15-formulario-intake-v1.0.0-offline.json`
- Modo harness: `offline`
- `apto_para_aprobacion_operativa`: `false`
- Model-card: `models/openai-compatible-eval/model-card.md`

## Riesgos y medidas

- La evaluación offline valida estructura de componente y suite, pero no comportamiento de un modelo.
- La exactitud de extracción, `no_invencion` y resistencia a prompt injection sobre salidas de modelo permanecen pendientes.
- No existe proveedor ni `model_id` autorizado para ejecutar evaluación en modo `model`.
- Se mantienen prohibidos PII real, datos de menores, salud, credenciales e identificadores oficiales.
- La evidencia actual no constituye aprobación operativa.

## Decisión

- [x] prueba
- [ ] aprobado (propósito y contexto limitados)
- [ ] restringido
- [ ] rechazo
- [ ] suspensión

Condiciones:

Mantener `formulario-intake` en estado `prueba`. La evidencia actual permite validar la suite y la ejecución estructural reproducible, pero no permite concluir desempeño de un modelo ni autorización operativa.

Próxima revisión:

Después de disponer de un proveedor/modelo autorizado para evaluación sintética y ejecutar el modo `model`, o ante cambios relevantes en el componente, suite o gobernanza.

## Notas

Sin PII real ni secretos en este archivo.
