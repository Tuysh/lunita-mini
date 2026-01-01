from groq import Groq


def nuevo_cliente(token: str) -> Groq:
    return Groq(api_key=token)
