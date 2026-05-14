"""
test_api_publica.py
===================
Pruebas básicas de la API pública de Templates Library.
"""

# =============================================================================
# Carga de librerías
# =============================================================================

from pathlib import Path

import pytest

import templates_library as tl
from templates_library.modulos.proyectos import crear_proyecto
from templates_library.modulos.resultados import (
    crear_estructura_resultados,
    guardar_md,
    listar_resultados,
)
from templates_library.utils import obtener_directorio_templates


# =============================================================================
# Pruebas de API pública
# =============================================================================

def test_api_publica_expone_funciones_principales() -> None:
    """
    Verifica que el paquete raíz exporta las funciones principales.
    """
    assert tl.__version__ == "0.1.0"
    assert callable(tl.crear_proyecto)
    assert callable(tl.guardar_imagen)
    assert callable(tl.guardar_informe)
    assert callable(tl.guardar_md)
    assert callable(tl.listar_resultados)


def test_directorio_templates_empaquetado_existe() -> None:
    """
    Verifica que las plantillas viven dentro del paquete.
    """
    templates = obtener_directorio_templates()

    assert templates.exists()
    assert (templates / "latex_report" / "main.tex").exists()
    assert (templates / "slides_HTML" / "index.html").exists()


def test_crear_proyecto_python(tmp_path: Path) -> None:
    """
    Verifica la creación mínima de un proyecto Python.
    """
    ruta = crear_proyecto("demo_python", tipo="python", directorio_base=tmp_path, verbose=False)

    assert ruta == (tmp_path / "demo_python").resolve()
    assert (ruta / "main.py").exists()
    assert (ruta / "src" / "__init__.py").exists()
    assert (ruta / "README.md").exists()


def test_resultados_markdown(tmp_path: Path) -> None:
    """
    Verifica la creación de carpetas de resultados y guardado de Markdown.
    """
    origen = tmp_path / "nota.md"
    origen.write_text("# Nota\n", encoding="utf-8")

    rutas = crear_estructura_resultados(tmp_path)
    destino = guardar_md(origen, directorio_base=tmp_path)
    resultados = listar_resultados(tmp_path)

    assert rutas["md"].exists()
    assert destino.exists()
    assert destino.parent.name == "Resultados_md"
    assert destino in resultados["md"]


def test_crear_proyecto_rechaza_tipo_invalido(tmp_path: Path) -> None:
    """
    Verifica que un tipo de proyecto desconocido produce ValueError.
    """
    with pytest.raises(ValueError):
        crear_proyecto("demo", tipo="desconocido", directorio_base=tmp_path, verbose=False)
