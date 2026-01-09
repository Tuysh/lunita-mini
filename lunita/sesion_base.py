"""Base para las conversaciones con Lunita.

Este módulo define la estructura fundamental que todas las sesiones de
conversación deben seguir, asegurando que se comporten de manera consistente.
"""

from abc import ABC, abstractmethod
from typing import Any

from groq.types.chat import ChatCompletionMessageParam

from .configuracion import ConfigurarEstrellas
from .historial import Historial


class SesionBase(ABC):
    """Estructura base para una sesión de conversación.

    Esta clase abstracta define las funciones y propiedades que todas las
    sesiones deben tener, como el historial y la capacidad de predecir.
    No se usa directamente, sino como molde para otras clases.

    Args:
        configuracion: Ajustes para personalizar la conversación.
    """

    def __init__(self, configuracion: ConfigurarEstrellas) -> None:
        self._configuracion = configuracion
        self._historial = Historial(
            mensajes=configuracion.historial, max_mensajes=configuracion.max_mensajes
        )

    @abstractmethod
    def predecir(self, entrada: str) -> Any:
        """Envía un mensaje a Lunita y espera su respuesta.

        Args:
            entrada: El texto que quieres enviar en la conversación.
        """
        pass

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        """Obtiene todos los mensajes intercambiados en esta conversación.

        Returns:
            Lista con todos los mensajes (tuyos y de Lunita) en orden.

        Examples:
            >>> print(f"Total de mensajes: {len(sesion.historial)}")
        """
        return self._historial.historial
