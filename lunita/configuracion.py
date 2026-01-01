from typing import Literal

from groq.types.chat import ChatCompletionMessageParam

from .constantes import PROMPT_LUNITA


class ConfigurarEstrellas:
    def __init__(
        self,
        token: str,
        modo: Literal["normal", "avanzado"] = "normal",
        historial: list[ChatCompletionMessageParam] = [],
    ):
        self.token = token
        self._temperatura = 1.1
        self._historial = historial

        self._modelo = (
            "openai/gpt-oss-120b" if modo == "avanzado" else "openai/gpt-oss-20b"
        )

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        return self._historial

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def temperatura(self) -> float:
        return self._temperatura

    def prompt(self) -> str:
        return PROMPT_LUNITA
