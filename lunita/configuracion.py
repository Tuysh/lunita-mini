"""Configuración de las conversaciones con Lunita.

Este módulo maneja todos los ajustes necesarios para hablar con Lunita,
como el token de acceso, el modelo y el historial previo.
"""

from typing import Optional

from groq.types.chat import ChatCompletionMessageParam

from .constantes import PROMPT_LUNITA


class ConfigurarEstrellas:
    """Ajustes para personalizar tu conversación con Lunita.

    Esta clase guarda toda la información necesaria para crear una sesión
    con Lunita, como tu token de acceso y qué modelo de IA usar.

    Examples:
        Configuración básica:

        >>> from lunita import ConfigurarEstrellas
        >>> config = ConfigurarEstrellas(token="tu-token-de-groq")

        Configuración con un modelo específico:

        >>> config = ConfigurarEstrellas(
        ...     token="tu-token-de-groq",
        ...     modelo="openai/gpt-oss-20b"
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
        modelo: Nombre del modelo de Groq a usar (default: "openai/gpt-oss-120b").
        historial: Lista de mensajes previos si quieres continuar una conversación.
        instrucciones_adicionales: Texto extra para personalizar la personalidad de Lunita.
        max_mensajes: Número máximo de mensajes a guardar en el historial.
        temperatura: Nivel de creatividad de las respuestas (default 1.1).
    """

    def __init__(
        self,
        token: str,
        modelo: str = "openai/gpt-oss-120b",
        historial: Optional[list[ChatCompletionMessageParam]] = None,
        instrucciones_adicionales: Optional[str] = None,
        max_mensajes: int = 15,
        temperatura: float = 1.1,
    ):
        if not token or not token.strip():
            raise ValueError("El token no puede estar vacío.")

        self.token = token
        self._temperatura = temperatura
        self._historial = historial.copy() if historial is not None else []
        self._instrucciones = instrucciones_adicionales
        self._max_mensajes = max_mensajes
        self._modelo = modelo

    def __repr__(self) -> str:
        return (
            f"ConfigurarEstrellas(modelo='{self._modelo}', "
            f"temperatura={self._temperatura}, "
            f"mensajes_historial={len(self._historial)})"
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
            Nombre del modelo.
        """
        return self._modelo

    @property
    def temperatura(self) -> float:
        """Obtiene el nivel de creatividad de las respuestas.

        Returns:
            Valor numérico de temperatura (mayor = más creativa).
        """
        return self._temperatura

    @property
    def max_mensajes(self) -> int:
        """Obtiene el número máximo de mensajes en el historial.

        Returns:
            Número máximo de mensajes a mantener en el historial.
        """
        return self._max_mensajes

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
