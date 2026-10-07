import shutil
import subprocess

from backend.arm64.runtime import AR, AS

LD = 'aarch64-linux-gnu-ld'
QEMU = 'qemu-aarch64'

def herramientas_faltantes():
    return [herramienta for herramienta in (AS, AR, LD, QEMU) if shutil.which(herramienta) is None]

def correr(comando, carpeta):
    return subprocess.run(comando, cwd=carpeta, capture_output=True, text=True)
