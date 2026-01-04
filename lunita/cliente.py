"""Creación de clientes para conectarse con Groq.

Este módulo crea las conexiones necesarias para comunicarse con la API
de Groq, tanto de forma normal como asincrónica.
"""

from groq import APIStatusError, AsyncGroq, Groq

from .utils import ErroresMagicos


def nuevo_cliente(token: str) -> Groq:
    """Crea un cliente para hacer peticiones normales a Groq.

    Args:
        token: Tu clave de API de Groq.

    Returns:
        Cliente configurado y listo para usar.
    """
    try:
        return Groq(api_key=token)
    except APIStatusError as http_err:
        raise ErroresMagicos(http_err) from http_err
    except Exception as err:
        raise RuntimeError(
            f"!Error desconocido¡ Ni lunita puede adivinar que fue: {err}"
        ) from err


def nuevo_cliente_asincrono(token: str) -> AsyncGroq:
    """Crea un cliente para hacer peticiones asincrónicas a Groq.

    Args:
        token: Tu clave de API de Groq.

    Returns:
        Cliente asincrónico configurado y listo para usar.
    """
    try:
        return AsyncGroq(api_key=token)
    except APIStatusError as http_err:
        raise ErroresMagicos(http_err) from http_err
    except Exception as err:
        raise RuntimeError(
            f"!Error desconocido¡ Ni lunita puede adivinar que fue: {err}"
        ) from err
