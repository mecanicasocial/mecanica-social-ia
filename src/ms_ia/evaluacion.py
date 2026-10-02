"""Motor de puntaje ponderado para admisión (Fase 0, Paso 2).

Pondera tres criterios (0-4) extraídos por el LLM de admisión y produce
un veredicto determinista. Es una función pura: sin BD, sin HTTP.
Reglas de negocio (acordadas con Leodan, 2026-10-01):
  - Pesos: alineacion_mision 40%, disponibilidad_tiempo 30%, impacto_territorial 30%.
  - Umbral de aprobación: puntaje >= 3.0 -> RECOMENDADO_PARA_COMITE.
  - Si falta cualquier criterio (None), no se calcula puntaje: REVISION_REQUERIDA.
"""
from typing import Optional

UMBRAL_APROBACION = 3.0

PESOS = {
    "alineacion_mision": 0.4,
    "disponibilidad_tiempo": 0.3,
    "impacto_territorial": 0.3,
}


def calcular_puntaje_ponderado(
    alineacion_mision: Optional[int],
    disponibilidad_tiempo: Optional[int],
    impacto_territorial: Optional[int],
) -> dict:
    """Calcula el puntaje ponderado y el veredicto de admisión.

    Si falta cualquier criterio, devuelve REVISION_REQUERIDA sin calcular
    puntaje (puntaje_ponderado queda en None), para no disfrazar una
    extracción incompleta como una evaluación completa.
    """
    criterios = {
        "alineacion_mision": alineacion_mision,
        "disponibilidad_tiempo": disponibilidad_tiempo,
        "impacto_territorial": impacto_territorial,
    }

    if any(valor is None for valor in criterios.values()):
        return {"puntaje_ponderado": None, "veredicto": "REVISION_REQUERIDA"}

    for nombre, valor in criterios.items():
        if not isinstance(valor, int) or not (0 <= valor <= 4):
            raise ValueError(
                f"El criterio '{nombre}' debe ser un entero entre 0 y 4. Recibido: {valor!r}"
            )

    puntaje = sum(criterios[c] * PESOS[c] for c in criterios)
    puntaje_redondeado = round(puntaje, 2)

    veredicto = (
        "RECOMENDADO_PARA_COMITE"
        if puntaje_redondeado >= UMBRAL_APROBACION
        else "REVISION_REQUERIDA"
    )

    return {"puntaje_ponderado": puntaje_redondeado, "veredicto": veredicto}
