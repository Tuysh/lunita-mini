"""Creación de clientes para conectarse con Groq.

Este módulo crea las conexiones necesarias para comunicarse con la API
de Groq, tanto de forma normal como asincrónica.
"""

from groq import AsyncGroq, Groq


def nuevo_cliente(token: str) -> Groq:
    """Crea un cliente para hacer peticiones normales a Groq.

    Args:
        token: Tu clave de API de Groq.

    Returns:
        Cliente configurado y listo para usar.
    """
    return Groq(api_key=token)


def nuevo_cliente_asincrono(token: str) -> AsyncGroq:
    """Crea un cliente para hacer peticiones asincrónicas a Groq.

    Args:
        token: Tu clave de API de Groq.

    Returns:
        Cliente asincrónico configurado y listo para usar.
    """
    return AsyncGroq(api_key=token)
