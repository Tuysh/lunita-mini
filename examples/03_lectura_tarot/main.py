import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv

from lunita import ConfigurarEstrellas, Sesion

load_dotenv()
token = os.getenv("TOKEN")

INSTRUCCIONES_TAROT = """
IMPORTANTE: Estás en modo "Lectura de Tarot".
1. Cada vez que respondas, debes mencionar que estás sacando una carta específica (inventa el nombre, ej: "El Gato Invertido", "La Cuchara de Plata").
2. Tu interpretación debe ser dramática pero terminar siendo absurdamente optimista.
3. Usa emojis relacionados con magia y cartas (🃏, ✨, 🔮).
"""


def main():
    print("🃏 --- Lectura de Tarot con Lunita --- 🃏")

    if not token:
        print("❌ Falta el TOKEN.")
        return

    # 1. Configuración Personalizada
    config = ConfigurarEstrellas(
        token=token,
        modelo="llama-3.1-8b-instant",  # Usamos un modelo potente si es posible, o el default
        temperatura=1.5,  # Muy alta creatividad para que invente cartas locas
        instrucciones_adicionales=INSTRUCCIONES_TAROT,
        max_mensajes=5,  # Historial corto para lecturas puntuales
    )

    sesion = Sesion(config)

    print("Lunita está barajando las cartas... 🔀")
    time.sleep(1)

    while True:
        consulta = input("\n🃏 ¿Qué quieres preguntar a las cartas? (o 'salir'): ")

        if consulta.lower() in ["salir", "exit"]:
            break

        print("\nSacando carta... 🖐️")
        time.sleep(1)

        respuesta = sesion.predecir(consulta)
        print(f"\n🔮 Interpretación:\n{respuesta}")


if __name__ == "__main__":
    main()
