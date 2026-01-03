"""Manejo de conversaciones asincrónicas con Lunita.

Este módulo permite crear conversaciones con Lunita sin bloquear tu programa,
ideal para aplicaciones web o cuando necesitas hacer varias cosas a la vez.
"""

from groq.types.chat import ChatCompletionMessageParam

from .cliente import nuevo_cliente_asincrono
from .configuracion import ConfigurarEstrellas
from .historial import Historial


class SesionAsincrona:
    """Crea y maneja una conversación asincrónica con Lunita.

    Usa esta clase cuando tu programa necesite hacer otras cosas mientras
    espera la respuesta de Lunita. Perfecto para servidores web o bots.

    Examples:
        Crear una conversación asincrónica:

        >>> import asyncio
        >>> from lunita import SesionAsincrona, ConfigurarEstrellas
        >>>
        >>> async def hablar_con_lunita():
        ...     config = ConfigurarEstrellas(token="tu-token-aqui")
        ...     sesion = SesionAsincrona(config)
        ...     respuesta = await sesion.predecir("Hola Lunita!")
        ...     print(respuesta)
        >>>
        >>> asyncio.run(hablar_con_lunita())

        Manejar múltiples conversaciones a la vez:

        >>> async def varias_consultas():
        ...     config = ConfigurarEstrellas(token="tu-token-aqui")
        ...     sesion = SesionAsincrona(config)
        ...
        ...     # Estas tres se ejecutan al mismo tiempo
        ...     respuestas = await asyncio.gather(
        ...         sesion.predecir("¿Cómo estará el clima?"),
        ...         sesion.predecir("¿Tendré suerte hoy?"),
        ...         sesion.predecir("¿Qué me depara el futuro?")
        ...     )
        ...     for r in respuestas:
        ...         print(r)

    Args:
        configuracion: Objeto con los ajustes de la conversación (token, modo, etc.)
    """

    def __init__(self, configuracion: ConfigurarEstrellas):
        self._configuracion = configuracion
        self._historial: Historial = Historial(mensajes=configuracion.historial)
        self._cliente = nuevo_cliente_asincrono(self._configuracion.token)

    async def predecir(self, entrada: str) -> str | None:
        """Envía un mensaje a Lunita y espera su respuesta de forma asincrónica.

        Args:
            entrada: El mensaje que quieres enviarle a Lunita.

        Returns:
            La respuesta de Lunita como texto, o None si algo salió mal.

        Raises:
            RuntimeError: Si hubo un problema al conectarse o recibir la respuesta.

        Examples:
            >>> respuesta = await sesion.predecir("Dame un consejo")
            >>> print(respuesta)
        """
        try:
            respuesta = await self._cliente.chat.completions.create(
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
        except Exception as e:
            raise RuntimeError(f"Error al obtener predicción: {e}") from e

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        """Obtiene todos los mensajes intercambiados en esta conversación.

        Returns:
            Lista con todos los mensajes (tuyos y de Lunita) en orden.

        Examples:
            >>> print(f"Total de mensajes: {len(sesion.historial)}")
        """
        return self._historial.historial
