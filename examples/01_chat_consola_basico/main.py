import os
import sys

# Agregamos el directorio raíz al path para poder importar lunita si no está instalada
# Esto es solo para que funcione el ejemplo dentro del repositorio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv

from lunita import ConfigurarEstrellas, ErroresMagicos, Sesion

# Cargamos las variables de entorno (.env)
load_dotenv()
token = os.getenv("TOKEN")


def main():
    print("🌙 --- Chat con Lunita (Sincrónico) --- 🌙")
    print("Escribe 'salir' para terminar la conversación.\n")

    if not token:
        print("❌ Error: No se encontró la variable de entorno 'TOKEN'.")
        print("Asegúrate de tener un archivo .env con tu clave de API de Groq.")
        return

    # 1. Configuración de credenciales y personalidad
    try:
        configuracion = ConfigurarEstrellas(
            token=token,
            temperatura=1.2,  # Un poco más creativa
            instrucciones_adicionales="Eres especialmente amable hoy.",
        )

        # 2. Inicio de sesión con el personaje
        sesion = Sesion(configuracion=configuracion)

    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return

    # 3. Bucle de interacción
    while True:
        try:
            # Solicitar pregunta al usuario
            pregunta = input("\n👤 Tú: ")

            if not pregunta.strip():
                continue

            # Salir si el usuario escribe 'salir'
            if pregunta.lower() in ["salir", "exit", "adios"]:
                print("👋 ¡Hasta luego amiguito!")
                break

            print("⏳ Lunita está consultando los astros...", end="\r")

            # 4. Consulta a la vidente
            respuesta = sesion.predecir(pregunta)

            # Borramos el mensaje de espera
            print(" " * 40, end="\r")

            # Mostrar la respuesta
            print(f"🔮 Lunita: {respuesta}")

        except ErroresMagicos as e:
            print(f"\n✨ Error Mágico: {e}")
        except KeyboardInterrupt:
            print("\n👋 ¡Interrupción detectada! Adiós.")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            break


if __name__ == "__main__":
    main()
