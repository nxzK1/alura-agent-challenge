# Deploy — Alura Agent (OCI)

Instancia: Ubuntu 24.04, shape `VM.Standard.E5.Flex` (AMD x86_64), pagada con crédito de prueba OCI (no Always Free — hubo "out of capacity" en Ampere A1, E3 y E4). Ubuntu 24.04 trae Python 3.12 por defecto, necesario para `langchain-classic` (requiere >= 3.10; con Ubuntu 20.04 y Python 3.9 esto falla).

**IP pública actual:** `159.112.146.116` (puede cambiar si la instancia se detiene y se vuelve a iniciar).

## Pasos

1. Crear la instancia en OCI (`VM.Standard.E5.Flex`, imagen **Ubuntu 24.04**).
2. Abrir los puertos 8000 (API) y 8501 (interfaz Streamlit) en **dos capas de firewall distintas** (ambas son necesarias):
   - **Security List de OCI** (nivel de red virtual): subnet de la instancia → Security Lists → Add Ingress Rules → Source `0.0.0.0/0`, TCP, puerto `8000` — y repetir la regla para el puerto `8501`.
   - **iptables del sistema operativo** (las imágenes Ubuntu de OCI traen reglas que bloquean todo excepto el puerto 22 por defecto):
     ```bash
     sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
     sudo iptables -I INPUT -p tcp --dport 8501 -j ACCEPT
     sudo apt install -y iptables-persistent
     sudo netfilter-persistent save
     ```
3. Conectarse por SSH:
   ```bash
   ssh -i ~/.ssh/id_ed25519 ubuntu@<IP_PUBLICA>
   ```
4. Ejecutar `setup_oci.sh` (ver este mismo directorio) — instala Python, Git, `zstd` (requerido por el instalador de Ollama), Ollama, descarga los modelos, clona el repo, crea el entorno virtual (`.venv`) e instala las dependencias con versiones fijas (`requirements.txt`).
5. Subir los PDFs desde la máquina local:
   ```bash
   scp -i ~/.ssh/id_ed25519 data/*.pdf ubuntu@<IP_PUBLICA>:~/alura-agent-challenge/data/
   ```
6. Generar la base vectorial y probar el agente:
   ```bash
   source .venv/bin/activate
   python src/document_loader/pdf_loader.py
   python src/agent/agent.py
   ```
7. Configurar la API como servicio persistente con `systemd`:
   ```bash
   sudo nano /etc/systemd/system/alura-agent.service
   ```
   Contenido:
   ```ini
   [Unit]
   Description=Alura Agent API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/alura-agent-challenge
   ExecStart=/home/ubuntu/alura-agent-challenge/.venv/bin/uvicorn src.api:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
   Activar:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable alura-agent
   sudo systemctl start alura-agent
   sudo systemctl status alura-agent   # debe decir "active (running)"
   ```
8. Configurar la interfaz web (MIA, Streamlit) como un **segundo servicio systemd independiente** — corre en su propio puerto (8501) y llama a la API por HTTP, así que puede reiniciarse o fallar sin afectar a la API:
   ```bash
   sudo nano /etc/systemd/system/alura-agent-webapp.service
   ```
   Contenido:
   ```ini
   [Unit]
   Description=Alura Agent Webapp (MIA - Streamlit)
   After=network.target alura-agent.service

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/alura-agent-challenge
   Environment="API_URL=http://localhost:8000"
   ExecStart=/home/ubuntu/alura-agent-challenge/.venv/bin/streamlit run src/webapp/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
   Activar:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable alura-agent-webapp
   sudo systemctl start alura-agent-webapp
   sudo systemctl status alura-agent-webapp
   ```
   Nota: `API_URL=http://localhost:8000` funciona porque ambos servicios corren en la misma instancia

## Problemas encontrados durante el deploy (y su solución)

Logs reales porque fue un proceso real de prueba y error, no un camino directo:

| Problema | Causa | Solución |
|---|---|---|
| `RuntimeError: unsupported version of sqlite3` | Ubuntu trae una versión de sqlite3 más antigua que la que Chroma requiere | Parche con `pysqlite3-binary` en `pdf_loader.py` y `agent.py` (solo se activa en Linux) |
| `TypeError: 'type' object is not subscriptable` (posthog) | El entorno virtual se creó con Python 3.8, insuficiente para sintaxis moderna de tipos | Usar Python 3.10+ (Ubuntu 24.04 ya trae 3.12) |
| `ModuleNotFoundError: langchain_classic` | LangChain movió `create_retrieval_chain` a un paquete separado (`langchain-classic`), que además requiere Python >= 3.10 | Agregar `langchain-classic` a `requirements.txt` y usar Python 3.10+ |
| API no accesible desde el navegador pese a estar corriendo | Firewall interno (`iptables`) de la imagen Ubuntu de OCI, además de la Security List | Abrir el puerto también con `iptables -I INPUT ...` |

## Importante: la instancia es de pago (crédito de prueba)

A diferencia de Always Free, esta instancia consume el crédito de $300 (vigente hasta el 31 de agosto) mientras esté **"Running"**. Se detiene (Stop) desde la consola cuando no está en uso activo, y se reinicia (Start) para retomar — el disco y todo lo instalado persisten entre paradas, solo cambia la IP pública al reiniciar.

## Enlace / captura de la app funcionando

- **Interfaz web (MIA):** `http://159.112.146.116:8501`
- **Swagger UI (API):** `http://159.112.146.116:8000/docs`
- Ver capturas en [`../docs/images/`](../docs/images/)