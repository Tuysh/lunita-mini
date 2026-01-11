import os
import sys
from contextlib import asynccontextmanager

# Hack para importar lunita desde el repo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lunita import ConfigurarEstrellas, ErroresMagicos, SesionAsincrona

load_dotenv()


# --- Modelos de Datos ---
class Consulta(BaseModel):
    mensaje: str


class Respuesta(BaseModel):
    prediccion: str


# --- Estado Global ---
# En una app real, gestionaríamos sesiones por usuario,
# pero aquí usaremos una sesión global simple.
sesion_global = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio: Configurar Lunita
    global sesion_global
    token = os.getenv("TOKEN")
    if not token:
        print("ADVERTENCIA: No se encontró TOKEN. La API fallará.")
    else:
        config = ConfigurarEstrellas(token=token)
        sesion_global = SesionAsincrona(config)
        print("Lunita lista para recibir peticiones vía Web!")

    yield

    # Cierre: Limpieza si fuera necesaria
    print("Lunita se va a dormir.")


app = FastAPI(title="API de Lunita", lifespan=lifespan)


@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de Lunita. Ve a /docs para probar."}


@app.post("/consultar", response_model=Respuesta)
async def consultar_oraculo(consulta: Consulta):
    global sesion_global

    if not sesion_global:
        raise HTTPException(
            status_code=500, detail="Lunita no está configurada (falta TOKEN)."
        )

    try:
        # Usamos el modo asíncrono pero recolectamos todo el texto
        # (no streaming) para devolver un JSON simple.
        texto_completo = ""
        async for fragmento in sesion_global.predecir(consulta.mensaje):
            texto_completo += fragmento

        return Respuesta(prediccion=texto_completo)

    except ErroresMagicos as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")


if __name__ == "__main__":
    import uvicorn

    # Ejecuta el servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)
