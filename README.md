# Alura Agent

Agente de Inteligencia Artificial capaz de recibir y responder preguntas en lenguaje natural sobre documentos propios del usuario (PDF y CSV).

## 🎯 Objetivo

Permitir que un usuario cargue un documento (PDF como fuente principal, CSV como fuente secundaria) y converse con un agente de IA que responde preguntas basándose en el contenido de ese documento.

## 🏗️ Arquitectura

El proyecto se desarrolla en 3 etapas:

1. **Procesamiento de documentos** — Carga de PDF (vía `pypdf`) y CSV (vía `pandas`), y preparación del contenido para que el agente pueda consultarlo.
2. **Construcción del agente** — Agente basado en LangChain que combina:
   - **RAG (Retrieval-Augmented Generation)** para responder preguntas sobre el contenido del PDF.
   - **Ejecución de herramientas** (tool use) para responder preguntas analíticas sobre el CSV (ej. promedios, filtros).
3. **Deploy** — Despliegue del agente en OCI (Oracle Cloud Infrastructure).

> 📄 Ver [`docs/architecture.md`](docs/architecture.md) para el detalle técnico de la arquitectura.

## 🧰 Stack tecnológico

| Componente        | Tecnología                          |
|--------------------|--------------------------------------|
| Lenguaje            | Python                              |
| Framework de agente | LangChain                           |
| Procesamiento PDF   | PyPDF                               |
| Procesamiento CSV   | Pandas                              |
| Modelo de lenguaje  | Gemma (autoalojado, vía Google Colab) |
| Prototipado         | Google Colab                        |
| Deploy              | OCI (Oracle Cloud Infrastructure)   |

## 📁 Estructura del proyecto

```
alura-agent/
├── notebooks/              # Prototipos y experimentos en Colab
├── src/
│   ├── document_loader/    # Etapa 1: carga y procesamiento de PDF/CSV
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

> _Se completará a medida que el agente esté funcional, con capturas de preguntas y respuestas reales._

```
Usuario: ¿De qué trata el documento cargado?
Agente: [respuesta generada por el agente]

Usuario: ¿Cuál es el promedio de la columna "ventas" en el CSV?
Agente: [respuesta generada ejecutando la consulta sobre el CSV]
```

## ☁️ Deploy

> _Se completará en la Etapa 3, con el enlace y/o captura de pantalla de la aplicación funcionando en OCI._

## 📌 Estado del proyecto

- [x] Estructura inicial del repositorio
- [ ] Etapa 1: Carga y procesamiento de documentos
- [ ] Etapa 2: Construcción del agente
- [ ] Etapa 3: Deploy en OCI

## 📄 Licencia

Proyecto educativo desarrollado como parte de un programa de formación.
