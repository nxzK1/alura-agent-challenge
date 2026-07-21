# Deploy — Alura Agent (OCI)

Instancia: Ubuntu 22.04, shape `VM.Standard.E5.Flex` (AMD x86_64), pagada con crédito de prueba OCI (no Always Free — hubo "out of capacity" en Ampere A1, E3 y E4).

## Pasos

1. Crear la instancia en OCI (VM.Standard.E5.Flex, imagen Ubuntu).
2. Abrir el puerto 8000 en la Security List de la subnet (regla de Ingress: `0.0.0.0/0`, TCP, puerto 8000).
3. Conectarse por SSH:
```bash
   ssh -i ~/.ssh/id_ed25519 ubuntu@<IP_PUBLICA>
```
4. Ejecutar `setup_oci.sh` (ver este mismo directorio) — instala Python, Git, Ollama, descarga los modelos, clona el repo e instala dependencias.
5. Subir los PDFs desde la máquina local (no viajan por Git, están en `.gitignore`):
```bash
   scp -i ~/.ssh/id_ed25519 data/*.pdf ubuntu@<IP_PUBLICA>:~/alura-agent/data/
```
6. Levantar la API:
```bash
   source venv/bin/activate
   uvicorn src.api:app --host 0.0.0.0 --port 8000
```
   (`--host 0.0.0.0` es necesario para aceptar conexiones externas, no solo desde la propia instancia.)

## Enlace / captura de la app funcionando

> _Se completará una vez validado el deploy: `http://<IP_PUBLICA>:8000/docs`_