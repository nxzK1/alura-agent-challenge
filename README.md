# Alura Agent

Agente de Inteligencia Artificial capaz de recibir y responder preguntas en lenguaje natural sobre documentos PDF propios del usuario. Se expone al usuario final a través de una interfaz web llamada **MIA** (Asistente Virtual de Clínica FIC-Integra).

## 🎯 Objetivo

Permitir que un usuario cargue documentos PDF y converse con un agente de IA que responde preguntas basándose en el contenido de esos documentos.

## 🏗️ Arquitectura

El proyecto se desarrolla en 3 etapas:

1. **Procesamiento de documentos** — Carga de PDF (vía `pypdf`) y preparación del contenido (fragmentación + embeddings) para que el agente pueda consultarlo.
2. **Construcción del agente** — Agente basado en LangChain que usa **RAG (Retrieval-Augmented Generation)** para responder preguntas sobre el contenido de los PDFs, con Gemma como modelo de lenguaje (vía Ollama).
3. **Deploy** — API con FastAPI + interfaz web con Streamlit (**MIA**), ambas desplegadas en una instancia de OCI, corriendo de forma persistente como servicios `systemd`.

> 📄 Ver [`docs/architecture.md`](docs/architecture.md) para el detalle técnico de la arquitectura.

## 🧰 Stack tecnológico

| Componente             | Tecnología                                    |
|-------------------------|------------------------------------------------|
| Lenguaje                 | Python 3.10+                                  |
| Framework de agente      | LangChain (`langchain` + `langchain-classic`) |
| Procesamiento PDF        | PyPDF                                         |
| Base vectorial           | Chroma                                        |
| Modelo de lenguaje       | Gemma (autoalojado vía Ollama)                |
| API                      | FastAPI + Uvicorn                             |
| Interfaz web             | Streamlit ("MIA")                             |
| Entorno de desarrollo    | IDE local (VS Code)                           |
| Deploy                   | OCI — instancia Ubuntu 24.04, servicios `systemd` |

## 📁 Estructura del proyecto

```
alura-agent-challenge/
├── src/
│   ├── document_loader/    # Etapa 1: carga y procesamiento de PDF
│   │   └── pdf_loader.py
│   ├── agent/               # Etapa 2: lógica del agente (RAG)
│   │   └── agent.py
│   ├── webapp/              # Interfaz web (MIA)
│   │   └── streamlit_app.py
│   ├── app.py                # Punto de entrada local (consola)
|   ├── _sqlite_fix.py        # FixPatch para Linux (solo este SO)
│   └── api.py                # Punto de entrada API (FastAPI, usado en el deploy)
├── .streamlit/
│   └── config.toml           # Tema visual base de la interfaz (MIA)
├── deploy/                 # Etapa 3: scripts y guía de despliegue en OCI
│   ├── setup_oci.sh
│   └── README.md
└── docs/
    ├── images/              # Capturas del agente en funcionamiento
    └── architecture.md      # Detalle técnico de la arquitectura
```

## ⚙️ Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/nxzK1/alura-agent-challenge.git
cd alura-agent-challenge

# 2. Crear entorno virtual
python -m venv .venv
source .venv\Scripts\Activate.ps1   # En Linux: .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus propias rutas/modelo si es necesario

# 5. Descargar los modelos usados por el agente (requiere Ollama instalado)
ollama pull gemma3:4b
ollama pull nomic-embed-text

# 6. Cargar tus PDFs en la carpeta data/, y generar la base vectorial
python src/document_loader/pdf_loader.py

# 7a. Ejecutar el agente por consola (opcional, para pruebas rápidas)
python src/app.py

# 7b. Levantar la API + la interfaz web MIA (dos terminales distintas)
uvicorn src.api:app --reload
streamlit run src/webapp/streamlit_app.py
```

## 💬 Ejemplos de uso

Preguntas reales probadas contra los documentos de la clínica ficticia FIC-Integra:

```
Usuario: ¿Qué debo llevar a mi primera consulta?
Agente: Debe presentar su documento de identidad vigente, la credencial de
su cobertura médica o seguro, y cualquier estudio médico realizado en los
últimos 6 meses.

Tú: ¿Cuántas horas de ayuno necesito antes de un análisis de sangre?
Agente: Se requiere un ayuno estricto de 8 horas, permitiendo solo agua
simple en cantidades moderadas.

Tú: ¿Qué pasa si no me presento a mi cita y no aviso?
Agente: Perderá la prioridad para turnos web durante los siguientes 30 días
y deberá abonar el 30% de la consulta antes de agendar un nuevo turno.

Tú: Si tengo cobertura NorteSalud Care y falto a mi cita sin avisar, ¿qué me pasa?
Agente: [respuesta combinando ambos documentos: requisitos de autorización
previa de NorteSalud Care y la sanción por inasistencia]

Tú: ¿Cuál es la capital de Francia?
Agente: No encontré esa información en los documentos de la clínica
disponibles. Puedo ayudarte con preguntas sobre turnos, coberturas médicas,
políticas de cancelación, instrucciones para consultas o privacidad de datos.
```

> En la API (`/preguntar`) la respuesta incluye además el/los PDF(s) de origen. En la interfaz MIA esa información se pide igual, pero no se muestra al usuario final (pensado como una vista más limpia y orientada al paciente).

## ☁️ Deploy

La API y la interfaz web (MIA) están desplegadas en una instancia de OCI, cada una corriendo de forma persistente como su propio servicio `systemd`.

- **Interfaz web (MIA):** `http://159.112.146.116:8501`
- **Documentación interactiva de la API (Swagger UI):** `http://159.112.146.116:8000/docs`
- **Endpoint de salud:** `http://159.112.146.116:8000/salud`

> ⚠️ La instancia se detiene cuando no está en uso activo (para no consumir crédito de nube innecesariamente) — si el enlace no responde, puede que esté detenida en ese momento.

**Capturas del deploy funcionando:**

![API funcionando en OCI](docs/images/deploy-docs.png)

> Ver [`deploy/README.md`](deploy/README.md) para la guía completa paso a paso de cómo se desplegó (creación de la instancia, configuración de red, y puesta en marcha de ambos servicios).

## 📌 Estado del proyecto

- [x] Estructura inicial del repositorio
- [x] Etapa 1: Carga y procesamiento de documentos (PDF)
- [x] Etapa 2: Construcción del agente (RAG con LangChain + Ollama/Gemma)
- [x] Etapa 3: Deploy en OCI (API con FastAPI + interfaz web MIA con Streamlit, ambas como servicios systemd persistentes)

## 📄 Licencia

Proyecto educativo desarrollado como parte de un programa de formación.