"""Lógica de búsqueda de normas (sin dependencias externas)."""
import json
import unicodedata
from pathlib import Path

RUTA_DATOS = Path(__file__).parent / "data" / "normas.json"

TEMAS = {
    "espacios": "Espacios públicos",
    "planificacion": "Planificación urbana",
    "diseno": "Diseño y habilitación",
    "municipal": "Gestión municipal",
}


def cargar_normas(ruta=RUTA_DATOS):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def normalizar(texto):
    """Minúsculas y sin tildes: 'Áreas' -> 'areas'."""
    texto = unicodedata.normalize("NFD", str(texto or "").lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.split())


def tokens(consulta):
    return [t for t in normalizar(consulta).split(" ") if t]


def puntuar(norma, palabras):
    """0 = no coincide. Todas las palabras deben aparecer en algún campo."""
    if not palabras:
        return 1
    campos = [
        (normalizar(norma.get("numero")), 8),
        (normalizar(norma.get("titulo")), 5),
        (normalizar(" ".join(norma.get("palabras", []))), 4),
        (normalizar(f"{norma.get('tipo', '')} {norma.get('entidad', '')}"), 2),
        (normalizar(norma.get("resumen")), 1),
    ]
    total = 0
    for palabra in palabras:
        mejor = max((peso for texto, peso in campos if palabra in texto), default=0)
        if mejor == 0:
            return 0
        total += mejor
    return total


def buscar(normas, texto="", tema=None, tipo=None, solo_verificadas=False):
    palabras = tokens(texto)
    resultados = []
    for n in normas:
        if tema and tema not in n["temas"]:
            continue
        if tipo and n["tipo"] != tipo:
            continue
        if solo_verificadas and not n.get("verificado"):
            continue
        p = puntuar(n, palabras)
        if p > 0:
            resultados.append((p, n))
    resultados.sort(key=lambda r: (r[0], str(r[1].get("fecha", ""))), reverse=True)
    return [n for _, n in resultados]
