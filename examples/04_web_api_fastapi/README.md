# Ejemplo 04: API Web con FastAPI

Este ejemplo muestra cómo integrar **Lunita** en una aplicación web moderna usando **FastAPI**. Exponemos un endpoint REST que recibe preguntas y devuelve las predicciones en formato JSON.

## Estructura
- `main.py`: La aplicación FastAPI.
- `requirements.txt`: Dependencias (incluye fastapi y uvicorn).

## Requisitos
- Python 3.9+
- API Key de Groq.

## Configuración
1. `pip install -r requirements.txt`
2. Crea tu `.env` con `TOKEN=...`

## Ejecución
```bash
python main.py
```
O usando uvicorn directamente:
```bash
uvicorn main:app --reload
```

## Uso
1. Abre tu navegador en `http://localhost:8000/docs`.
2. Busca el endpoint `POST /consultar`.
3. Haz clic en "Try it out".
4. Envía un JSON como:
   ```json
   {
     "mensaje": "¿Encontraré el amor?"
   }
   ```
5. Recibirás una respuesta JSON con la predicción de Lunita.

## Detalles Técnicos
- Usa `SesionAsincrona` para no bloquear el servidor mientras Groq piensa.
- Usa el evento `lifespan` de FastAPI para inicializar la sesión una sola vez al arrancar.
