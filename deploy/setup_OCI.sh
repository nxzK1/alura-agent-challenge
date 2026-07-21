#!/bin/bash
# setup_oci.sh
#
# Script de configuración inicial para desplegar Alura Agent en una
# instancia de OCI (Ubuntu, VM.Standard.E5.Flex / AMD x86_64).
#
# Uso: copiar y pegar cada bloque en la terminal SSH de la instancia,
# o ejecutar el script completo con: bash setup_oci.sh

set -e  # Detiene el script si algún comando falla, en vez de seguir a ciegas

echo "== 1. Actualizando el sistema =="
sudo apt update && sudo apt upgrade -y

echo "== 2. Instalando Python y Git =="
sudo apt install -y python3-venv python3-pip git zstd

echo "== 3. Instalando Ollama (x86_64) =="
curl -fsSL https://ollama.com/install.sh | sh

echo "== 4. Descargando modelos (mismo usado en local) =="
ollama pull gemma3:4b
ollama pull nomic-embed-text

echo "== 5. Clonando el repositorio =="
git clone https://github.com/nxzK1/alura-agent-challenge.git
cd alura-agent-challenge-main

echo "== 6. Creando entorno virtual e instalando dependencias =="
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "== 7. Configurando variables de entorno =="
cp .env.example .env

echo "== Listo =="
echo "Recuerda subir tus PDFs a data/ desde tu máquina local con scp,"
echo "y luego correr: uvicorn src.api:app --host 0.0.0.0 --port 8000"