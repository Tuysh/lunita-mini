"""Utilidades para el manejo de errores.

Este módulo exporta las herramientas para manejar errores
de forma amigable en toda la librería.
"""

from .errores import APIStatusError, ErroresMagicos

__all__ = ["ErroresMagicos", "APIStatusError"]
