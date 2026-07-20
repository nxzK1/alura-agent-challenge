import os
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from pypdf import PdfReader

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_PERSIST_DIRECTORY = "./chroma_db"

def cargar_pdfs(directorio: str) -> list:
    """
    Carga todos los archivos .pdf encontrados en 'directorio'.

    Devuelve una lista de objetos Document para LangChain, uno por página.
    cada uno con metadata que incluye al menos:
        - "source": ruta/nombre del archivo PDF de origen
        - "page": número de pagina dentro del archivo PDF
    """
    directorio_path = Path(directorio)
    archivos_pdf = sorted(directorio_path.glob("*.pdf"))

    if not archivos_pdf:
        raise FileNotFoundError(f"No se encontraron archivos PDF en el directorio: '{directorio}'. "
                                f"Asegúrese de que el directorio exista y contenga archivos PDF.")

    documentos = []
    for archivo in archivos_pdf:
        print(f"Cargando PDF: {archivo.name}")
        lector = PdfReader(str(archivo))

        for numero_pagina, pagina in enumerate(lector.pages):
            texto = pagina.extract_text() or ""
            """ Si una pagina no tiene texto extraible (Por ejemplo una imagen sin OCR), se omite y se emite una advertencia."""

            if not texto.strip():
                print(f"Advertencia: La página {numero_pagina + 1} de '{archivo.name}' está vacía o no se pudo extraer texto.")
                continue

            documentos.append(
                Document(
                    page_content=texto,
                    metadata={"source": archivo.name, "page": numero_pagina + 1},
                )
            )
    
    print(f"Total de páginas cargadas: {len(documentos)} (de {len(archivos_pdf)} archivos PDF)")
    return documentos


def fragmentar_documentos(documentos: list) -> list:
    """
    Divide los documentos (Por página) en fragmentos más pequeños para su posterior procesamiento.
    Preservando la metadata original (source, page) en cada fragmento.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators = ["\n\n", "\n", ". ", " ", ""],
    )
    fragmentos = splitter.split_documents(documentos)
    print(f"Total de fragmentos generados: {len(fragmentos)} (de {len(documentos)} páginas originales)")
    return fragmentos

def construir_vectorstore(fragmentos: list, persist_directory: str = DEFAULT_PERSIST_DIRECTORY) -> Chroma:
    """
    Genera embeddings para cada fragmento y los guarda en una base vectorial Chroma persistente en 'persist_directory'.
    """
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    print(f"Generando embeddings usando el modelo '{EMBEDDING_MODEL}'... Esto puede tardar un poco dependiendo del tamaño de los fragmentos.")
    vectorstore = Chroma.from_documents(
        documents=fragmentos,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    print(f"Base vectorial guardada en: {persist_directory}")
    return vectorstore

def procesar_pdfs(directorio: str, persist_directory: str = DEFAULT_PERSIST_DIRECTORY) -> Chroma:
    """
    Función principal para cargar PDFs, fragmentarlos y construir la base vectorial.
    pipeline completo (cargar → fragmentar → generar embeddings → guardar)
    """
    documentos = cargar_pdfs(directorio)
    fragmentos = fragmentar_documentos(documentos)
    vectorstore = construir_vectorstore(fragmentos, persist_directory)
    return vectorstore

if __name__ == "__main__":
    #   python src/document_loader/pdf_loader.py
    directorio_documentos = os.environ.get("DOCUMENTS_DIR", "./data")
    procesar_pdfs(directorio_documentos)