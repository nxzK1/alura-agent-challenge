import os
import sys
from contextlib import asynccontextmanager

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from agent.agent import construir_agente, responder_pregunta

load_dotenv()

CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_db")

estado = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta al iniciar y cerrar la aplicación FastAPI. Carga el agente RAG al iniciar."""
    print(f"Cargando agente, esto puede demorar unos segundos...")
    estado["agente"] = construir_agente(CHROMA_PERSIST_DIR)
    print(f"Servidor listo, agente cargado. Puede comenzar a realizar preguntas.")
    yield

app = FastAPI(
    title = "AGENTE MIA - API",
    description = "API del asistente de la Clinica FICIntegra, basada en RAG sobre documentos PDF. Powered by LangChain, Gemma y Ollama.",
    lifespan=lifespan,
)

class PreguntaRequest(BaseModel):
    pregunta: str


class RespuestaResponse(BaseModel):
    respuesta: str
    fuentes: list[str]


@app.get("/salud")
def salud():
    """Chequea de manera simple si el servidor está activo y el agente cargado."""
    return {"status": "ok", "agente_listo": "agente" in estado}

@app.post("/preguntar", response_model=RespuestaResponse)
def preguntar(request: PreguntaRequest):
    """Recibe una pregunta, la ejecuta contra el agente RAG y devuelve la respuesta junto con las fuentes utilizadas."""
    if "agente" not in estado:
        return {"error": "El agente no está cargado. Intente nuevamente más tarde."}
    
    resultado = responder_pregunta(estado["agente"], request.pregunta)
    return RespuestaResponse(respuesta=resultado["respuesta"], fuentes=resultado["fuentes"])