import pytest
from ms_ia.evaluacion import calcular_puntaje_ponderado


def test_puntaje_maximo_aprueba():
    resultado = calcular_puntaje_ponderado(4, 4, 4)
    assert resultado["puntaje_ponderado"] == 4.0
    assert resultado["veredicto"] == "RECOMENDADO_PARA_COMITE"


def test_puntaje_en_el_umbral_exacto_aprueba():
    # 3*0.4 + 3*0.3 + 3*0.3 = 3.0
    resultado = calcular_puntaje_ponderado(3, 3, 3)
    assert resultado["puntaje_ponderado"] == 3.0
    assert resultado["veredicto"] == "RECOMENDADO_PARA_COMITE"


def test_puntaje_justo_bajo_el_umbral_va_a_revision():
    # 3*0.4 + 2*0.3 + 3*0.3 = 2.7
    resultado = calcular_puntaje_ponderado(3, 2, 3)
    assert resultado["puntaje_ponderado"] == 2.7
    assert resultado["veredicto"] == "REVISION_REQUERIDA"


def test_puntaje_bajo_va_a_revision():
    resultado = calcular_puntaje_ponderado(2, 2, 2)
    assert resultado["puntaje_ponderado"] == 2.0
    assert resultado["veredicto"] == "REVISION_REQUERIDA"


@pytest.mark.parametrize("criterios", [
    (None, 4, 4),
    (4, None, 4),
    (4, 4, None),
    (None, None, None),
])
def test_criterio_faltante_fuerza_revision_sin_calcular_puntaje(criterios):
    resultado = calcular_puntaje_ponderado(*criterios)
    assert resultado["puntaje_ponderado"] is None
    assert resultado["veredicto"] == "REVISION_REQUERIDA"


def test_valor_fuera_de_rango_lanza_excepcion():
    with pytest.raises(ValueError):
        calcular_puntaje_ponderado(5, 2, 2)


def test_valor_negativo_lanza_excepcion():
    with pytest.raises(ValueError):
        calcular_puntaje_ponderado(-1, 2, 2)
