"""Ejecutar desde la raíz del proyecto: python tests/test_buscador.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from buscador import TEMAS, buscar, cargar_normas, normalizar  # noqa: E402

NORMAS = cargar_normas()
pruebas = 0


def prueba(nombre):
    def deco(fn):
        global pruebas
        fn()
        pruebas += 1
        print("ok -", nombre)
        return fn
    return deco


@prueba("normalizar quita tildes y mayúsculas")
def _():
    assert normalizar("  Áreas  VERDES ") == "areas verdes"


@prueba("ids únicos y campos obligatorios")
def _():
    ids = set()
    for n in NORMAS:
        assert n["id"] not in ids, n["id"]
        ids.add(n["id"])
        for campo in ("temas", "tipo", "numero", "titulo", "resumen", "entidad", "estado", "url"):
            assert n.get(campo), f"falta {campo} en {n['id']}"
        assert all(t in TEMAS for t in n["temas"]), n["id"]
        assert isinstance(n["verificado"], bool), n["id"]
        assert n["url"].startswith("https://"), n["id"]


@prueba("los cuatro temas tienen normas")
def _():
    for t in TEMAS:
        assert buscar(NORMAS, tema=t), t


@prueba("'areas verdes' encuentra el reglamento de espacios públicos")
def _():
    assert any(n["id"] == "ds-001-2023-vivienda" for n in buscar(NORMAS, "areas verdes"))


@prueba("búsqueda por número")
def _():
    assert buscar(NORMAS, "31199")[0]["id"] == "ley-31199"


@prueba("con y sin tildes da lo mismo")
def _():
    a = [n["id"] for n in buscar(NORMAS, "habilitación urbana")]
    b = [n["id"] for n in buscar(NORMAS, "habilitacion urbana")]
    assert a == b and "ley-29090" in a


@prueba("sin coincidencias devuelve vacío")
def _():
    assert buscar(NORMAS, "zzzxxyy") == []


@prueba("solo verificadas")
def _():
    r = buscar(NORMAS, solo_verificadas=True)
    assert r and all(n["verificado"] for n in r)


@prueba("tema + texto")
def _():
    r = buscar(NORMAS, "ordenanza", tema="municipal")
    assert r and all("municipal" in n["temas"] for n in r)


print(f"\n{pruebas} pruebas pasaron")
