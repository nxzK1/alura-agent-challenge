# Alura Agent

Agente de Inteligencia Artificial capaz de recibir y responder preguntas en lenguaje natural sobre documentos PDF propios del usuario.

## 🎯 Objetivo

Permitir que un usuario cargue documentos PDF y converse con un agente de IA que responde preguntas basándose en el contenido de esos documentos.

## 🏗️ Arquitectura

El proyecto se desarrolla en 3 etapas:

1. **Procesamiento de documentos** — Carga de PDF (vía `pypdf`) y preparación del contenido (fragmentación + embeddings) para que el agente pueda consultarlo.
2. **Construcción del agente** — Agente basado en LangChain que usa **RAG (Retrieval-Augmented Generation)** para responder preguntas sobre el contenido de los PDFs, con Gemma como modelo de lenguaje (vía Ollama).
3. **Deploy** — Despliegue del agente en OCI (Oracle Cloud Infrastructure).

> 📄 Ver [`docs/architecture.md`](docs/architecture.md) para el detalle técnico de la arquitectura.

## 🧰 Stack tecnológico

| Componente        | Tecnología                          |
|--------------------|--------------------------------------|
| Lenguaje            | Python                              |
| Framework de agente | LangChain                           |
| Procesamiento PDF   | PyPDF                               |
| Modelo de lenguaje  | Gemma (autoalojado localmente vía Ollama) |
| Entorno de desarrollo | IDE local (VS Code / PyCharm)     |
| Deploy              | OCI (Oracle Cloud Infrastructure)   |

## 📁 Estructura del proyecto

```
alura-agent/
├── notebooks/              # Prototipos y experimentos en Colab
├── src/
│   ├── document_loader/    # Etapa 1: carga y procesamiento de PDF
│   ├── agent/               # Etapa 2: lógica del agente
│   └── app.py                # Punto de entrada local
├── deploy/                 # Etapa 3: configuración de despliegue en OCI
└── docs/                   # Documentación de arquitectura
```

## ⚙️ Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/alura-agent.git
cd alura-agent

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus propias credenciales/rutas

# 5. Ejecutar el agente localmente
python src/app.py
```

## 💬 Ejemplos de uso

> _Se completará con capturas reales de la consola una vez validadas las respuestas finales._

```
Tú: ¿Cuál es la política de cancelación de turnos?
Agente: [respuesta generada por el agente, basada en politica_cancelaciones.pdf]
(Fuente: politica_cancelaciones.pdf)

Tú: ¿Qué coberturas médicas acepta la clínica?
Agente: [respuesta generada por el agente, basada en guia_coberturas_medicas.pdf]
(Fuente: guia_coberturas_medicas.pdf)
```

## ☁️ Deploy

> _Se completará en la Etapa 3, con el enlace y/o captura de pantalla de la aplicación funcionando en OCI._

## 📌 Estado del proyecto

- [x] Estructura inicial del repositorio
- [x] Etapa 1: Carga y procesamiento de documentos (PDF)
- [x] Etapa 2: Construcción del agente (RAG con LangChain + Ollama/Gemma)
- [ ] Etapa 3: Deploy en OCI

## 📄 Licencia

Proyecto educativo desarrollado como parte de un programa de formación.