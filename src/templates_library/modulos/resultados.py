"""
funciones_template.py
=====================
Librería de utilidades para la organización automática de resultados en carpetas
estructuradas dentro del directorio de trabajo actual. Proporciona funciones para
guardar imágenes, informes/presentaciones en PDF y documentos Markdown en
subcarpetas estandarizadas, facilitando la gestión y trazabilidad de los
resultados generados por cualquier proyecto o script.

Estructura de carpetas generada:
    ./Resultados_imagenes/   → Imágenes (png, jpg, jpeg, svg, gif, bmp, tiff, webp)
    ./Resultados_informes/   → Informes y presentaciones (pdf, pptx, docx, xlsx)
    ./Resultados_md/         → Documentos Markdown (md, txt)

Uso básico:
    import funciones_template as ft

    ft.guardar_imagen("mi_grafico.png")
    ft.guardar_informe("reporte_final.pdf")
    ft.guardar_md("resumen.md")

Autor: Henry Maldonado
Fecha: 2026-05-12
"""

# =============================================================================
# Carga de librerías
# =============================================================================

import os
import shutil
import datetime
from pathlib import Path
from typing import Optional, Union


# =============================================================================
# Definición de constantes
# =============================================================================

# Nombres de las carpetas de resultados
CARPETA_IMAGENES  = "Resultados_imagenes"
CARPETA_INFORMES  = "Resultados_informes"
CARPETA_MD        = "Resultados_md"

# Extensiones válidas por tipo
EXTENSIONES_IMAGENES = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".bmp", ".tiff", ".webp"}
EXTENSIONES_INFORMES = {".pdf", ".pptx", ".docx", ".xlsx", ".ppt", ".xls"}
EXTENSIONES_MD       = {".md", ".txt"}


# =============================================================================
# Definición de funciones auxiliares
# =============================================================================

def _crear_carpeta(ruta_carpeta: Path) -> Path:
    """
    Crea una carpeta en la ruta especificada si no existe.

    Funcionalidad:
        Verifica si la carpeta destino existe y, en caso contrario, la crea
        incluyendo todos los directorios padre necesarios.

    Argumentos:
        ruta_carpeta (Path): Ruta absoluta o relativa de la carpeta a crear.

    Salidas:
        Path: La ruta de la carpeta creada o ya existente.
    """
    ruta_carpeta.mkdir(parents=True, exist_ok=True)
    return ruta_carpeta


def _copiar_o_mover_archivo(
    archivo_origen: Union[str, Path],
    carpeta_destino: Path,
    mover: bool = False,
    agregar_timestamp: bool = False
) -> Path:
    """
    Copia o mueve un archivo a la carpeta destino especificada.

    Funcionalidad:
        Verifica la existencia del archivo origen, opcionalmente agrega un
        timestamp al nombre para evitar colisiones, y luego copia o mueve
        el archivo a la carpeta destino. Crea la carpeta destino si no existe.

    Argumentos:
        archivo_origen      (Union[str, Path]): Ruta del archivo a copiar o mover.
        carpeta_destino     (Path)            : Ruta de la carpeta destino.
        mover               (bool)            : Si es True, mueve el archivo; si es False,
                                                lo copia. Por defecto False (copia).
        agregar_timestamp   (bool)            : Si es True, agrega un timestamp
                                                al nombre del archivo. Por defecto False.

    Salidas:
        Path: Ruta completa del archivo en la carpeta destino.

    Excepciones:
        FileNotFoundError : Si el archivo origen no existe.
        ValueError        : Si la extensión del archivo no es compatible.
    """
    archivo_origen = Path(archivo_origen)

    if not archivo_origen.exists():
        raise FileNotFoundError(
            f"El archivo '{archivo_origen}' no fue encontrado."
        )

    # Construir el nombre de destino
    _crear_carpeta(carpeta_destino)

    if agregar_timestamp:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_destino = f"{archivo_origen.stem}_{ts}{archivo_origen.suffix}"
    else:
        nombre_destino = archivo_origen.name

    ruta_destino = carpeta_destino / nombre_destino

    if mover:
        shutil.move(str(archivo_origen), str(ruta_destino))
    else:
        shutil.copy2(str(archivo_origen), str(ruta_destino))

    return ruta_destino


def _validar_extension(archivo: Path, extensiones_validas: set) -> None:
    """
    Valida que la extensión del archivo sea parte del conjunto permitido.

    Funcionalidad:
        Compara la extensión del archivo (en minúsculas) contra un conjunto
        de extensiones válidas y lanza un ValueError si no coincide.

    Argumentos:
        archivo            (Path): Ruta del archivo a validar.
        extensiones_validas (set): Conjunto de extensiones permitidas
                                   (ej. {'.png', '.jpg'}).

    Salidas:
        None

    Excepciones:
        ValueError: Si la extensión del archivo no está en el conjunto válido.
    """
    ext = archivo.suffix.lower()
    if ext not in extensiones_validas:
        raise ValueError(
            f"Extensión '{ext}' no válida. Se esperaba una de: "
            f"{sorted(extensiones_validas)}"
        )


# =============================================================================
# Definición de funciones principales
# =============================================================================

def guardar_imagen(
    archivo_origen: Union[str, Path],
    directorio_base: Optional[Union[str, Path]] = None,
    mover: bool = False,
    agregar_timestamp: bool = False
) -> Path:
    """
    Guarda una imagen en la carpeta 'Resultados_imagenes'.

    Funcionalidad:
        Copia (o mueve) un archivo de imagen al subdirectorio 'Resultados_imagenes'
        dentro del directorio base indicado (por defecto, el directorio de trabajo
        actual). Valida que la extensión corresponda a un formato de imagen soportado.

    Argumentos:
        archivo_origen      (Union[str, Path])           : Ruta del archivo de imagen a guardar.
        directorio_base     (Optional[Union[str, Path]]) : Directorio raíz donde se creará
                                                           'Resultados_imagenes'. Si es None,
                                                           usa el directorio actual (cwd).
        mover               (bool)                       : Si True, mueve el archivo en lugar
                                                           de copiarlo. Por defecto False.
        agregar_timestamp   (bool)                       : Si True, agrega timestamp al nombre
                                                           del archivo. Por defecto False.

    Salidas:
        Path: Ruta completa del archivo guardado en 'Resultados_imagenes'.

    Excepciones:
        FileNotFoundError : Si el archivo origen no existe.
        ValueError        : Si la extensión no es una imagen válida.

    Ejemplo:
        >>> ruta = guardar_imagen("grafico.png")
        >>> print(ruta)
        Resultados_imagenes/grafico.png
    """
    archivo_origen = Path(archivo_origen)
    _validar_extension(archivo_origen, EXTENSIONES_IMAGENES)

    base = Path(directorio_base) if directorio_base else Path.cwd()
    carpeta_destino = base / CARPETA_IMAGENES

    ruta_guardada = _copiar_o_mover_archivo(
        archivo_origen, carpeta_destino, mover=mover, agregar_timestamp=agregar_timestamp
    )

    print(f"[OK] Imagen guardada en: {ruta_guardada}")
    return ruta_guardada


def guardar_informe(
    archivo_origen: Union[str, Path],
    directorio_base: Optional[Union[str, Path]] = None,
    mover: bool = False,
    agregar_timestamp: bool = False
) -> Path:
    """
    Guarda un informe o presentación en la carpeta 'Resultados_informes'.

    Funcionalidad:
        Copia (o mueve) un archivo de informe o presentación al subdirectorio
        'Resultados_informes' dentro del directorio base indicado (por defecto,
        el directorio de trabajo actual). Soporta formatos PDF, PPTX, DOCX y XLSX.

    Argumentos:
        archivo_origen      (Union[str, Path])           : Ruta del archivo de informe a guardar.
        directorio_base     (Optional[Union[str, Path]]) : Directorio raíz donde se creará
                                                           'Resultados_informes'. Si es None,
                                                           usa el directorio actual (cwd).
        mover               (bool)                       : Si True, mueve el archivo en lugar
                                                           de copiarlo. Por defecto False.
        agregar_timestamp   (bool)                       : Si True, agrega timestamp al nombre
                                                           del archivo. Por defecto False.

    Salidas:
        Path: Ruta completa del archivo guardado en 'Resultados_informes'.

    Excepciones:
        FileNotFoundError : Si el archivo origen no existe.
        ValueError        : Si la extensión no es un informe válido.

    Ejemplo:
        >>> ruta = guardar_informe("reporte_anual.pdf")
        >>> print(ruta)
        Resultados_informes/reporte_anual.pdf
    """
    archivo_origen = Path(archivo_origen)
    _validar_extension(archivo_origen, EXTENSIONES_INFORMES)

    base = Path(directorio_base) if directorio_base else Path.cwd()
    carpeta_destino = base / CARPETA_INFORMES

    ruta_guardada = _copiar_o_mover_archivo(
        archivo_origen, carpeta_destino, mover=mover, agregar_timestamp=agregar_timestamp
    )

    print(f"[OK] Informe guardado en: {ruta_guardada}")
    return ruta_guardada


def guardar_md(
    archivo_origen: Union[str, Path],
    directorio_base: Optional[Union[str, Path]] = None,
    mover: bool = False,
    agregar_timestamp: bool = False
) -> Path:
    """
    Guarda un documento Markdown o texto en la carpeta 'Resultados_md'.

    Funcionalidad:
        Copia (o mueve) un archivo Markdown o de texto plano al subdirectorio
        'Resultados_md' dentro del directorio base indicado (por defecto,
        el directorio de trabajo actual). Soporta formatos .md y .txt.

    Argumentos:
        archivo_origen      (Union[str, Path])           : Ruta del archivo Markdown a guardar.
        directorio_base     (Optional[Union[str, Path]]) : Directorio raíz donde se creará
                                                           'Resultados_md'. Si es None,
                                                           usa el directorio actual (cwd).
        mover               (bool)                       : Si True, mueve el archivo en lugar
                                                           de copiarlo. Por defecto False.
        agregar_timestamp   (bool)                       : Si True, agrega timestamp al nombre
                                                           del archivo. Por defecto False.

    Salidas:
        Path: Ruta completa del archivo guardado en 'Resultados_md'.

    Excepciones:
        FileNotFoundError : Si el archivo origen no existe.
        ValueError        : Si la extensión no es .md ni .txt.

    Ejemplo:
        >>> ruta = guardar_md("resumen_experimento.md")
        >>> print(ruta)
        Resultados_md/resumen_experimento.md
    """
    archivo_origen = Path(archivo_origen)
    _validar_extension(archivo_origen, EXTENSIONES_MD)

    base = Path(directorio_base) if directorio_base else Path.cwd()
    carpeta_destino = base / CARPETA_MD

    ruta_guardada = _copiar_o_mover_archivo(
        archivo_origen, carpeta_destino, mover=mover, agregar_timestamp=agregar_timestamp
    )

    print(f"[OK] Documento Markdown guardado en: {ruta_guardada}")
    return ruta_guardada


def crear_estructura_resultados(
    directorio_base: Optional[Union[str, Path]] = None
) -> dict:
    """
    Crea todas las carpetas de resultados de forma anticipada.

    Funcionalidad:
        Inicializa de una sola vez las tres carpetas de resultados estándar
        (Resultados_imagenes, Resultados_informes, Resultados_md) dentro del
        directorio base especificado. Útil para preparar la estructura al inicio
        de un script antes de generar cualquier resultado.

    Argumentos:
        directorio_base (Optional[Union[str, Path]]): Directorio raíz donde se crearán
                                                      las carpetas. Si es None, usa el
                                                      directorio actual (cwd).

    Salidas:
        dict: Diccionario con las rutas creadas, con claves:
              'imagenes' (Path), 'informes' (Path), 'md' (Path).

    Ejemplo:
        >>> rutas = crear_estructura_resultados()
        >>> print(rutas['imagenes'])
        /home/usuario/proyecto/Resultados_imagenes
    """
    base = Path(directorio_base) if directorio_base else Path.cwd()

    rutas = {
        "imagenes" : _crear_carpeta(base / CARPETA_IMAGENES),
        "informes" : _crear_carpeta(base / CARPETA_INFORMES),
        "md"       : _crear_carpeta(base / CARPETA_MD),
    }

    print(f"[OK] Estructura de resultados creada en: {base}")
    for clave, ruta in rutas.items():
        print(f"    [{clave}] -> {ruta}")

    return rutas


def listar_resultados(
    directorio_base: Optional[Union[str, Path]] = None
) -> dict:
    """
    Lista los archivos existentes en cada carpeta de resultados.

    Funcionalidad:
        Recorre las tres carpetas de resultados estándar y devuelve un diccionario
        con las listas de archivos encontrados en cada una. Si una carpeta no existe,
        su entrada en el diccionario será una lista vacía.

    Argumentos:
        directorio_base (Optional[Union[str, Path]]): Directorio raíz donde se buscan
                                                      las carpetas. Si es None, usa el
                                                      directorio actual (cwd).

    Salidas:
        dict: Diccionario con listas de objetos Path, con claves:
              'imagenes' (list[Path]), 'informes' (list[Path]), 'md' (list[Path]).

    Ejemplo:
        >>> resultados = listar_resultados()
        >>> for img in resultados['imagenes']:
        ...     print(img.name)
    """
    base = Path(directorio_base) if directorio_base else Path.cwd()

    carpetas = {
        "imagenes" : base / CARPETA_IMAGENES,
        "informes" : base / CARPETA_INFORMES,
        "md"       : base / CARPETA_MD,
    }

    resultados = {}
    for clave, carpeta in carpetas.items():
        if carpeta.exists():
            archivos = [f for f in carpeta.iterdir() if f.is_file()]
            resultados[clave] = archivos
            print(f"[{clave.upper()}] {carpeta.name} ({len(archivos)} archivos):")
            for archivo in archivos:
                print(f"    - {archivo.name}")
        else:
            resultados[clave] = []
            print(f"[{clave.upper()}] Carpeta '{carpeta.name}' no existe aún.")

    return resultados


# =============================================================================
# Código main — Demostración de uso de la librería
# =============================================================================

if __name__ == "__main__":

    import tempfile

    print("=" * 60)
    print("  resultados.py - Demostracion de uso")
    print("=" * 60)

    # Usamos un directorio temporal para la demo sin ensuciar el proyecto
    with tempfile.TemporaryDirectory() as dir_demo:

        base_demo = Path(dir_demo)
        print(f"\n[DEMO] Directorio de prueba: {base_demo}\n")

        # 1. Crear la estructura de carpetas anticipadamente
        print("-- Paso 1: Crear estructura de resultados --")
        rutas = crear_estructura_resultados(base_demo)

        # 2. Crear archivos de prueba temporales para simular resultados reales
        print("\n-- Paso 2: Crear archivos de prueba --")

        archivo_png  = base_demo / "grafico_ejemplo.png"
        archivo_pdf  = base_demo / "reporte_ejemplo.pdf"
        archivo_md   = base_demo / "notas_ejemplo.md"

        archivo_png.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)  # PNG mínimo falso
        archivo_pdf.write_bytes(b"%PDF-1.4\n%EOF")                      # PDF mínimo falso
        archivo_md.write_text("# Notas de ejemplo\n\nContenido de prueba.", encoding="utf-8")

        print(f"  Creado: {archivo_png.name}")
        print(f"  Creado: {archivo_pdf.name}")
        print(f"  Creado: {archivo_md.name}")

        # 3. Usar las funciones de la librería para guardar en las carpetas
        print("\n-- Paso 3: Guardar archivos con la librería --")
        guardar_imagen(archivo_png,  directorio_base=base_demo)
        guardar_informe(archivo_pdf, directorio_base=base_demo)
        guardar_md(archivo_md,       directorio_base=base_demo)

        # 4. Guardar con timestamp activado
        print("\n-- Paso 4: Guardar con timestamp --")
        guardar_imagen(archivo_png, directorio_base=base_demo, agregar_timestamp=True)

        # 5. Listar todos los resultados generados
        print("\n-- Paso 5: Listar resultados --")
        listar_resultados(base_demo)

    print("\n[DEMO] Finalizada correctamente.")
