"""Gestión del historial de mensajes en conversaciones.

Este módulo maneja la lista de mensajes intercambiados, manteniendo
solo los más recientes para no sobrecargar la memoria.
"""

from json import dumps
from typing import Optional

from groq.types.chat import ChatCompletionMessageParam

from .constantes import PROMPT_RESUMEN


class Historial:
    """Almacena y administra los mensajes de una conversación.

    Guarda automáticamente solo los mensajes más recientes para no usar
    demasiada memoria. Cuando se llega al límite, elimina los más antiguos.

    Args:
        mensajes: Lista de mensajes previos (opcional).
        max_mensajes: Cantidad máxima de mensajes a recordar (por defecto 20).
    """

    def __init__(
        self,
        mensajes: Optional[list[ChatCompletionMessageParam]] = None,
        max_mensajes: int = 20,
        token: Optional[str] = None,
    ):
        if mensajes is None:
            mensajes = []

        self._mensajes: list[ChatCompletionMessageParam] = (
            mensajes[-max_mensajes:] if len(mensajes) > max_mensajes else mensajes
        )
        self._max_mensajes = max_mensajes
        self._token = token

    def __resumir_historial(self) -> str:
        from .cliente import nuevo_cliente

        cliente = nuevo_cliente(self._token)
        return (
            cliente.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": PROMPT_RESUMEN,
                    },
                    {
                        "role": "user",
                        "content": f"Resumen el siguiente historial de mensajes: {dumps(self._mensajes[0 : self._max_mensajes], indent=2)}",
                    },
                ],
                temperature=0,
            )
            .choices[0]
            .message.content
        )

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        """Obtiene la lista de mensajes almacenados.

        Returns:
            Lista con todos los mensajes guardados.
        """
        return self._mensajes

    @historial.setter
    def historial(self, valor: list[ChatCompletionMessageParam]):
        """Reemplaza todos los mensajes con una nueva lista.

        Si la lista es muy larga, solo guarda los mensajes más recientes.

        Args:
            valor: Nueva lista de mensajes.
        """
        if len(valor) > self._max_mensajes:
            self._mensajes = valor[-self._max_mensajes :]
            if self._token is not None:
                self._mensajes.insert(
                    0,
                    {
                        "role": "user",
                        "content": f"<SYSTEM_NOTE>Contexto de la conversación: {self.__resumir_historial()}</SYSTEM_NOTE>",
                    },
                )
                return

            self._mensajes = valor[-self._max_mensajes :]
            return

        self._mensajes = valor

    def agregar_mensaje(self, *mensajes: ChatCompletionMessageParam) -> None:
        """Añade uno o más mensajes al final del historial.

        Si al agregar se supera el límite, elimina automáticamente
        los mensajes más antiguos para hacer espacio.

        Args:
            *mensajes: Uno o más mensajes para agregar.
        """
        if len(self._mensajes) + len(mensajes) > self._max_mensajes:
            if self._token is not None:
                self._mensajes = [
                    {
                        "role": "user",
                        "content": f"<SYSTEM_NOTE>Contexto de la conversación: {self.__resumir_historial()}</SYSTEM_NOTE>",
                    }
                ]
            else:
                exceso = len(self._mensajes) + len(mensajes) - self._max_mensajes
                self._mensajes = self._mensajes[exceso:]

        self._mensajes.extend(mensajes)
