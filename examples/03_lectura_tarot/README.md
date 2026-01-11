# Ejemplo 03: Lectura de Tarot (Personalización)

Este ejemplo demuestra cómo modificar profundamente la personalidad de Lunita usando `ConfigurarEstrellas`. Aquí la convertimos en una tarotista que inventa cartas absurdas.

## Conceptos Clave
- **Instrucciones Adicionales**: Inyectamos reglas específicas en el prompt del sistema.
- **Temperatura Alta (1.5)**: Forzamos al modelo a ser más "alocado" y creativo, ideal para inventar cartas de tarot que no existen.
- **Modelo Específico**: Muestra cómo solicitar un modelo concreto de Groq (ej. `llama-3.1-8b-instant`).

## Ejecución
1. `pip install -r requirements.txt`
2. Configura `.env`
3. `python main.py`

¡Diviértete viendo qué cartas inventa Lunita!
