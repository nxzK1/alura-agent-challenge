# Arquitectura — Alura Agent

## Visión general

Alura Agent combina dos patrones de IA distintos según el tipo de documento cargado:

- **PDF → RAG (Retrieval-Augmented Generation):** el documento se divide en fragmentos, se convierte en vectores (embeddings) y se almacena en una base vectorial. Cuando el usuario pregunta, se recuperan los fragmentos más relevantes y se envían al modelo como contexto.
- **CSV → Agente con herramientas (tool use):** en vez de "buscar texto parecido", el agente ejecuta operaciones reales sobre los datos (con Pandas) para responder preguntas analíticas (promedios, filtros, agrupaciones).

## Etapa 1 — Procesamiento de documentos

- `pdf_loader.py`: extrae texto de PDFs con `pypdf`, lo divide en fragmentos (chunks) y genera embeddings.
- `csv_loader.py`: carga el CSV con `pandas` y expone funciones que el agente puede invocar como herramientas.

## Etapa 2 — Agente

- Construido con LangChain.
- Combina un *retriever* (para el PDF) con *tools* personalizadas (para el CSV).
- Recibe la pregunta del usuario, decide qué fuente(s) consultar, y genera la respuesta con el modelo de lenguaje (Gemma).

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
  ├── ¿Pregunta sobre el PDF? → Retriever (RAG) → Fragmentos relevantes → LLM
  └── ¿Pregunta sobre el CSV? → Tool (Pandas)   → Resultado calculado  → LLM
  │
  ▼
Respuesta al usuario
```
