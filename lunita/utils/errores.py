"""Manejo de errores con mensajes personalizados de Lunita.

Este módulo convierte los errores técnicos de la API en mensajes
amigables y divertidos que coinciden con la personalidad de Lunita.
"""

from groq import APIStatusError


class ErroresMagicos(Exception):
    """Traduce errores de la API a mensajes divertidos de Lunita.

    Cuando algo sale mal al comunicarse con la API, esta clase
    convierte los códigos de error técnicos en mensajes graciosos
    que encajan con el personaje de Lunita la vidente.

    Examples:
        >>> try:
        ...     # Código que puede fallar
        ...     cliente.chat.completions.create(...)
        ... except APIStatusError as e:
        ...     raise ErroresMagicos(e)
        ...     # Muestra: "¡Uy! Parece que se te olvidó el token mágico..."

    Args:
        http_error: El error original de la API de Groq.
    """

    MENSAJES = {
        400: "¡Ah, caray! Creo que leí las cartas al revés. Tu mensajito llegó un poquito confuso.",
        401: "¡Uy! Parece que se te olvidó el token mágico, los duendes no te dejan pasar.",
        403: "¡Uy! Parece que se te olvidó el token mágico, los duendes no te dejan pasar.",
        404: "¡Oh no! Busqué en mi bola de cristal y en el tarro de galletitas, ¡pero no encontré nada!",
        413: "¡Guau! Ese mensaje es más grande que mi amor por la humanidad. ¡No cabe en mi calderito!",
        422: "Entendí tus palabras, pero mi cabecita se hizo un lío. ¡Es como usar un calcetín de oráculo!",
        429: "¡Ay, me dio un mareo de tantas visiones! Necesito un té de manzanilla.",
        498: "¡Ay, me dio un mareo de tantas visiones! Necesito un té de manzanilla.",
    }

    def __init__(self, http_error: APIStatusError) -> None:
        status = http_error.response.status_code

        if status >= 500:
            mensaje = "¡Oh no! Se me rompió la varita o la bola de cristal se quedó sin pilas."
        else:
            mensaje = self.MENSAJES.get(
                status, f"Algo raro pasó en el cosmos (Error {status})."
            )

        super().__init__(mensaje)
