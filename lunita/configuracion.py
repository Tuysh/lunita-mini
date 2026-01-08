"""Configuración de las conversaciones con Lunita.

Este módulo maneja todos los ajustes necesarios para hablar con Lunita,
como el token de acceso, el modo de inteligencia y el historial previo.
"""

from typing import Literal, Optional

from groq.types.chat import ChatCompletionMessageParam

from .constantes import PROMPT_LUNITA


class ConfigurarEstrellas:
    """Ajustes para personalizar tu conversación con Lunita.

    Esta clase guarda toda la información necesaria para crear una sesión
    con Lunita, como tu token de acceso y qué tan inteligente quieres que sea.

    Examples:
        Configuración básica:

        >>> from lunita import ConfigurarEstrellas
        >>> config = ConfigurarEstrellas(token="tu-token-de-groq")

        Configuración en modo avanzado (más inteligente):

        >>> config = ConfigurarEstrellas(
        ...     token="tu-token-de-groq",
        ...     modo="avanzado"
        ... )

        Continuar una conversación previa:

        >>> historial_anterior = [
        ...     {"role": "user", "content": "Hola"},
        ...     {"role": "assistant", "content": "¡Hola amiguito!"}
        ... ]
        >>> config = ConfigurarEstrellas(
        ...     token="tu-token-de-groq",
        ...     historial=historial_anterior
        ... )

    Args:
        token: Tu clave de API de Groq para poder usar Lunita.
        modo: "normal" para respuestas rápidas, "avanzado" para respuestas más elaboradas.
        historial: Lista de mensajes previos si quieres continuar una conversación.
        instrucciones_adicionales: Texto extra para personalizar la personalidad de Lunita.
    """

    def __init__(
        self,
        token: str,
        modo: Literal["normal", "avanzado"] = "normal",
        historial: Optional[list[ChatCompletionMessageParam]] = None,
        instrucciones_adicionales: Optional[str] = None,
    ):
        self.token = token
        self._temperatura = 1.1
        self._historial = historial.copy() if historial is not None else []
        self._instrucciones = instrucciones_adicionales

        self._modelo = (
            "openai/gpt-oss-120b" if modo == "avanzado" else "openai/gpt-oss-20b"
        )

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        """Obtiene el historial de mensajes configurado.

        Returns:
            Lista de mensajes que se usarán como contexto inicial.
        """
        return self._historial

    @property
    def modelo(self) -> str:
        """Obtiene el nombre del modelo de IA que se está usando.

        Returns:
            Nombre del modelo (depende del modo elegido).
        """
        return self._modelo

    @property
    def temperatura(self) -> float:
        """Obtiene el nivel de creatividad de las respuestas.

        Returns:
            Valor numérico de temperatura (mayor = más creativa).
        """
        return self._temperatura

    def prompt(self) -> str:
        """Obtiene las instrucciones que definen la personalidad de Lunita.

        Returns:
            Texto con las instrucciones del sistema para Lunita.
        """
        extra = (
            f"\nINSTRUCCIONES ADICIONALES\n{self._instrucciones}"
            if self._instrucciones
            else ""
        )

        prompt_final = f"{PROMPT_LUNITA}{extra}"

        return prompt_final
