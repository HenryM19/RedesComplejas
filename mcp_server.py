"""
mcp_server.py
=============
Servidor MCP (Model Context Protocol) que expone todas las funciones de 
Templates_Library como herramientas disponibles para Claude.

Permite que Claude acceda a:
  - Crear proyectos con estructura automática
  - Guardar imágenes, informes y documentos MD en carpetas organizadas
  - Convertir Markdown a LaTeX
  - Listar archivos de resultados

Autor: Henry Maldonado
Fecha: 2026-05-14
"""

# =============================================================================
# Carga de librerías
# =============================================================================

import os
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Importar módulos locales
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    from crear_proyecto import crear_proyecto, listar_tipos_disponibles, TIPOS_PROYECTO
    from funciones_template import (
        guardar_imagen,
        guardar_informe,
        guardar_md,
        crear_estructura_resultados,
        listar_resultados
    )
except ImportError as e:
    print(f"[ERROR] No se pudieron importar los módulos: {e}")
    sys.exit(1)


# =============================================================================
# Configuración de la aplicación FastAPI
# =============================================================================

app = FastAPI(
    title="Templates_Library MCP Server",
    description="Servidor MCP que expone funciones de Templates_Library",
    version="1.0.0"
)


# =============================================================================
# Endpoint de salud (Health Check)
# =============================================================================

@app.get("/health")
async def health() -> dict[str, str]:
    """
    Endpoint de verificación de salud.
    
    Funcionalidad:
        Verifica que el servidor está activo y funcionando correctamente.
        Render usa este endpoint para monitorear el servicio.
    
    Salidas:
        dict: Status del servidor.
    """
    return {"status": "ok", "service": "Templates_Library MCP Server"}


# =============================================================================
# Endpoint: Crear proyecto
# =============================================================================

@app.post("/tools/crear_proyecto")
async def tool_crear_proyecto(
    nombre_proyecto: str,
    tipo: str = "python",
    directorio_base: str | None = None
) -> dict[str, Any]:
    """
    Crea un nuevo proyecto con estructura automática.
    
    Funcionalidad:
        Genera carpetas y archivos base según el tipo de proyecto seleccionado.
        Tipos disponibles: python, latex, julia, notebook, matlab.
    
    Argumentos:
        nombre_proyecto (str)          : Nombre del proyecto.
        tipo (str)                     : Tipo de proyecto (default: python).
        directorio_base (str | None)   : Directorio donde crear el proyecto.
    
    Salidas:
        dict: Información del proyecto creado.
    
    Excepciones (HTTP):
        400: Parámetros inválidos.
        500: Error durante la creación.
    """
    try:
        if not nombre_proyecto or not nombre_proyecto.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        
        if tipo not in TIPOS_PROYECTO:
            disponibles = ", ".join(TIPOS_PROYECTO.keys())
            raise ValueError(f"Tipo '{tipo}' no válido. Disponibles: {disponibles}")
        
        base = Path(directorio_base).resolve() if directorio_base else None
        ruta = crear_proyecto(
            nombre_proyecto=nombre_proyecto,
            tipo=tipo,
            directorio_base=base,
            verbose=True
        )
        
        return {
            "status": "success",
            "nombre": nombre_proyecto,
            "tipo": tipo,
            "ruta": str(ruta),
            "estructura": _obtener_estructura_carpetas(ruta)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# =============================================================================
# Endpoint: Listar tipos de proyectos disponibles
# =============================================================================

@app.get("/tools/listar_tipos")
async def tool_listar_tipos() -> dict[str, Any]:
    """
    Lista todos los tipos de proyectos disponibles.
    
    Funcionalidad:
        Retorna información sobre cada tipo de proyecto soportado,
        incluyendo descripción, carpetas y archivos que se generan.
    
    Salidas:
        dict: Catálogo de tipos de proyecto.
    """
    tipos_info = {}
    for tipo, config in TIPOS_PROYECTO.items():
        tipos_info[tipo] = {
            "descripcion": config.get("descripcion", ""),
            "carpetas": config.get("carpetas", []),
            "tiene_template": bool(config.get("directorio_plantilla"))
        }
    
    return {
        "status": "success",
        "tipos_disponibles": tipos_info,
        "total": len(tipos_info)
    }


# =============================================================================
# Endpoint: Guardar imagen
# =============================================================================

@app.post("/tools/guardar_imagen")
async def tool_guardar_imagen(
    archivo_origen: str,
    directorio_base: str | None = None,
    agregar_timestamp: bool = False
) -> dict[str, Any]:
    """
    Guarda una imagen en la carpeta 'Resultados_imagenes'.
    
    Funcionalidad:
        Copia una imagen a una carpeta de resultados organizada.
        Soporta: PNG, JPG, JPEG, SVG, GIF, BMP, TIFF, WEBP.
    
    Argumentos:
        archivo_origen (str)           : Ruta del archivo de imagen.
        directorio_base (str | None)   : Directorio raíz para resultados.
        agregar_timestamp (bool)       : Agregar timestamp al nombre.
    
    Salidas:
        dict: Información del archivo guardado.
    
    Excepciones (HTTP):
        400: Archivo no válido o no existe.
        500: Error durante el guardado.
    """
    try:
        ruta_imagen = Path(archivo_origen)
        if not ruta_imagen.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {archivo_origen}")
        
        base = Path(directorio_base) if directorio_base else None
        ruta_guardada = guardar_imagen(
            archivo_origen=ruta_imagen,
            directorio_base=base,
            agregar_timestamp=agregar_timestamp
        )
        
        return {
            "status": "success",
            "archivo_original": str(ruta_imagen),
            "archivo_guardado": str(ruta_guardada),
            "size_bytes": ruta_guardada.stat().st_size if ruta_guardada.exists() else 0
        }
    
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# =============================================================================
# Endpoint: Guardar informe
# =============================================================================

@app.post("/tools/guardar_informe")
async def tool_guardar_informe(
    archivo_origen: str,
    directorio_base: str | None = None,
    agregar_timestamp: bool = False
) -> dict[str, Any]:
    """
    Guarda un informe o presentación en 'Resultados_informes'.
    
    Funcionalidad:
        Copia un informe a una carpeta de resultados organizada.
        Soporta: PDF, PPTX, DOCX, XLSX, PPT, XLS.
    
    Argumentos:
        archivo_origen (str)           : Ruta del informe.
        directorio_base (str | None)   : Directorio raíz para resultados.
        agregar_timestamp (bool)       : Agregar timestamp al nombre.
    
    Salidas:
        dict: Información del archivo guardado.
    
    Excepciones (HTTP):
        400: Archivo no válido o no existe.
        500: Error durante el guardado.
    """
    try:
        ruta_informe = Path(archivo_origen)
        if not ruta_informe.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {archivo_origen}")
        
        base = Path(directorio_base) if directorio_base else None
        ruta_guardada = guardar_informe(
            archivo_origen=ruta_informe,
            directorio_base=base,
            agregar_timestamp=agregar_timestamp
        )
        
        return {
            "status": "success",
            "archivo_original": str(ruta_informe),
            "archivo_guardado": str(ruta_guardada),
            "size_bytes": ruta_guardada.stat().st_size if ruta_guardada.exists() else 0
        }
    
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# =============================================================================
# Endpoint: Guardar Markdown
# =============================================================================

@app.post("/tools/guardar_md")
async def tool_guardar_md(
    archivo_origen: str,
    directorio_base: str | None = None,
    agregar_timestamp: bool = False
) -> dict[str, Any]:
    """
    Guarda un documento Markdown en 'Resultados_md'.
    
    Funcionalidad:
        Copia un documento MD o TXT a una carpeta de resultados organizada.
        Soporta: MD, TXT.
    
    Argumentos:
        archivo_origen (str)           : Ruta del documento.
        directorio_base (str | None)   : Directorio raíz para resultados.
        agregar_timestamp (bool)       : Agregar timestamp al nombre.
    
    Salidas:
        dict: Información del archivo guardado.
    
    Excepciones (HTTP):
        400: Archivo no válido o no existe.
        500: Error durante el guardado.
    """
    try:
        ruta_md = Path(archivo_origen)
        if not ruta_md.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {archivo_origen}")
        
        base = Path(directorio_base) if directorio_base else None
        ruta_guardada = guardar_md(
            archivo_origen=ruta_md,
            directorio_base=base,
            agregar_timestamp=agregar_timestamp
        )
        
        return {
            "status": "success",
            "archivo_original": str(ruta_md),
            "archivo_guardado": str(ruta_guardada),
            "size_bytes": ruta_guardada.stat().st_size if ruta_guardada.exists() else 0
        }
    
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# =============================================================================
# Endpoint: Crear estructura de resultados
# =============================================================================

@app.post("/tools/crear_estructura_resultados")
async def tool_crear_estructura_resultados(
    directorio_base: str | None = None
) -> dict[str, Any]:
    """
    Crea las carpetas de resultados estándar.
    
    Funcionalidad:
        Genera Resultados_imagenes/, Resultados_informes/ y Resultados_md/
        en el directorio especificado.
    
    Argumentos:
        directorio_base (str | None): Directorio raíz.
    
    Salidas:
        dict: Rutas de las carpetas creadas.
    """
    try:
        base = Path(directorio_base) if directorio_base else None
        carpetas_creadas = crear_estructura_resultados(directorio_base=base)
        
        return {
            "status": "success",
            "carpetas_creadas": carpetas_creadas
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# =============================================================================
# Endpoint: Listar resultados
# =============================================================================

@app.get("/tools/listar_resultados")
async def tool_listar_resultados(
    directorio_base: str | None = None
) -> dict[str, Any]:
    """
    Lista los archivos en las carpetas de resultados.
    
    Funcionalidad:
        Muestra qué archivos hay en Resultados_imagenes/, Resultados_informes/
        y Resultados_md/.
    
    Argumentos:
        directorio_base (str | None): Directorio raíz.
    
    Salidas:
        dict: Inventario de archivos por carpeta.
    """
    try:
        base = Path(directorio_base) if directorio_base else None
        resultados = listar_resultados(directorio_base=base)
        
        return {
            "status": "success",
            "resultados": resultados
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# =============================================================================
# Funciones auxiliares
# =============================================================================

def _obtener_estructura_carpetas(ruta: Path) -> dict[str, Any]:
    """
    Obtiene la estructura de carpetas y archivos creados.
    
    Funcionalidad:
        Recorre la carpeta del proyecto y retorna un árbol de contenido.
    
    Argumentos:
        ruta (Path): Ruta del proyecto.
    
    Salidas:
        dict: Árbol de contenido.
    """
    estructura = {}
    
    for item in ruta.rglob("*"):
        rel_path = str(item.relative_to(ruta))
        if item.is_file():
            estructura[rel_path] = "archivo"
        elif item.is_dir():
            estructura[rel_path] = "carpeta"
    
    return estructura


# =============================================================================
# Información de herramientas disponibles (para MCP)
# =============================================================================

@app.get("/tools")
async def list_tools() -> dict[str, Any]:
    """
    Lista todas las herramientas disponibles en el servidor MCP.
    
    Salidas:
        dict: Catálogo de herramientas con sus descripciones.
    """
    return {
        "status": "success",
        "tools": [
            {
                "name": "crear_proyecto",
                "description": "Crea un nuevo proyecto con estructura automática",
                "endpoint": "/tools/crear_proyecto",
                "method": "POST",
                "params": {
                    "nombre_proyecto": "string (requerido)",
                    "tipo": "string (default: python)",
                    "directorio_base": "string (opcional)"
                }
            },
            {
                "name": "listar_tipos",
                "description": "Lista tipos de proyectos disponibles",
                "endpoint": "/tools/listar_tipos",
                "method": "GET"
            },
            {
                "name": "guardar_imagen",
                "description": "Guarda imagen en Resultados_imagenes/",
                "endpoint": "/tools/guardar_imagen",
                "method": "POST",
                "params": {
                    "archivo_origen": "string (requerido)",
                    "directorio_base": "string (opcional)",
                    "agregar_timestamp": "boolean (default: false)"
                }
            },
            {
                "name": "guardar_informe",
                "description": "Guarda informe en Resultados_informes/",
                "endpoint": "/tools/guardar_informe",
                "method": "POST",
                "params": {
                    "archivo_origen": "string (requerido)",
                    "directorio_base": "string (opcional)",
                    "agregar_timestamp": "boolean (default: false)"
                }
            },
            {
                "name": "guardar_md",
                "description": "Guarda documento Markdown en Resultados_md/",
                "endpoint": "/tools/guardar_md",
                "method": "POST",
                "params": {
                    "archivo_origen": "string (requerido)",
                    "directorio_base": "string (opcional)",
                    "agregar_timestamp": "boolean (default: false)"
                }
            },
            {
                "name": "crear_estructura_resultados",
                "description": "Crea carpetas de resultados estándar",
                "endpoint": "/tools/crear_estructura_resultados",
                "method": "POST",
                "params": {
                    "directorio_base": "string (opcional)"
                }
            },
            {
                "name": "listar_resultados",
                "description": "Lista archivos en carpetas de resultados",
                "endpoint": "/tools/listar_resultados",
                "method": "GET",
                "params": {
                    "directorio_base": "string (opcional)"
                }
            }
        ],
        "total_tools": 7
    }


# =============================================================================
# Punto de entrada — Main
# =============================================================================

if __name__ == "__main__":
    # Obtener puerto de variable de entorno (Render lo proporciona)
    puerto = int(os.getenv("PORT", 8000))
    
    # Ejecutar servidor con uvicorn
    uvicorn.run(
        "mcp_server:app",
        host="0.0.0.0",
        port=puerto,
        reload=False,
        log_level="info"
    )
