#!/usr/bin/env python3
"""
Convierte las landings autónomas (documento HTML completo) en fragmentos
publicables como Artifact de Claude, que envuelve el archivo en su propio
esqueleto <!doctype html><head></head><body>...</body>.

El fragmento conserva <title> y <style> al inicio para que el visor detecte
el nombre de la página y aplique los estilos antes de pintar.

Uso:
    python3 tools/build_artifacts.py [directorio_de_salida]

Salida por defecto: build/
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PAGINAS = ["modelo-1-recorrido-binacional.html", "modelo-2-bento-vertical.html"]


def a_fragmento(html: str) -> str:
    """Extrae title + style + contenido de <body> en ese orden."""
    titulo = re.search(r"<title>.*?</title>", html, re.S)
    estilos = re.findall(r"<style>.*?</style>", html, re.S)
    mapa = re.findall(r'<script type="importmap">.*?</script>', html, re.S)
    cuerpo = re.search(r"<body[^>]*>(.*)</body>", html, re.S)

    if not cuerpo:
        raise ValueError("No se encontró <body> en el documento")

    partes = []
    if titulo:
        partes.append(titulo.group(0))
    partes.extend(estilos)
    partes.extend(mapa)
    partes.append(cuerpo.group(1).strip())
    return "\n\n".join(partes) + "\n"


def main() -> int:
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "build"
    salida.mkdir(parents=True, exist_ok=True)

    for nombre in PAGINAS:
        origen = RAIZ / nombre
        if not origen.exists():
            print(f"  falta {nombre}", file=sys.stderr)
            return 1
        destino = salida / nombre.replace(".html", ".artifact.html")
        destino.write_text(a_fragmento(origen.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"  {nombre} -> {destino}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
