from groq import AsyncGroq, Groq


def nuevo_cliente(token: str) -> Groq:
    return Groq(api_key=token)


def nuevo_cliente_asincrono(token: str) -> AsyncGroq:
    return AsyncGroq(api_key=token)
