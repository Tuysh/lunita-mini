"""Manejo de conversaciones sincrónicas con Lunita.

Este módulo permite crear conversaciones con Lunita de forma directa,
esperando cada respuesta antes de continuar.
"""

from groq.types.chat import ChatCompletionMessageParam

from .cliente import nuevo_cliente
from .configuracion import ConfigurarEstrellas
from .historial import Historial
from .utils import APIStatusError, ErroresMagicos


class Sesion:
    """Crea y maneja una conversación con Lunita.

    Usa esta clase cuando quieras hablar con Lunita de forma normal,
    esperando su respuesta antes de enviar el siguiente mensaje.

    Examples:
        Crear una conversación básica:

        >>> from lunita import Sesion, ConfigurarEstrellas
        >>> config = ConfigurarEstrellas(token="tu-token-aqui")
        >>> sesion = Sesion(config)
        >>> respuesta = sesion.predecir("Hola Lunita, ¿cómo estás?")
        >>> print(respuesta)

        Conversar varias veces y ver el historial:

        >>> respuesta1 = sesion.predecir("¿Puedes leerme el tarot?")
        >>> respuesta2 = sesion.predecir("¿Qué significa?")
        >>> print(f"Mensajes intercambiados: {len(sesion.historial)}")

    Args:
        configuracion: Objeto con los ajustes de la conversación (token, modo, etc.)
    """

    def __init__(self, configuracion: ConfigurarEstrellas):
        self._configuracion = configuracion
        self._historial: Historial = Historial(mensajes=configuracion.historial)
        self._cliente = nuevo_cliente(self._configuracion.token)

    def predecir(self, entrada: str) -> str | None:
        """Envía un mensaje a Lunita y espera su respuesta.

        Args:
            entrada: El mensaje que quieres enviarle a Lunita.

        Returns:
            La respuesta de Lunita como texto, o None si algo salió mal.

        Raises:
            RuntimeError: Si hubo un problema al conectarse o recibir la respuesta.

        Examples:
            >>> respuesta = sesion.predecir("Necesito un consejo")
            >>> print(respuesta)
        """
        try:
            respuesta = self._cliente.chat.completions.create(
                model=self._configuracion.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": self._configuracion.prompt(),
                    },
                    *self._historial.historial,
                    {"role": "user", "content": entrada.strip()},
                ],
                temperature=self._configuracion.temperatura,
            )

            prediccion = respuesta.choices[0].message.content

            self._historial.agregar_mensaje(
                {"role": "user", "content": entrada},
                {"role": "assistant", "content": prediccion},
            )

            return prediccion
        except APIStatusError as http_err:
            raise ErroresMagicos(http_err) from http_err
        except Exception as e:
            raise RuntimeError(
                f"!Error desconocido¡ Ni lunita puede adivinar que fue: {e}"
            ) from e

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        """Obtiene todos los mensajes intercambiados en esta conversación.

        Returns:
            Lista con todos los mensajes (tuyos y de Lunita) en orden.

        Examples:
            >>> print(f"Total de mensajes: {len(sesion.historial)}")
        """
        return self._historial.historial
