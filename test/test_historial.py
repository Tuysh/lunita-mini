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


def test_historial_elimina_mensajes_antiguos():
    """Verifica que al superar el límite se eliminan los mensajes más antiguos."""
    h = Historial(max_mensajes=4)

    # Llenar hasta el límite
    mensajes_iniciales: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "M1"},
        {"role": "assistant", "content": "R1"},
        {"role": "user", "content": "M2"},
        {"role": "assistant", "content": "R2"},
    ]
    h.agregar_mensaje(*mensajes_iniciales)

    assert len(h.historial) == 4

    # Agregar uno más para superar el límite
    h.agregar_mensaje({"role": "user", "content": "M3"})

    # Verificaciones
    entradas = h.historial

    # Debe mantener solo los últimos 4 mensajes (elimina el más antiguo)
    assert len(entradas) == 4
    assert entradas[0] == {"role": "assistant", "content": "R1"}
    assert entradas[1] == {"role": "user", "content": "M2"}
    assert entradas[2] == {"role": "assistant", "content": "R2"}
    assert entradas[3] == {"role": "user", "content": "M3"}
