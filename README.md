# Lunita SDK mini

¡Ya está aquí la versión compacta de Lunita!

Conserva toda su esencia de vidente torpe y distraída, pero optimizada para ser mucho más rápida y económica.

## ¿Qué cambia en esta versión?

La principal diferencia radica en la concisión de las respuestas y el consumo de recursos. La versión Mini está diseñada para interacciones directas sin perder el carisma.

**Comparativa de Tokens**

| Caracteristica     | Lunita Estándar               | Lunita Mini                  |
| ------------------ | ----------------------------- | ---------------------------- |
| Tokens por mensaje | ~3,000                        | ~600                         |
| Enfoque            | Narrativa extensa y detallada | Respuestas breves y directas |

### Ejemplos de Respuesta

**Entrada:** ¿Debería desplegar a producción un viernes?


**Lunita Estándar**

```txt
¡Ay no! ✨ E-este... o sea, viernes... producción... yo vi algo pero creo que me confundí con la fecha otra vez.

Vi que el viernes pasado tu código se desplegó perfecto y todos celebraron con pizza, ¿o fue que el próximo viernes va a haber un pequeño errorcito? Ay, no sé si ya pasó o va a pasar... Suspiro.

Bueno... lo único que veo clarito es que alguien va a comer un sándwich de jamón y queso durante el despliegue. 🥪 ¿Eso ayuda? ¿O soy muy rara?

¿Sigues ahí? Es que mi don está más confundido que yo misma hoy. Y-yo creo que mejor pregúntale a alguien que no tenga dislexia temporal como yo...

Pero por si acaso, ¿quieres que saque las cartas del tarot? A veces son más claras que mis visiones revueltas. 🔮
```

**Lunita Mini**

```txt
mmm... el tarot dice que el viernes es el día de la luna llena de… ah, espera, eso es el “Tarot de los Gatos”. 😹 Así que si tu código no se sienta cómodo, mejor espera un par de días y luego conviértelo en un “gatito” en producción. ¡Siempre habrá una solución, amiguito! 🌕✨
```

## Tecnologías y Modelos

Para lograr la eficiencia de Lunita Mini, utilizamos Groq como proveedor de alta velocidad.

- **Modelos base:** `openai/gpt-oss-120b` y `openai/gpt-oss-20b`.

- **Arquitectura:** Se eliminó la dependencia de Pydantic, ya que esta versión no requiere el uso de herramientas (tool use), lo que aligera la carga del SDK.

## Guía de Uso

Integrar la versión Mini en tu proyecto es muy sencillo:

```python
import os
from lunita import Sesion, ConfigurarEstrellas
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

def main():
    if not token:
        print("Error: No se encontró el token de acceso.")
        return

    # Configuración de credenciales
    configuracion = ConfigurarEstrellas(token=token)

    # Inicio de sesión con el personaje
    sesion = Sesion(configuracion=configuracion)

    # Consulta a la vidente
    respuesta = sesion.predecir("¿Qué dice mi suerte hoy?")

    print(f"🔮 Respuesta de Lunita: {respuesta}")

if __name__ == "__main__":
    main()
```
