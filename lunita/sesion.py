from .cliente import nuevo_cliente
from .configuracion import ConfigurarEstrellas
from groq.types.chat import ChatCompletionMessageParam


class Sesion:
    def __init__(self, configuracion: ConfigurarEstrellas):
        self._configuracion = configuracion
        self._historial: list[ChatCompletionMessageParam] = (
            self._configuracion.historial
        )
        self._cliente = nuevo_cliente(self._configuracion.token)

    def predecir(self, entrada: str) -> str | None:
        try:
            respuesta = self._cliente.chat.completions.create(
                model=self._configuracion.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": self._configuracion.prompt(),
                    },
                    *self._historial,
                    {"role": "user", "content": entrada},
                ],
                temperature=self._configuracion.temperatura,
            )

            prediccion = respuesta.choices[0].message.content

            self._historial.append({"role": "user", "content": entrada})
            self._historial.append({"role": "assistant", "content": prediccion})

            return prediccion
        except Exception as e:
            raise RuntimeError(f"Error al obtener predicción: {e}") from e

    @property
    def historial(self) -> list[ChatCompletionMessageParam]:
        return self._historial

    @historial.setter
    def historial(self, valor: list[ChatCompletionMessageParam]):
        self._historial = valor
