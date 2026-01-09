# Lunita

Lunita es un SDK que te permite interactuar con una IA temática: una vidente torpe y distraída que siempre interpreta todo de forma optimista. Consulta tu suerte, tus miedos, tus dudas... y obtén respuestas creativas, humorísticas y sorprendentemente sabias.

## Installation

Usa el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar lunita-mini.

```bash
pip install lunita-mini
```

## Requirements

- Python >= 3.10
- [Groq API token](https://console.groq.com/keys) (gratuito)

## Quick Start

```python
import os
from lunita import Sesion, ConfigurarEstrellas
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

# Configuración
config = ConfigurarEstrellas(token=token)

# Crear sesión
sesion = Sesion(configuracion=config)

# Consultar
respuesta = sesion.predecir("¿Qué dice mi suerte hoy?")
print(f"🔮 Lunita: {respuesta}")
```

## Configuration

```python
from lunita import ConfigurarEstrellas

# Configuración básica
config = ConfigurarEstrellas(
    token="tu-groq-api-token",  # Requerido
    modo="normal",              # "normal" (rápido) o "avanzado" (elaborado)
)

# Configuración avanzada
config = ConfigurarEstrellas(
    token="tu-groq-api-token",
    modo="avanzado",
    instrucciones_adicionales="Sé más optimista que nunca",  # Personalización
    historial=[],               # Continuar conversaciones previas
)
```

## Documentation

Para más detalles sobre Lunita, consulta:

- [GitHub Repository](https://github.com/Tuysh/lunita-mini)
- [Project Wiki](https://github.com/Tuysh/lunita-mini/wiki)
- [PyPI Package](https://pypi.org/project/lunita-mini/)

## Contributing

Pull requests son bienvenidos. Para cambios importantes, abre un issue primero para discutir qué te gustaría cambiar.

Asegúrate de actualizar los tests según sea necesario.

## License

[MIT](https://choosealicense.com/licenses/mit/)
