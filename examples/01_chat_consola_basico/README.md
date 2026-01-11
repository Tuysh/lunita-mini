# Ejemplo 01: Chat de Consola Básico

Este es el ejemplo más sencillo de cómo usar **Lunita**. Implementa un chat interactivo en la terminal donde puedes conversar con Lunita y recibir sus predicciones de forma sincrónica (esperando a que termine de generar la respuesta completa).

## Estructura
- `main.py`: El código principal del chat.
- `requirements.txt`: Las librerías necesarias.

## Requisitos
- Python 3.9 o superior.
- Una API Key de Groq.

## Configuración
1. Crea un archivo `.env` en esta carpeta o en la raíz del proyecto con tu token:
   ```env
   TOKEN=gsk_...
   ```

## Ejecución

1. Instala las dependencias (si no tienes instalado el paquete principal):
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el script:
   ```bash
   python main.py
   ```

## Lo que aprenderás
- Cómo inicializar `ConfigurarEstrellas` con tu token.
- Cómo crear una `Sesion` básica.
- Cómo usar el método `predecir()` para enviar y recibir mensajes.
- Cómo manejar excepciones básicas con `ErroresMagicos`.
