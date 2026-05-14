"""
recursos.py
===========
Funciones auxiliares para resolver rutas internas del paquete.

Este módulo centraliza el acceso a recursos empaquetados, como las plantillas
LaTeX, HTML y guías de estilo incluidas en la distribución.
"""

# =============================================================================
# Carga de librerías
# =============================================================================

from pathlib import Path


# =============================================================================
# Definición de funciones auxiliares
# =============================================================================

def obtener_directorio_templates() -> Path:
    """
    Devuelve la ruta absoluta al directorio de plantillas del paquete.

    Funcionalidad:
        Calcula la ubicación de ``templates_library/templates`` a partir del
        archivo actual. Esta ruta se usa desde los módulos de creación de
        proyectos y conversión de documentos.

    Argumentos:
        None

    Salidas:
        Path: Ruta absoluta al directorio de plantillas empaquetadas.
    """
    return Path(__file__).resolve().parents[1] / "templates"
