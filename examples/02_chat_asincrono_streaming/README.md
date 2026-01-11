# Ejemplo 02: Chat Asíncrono con Streaming

Este ejemplo muestra cómo usar la capacidad de **streaming** de Lunita. A diferencia del ejemplo básico, aquí las respuestas de Lunita aparecen en la pantalla poco a poco, a medida que se generan, dando una sensación de conversación más natural y rápida.

## Estructura
- `main.py`: Script con bucle asíncrono (`asyncio`).
- `requirements.txt`: Dependencias.

## Requisitos
- Python 3.9+
- API Key de Groq.

## Configuración
1. Configura tu `.env` con `TOKEN=...`

## Ejecución
```bash
python main.py
```

## Conceptos Clave
- **SesionAsincrona**: La clase para operaciones no bloqueantes.
- **Async Generator**: El método `predecir()` devuelve un generador que se consume con `async for`.
- **Streaming**: Verás cómo el texto se imprime fragmento a fragmento.
