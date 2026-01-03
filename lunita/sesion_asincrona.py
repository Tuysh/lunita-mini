from groq.types.chat import ChatCompletionMessageParam

from .cliente import nuevo_cliente_asincrono
from .configuracion import ConfigurarEstrellas
from .historial import Historial


class SesionAsincrona:
    def __init__(self, configuracion: ConfigurarEstrellas):
        self._configuracion = configuracion
        self._historial: Historial = Historial()
        self._cliente = nuevo_cliente_asincrono(self._configuracion.token)

    async def predecir(self, entrada: str) -> str | None:
        try:
            respuesta = await self._cliente.chat.completions.create(
                model=self._configuracion.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": self._configuracion.prompt(),
                    },
                    *self._historial.historial,
                    {"role": "user", "content": entrada.strip()},
                ],
                temperature=self._configuracion.temperatura,
            )

            prediccion = respuesta.choices[0].message.content

            self._historial.agregar_mensaje(
                {"role": "user", "content": entrada},
                {"role": "assistant", "content": prediccion},
            )

            return prediccion
        except Exception as e:
            raise RuntimeError(f"Error al obtener predicción: {e}") from e

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        return self._historial.historial
