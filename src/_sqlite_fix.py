"""
Parche para un problema conocido de Chroma en Linux: algunas distribuciones
(como Ubuntu) traen preinstalada una versión de sqlite3 más antigua que la
mínima que Chroma requiere (>= 3.35.0), lo que genera:

    RuntimeError: Your system has an unsupported version of sqlite3.

La solución es reemplazar el módulo sqlite3 de Python por el que trae el
paquete `pysqlite3-binary` (una versión moderna, empaquetada aparte).

Este archivo debe importarse ANTES que cualquier import de chromadb o
langchain_chroma — por eso se importa como primera línea en pdf_loader.py,
agent.py y api.py.

En Windows (donde este problema no ocurre) o si el paquete no está
instalado, el import falla silenciosamente y no se hace nada — así el
mismo código sirve tanto para desarrollo local como para la instancia OCI.
"""

try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    # pysqlite3-binary no está instalado (ej. en Windows local, donde no
    # hace falta)
    pass