import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Agregar el directorio actual al path para importar módulos locales.

from dotenv import load_dotenv

from document_loader.pdf_loader import procesar_pdfs
from agent.agent import construir_agente, responder_pregunta

load_dotenv()  # Cargar variables de entorno desde el archivo .env

DOCUMENTS_DIR = os.environ.get("DOCUMENTS_DIR", "./data")
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_db")

def preparar_base_vectorial(
    documents_dir : str = DOCUMENTS_DIR,
    persist_directory : str = CHROMA_PERSIST_DIR,
) -> None:
    """
    Función para generar la base vectorial si no existe.
    """

    ya_existe = os.path.isdir(persist_directory) and len(os.listdir(persist_directory)) > 0

    if ya_existe:
        print(f"La base vectorial ya existe en '{persist_directory}', se reutilizará sin re-procesar los PDFs.\n")
        return
    
    print(f"No se encontró una base vectorial en '{persist_directory}', Procesando PDFs...\n")
    procesar_pdfs(documents_dir, persist_directory)
    print()

def iniciar_chatbot() -> None:
    """
    Función principal para iniciar el Loop del chatbot por consola.
    """
    print("="*50)
    print(" Bienvenido soy el Asistente virtual de la Clínica FICIntegra - Mia.")
    print("=" * 60)
    print("Escribe tu pregunta sobre la clínica, o 'salir' para terminar.\n")

    agente = construir_agente(CHROMA_PERSIST_DIR)

    while True:
        pregunta = input("Tú: ").strip()

        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("Terminando la conversación. ¡Hasta luego!")
            break
        if not pregunta:
            continue  # Ignorar entradas vacías

        respuesta = responder_pregunta(agente, pregunta)

        print(f"\nMia: {respuesta['respuesta']}")
        if respuesta["fuentes"]:
            print(f"(Fuente: {', '.join(respuesta['fuentes'])})")
        print()

def main() -> None:
    preparar_base_vectorial(DOCUMENTS_DIR, CHROMA_PERSIST_DIR)
    iniciar_chatbot()

if __name__ == "__main__":
    main()