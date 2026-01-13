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
    demasiada memoria. Cuando se llega al límite, elimina los más antiguos
    o los resume si se proporciona un token de API.

    Args:
        mensajes: Lista de mensajes previos (opcional).
        max_mensajes: Cantidad máxima de mensajes a recordar (por defecto 20).
        token: Clave de API de Groq para generar resúmenes automáticos (opcional).
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

    def __resumir_historial(
        self, mensajes_a_resumir: Optional[list[ChatCompletionMessageParam]] = None
    ) -> str:
        from .cliente import nuevo_cliente

        if self._token is None:
            return ""

        # Si no se pasan mensajes específicos, usar los actuales (comportamiento fallback)
        if mensajes_a_resumir is None:
            mensajes_a_resumir = self._mensajes

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
                        "content": f"Resumen el siguiente historial de mensajes: {dumps(mensajes_a_resumir, indent=2)}",
                    },
                ],
                temperature=0,
            )
            .choices[0]
            .message.content
            or ""
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
        # Delegamos en agregar_mensaje para mantener la lógica de resumen consistente
        # Limpiamos primero para simular una asignación completa
        self._mensajes = []
        self.agregar_mensaje(*valor)

    def agregar_mensaje(self, *mensajes: ChatCompletionMessageParam) -> None:
        """Añade uno o más mensajes al final del historial.

        Si al agregar se supera el límite, elimina automáticamente
        los mensajes más antiguos o los resume inteligentemente.

        Args:
            *mensajes: Uno o más mensajes para agregar.
        """
        todos_mensajes = list(self._mensajes) + list(mensajes)

        if len(todos_mensajes) <= self._max_mensajes:
            self._mensajes = todos_mensajes
            return

        # Se excede el límite
        if self._token is None:
            # Sin token: Comportamiento simple, recortar los más antiguos
            self._mensajes = todos_mensajes[-self._max_mensajes :]
            return

        # Con token: Comportamiento inteligente (Ventana Deslizante)
        # Estrategia: Mantener los últimos ~50% de mensajes en crudo y resumir el resto.
        # Esto reduce llamadas a la API y preserva el contexto inmediato.

        # Cantidad de mensajes a mantener en texto plano (crudos)
        # Aseguramos al menos 2 para contexto mínimo inmediato, o la mitad del buffer.
        mensajes_a_mantener_count = max(2, self._max_mensajes // 2)

        # Punto de corte: todo lo anterior a esto se resume
        corte = len(todos_mensajes) - mensajes_a_mantener_count

        # Si por alguna razón el corte es negativo o cero (no debería con la lógica arriba),
        # ajustamos para resumir al menos algo si es necesario, o nada.
        if corte <= 0:
            self._mensajes = todos_mensajes[-self._max_mensajes :]
            return

        mensajes_para_resumir = todos_mensajes[:corte]
        mensajes_recientes = todos_mensajes[corte:]

        resumen_texto = self.__resumir_historial(mensajes_para_resumir)

        nuevo_mensaje_resumen: ChatCompletionMessageParam = {
            "role": "user",
            "content": f"<SYSTEM_NOTE>Resumen de conversación previa: {resumen_texto}</SYSTEM_NOTE>",
        }

        self._mensajes = [nuevo_mensaje_resumen] + mensajes_recientes
