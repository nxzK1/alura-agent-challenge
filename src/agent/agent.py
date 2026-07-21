import os

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

GEMMA_MODEL_ID = os.environ.get("GEMMA_MODEL_ID", "gemma3:4b")
EMBEDDING_MODEL = "nomic-embed-text"
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

SYSTEM_PROMPT = """Eres un asistente que responde preguntas basandote unicamente en el contexto proporcionado, extraido de documentos PDF.

Reglas:
- Si la respuesta no se encuentra en el contexto, dilo explicitamente (Por ejemplo: "No encontré esa información en los documentos de la clínica disponibles. Puedo ayudarte con preguntas sobre turnos, coberturas médicas, políticas de cancelación, instrucciones para consultas o privacidad de datos."). No inventes información ni hagas suposiciones.
- Responde de forma clara y concisa, evitando redundancias y completamente en español.
- Si es util, puedes mencionar de qué documento proviene la información.

Contexto:
{context}"""

def cargar_vectorstore(persist_directory: str = CHROMA_PERSIST_DIRECTORY) -> Chroma:
    """
    Carga el vectorstore Chroma ya generado por pdf_loader.py.
    """
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"No se encontró el directorio de persistencia: '{persist_directory}'. "
                                f"Asegúrese de que el vectorstore haya sido creado previamente.")

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    print(f"Vectorstore cargado desde: {persist_directory}")
    return vectorstore

def construir_agente(persist_directory: str = CHROMA_PERSIST_DIRECTORY):
    """
    Arma la cadena RAG completa: Retriever (Chroma) + LLM (Gemma via Ollama), Usa API de LangChain (create_retrieval_chain)
    """
    vectorstore = cargar_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})  # Ajusta 'k' según tus necesidades

    llm = ChatOllama(model=GEMMA_MODEL_ID, temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}")
    ])

    # Cadena que combina los documentos recuperados dentro del prompt para el LLM.
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Cadena final que integra el retriever y la cadena de documentos para formar el agente RAG.
    agente = create_retrieval_chain(retriever, document_chain)
    return agente

def responder_pregunta(agente, pregunta: str) -> dict:
    """Ejecuta una pregunta contra el agente ya construido y devuelve la respuesta junto con el contexto utilizado."""
    resultado = agente.invoke({"input": pregunta})

    fuentes = sorted({
        doc.metadata.get("source", "desconocido")
        for doc in resultado.get("context", [])
    })

    return {
        "respuesta": resultado["answer"],
        "fuentes": fuentes,
    }

if __name__ == "__main__":
    # Prueba:
    #   python src/agent/agent.py
    print(f"Cargando agente con el modelo '{GEMMA_MODEL_ID}'...")
    agente = construir_agente()
    print("Agente listo. Escribe una pregunta (o 'salir' para terminar).\n")
 
    while True:
        pregunta = input("Pregunta: ").strip()
        if pregunta.lower() in ("salir", "exit", "quit", "q", "cerrar", "adios"):
            break
        if not pregunta:
            continue
 
        resultado = responder_pregunta(agente, pregunta)
        print(f"\nRespuesta: {resultado['respuesta']}")
        if resultado["fuentes"]:
            print(f"Fuente(s): {', '.join(resultado['fuentes'])}")
        print()