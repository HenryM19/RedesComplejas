"""
modulos
=======
Módulos funcionales de Templates Library.

Agrupa la lógica principal por responsabilidad: creación de proyectos,
organización de resultados y conversión de documentos.
"""

# =============================================================================
# Carga de librerías
# =============================================================================

from importlib import import_module
from typing import Any


# =============================================================================
# API pública del subpaquete
# =============================================================================

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
}

__all__ = list(_EXPORTS.keys())


# =============================================================================
# Resolución perezosa de símbolos públicos
# =============================================================================

def __getattr__(name: str) -> Any:
    """
    Resuelve bajo demanda los símbolos públicos del subpaquete.

    Argumentos:
        name (str): Nombre del símbolo solicitado.

    Salidas:
        Any: Objeto público solicitado.

    Excepciones:
        AttributeError: Si el nombre no pertenece al subpaquete.
    """
    if name not in _EXPORTS:
        raise AttributeError(f"module 'templates_library.modulos' has no attribute {name!r}")

    module_name, attr_name = _EXPORTS[name]
    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
