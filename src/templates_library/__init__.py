"""
templates_library
=================
Librería Python para crear proyectos, organizar resultados y convertir
documentos Markdown a LaTeX usando plantillas académicas.

La API pública usa carga perezosa para exponer funciones cómodas sin importar
módulos CLI antes de tiempo.
"""

# =============================================================================
# Carga de librerías
# =============================================================================

from importlib import import_module
from typing import Any


# =============================================================================
# Metadatos y API pública
# =============================================================================

__version__ = "0.1.0"

_EXPORTS = {
    "ConversorMdLatex": ("templates_library.modulos.conversion", "ConversorMdLatex"),
    "TIPOS_PROYECTO": ("templates_library.modulos.proyectos", "TIPOS_PROYECTO"),
    "crear_estructura_resultados": (
        "templates_library.modulos.resultados",
        "crear_estructura_resultados",
    ),
    "crear_proyecto": ("templates_library.modulos.proyectos", "crear_proyecto"),
    "guardar_imagen": ("templates_library.modulos.resultados", "guardar_imagen"),
    "guardar_informe": ("templates_library.modulos.resultados", "guardar_informe"),
    "guardar_md": ("templates_library.modulos.resultados", "guardar_md"),
    "listar_resultados": ("templates_library.modulos.resultados", "listar_resultados"),
    "listar_tipos_disponibles": (
        "templates_library.modulos.proyectos",
        "listar_tipos_disponibles",
    ),
}

__all__ = ["__version__", *_EXPORTS.keys()]


# =============================================================================
# Resolución perezosa de símbolos públicos
# =============================================================================

def __getattr__(name: str) -> Any:
    """
    Resuelve bajo demanda los símbolos de la API pública.

    Funcionalidad:
        Importa el módulo propietario solo cuando el usuario accede al símbolo.
        Esto evita efectos secundarios al ejecutar módulos con ``python -m``.

    Argumentos:
        name (str): Nombre del símbolo solicitado.

    Salidas:
        Any: Objeto público solicitado.

    Excepciones:
        AttributeError: Si el nombre no pertenece a la API pública.
    """
    if name not in _EXPORTS:
        raise AttributeError(f"module 'templates_library' has no attribute {name!r}")

    module_name, attr_name = _EXPORTS[name]
    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
