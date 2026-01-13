"""Configuración de las conversaciones con Lunita.

Este módulo maneja todos los ajustes necesarios para hablar con Lunita,
como el token de acceso, el modelo y el historial previo.
"""

from dataclasses import dataclass, field
from typing import Optional

from groq.types.chat import ChatCompletionMessageParam

from .constantes import PROMPT_LUNITA


@dataclass
class ConfigurarEstrellas:
    """Ajustes para personalizar tu conversación con Lunita.

    Esta clase guarda toda la información necesaria para crear una sesión
    con Lunita, de forma estructurada y limpia.

    Args:
        token: Tu clave de API de Groq para poder usar Lunita.
        modelo: Nombre del modelo de Groq a usar (default: "openai/gpt-oss-120b").
        historial: Lista de mensajes previos si quieres continuar una conversación.
        instrucciones_adicionales: Texto extra para personalizar la personalidad.
        max_mensajes: Número máximo de mensajes a guardar en el historial.
        temperatura: Nivel de creatividad de las respuestas.
    """

    token: str
    modelo: str = "openai/gpt-oss-120b"
    historial: list[ChatCompletionMessageParam] = field(
        default_factory=list[ChatCompletionMessageParam]
    )
    instrucciones_adicionales: Optional[str] = None
    max_mensajes: int = 15
    temperatura: float = 1.1

    def __post_init__(self):
        """Valida y ajusta los valores después de la inicialización."""
        if not self.token or not self.token.strip():
            raise ValueError("El token no puede estar vacío.")

        # Aseguramos que el historial sea una copia independiente
        if self.historial:
            self.historial = list(self.historial)

    def prompt(self) -> str:
        """Obtiene las instrucciones que definen la personalidad de Lunita.

        Returns:
            Texto con las instrucciones del sistema para Lunita.
        """
        extra = (
            f"\nINSTRUCCIONES ADICIONALES\n{self.instrucciones_adicionales}"
            if self.instrucciones_adicionales
            else ""
        )
        return f"{PROMPT_LUNITA}{extra}"
