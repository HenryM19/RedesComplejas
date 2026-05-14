"""
crear_proyecto.py
=================
Script CLI para la creación automática de proyectos con estructura de carpetas
estandarizada. Recibe como parámetro obligatorio el nombre del proyecto y como
parámetro opcional el tipo de proyecto, y genera toda la jerarquía de directorios
y archivos base necesarios para comenzar a trabajar de forma organizada.

Project types available:
    - python    : Standard structure for Python projects with docs/, src/data/,
                  src/functions/, results/reports/ and results/images/.
    - latex     : LaTeX document with the UCUENCA template (Template, Portada,
                  references.bib, images/, main.tex).
    - julia     : Julia project with main.jl and shared resource folders
                  for docs, src and results.
    - notebook  : Notebook project with main.ipynb and shared resource folders
                  for docs, src and results.
    - matlab    : MATLAB project with main.m and shared resource folders
                  for docs, src and results.

Usage from terminal:
    python crear_proyecto.py <project_name> [--type TYPE] [--2route <path>]

Ejemplos:
    python crear_proyecto.py my_experiment
    python crear_proyecto.py image_classifier --type python
    python crear_proyecto.py control_lab      --type latex
    python crear_proyecto.py pde_solver       --type julia
    python crear_proyecto.py analysis_data    --2route C:/Projects
    python crear_proyecto.py --list_type

Autor: Henry Maldonado
Fecha: 2026-05-12
"""

# =============================================================================
# Carga de librerías
# =============================================================================

import os
import sys
import shutil
import argparse
import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4


# =============================================================================
# Definición de constantes — Directorio de plantillas
# =============================================================================

# Directorio donde viven las plantillas de cada tipo de proyecto.
# Se ubica junto a este mismo script para portabilidad.
DIR_TEMPLATES: Path = Path(__file__).parent / "templates"

# Default project type
TIPO_POR_DEFECTO: str = "python"


# =============================================================================
# Definición de las plantillas de proyecto
# =============================================================================
#
# Cada entrada del diccionario TIPOS_PROYECTO tiene la forma:
#   {
#     "descripcion"       : str         — Texto descriptivo para --list_type
#     "carpetas"          : list[str]   — Subcarpetas a crear (siempre)
#     "archivos_texto"    : dict[str,str|None]
#                           rel_path → contenido (None = generado dinámicamente)
#     "directorio_plantilla": str|None  — Subcarpeta dentro de DIR_TEMPLATES
#                           cuyos archivos se copian al raíz del proyecto.
#                           Si es None, no se copia nada adicional.
#   }
#
# "directorio_plantilla" y "archivos_texto" no son mutuamente excluyentes:
# primero se copian los archivos del template y después se escriben los
# archivos_texto (que pueden sobreescribir entradas del template si hiciera falta).

TIPOS_PROYECTO: dict[str, dict] = {

    # ------------------------------------------------------------------
    # python
    # ------------------------------------------------------------------
    "python": {
        "descripcion": (
            "Python project with main.py at root plus docs/, src/data/, "
            "src/functions/, results/reports/, results/images/ and README.md."
        ),
        "carpetas": [
            "src/data",
            "src/functions",
            "docs",
            "results/reports",
            "results/images",
        ],
        "archivos_texto": {
            "src/__init__.py": (
                '"""\nPaquete principal del proyecto.\n"""\n'
            ),
            "src/functions/__init__.py": (
                '"""\nMódulo de funciones utilitarias del proyecto.\n"""\n'
            ),
            "main.py": (
                '"""\nmain.py\n=======\nPunto de entrada principal del proyecto.\n"""\n\n'
                '# import funciones_template as ft\n\n\n'
                'def main() -> None:\n'
                '    """Función principal de ejecución."""\n'
                '    print("Proyecto iniciado.")\n\n\n'
                'if __name__ == "__main__":\n'
                '    main()\n'
            ),
            "docs/.gitkeep":        "",
            "results/reports/.gitkeep": "",
            "results/images/.gitkeep":  "",
            "src/data/.gitkeep":    "",
            "README.md": None,   # Generado dinámicamente
        },
        "directorio_plantilla": None,
    },

    # ------------------------------------------------------------------
    # latex
    # ------------------------------------------------------------------
    "latex": {
        "descripcion": (
            "LaTeX document with the UCUENCA template. "
            "Creates images/, Template/ (with Template.tex, Portada.tex, logo), "
            "references.bib and main.tex ready to compile."
        ),
        "carpetas": [
            "images",
            "Template",
        ],
        "archivos_texto": {},    # Todo viene del directorio_plantilla
        "directorio_plantilla": "latex",
    },

    # ------------------------------------------------------------------
    # julia
    # ------------------------------------------------------------------
    "julia": {
        "descripcion": (
            "Julia project with main.jl at root plus docs/, src/data/, "
            "src/functions/, results/reports/, results/images/ and README.md."
        ),
        "carpetas": [
            "src/data",
            "src/functions",
            "docs",
            "results/reports",
            "results/images",
        ],
        "archivos_texto": {
            "Project.toml": (
                "name = \"{project_name}\"\n"
                "uuid = \"{uuid}\"\n"
                "authors = [\"Your Name\"]\n"
                "version = \"0.1.0\"\n"
            ),
            "main.jl": (
                "println(\"Julia project ready.\")\n"
            ),
            "README.md": None,
            "src/data/.gitkeep": "",
            "src/functions/.gitkeep": "",
            "docs/.gitkeep": "",
            "results/reports/.gitkeep": "",
            "results/images/.gitkeep": "",
        },
        "directorio_plantilla": None,
    },

    # ------------------------------------------------------------------
    # notebook
    # ------------------------------------------------------------------
    "notebook": {
        "descripcion": (
            "Notebook project with main.ipynb at root plus docs/, src/data/, "
            "src/functions/, results/reports/, results/images/ and README.md."
        ),
        "carpetas": [
            "src/data",
            "src/functions",
            "docs",
            "results/reports",
            "results/images",
        ],
        "archivos_texto": {
            "main.ipynb": (
                "{\n"
                "  \"cells\": [\n"
                "    {\n"
                "      \"cell_type\": \"markdown\",\n"
                "      \"metadata\": {\n"
                "        \"language\": \"markdown\"\n"
                "      },\n"
                "      \"source\": [\n"
                "        \"# Notebook project\\n\",\n"
                "        \"Project: {project_name}\\n\"\n"
                "      ]\n"
                "    },\n"
                "    {\n"
                "      \"cell_type\": \"code\",\n"
                "      \"execution_count\": null,\n"
                "      \"metadata\": {\n"
                "        \"language\": \"python\"\n"
                "      },\n"
                "      \"outputs\": [],\n"
                "      \"source\": [\n"
                "        \"print('Notebook project ready.')\\n\"\n"
                "      ]\n"
                "    }\n"
                "  ],\n"
                "  \"metadata\": {\n"
                "    \"kernelspec\": {\n"
                "      \"display_name\": \"Python 3\",\n"
                "      \"language\": \"python\",\n"
                "      \"name\": \"python3\"\n"
                "    },\n"
                "    \"language_info\": {\n"
                "      \"name\": \"python\"\n"
                "    }\n"
                "  },\n"
                "  \"nbformat\": 4,\n"
                "  \"nbformat_minor\": 5\n"
                "}\n"
            ),
            "requirements.txt": (
                "jupyter\nipykernel\npandas\nmatplotlib\n"
            ),
            "README.md": None,
            "src/data/.gitkeep": "",
            "src/functions/.gitkeep": "",
            "docs/.gitkeep": "",
            "results/reports/.gitkeep": "",
            "results/images/.gitkeep": "",
        },
        "directorio_plantilla": None,
    },

    # ------------------------------------------------------------------
    # matlab
    # ------------------------------------------------------------------
    "matlab": {
        "descripcion": (
            "MATLAB project with main.m at root plus docs/, src/data/, "
            "src/functions/, results/reports/, results/images/ and README.md."
        ),
        "carpetas": [
            "src/data",
            "src/functions",
            "docs",
            "results/reports",
            "results/images",
        ],
        "archivos_texto": {
            "main.m": (
                "clc;\nclear;\n\ndisp('MATLAB project ready.');\n"
            ),
            "src/functions/placeholder.m": (
                "function output = placeholder(input)\n"
                "%PLACEHOLDER Example helper function.\n"
                "output = input;\n"
                "end\n"
            ),
            "README.md": None,
            "src/data/.gitkeep": "",
            "docs/.gitkeep": "",
            "results/reports/.gitkeep": "",
            "results/images/.gitkeep": "",
        },
        "directorio_plantilla": None,
    },
}


# =============================================================================
# Definición de funciones auxiliares
# =============================================================================

def crear_carpeta(ruta: Path) -> None:
    """
    Crea una carpeta en la ruta indicada si no existe.

    Funcionalidad:
        Utiliza mkdir con parents=True y exist_ok=True para crear también
        directorios padre faltantes sin lanzar error si ya existe.

    Argumentos:
        ruta (Path): Ruta de la carpeta a crear.

    Salidas:
        None
    """
    ruta.mkdir(parents=True, exist_ok=True)


def crear_archivo_texto(ruta: Path, contenido: str) -> None:
    """
    Escribe un archivo de texto solo si no existe previamente.

    Funcionalidad:
        Protege archivos existentes de ser sobreescritos al re-ejecutar
        el script sobre un proyecto ya creado.

    Argumentos:
        ruta      (Path): Ruta completa del archivo.
        contenido (str) : Texto inicial del archivo.

    Salidas:
        None
    """
    if not ruta.exists():
        ruta.write_text(contenido, encoding="utf-8")


def copiar_directorio_plantilla(origen: Path, destino: Path, verbose: bool) -> None:
    """
    Copia recursivamente los archivos de un directorio plantilla al proyecto.

    Funcionalidad:
        Recorre todos los archivos del directorio origen y los copia al
        directorio destino manteniendo la estructura de subcarpetas.
        Los archivos que ya existen en destino no se sobreescriben.

    Argumentos:
        origen  (Path): Ruta del directorio plantilla fuente.
        destino (Path): Ruta raíz del proyecto destino.
        verbose (bool): Si True, imprime cada archivo copiado.

    Salidas:
        None

    Excepciones:
        FileNotFoundError: Si el directorio origen no existe.
    """
    if not origen.exists():
        raise FileNotFoundError(
            f"Directorio de plantilla no encontrado: '{origen}'\n"
            f"Verifica que la carpeta 'templates/' esté junto a crear_proyecto.py."
        )

    for archivo_origen in sorted(origen.rglob("*")):
        if archivo_origen.is_dir():
            continue

        ruta_relativa = archivo_origen.relative_to(origen)
        archivo_destino = destino / ruta_relativa

        # Crear carpeta padre si hace falta
        archivo_destino.parent.mkdir(parents=True, exist_ok=True)

        # No sobreescribir archivos ya existentes
        if not archivo_destino.exists():
            shutil.copy2(str(archivo_origen), str(archivo_destino))
            if verbose:
                print(f"  ✔  {ruta_relativa}")
        else:
            if verbose:
                print(f"  ·  {ruta_relativa}  (ya existe, omitido)")


def generar_readme(nombre_proyecto: str, tipo: str) -> str:
    """
    Genera el contenido del README.md inicial para un proyecto Python.

    Funcionalidad:
        Construye un texto Markdown con encabezado, descripción, tipo,
        fecha de creación y estructura de carpetas del proyecto.

    Argumentos:
        nombre_proyecto (str): Nombre del proyecto.
        tipo            (str): Tipo de proyecto.

    Salidas:
        str: Contenido completo del README.md.
    """
    fecha = datetime.date.today().isoformat()
    carpetas = TIPOS_PROYECTO[tipo]["carpetas"]
    lineas = "\n".join(f"    {c}/" for c in carpetas)

    return (
        f"# {nombre_proyecto}\n\n"
        f"**Tipo:** `{tipo}`  \n"
        f"**Fecha de creación:** {fecha}\n\n"
        "## Descripción\n\n"
        "> Agrega aquí una descripción del proyecto.\n\n"
        "## Estructura\n\n"
        "```\n"
        f"{nombre_proyecto}/\n"
        f"{lineas}\n"
        "```\n\n"
        "## Usage\n\n"
        "```bash\n"
        "# Add your start command here\n"
        "```\n"
    )


def normalizar_nombre_modulo(nombre: str) -> str:
    """
    Convierte un nombre de proyecto en un identificador válido para módulos.

    Funcionalidad:
        Reemplaza guiones y espacios por guiones bajos, elimina caracteres no
        alfanuméricos y garantiza que el nombre no empiece por un dígito.

    Argumentos:
        nombre (str): Nombre original del proyecto.

    Salidas:
        str: Nombre normalizado para módulos o archivos fuente.
    """
    base = "".join(
        caracter if caracter.isalnum() or caracter == "_" else "_"
        for caracter in nombre.strip().replace("-", "_").replace(" ", "_")
    )
    base = "_".join(segmento for segmento in base.split("_") if segmento)
    if not base:
        return "project_module"
    if base[0].isdigit():
        base = f"project_{base}"
    return base


def nombre_modulo_julia(nombre: str) -> str:
    """
    Genera un nombre de módulo válido para Julia en formato PascalCase.

    Argumentos:
        nombre (str): Nombre original del proyecto.

    Salidas:
        str: Nombre de módulo Julia.
    """
    normalizado = normalizar_nombre_modulo(nombre)
    partes = [parte for parte in normalizado.split("_") if parte]
    return "".join(parte.capitalize() for parte in partes) or "ProjectModule"


def resolver_contenido_archivo(contenido: Optional[str], nombre_proyecto: str, tipo: str) -> str:
    """
    Resuelve el contenido final de un archivo base del proyecto.

    Funcionalidad:
        Genera README dinámico cuando corresponde y formatea plantillas de texto
        con variables derivadas del nombre del proyecto.

    Argumentos:
        contenido       (Optional[str]): Plantilla de contenido o None.
        nombre_proyecto (str)          : Nombre del proyecto.
        tipo            (str)          : Tipo de proyecto.

    Salidas:
        str: Contenido final listo para escribir.
    """
    if contenido is None:
        return generar_readme(nombre_proyecto, tipo)

    modulo_archivo = normalizar_nombre_modulo(nombre_proyecto)
    modulo_julia = nombre_modulo_julia(nombre_proyecto)

    reemplazos = {
        "{project_name}": modulo_archivo,
        "{module_name}": modulo_julia,
        "{original_project_name}": nombre_proyecto,
        "{uuid}": str(uuid4()),
    }

    for marcador, valor in reemplazos.items():
        contenido = contenido.replace(marcador, valor)

    return contenido


def validar_nombre_proyecto(nombre: str) -> None:
    """
    Valida que el nombre del proyecto sea apto para usarse como carpeta.

    Funcionalidad:
        Rechaza nombres vacíos y nombres con caracteres prohibidos en
        sistemas de archivos Windows y Unix.

    Argumentos:
        nombre (str): Nombre propuesto para el proyecto.

    Salidas:
        None

    Excepciones:
        ValueError: Si el nombre no es válido.
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del proyecto no puede estar vacío.")

    caracteres_prohibidos = set(r'\/:*?"<>|')
    encontrados = caracteres_prohibidos.intersection(set(nombre))
    if encontrados:
        raise ValueError(
            f"El nombre '{nombre}' contiene caracteres no permitidos: "
            f"{sorted(encontrados)}"
        )


# =============================================================================
# Definición de función principal de creación
# =============================================================================

def crear_proyecto(
    nombre_proyecto: str,
    tipo: str = TIPO_POR_DEFECTO,
    directorio_base: Optional[Path] = None,
    verbose: bool = True
) -> Path:
    """
    Crea la estructura completa de un proyecto según el tipo especificado.

    Funcionalidad:
        1. Valida nombre y tipo.
        2. Crea el directorio raíz del proyecto.
        3. Crea todas las subcarpetas definidas en la plantilla.
        4. Copia archivos desde el directorio_plantilla (si aplica).
        5. Escribe archivos_texto adicionales (README generado, __init__.py, etc.).

    Argumentos:
        nombre_proyecto (str)           : Nombre de la carpeta raíz del proyecto.
        tipo            (str)           : Tipo de proyecto. Clave de TIPOS_PROYECTO.
        directorio_base (Optional[Path]): Dónde crear el proyecto. None → cwd.
        verbose         (bool)          : Mostrar progreso en consola.

    Salidas:
        Path: Ruta absoluta de la carpeta raíz creada.

    Excepciones:
        ValueError      : Nombre o tipo inválidos.
        FileNotFoundError: Directorio plantilla no encontrado.
        PermissionError : Sin permisos de escritura.
    """
    # --- Validaciones ---
    validar_nombre_proyecto(nombre_proyecto)

    if tipo not in TIPOS_PROYECTO:
        raise ValueError(
            f"Tipo '{tipo}' no reconocido. "
            f"Disponibles: {list(TIPOS_PROYECTO.keys())}"
        )

    plantilla = TIPOS_PROYECTO[tipo]
    base = directorio_base if directorio_base else Path.cwd()
    ruta_proyecto = base / nombre_proyecto

    if verbose:
        print("=" * 60)
        print(f"  Creando proyecto : {nombre_proyecto}")
        print(f"  Tipo             : {tipo}")
        print(f"  Ubicación        : {ruta_proyecto}")
        print("=" * 60)

    # --- Carpeta raíz ---
    ya_existia = ruta_proyecto.exists()
    crear_carpeta(ruta_proyecto)

    if ya_existia and verbose:
        print(f"\n[!] '{nombre_proyecto}' ya existía. "
              "Se agregarán los elementos faltantes.\n")

    # --- Subcarpetas ---
    if verbose:
        print("\n[Carpetas]")

    for carpeta_rel in plantilla["carpetas"]:
        crear_carpeta(ruta_proyecto / carpeta_rel)
        if verbose:
            print(f"  ✔  {carpeta_rel}/")

    # --- Archivos del directorio plantilla ---
    dir_plantilla_nombre = plantilla.get("directorio_plantilla")
    if dir_plantilla_nombre:
        origen_plantilla = DIR_TEMPLATES / dir_plantilla_nombre
        if verbose:
            print(f"\n[Archivos del template '{dir_plantilla_nombre}']")
        copiar_directorio_plantilla(origen_plantilla, ruta_proyecto, verbose)

    # --- Archivos texto adicionales ---
    archivos_texto = plantilla.get("archivos_texto", {})
    if archivos_texto and verbose:
        print("\n[Archivos base]")

    for archivo_rel, contenido in archivos_texto.items():
        ruta_archivo = ruta_proyecto / archivo_rel

        contenido = resolver_contenido_archivo(contenido, nombre_proyecto, tipo)

        crear_archivo_texto(ruta_archivo, contenido)

        if verbose:
            estado = "✔" if ruta_archivo.exists() else "✖"
            print(f"  {estado}  {archivo_rel}")

    # --- Resumen ---
    if verbose:
        print("\n" + "-" * 60)
        print(f"  Proyecto '{nombre_proyecto}' creado exitosamente.")
        print(f"  Ruta: {ruta_proyecto.resolve()}")
        print("-" * 60)

    return ruta_proyecto.resolve()


# =============================================================================
# Definición de función de listado de tipos
# =============================================================================

def listar_tipos_disponibles() -> None:
    """
    Imprime en consola los tipos de proyecto disponibles y su estructura.

    Funcionalidad:
        Recorre TIPOS_PROYECTO mostrando descripción, carpetas y archivos
        de cada tipo registrado.

    Argumentos:
        None

    Salidas:
        None
    """
    print("\nTipos de proyecto disponibles:\n")
    for tipo, plantilla in TIPOS_PROYECTO.items():
        print(f"  [{tipo}]")
        print(f"    {plantilla['descripcion']}")
        print("    Carpetas:")
        for c in plantilla["carpetas"]:
            print(f"      - {c}/")
        dir_tmpl = plantilla.get("directorio_plantilla")
        if dir_tmpl:
            origen = DIR_TEMPLATES / dir_tmpl
            if origen.exists():
                archivos = [str(f.relative_to(origen)) for f in sorted(origen.rglob("*")) if f.is_file()]
                print("    Archivos del template:")
                for a in archivos:
                    print(f"      - {a}")
        archivos_txt = plantilla.get("archivos_texto", {})
        if archivos_txt:
            print("    Archivos generados:")
            for a in archivos_txt:
                print(f"      - {a}")
        print()


# =============================================================================
# Configuración del parser CLI
# =============================================================================

def configurar_parser() -> argparse.ArgumentParser:
    """
    Configura y retorna el parser de argumentos de línea de comandos.

    Funcionalidad:
        Define argumentos posicionales y opcionales del script CLI.

    Argumentos:
        None

    Salidas:
        argparse.ArgumentParser: Parser listo para parsear sys.argv.
    """
    parser = argparse.ArgumentParser(
        prog="create_project",
        description=(
            "Create the base folder and file structure for a new project."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python crear_proyecto.py my_experiment\n"
            "  python crear_proyecto.py lab_report --type latex\n"
            "  python crear_proyecto.py pde_solver --type julia\n"
            "  python crear_proyecto.py analysis --2route C:/Projects\n"
            "  python crear_proyecto.py --list_type\n"
        )
    )

    parser.add_argument(
        "nombre",
        nargs="?",
        type=str,
        help="Project root folder name to create."
    )
    parser.add_argument(
        "--type",
        "--tipo",
        type=str,
        default=TIPO_POR_DEFECTO,
        metavar="TYPE",
        help=(
            f"Project type (default: '{TIPO_POR_DEFECTO}'). "
            "Use --list_type to view the available options."
        )
    )
    parser.add_argument(
        "--2route",
        "--base",
        type=str,
        default=None,
        metavar="PATH",
        help="Directory where the project will be created (default: current directory)."
    )
    parser.add_argument(
        "--list_type",
        "--listar-tipos",
        action="store_true",
        help="Show the available project types and their structure."
    )
    parser.add_argument(
        "--quiet",
        "--silencioso",
        action="store_true",
        help="Suppress console output."
    )

    return parser


# =============================================================================
# Código main — Punto de entrada del script
# =============================================================================

if __name__ == "__main__":

    # Parsear argumentos de línea de comandos
    parser = configurar_parser()
    args = parser.parse_args()

    # Mostrar tipos y salir si se solicitó
    if getattr(args, "list_type"):
        listar_tipos_disponibles()
        sys.exit(0)

    # Verificar que se proporcionó el nombre
    if not getattr(args, "nombre"):
        parser.print_help()
        print("\n[ERROR] Debes proporcionar el nombre del proyecto.")
        sys.exit(1)

    # Resolver directorio base si se especificó
    directorio_base = Path(getattr(args, "2route")).resolve() if getattr(args, "2route") else None

    # Crear el proyecto
    try:
        crear_proyecto(
            nombre_proyecto=getattr(args, "nombre"),
            tipo=getattr(args, "type"),
            directorio_base=directorio_base,
            verbose=not getattr(args, "quiet"),
        )
        sys.exit(0)

    except (ValueError, FileNotFoundError, PermissionError) as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
