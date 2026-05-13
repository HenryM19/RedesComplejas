"""
crear_proyecto.py
=================
Script CLI para la creación automática de proyectos con estructura de carpetas
estandarizada. Recibe como parámetro obligatorio el nombre del proyecto y como
parámetro opcional el tipo de proyecto, y genera toda la jerarquía de directorios
y archivos base necesarios para comenzar a trabajar de forma organizada.

Tipos de proyecto disponibles:
    - proyecto_python  : Estructura estándar para proyectos de ciencia de datos
                         o procesamiento en Python (src, results, experiments...).
    - proyecto_latex   : Documento LaTeX con la plantilla UCUENCA (Template, Portada,
                         references.bib, images/, main.tex).

Uso desde terminal:
    python crear_proyecto.py <nombre_proyecto> [--tipo TIPO] [--base <ruta>]

Ejemplos:
    python crear_proyecto.py mi_experimento
    python crear_proyecto.py clasificador_imagenes --tipo proyecto_python
    python crear_proyecto.py practica_control    --tipo proyecto_latex
    python crear_proyecto.py analisis_datos      --base C:/Proyectos
    python crear_proyecto.py --listar-tipos

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


# =============================================================================
# Definición de constantes — Directorio de plantillas
# =============================================================================

# Directorio donde viven las plantillas de cada tipo de proyecto.
# Se ubica junto a este mismo script para portabilidad.
DIR_TEMPLATES: Path = Path(__file__).parent / "templates"

# Tipo de proyecto por defecto
TIPO_POR_DEFECTO: str = "proyecto_python"


# =============================================================================
# Definición de las plantillas de proyecto
# =============================================================================
#
# Cada entrada del diccionario TIPOS_PROYECTO tiene la forma:
#   {
#     "descripcion"       : str         — Texto descriptivo para --listar-tipos
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
    # proyecto_python
    # ------------------------------------------------------------------
    "proyecto_python": {
        "descripcion": (
            "Proyecto de Python/ciencia de datos. "
            "Crea main.py en la raíz, src/, src/images/, src/data/, "
            "src/functions/, results/, experiments/ y README.md."
        ),
        "carpetas": [
            "src",
            "src/images",
            "src/data",
            "src/functions",
            "results",
            "experiments",
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
            "experiments/.gitkeep": "",
            "results/.gitkeep":     "",
            "src/data/.gitkeep":    "",
            "src/images/.gitkeep":  "",
            "README.md": None,   # Generado dinámicamente
        },
        "directorio_plantilla": None,
    },

    # ------------------------------------------------------------------
    # proyecto_latex
    # ------------------------------------------------------------------
    "proyecto_latex": {
        "descripcion": (
            "Documento LaTeX con plantilla UCUENCA. "
            "Crea images/, Template/ (con Template.tex, Portada.tex, logo), "
            "references.bib y main.tex listo para compilar."
        ),
        "carpetas": [
            "images",
            "Template",
        ],
        "archivos_texto": {},    # Todo viene del directorio_plantilla
        "directorio_plantilla": "latex",
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
        "## Uso\n\n"
        "```bash\n"
        "python src/main.py\n"
        "```\n"
    )


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

        if contenido is None:
            contenido = generar_readme(nombre_proyecto, tipo)

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
        prog="crear_proyecto",
        description=(
            "Crea la estructura de carpetas y archivos base para un nuevo proyecto."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python crear_proyecto.py mi_experimento\n"
            "  python crear_proyecto.py practica1 --tipo proyecto_latex\n"
            "  python crear_proyecto.py analisis  --base C:/Proyectos\n"
            "  python crear_proyecto.py --listar-tipos\n"
        )
    )

    parser.add_argument(
        "nombre",
        nargs="?",
        type=str,
        help="Nombre de la carpeta raíz del proyecto a crear."
    )
    parser.add_argument(
        "--tipo",
        type=str,
        default=TIPO_POR_DEFECTO,
        metavar="TIPO",
        help=(
            f"Tipo de proyecto (por defecto: '{TIPO_POR_DEFECTO}'). "
            "Use --listar-tipos para ver opciones."
        )
    )
    parser.add_argument(
        "--base",
        type=str,
        default=None,
        metavar="RUTA",
        help="Directorio donde se creará el proyecto (por defecto: directorio actual)."
    )
    parser.add_argument(
        "--listar-tipos",
        action="store_true",
        help="Muestra los tipos de proyecto disponibles y su estructura."
    )
    parser.add_argument(
        "--silencioso",
        action="store_true",
        help="Suprime la salida en consola."
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
    if args.listar_tipos:
        listar_tipos_disponibles()
        sys.exit(0)

    # Verificar que se proporcionó el nombre
    if not args.nombre:
        parser.print_help()
        print("\n[ERROR] Debes proporcionar el nombre del proyecto.")
        sys.exit(1)

    # Resolver directorio base si se especificó
    directorio_base = Path(args.base).resolve() if args.base else None

    # Crear el proyecto
    try:
        crear_proyecto(
            nombre_proyecto=args.nombre,
            tipo=args.tipo,
            directorio_base=directorio_base,
            verbose=not args.silencioso,
        )
        sys.exit(0)

    except (ValueError, FileNotFoundError, PermissionError) as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
