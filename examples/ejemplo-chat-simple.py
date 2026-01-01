import os

from dotenv import load_dotenv

from lunita import ConfigurarEstrellas, Sesion

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

    # Bucle de interacción simple
    while True:
        # Solicitar pregunta al usuario
        pregunta = input("Tú: ")

        # Salir si el usuario escribe 'salir'
        if pregunta.lower() == "salir":
            break

        # Consulta a la vidente
        respuesta = sesion.predecir(pregunta)

        # Mostrar la respuesta
        print(f"🔮 Lunita: {respuesta}")


if __name__ == "__main__":
    main()
