from unittest.mock import MagicMock, patch

from lunita.configuracion import ConfigurarEstrellas
from lunita.sesion import Sesion


@patch("lunita.sesion.nuevo_cliente")
def test_sesion_predecir_actualiza_historial(mock_nuevo_cliente: MagicMock):
    mock_groq = MagicMock()
    mock_nuevo_cliente.return_value = mock_groq
    mock_groq.chat.completions.create.return_value.choices[
        0
    ].message.content = "Respuesta de prueba"

    config = ConfigurarEstrellas(token="token-falso")
    sesion = Sesion(configuracion=config)

    resultado = sesion.predecir("Hola Lunita")

    assert resultado == "Respuesta de prueba"

    assert len(sesion.historial) == 2
    assert sesion.historial[0]["role"] == "user"
    assert sesion.historial[1]["role"] == "assistant"
