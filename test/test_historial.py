from groq.types.chat import ChatCompletionMessageParam

from lunita.historial import Historial


def test_historial_inicializacion():
    h = Historial()
    assert h is not None
    assert isinstance(h, Historial)


def test_historial_agregar_mensaje():
    h = Historial()
    h.agregar_mensaje({"role": "user", "content": "Hola!"})
    h.agregar_mensaje({"role": "assistant", "content": "Segunda entrada"})

    entradas = h.historial
    assert len(entradas) == 2
    assert entradas[0] == {"role": "user", "content": "Hola!"}
    assert entradas[1] == {"role": "assistant", "content": "Segunda entrada"}


def test_historial_agregar_multiples_mensajes():
    h = Historial()
    mensajes: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "Mensaje 1"},
        {"role": "assistant", "content": "Respuesta 1"},
        {"role": "user", "content": "Mensaje 2"},
    ]

    h.agregar_mensaje(*mensajes)

    entradas = h.historial
    assert len(entradas) == 3
    assert entradas == mensajes
    assert entradas[0] == {"role": "user", "content": "Mensaje 1"}
    assert entradas[1] == {"role": "assistant", "content": "Respuesta 1"}
    assert entradas[2] == {"role": "user", "content": "Mensaje 2"}


def test_historial_maximo_entradas_metodo():
    h = Historial(max_mensajes=3)

    mensajes: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "Mensaje 1"},
        {"role": "assistant", "content": "Respuesta 1"},
        {"role": "user", "content": "Mensaje 2"},
        {"role": "assistant", "content": "Respuesta 2"},
    ]

    for msg in mensajes:
        h.agregar_mensaje(msg)

    entradas = h.historial
    assert len(entradas) == 3
    assert entradas == mensajes[1:]


def test_historial_maximo_entrada_asignacion():
    h = Historial(max_mensajes=2)

    mensajes: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "Mensaje 1"},
        {"role": "assistant", "content": "Respuesta 1"},
        {"role": "user", "content": "Mensaje 2"},
    ]

    h.historial = mensajes

    entradas = h.historial
    assert len(entradas) == 2
    assert entradas == mensajes[1:]
