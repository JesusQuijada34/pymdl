#!/usr/bin/env python
import os
import hashlib
import datetime
from pathlib import Path

# 🎨 Colores simples
C = {
    "reset": "\033[0m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "cyan": "\033[96m",
    "bold": "\033[1m"
}
def color(txt, t): return f"{C.get(t, '')}{txt}{C['reset']}"

# 🔍 Filtrar archivos por fecha y hora
def archivos_actuales(ruta):
    ahora = datetime.datetime.now()
    hoy = ahora.date()
    hora = ahora.hour
    archivos = []
    for f in os.listdir(ruta):
        r = Path(ruta) / f
        if r.is_file():
            mod = datetime.datetime.fromtimestamp(r.stat().st_mtime)
            if mod.date() == hoy and mod.hour == hora:
                archivos.append((r, mod))
    return sorted(archivos, key=lambda x: x[1], reverse=True)

# 🔐 Hash MD5 + SHA256
def calcular_hashes(ruta):
    md5 = hashlib.md5()
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        while chunk := f.read(8192):
            md5.update(chunk)
            sha.update(chunk)
    return md5.hexdigest(), sha.hexdigest()

# 🚀 Interfaz simple
def main():
    print(color("[🧮] pyMDL — Verificador de HASH automático", "cyan"))
    entrada = input(color("[📁] Ruta del directorio (enter para usar tu carpeta personal): ", "yellow")).strip()
    carpeta = entrada if entrada else str(Path.home())
    print(color(f"[📂] Analizando: {carpeta}", "yellow"))
    if not os.path.isdir(carpeta):
        print(color("[❌] Ruta no válida.", "red"))
        return

    archivos = archivos_actuales(carpeta)
    if not archivos:
        print(color("[⛔️] No hay archivos en esta hora.", "red"))
        return

    print(color("[🕒] Archivos modificados en la hora actual:", "cyan"))
    for i, (r, mod) in enumerate(archivos):
        print(f"{color(f'[{i}]', 'green')} {r.name} — {mod.strftime('%H:%M:%S')}")

    try:
        idx = int(input(color("[👉] Elige el número del archivo: ", "yellow")))
        archivo = archivos[idx][0]
    except:
        print(color("[⚠️] Selección inválida.", "red"))
        return

    print(color(f"[🔍] Analizando: {archivo.name}", "cyan"))
    md5, sha = calcular_hashes(archivo)
    print(color("[📌] MD5    → ", "red") + md5)
    print(color("[📌] SHA256 → ", "red") + sha)
    print(color("[✅] Proceso completo.", "green"))

if __name__ == "__main__":
    main()

