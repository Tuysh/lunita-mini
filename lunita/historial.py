from groq.types.chat import ChatCompletionMessageParam


class Historial:
    def __init__(
        self, mensajes: list[ChatCompletionMessageParam] = [], max_mensajes: int = 20
    ):
        self._mensajes: list[ChatCompletionMessageParam] = mensajes
        self._max_mensajes = max_mensajes

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        return self._mensajes

    @historial.setter
    def historial(self, valor: list[ChatCompletionMessageParam]):
        if len(valor) > self._max_mensajes:
            self._mensajes = valor[-self._max_mensajes :]
            return

        self._mensajes = valor

    def agregar_mensaje(self, *mensajes: ChatCompletionMessageParam) -> None:
        if len(self._mensajes) + len(mensajes) > self._max_mensajes:
            exceso = len(self._mensajes) + len(mensajes) - self._max_mensajes
            self._mensajes = self._mensajes[exceso:]

        self._mensajes.extend(mensajes)
