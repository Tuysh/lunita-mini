"""Manejo de conversaciones asincrónicas con Lunita.

Este módulo permite crear conversaciones con Lunita sin bloquear tu programa,
ideal para aplicaciones web o cuando necesitas hacer varias cosas a la vez.
"""

from collections.abc import AsyncGenerator

from .cliente import nuevo_cliente_asincrono
from .configuracion import ConfigurarEstrellas
from .sesion_base import SesionBase
from .utils import APIStatusError, ErroresMagicos


class SesionAsincrona(SesionBase):
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
        super().__init__(configuracion)
        self._cliente = nuevo_cliente_asincrono(self._configuracion.token)

    async def predecir(self, entrada: str) -> AsyncGenerator[str, None]:
        """Envía un mensaje a Lunita y espera su respuesta de forma asincrónica.

        Args:
            entrada: El mensaje que quieres enviarle a Lunita.

        Returns:
            Generador asincrónico que yield fragmentos de la respuesta de Lunita como texto.

        Raises:
            RuntimeError: Si hubo un problema al conectarse o recibir la respuesta.

        Examples:
            >>> async for fragmento in sesion.predecir("Dame un consejo"):
            ...     print(fragmento, end="")
        """
        try:
            stream = await self._cliente.chat.completions.create(
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
                stream=True,
            )

            respuesta_completa = ""

            async for fragmento in stream:
                contenido = fragmento.choices[0].delta.content or ""

                if contenido:
                    respuesta_completa += contenido
                    yield contenido

            self._historial.agregar_mensaje(
                {"role": "user", "content": entrada},
                {"role": "assistant", "content": respuesta_completa},
            )

        except APIStatusError as http_err:
            raise ErroresMagicos(http_err) from http_err
        except Exception as e:
            raise RuntimeError(
                f"!Error desconocido¡ Ni lunita puede adivinar que fue: {e}"
            ) from e
