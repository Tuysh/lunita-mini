from groq.types.chat import ChatCompletionMessageParam

from lunita.configuracion import ConfigurarEstrellas


def test_configuracion_inicializacion():
    c = ConfigurarEstrellas(token="fake_token")

    assert c is not None
    assert isinstance(c, ConfigurarEstrellas)


def test_configuracion_atributos():
    token = "fake_token"

    historial1: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "¡Hola!"}
    ]
    historial2: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "Hola otra vez"}
    ]

    c1 = ConfigurarEstrellas(token=token, modo="avanzado", historial=historial1)
    c2 = ConfigurarEstrellas(token=token, modo="normal", historial=historial2)

    assert c1.token == token
    assert c1.modelo == "openai/gpt-oss-120b"
    assert c1.temperatura == 1.1
    assert c1.historial == historial1

    assert c2.token == token
    assert c2.modelo == "openai/gpt-oss-20b"
    assert c2.temperatura == 1.1
    assert c2.historial == historial2


def test_configuracion_prompt():
    c = ConfigurarEstrellas(token="fake_token")

    assert "Eres Lunita, una joven que actúa como una vidente" in c.prompt()
