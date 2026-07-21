# Arquitectura — Alura Agent

## Visión general

Alura Agent usa el patrón **RAG (Retrieval-Augmented Generation)**: los documentos PDF se dividen en fragmentos, se convierten en vectores (embeddings) y se almacenan en una base vectorial. Cuando el usuario pregunta, se recuperan los fragmentos más relevantes y se envían al modelo como contexto para generar la respuesta.

## Etapa 1 — Procesamiento de documentos

- `pdf_loader.py`: extrae texto de los PDFs con `pypdf`, lo divide en fragmentos (chunks) conservando metadata de origen (archivo y página), y genera embeddings con un modelo servido por Ollama (`nomic-embed-text`).

## Etapa 2 — Agente

- Construido con LangChain (`create_retrieval_chain` + `create_stuff_documents_chain`).
- El retriever busca en la base vectorial (Chroma) los fragmentos más relevantes para la pregunta.
- El modelo de lenguaje (Gemma, vía Ollama) genera la respuesta a partir de esos fragmentos, citando el documento de origen.

## Etapa 3 — Deploy

- Empaquetado del agente como servicio (API o CLI) para ejecución en OCI.
- Se documentará aquí la configuración final una vez completada esta etapa.

## Diagrama de flujo (alto nivel)

```
Usuario
  │
  ▼
Pregunta en lenguaje natural
  │
  ▼
Agente (LangChain)
  │
  ▼
Retriever (Chroma) → Fragmentos relevantes del PDF
  │
  ▼
LLM (Gemma vía Ollama) → Respuesta fundamentada en el contexto
  │
  ▼
Respuesta al usuario (con fuente citada)
```