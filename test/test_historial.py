from unittest.mock import MagicMock, patch
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


@patch("lunita.cliente.nuevo_cliente")
def test_historial_resumen_ventana_deslizante(mock_nuevo_cliente):
    # Configurar el mock
    mock_cliente_instance = MagicMock()
    mock_completions = MagicMock()
    mock_create = MagicMock()
    
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Resumen simulado"
    
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    mock_create.return_value = mock_response
    mock_completions.create = mock_create
    mock_cliente_instance.chat.completions = mock_completions
    mock_nuevo_cliente.return_value = mock_cliente_instance

    # Inicializar historial con límite pequeño y token
    h = Historial(max_mensajes=4, token="fake-token")
    
    # Llenar hasta el límite
    mensajes_iniciales: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "M1"},
        {"role": "assistant", "content": "R1"},
        {"role": "user", "content": "M2"},
        {"role": "assistant", "content": "R2"},
    ]
    h.agregar_mensaje(*mensajes_iniciales)
    
    assert len(h.historial) == 4
    
    # Agregar uno más para disparar el resumen
    h.agregar_mensaje({"role": "user", "content": "M3"})
    
    # Verificaciones
    entradas = h.historial
    
    # Lógica esperada:
    # Total temp: 5 [M1, R1, M2, R2, M3]
    # Mantener: max(2, 4//2) = 2. -> [R2, M3]
    # Resumir: [M1, R1, M2]
    # Resultado final: [Resumen, R2, M3] -> Longitud 3
    
    assert len(entradas) == 3
    assert entradas[0]["role"] == "user"
    assert "<SYSTEM_NOTE>Resumen de conversación previa: Resumen simulado</SYSTEM_NOTE>" in str(entradas[0]["content"])
    assert entradas[1] == {"role": "assistant", "content": "R2"}
    assert entradas[2] == {"role": "user", "content": "M3"}
    
    # Verificar que se llamó a la API
    mock_nuevo_cliente.assert_called_once_with("fake-token")
    mock_create.assert_called_once()
