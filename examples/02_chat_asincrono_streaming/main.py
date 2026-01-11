import asyncio
import os
import sys

# Agregamos el directorio raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv

from lunita import ConfigurarEstrellas, ErroresMagicos, SesionAsincrona

load_dotenv()
token = os.getenv("TOKEN")


async def chat_loop():
    print("🌙 --- Chat con Lunita (Asíncrono + Streaming) --- 🌙")
    print("Escribe 'salir' para terminar.\n")

    if not token:
        print("❌ Error: No se encontró la variable de entorno 'TOKEN'.")
        return

    # 1. Configuración
    configuracion = ConfigurarEstrellas(token=token)

    # 2. Sesión Asíncrona
    sesion = SesionAsincrona(configuracion=configuracion)

    while True:
        try:
            # En Python < 3.10 input() bloquea, pero para este ejemplo simple está bien.
            # En una app real usaríamos algo como aioconsole o una interfaz gráfica.
            pregunta = input("\n👤 Tú: ")

            if pregunta.lower() in ["salir", "exit"]:
                break

            print("🔮 Lunita: ", end="", flush=True)

            # 3. Consumo del generador asíncrono (Streaming)
            async for fragmento in sesion.predecir(pregunta):
                print(fragmento, end="", flush=True)

            print()  # Salto de línea al final

        except ErroresMagicos as e:
            print(f"\n✨ Error Mágico: {e}")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            break


def main():
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        print("\n👋 Adios!")


if __name__ == "__main__":
    main()
