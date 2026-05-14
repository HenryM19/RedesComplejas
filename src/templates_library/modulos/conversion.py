"""
md_a_latex.py
=============
Convierte un archivo Markdown (.md) a un documento LaTeX completo listo para
compilar, usando la plantilla institucional UCUENCA. Al ejecutarse, crea
automáticamente en el directorio de salida la carpeta Template/ (con los
archivos de estilo), la carpeta images/ y un references.bib vacío si no
existen, de modo que el .tex generado compile sin pasos adicionales.

Cajas especiales soportadas en blockquotes:
    > [!NOTE]        → infobox      (azul claro)
    > [!WARNING]     → warningbox   (amarillo)
    > [!OBJECTIVE]   → objetivebox  (objetivos de aprendizaje)
    > [!DELIVERABLE] → entregabox   (entregables)
    > [!EXERCISE]    → exercisebox  (ejercicio práctico)
    > texto libre    → quote

Uso desde terminal:
    python md_a_latex.py informe.md
    python md_a_latex.py informe.md --salida practica1.tex
    python md_a_latex.py informe.md --compilar
    python md_a_latex.py informe.md --sin-setup   (no copiar Template/)

Autor: Henry Maldonado
Fecha: 2026-05-12
"""

# =============================================================================
# Carga de librerías
# =============================================================================

import re
import sys
import shutil
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import Optional

from templates_library.utils.recursos import obtener_directorio_templates


# =============================================================================
# Definición de constantes
# =============================================================================

# Directorio de templates, relativo a este script
DIR_TEMPLATES: Path = obtener_directorio_templates()

# Subcarpeta de la plantilla LaTeX dentro de DIR_TEMPLATES
DIR_TEMPLATE_LATEX: Path = DIR_TEMPLATES / 'latex_report'

# Expresiones regulares
RE_FRONTMATTER  = re.compile(r'^---[ \t]*\n(.*?)\n---[ \t]*\n', re.DOTALL)
RE_CODIGO_INICIO = re.compile(r'^```(\w*)$')

# Mapa de lenguajes Markdown → identificador lstlisting
LANG_MAP: dict[str, str] = {
    'python':     'Python',
    'py':         'Python',
    'julia':      'Julia',
    'cpp':        'C++',
    'c++':        'C++',
    'c':          'C',
    'javascript': 'JavaScript',
    'js':         'JavaScript',
    'dart':       'Dart',
    'matlab':     'Matlab',
    'bash':       'bash',
    'sh':         'bash',
    'latex':      'TeX',
    'tex':        'TeX',
    'arduino':    'Arduino',
}

# Mapa tipo blockquote → entorno LaTeX UCUENCA
BLOCKQUOTE_ENTORNOS: dict[str, str] = {
    'note':        'infobox',
    'warning':     'warningbox',
    'objective':   'objetivebox',
    'deliverable': 'entregabox',
    'exercise':    'exercisebox',
    'quote':       'quote',
}

# Patrones para detectar el tipo de blockquote desde la primera línea
BLOCKQUOTE_KEYWORDS: list[tuple[str, str]] = [
    (r'^\[!NOTE\]',          'note'),
    (r'^\[!WARNING\]',       'warning'),
    (r'^\[!OBJECTIVE\]',     'objective'),
    (r'^\[!DELIVERABLE\]',   'deliverable'),
    (r'^\[!EXERCISE\]',      'exercise'),
    (r'^\*\*[Nn]ota',        'note'),
    (r'^\*\*[Aa]dvertencia', 'warning'),
    (r'^\*\*[Oo]bjetivo',    'objective'),
    (r'^\*\*[Ee]ntregable',  'deliverable'),
    (r'^\*\*[Ee]jercicio',   'exercise'),
]


# =============================================================================
# Definición de funciones auxiliares
# =============================================================================

def escapar_latex(texto: str) -> str:
    """
    Escapa caracteres especiales de LaTeX en texto plano.

    Funcionalidad:
        Sustituye caracteres con significado especial en LaTeX por su
        representación segura. La barra invertida se procesa primero.
        No escapa: $ (math inline) ni { } (necesarios en comandos generados).

    Argumentos:
        texto (str): Texto plano a procesar.

    Salidas:
        str: Texto con caracteres LaTeX escapados.
    """
    texto = texto.replace('\\', r'\textbackslash{}')
    for char, escape in [
        ('&', r'\&'), ('%', r'\%'), ('#', r'\#'),
        ('^', r'\textasciicircum{}'), ('~', r'\textasciitilde{}'),
    ]:
        texto = texto.replace(char, escape)
    return texto


def detectar_tipo_blockquote(primera_linea: str) -> tuple[str, str]:
    """
    Identifica el tipo de caja UCUENCA a partir de la primera línea del blockquote.

    Funcionalidad:
        Compara la primera línea contra los patrones de BLOCKQUOTE_KEYWORDS.
        Si hay coincidencia, retorna el tipo y la línea sin el marcador.
        Si no hay coincidencia, retorna 'quote' y la línea sin cambios.

    Argumentos:
        primera_linea (str): Primera línea del blockquote (sin el '>' inicial).

    Salidas:
        tuple[str, str]: (tipo, linea_limpia).
    """
    for patron, tipo in BLOCKQUOTE_KEYWORDS:
        if re.match(patron, primera_linea.strip()):
            linea_limpia = re.sub(patron, '', primera_linea.strip()).strip()
            return tipo, linea_limpia
    return 'quote', primera_linea


# =============================================================================
# Definición de la clase principal
# =============================================================================

class ConversorMdLatex:
    """
    Convierte un archivo Markdown a un proyecto LaTeX compilable con plantilla UCUENCA.

    Funcionalidad:
        1. Parsea el frontmatter YAML (título, autor, período, etc.).
        2. Prepara el directorio de salida: copia Template/, crea images/,
           copia references.bib si no existen.
        3. Convierte el cuerpo Markdown a LaTeX elemento por elemento.
        4. Escribe el archivo .tex listo para compilar.
        5. Opcionalmente compila a PDF con latexmk.

    Argumentos (constructor):
        ruta_md      (Path)         : Archivo .md de entrada.
        ruta_salida  (Optional[Path]): Archivo .tex de salida. None → mismo nombre.
        sin_setup    (bool)         : Si True, no copia Template/ ni crea carpetas.
        compilar     (bool)         : Si True, compila a PDF tras generar el .tex.
    """

    def __init__(
        self,
        ruta_md:     Path,
        ruta_salida: Optional[Path] = None,
        sin_setup:   bool = False,
        compilar:    bool = False,
    ) -> None:
        self.ruta_md    = Path(ruta_md)
        self.ruta_salida = Path(ruta_salida) if ruta_salida else self.ruta_md.with_suffix('.tex')
        self.sin_setup  = sin_setup
        self.compilar   = compilar

        self.frontmatter: dict[str, str] = {}
        self.cuerpo_md:   str = ''

    # ------------------------------------------------------------------
    # Método principal
    # ------------------------------------------------------------------

    def convertir(self) -> Path:
        """
        Ejecuta el flujo completo: setup → parse → conversión → escritura → (compilar).

        Funcionalidad:
            Orquesta todos los pasos: preparar directorio de salida, parsear
            frontmatter, procesar líneas Markdown y ensamblar el documento LaTeX.

        Argumentos:
            None

        Salidas:
            Path: Ruta al archivo .tex generado.
        """
        texto = self.ruta_md.read_text(encoding='utf-8')
        self._parsear_frontmatter(texto)

        if not self.sin_setup:
            self._preparar_directorio_latex()

        cuerpo_tex = self._procesar_lineas(self.cuerpo_md.splitlines())

        contenido = '\n'.join([
            self._generar_encabezado(),
            cuerpo_tex,
            self._generar_pie(),
        ])

        self.ruta_salida.write_text(contenido, encoding='utf-8')
        print(f'[OK] LaTeX generado  : {self.ruta_salida}')

        if self.compilar:
            self._compilar_pdf()

        return self.ruta_salida

    # ------------------------------------------------------------------
    # Setup del directorio de salida
    # ------------------------------------------------------------------

    def _preparar_directorio_latex(self) -> None:
        """
        Crea en el directorio de salida la estructura necesaria para compilar el .tex.

        Funcionalidad:
            Copia Template/ desde templates/latex_report/Template/ si no existe en el
            directorio de salida. Crea images/ si no existe. Copia references.bib
            si no existe. Informa de cada acción realizada en consola.
            Si templates/ no se encuentra, advierte pero no aborta.

        Argumentos:
            None (usa self.ruta_salida y DIR_TEMPLATE_LATEX).

        Salidas:
            None (efectos en el sistema de archivos).
        """
        dir_salida = self.ruta_salida.parent

        # --- Template/ ---
        origen_template = DIR_TEMPLATE_LATEX / 'Template'
        destino_template = dir_salida / 'Template'

        if not destino_template.exists():
            if origen_template.exists():
                shutil.copytree(str(origen_template), str(destino_template))
                print(f'[OK] Template copiado : {destino_template}')
            else:
                print(f'[!] No se encontró la plantilla en: {origen_template}')
                print(f'    Asegúrate de que templates/latex_report/Template/ esté instalado en el paquete.')
        else:
            print(f'[INFO] Template ya existe: {destino_template}')

        # --- images/ ---
        dir_images = dir_salida / 'images'
        if not dir_images.exists():
            dir_images.mkdir(parents=True)
            print(f'[OK] Carpeta creada   : {dir_images}')
        else:
            print(f'[INFO] images/ ya existe: {dir_images}')

        # --- references.bib ---
        origen_bib  = DIR_TEMPLATE_LATEX / 'references.bib'
        destino_bib = dir_salida / 'references.bib'

        if not destino_bib.exists():
            if origen_bib.exists():
                shutil.copy2(str(origen_bib), str(destino_bib))
                print(f'[OK] Bib copiado      : {destino_bib}')
            else:
                destino_bib.write_text(
                    '% references.bib — Agregar referencias en formato BibTeX\n',
                    encoding='utf-8'
                )
                print(f'[OK] Bib creado vacio : {destino_bib}')
        else:
            print(f'[INFO] references.bib ya existe')

    # ------------------------------------------------------------------
    # Parseo de frontmatter YAML
    # ------------------------------------------------------------------

    def _parsear_frontmatter(self, texto: str) -> None:
        """
        Extrae el bloque YAML delimitado por '---' al inicio del archivo.

        Funcionalidad:
            Carga cada par 'clave: valor' en self.frontmatter y guarda el
            resto del documento en self.cuerpo_md.

        Argumentos:
            texto (str): Contenido completo del archivo .md.

        Salidas:
            None (modifica self.frontmatter y self.cuerpo_md).
        """
        m = RE_FRONTMATTER.match(texto)
        if m:
            for linea in m.group(1).splitlines():
                if ':' in linea:
                    clave, _, valor = linea.partition(':')
                    self.frontmatter[clave.strip()] = valor.strip().strip('"\'')
            self.cuerpo_md = texto[m.end():]
        else:
            self.cuerpo_md = texto

    # ------------------------------------------------------------------
    # Conversión inline
    # ------------------------------------------------------------------

    def _convertir_inline(self, texto: str) -> str:
        """
        Convierte elementos inline de Markdown a sus equivalentes LaTeX.

        Funcionalidad:
            Procesa en orden: código inline (preservado con texttt), math inline
            (preservado tal cual), escapa chars especiales, aplica bold/italic/links.

        Argumentos:
            texto (str): Fragmento de texto Markdown.

        Salidas:
            str: Texto con elementos inline convertidos a LaTeX.
        """
        # 1. Preservar código inline `...`
        ph_code: list[str] = []
        def guardar_code(m: re.Match) -> str:
            ph_code.append(r'\texttt{' + m.group(1).replace('_', r'\_') + '}')
            return f'\x00CODE{len(ph_code)-1}\x00'
        texto = re.sub(r'`([^`]+)`', guardar_code, texto)

        # 2. Preservar math inline $...$
        ph_math: list[str] = []
        def guardar_math(m: re.Match) -> str:
            ph_math.append(m.group(0))
            return f'\x00MATH{len(ph_math)-1}\x00'
        texto = re.sub(r'\$[^$\n]+?\$', guardar_math, texto)

        # 3. Escapar caracteres especiales LaTeX en texto plano
        texto = escapar_latex(texto)

        # 4. Bold y Italic
        texto = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', texto)
        texto = re.sub(r'__(.+?)__',     r'\\textbf{\1}', texto)
        texto = re.sub(r'\*(.+?)\*',     r'\\textit{\1}', texto)
        texto = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\\textit{\1}', texto)

        # 5. Links [texto](url)
        texto = re.sub(r'\[(.+?)\]\((.+?)\)', r'\\href{\2}{\1}', texto)

        # 6. Restaurar placeholders
        for i, c in enumerate(ph_code): texto = texto.replace(f'\x00CODE{i}\x00', c)
        for i, c in enumerate(ph_math): texto = texto.replace(f'\x00MATH{i}\x00', c)

        return texto

    # ------------------------------------------------------------------
    # Conversión de tablas
    # ------------------------------------------------------------------

    def _convertir_tabla(self, filas: list[str]) -> str:
        """
        Convierte un bloque de tabla Markdown a entorno tabularx con booktabs.

        Funcionalidad:
            Usa la fila separadora (|---|) para determinar la alineación de cada
            columna (X=izquierda, c=centro, r=derecha) y genera toprule/midrule/
            bottomrule con la cabecera en negrita.

        Argumentos:
            filas (list[str]): Líneas de la tabla incluyendo cabecera y separador.

        Salidas:
            str: Código LaTeX del entorno tabularx completo.
        """
        if len(filas) < 2:
            return ''

        cabecera    = [c.strip() for c in filas[0].strip('|').split('|')]
        separadores = filas[1].strip('|').split('|')
        num_cols    = len(cabecera)

        alineaciones: list[str] = []
        for sep in separadores:
            s = sep.strip()
            if   s.startswith(':') and s.endswith(':'): alineaciones.append('c')
            elif s.endswith(':'):                        alineaciones.append('r')
            else:                                        alineaciones.append('X')

        lineas = [
            '',
            f'\\begin{{tabularx}}{{\\linewidth}}{{{"".join(alineaciones)}}}',
            '\\toprule',
            ' & '.join(f'\\textbf{{{self._convertir_inline(c)}}}' for c in cabecera) + r' \\',
            '\\midrule',
        ]
        for fila in filas[2:]:
            celdas = [self._convertir_inline(c.strip()) for c in fila.strip('|').split('|')]
            while len(celdas) < num_cols: celdas.append('')
            lineas.append(' & '.join(celdas[:num_cols]) + r' \\')
        lineas += ['\\bottomrule', '\\end{tabularx}', '']

        return '\n'.join(lineas)

    # ------------------------------------------------------------------
    # Flush helpers
    # ------------------------------------------------------------------

    def _flush_lista(self, tipo: str, items: list[str]) -> list[str]:
        """
        Cierra un entorno itemize o enumerate con los ítems acumulados.

        Argumentos:
            tipo  (str)       : 'itemize' o 'enumerate'.
            items (list[str]) : Líneas \\item acumuladas.

        Salidas:
            list[str]: Líneas LaTeX del entorno cerrado.
        """
        if not items:
            return []
        return [f'\\begin{{{tipo}}}'] + items + [f'\\end{{{tipo}}}', '']

    def _flush_blockquote(self, tipo: str, lineas: list[str]) -> list[str]:
        """
        Genera el entorno LaTeX para un blockquote según su tipo UCUENCA.

        Argumentos:
            tipo   (str)       : Clave de BLOCKQUOTE_ENTORNOS.
            lineas (list[str]) : Líneas de contenido del blockquote.

        Salidas:
            list[str]: Líneas LaTeX del entorno cerrado.
        """
        if not lineas:
            return []
        entorno = BLOCKQUOTE_ENTORNOS.get(tipo, 'quote')
        return ['', f'\\begin{{{entorno}}}', '\n'.join(lineas), f'\\end{{{entorno}}}', '']

    # ------------------------------------------------------------------
    # State machine principal
    # ------------------------------------------------------------------

    def _procesar_lineas(self, lineas: list[str]) -> str:
        """
        Convierte las líneas del cuerpo Markdown a LaTeX mediante una máquina de estados.

        Funcionalidad:
            Recorre las líneas manteniendo estado de contexto: bloque de código,
            math display, lista itemize, lista enumerate, tabla, blockquote.
            Cada cambio de contexto cierra el estado anterior antes de abrir el nuevo.
            Al final hace flush de cualquier estado que siga abierto.

        Argumentos:
            lineas (list[str]): Líneas del cuerpo del documento Markdown.

        Salidas:
            str: Cuerpo del documento en LaTeX.
        """
        salida: list[str] = []

        # Estado
        en_codigo        = False
        en_math_display  = False
        en_itemize       = False;  items_acum:  list[str] = []
        en_enumerate     = False;  enum_acum:   list[str] = []
        en_tabla         = False;  filas_tabla: list[str] = []
        en_blockquote    = False;  tipo_bq = 'quote'; lineas_bq: list[str] = []

        def flush_lista():
            nonlocal en_itemize, items_acum, en_enumerate, enum_acum
            if en_itemize:
                salida.extend(self._flush_lista('itemize', items_acum))
                en_itemize = False; items_acum = []
            if en_enumerate:
                salida.extend(self._flush_lista('enumerate', enum_acum))
                en_enumerate = False; enum_acum = []

        def flush_tabla():
            nonlocal en_tabla, filas_tabla
            if en_tabla:
                salida.append(self._convertir_tabla(filas_tabla))
                en_tabla = False; filas_tabla = []

        def flush_bq():
            nonlocal en_blockquote, lineas_bq, tipo_bq
            if en_blockquote:
                salida.extend(self._flush_blockquote(tipo_bq, lineas_bq))
                en_blockquote = False; lineas_bq = []; tipo_bq = 'quote'

        def flush_todo():
            flush_lista(); flush_tabla(); flush_bq()

        for linea in lineas:

            # ── MATH DISPLAY $$...$$  (marcadores solos en su línea) ──────
            if linea.strip() == '$$':
                if not en_math_display:
                    flush_todo(); salida.append('\\['); en_math_display = True
                else:
                    salida.append('\\]'); en_math_display = False
                continue
            if en_math_display:
                salida.append(linea); continue

            # ── BLOQUE DE CÓDIGO ```lang … ``` ────────────────────────────
            m_cod = RE_CODIGO_INICIO.match(linea)
            if m_cod and not en_codigo:
                flush_todo()
                lang_key = m_cod.group(1).lower()
                lang_lst = LANG_MAP.get(lang_key, lang_key.capitalize() if lang_key else '')
                opts = f'[language={lang_lst}]' if lang_lst else ''
                salida.append(f'\\begin{{lstlisting}}{opts}')
                en_codigo = True; continue

            if linea.strip() == '```' and en_codigo:
                salida.extend(['\\end{lstlisting}', ''])
                en_codigo = False; continue

            if en_codigo:
                salida.append(linea); continue

            # ── TABLA ─────────────────────────────────────────────────────
            if linea.startswith('|'):
                flush_lista(); flush_bq()
                en_tabla = True; filas_tabla.append(linea); continue
            elif en_tabla:
                flush_tabla()

            # ── BLOCKQUOTE ────────────────────────────────────────────────
            if linea.startswith('>'):
                flush_lista(); flush_tabla()
                contenido = linea[1:].strip()
                if not en_blockquote:
                    en_blockquote = True
                    tipo_bq, contenido = detectar_tipo_blockquote(contenido)
                if contenido:
                    lineas_bq.append(self._convertir_inline(contenido))
                continue
            elif en_blockquote:
                flush_bq()

            # ── LÍNEA VACÍA ───────────────────────────────────────────────
            if not linea.strip():
                flush_todo(); salida.append(''); continue

            # ── HEADINGS # ## ### #### ────────────────────────────────────
            m = re.match(r'^(#{1,4})\s+(.+)$', linea)
            if m:
                flush_todo()
                nivel = len(m.group(1))
                texto_h = self._convertir_inline(m.group(2))
                cmd = {1: 'chapter', 2: 'section', 3: 'subsection', 4: 'subsubsection'}[nivel]
                salida.extend(['', f'\\{cmd}{{{texto_h}}}']); continue

            # ── IMAGEN ![alt](path) o ![alt](path){ancho} ─────────────────
            m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)(?:\{([^}]*)\})?$', linea.strip())
            if m:
                flush_todo()
                alt   = self._convertir_inline(m.group(1))
                path  = m.group(2)
                ancho = m.group(3) or r'0.85\linewidth'
                salida.extend([
                    '', '\\begin{figure}[H]', '  \\centering',
                    f'  \\includegraphics[width={ancho}]{{{path}}}',
                    f'  \\caption{{{alt}}}',
                    '\\end{figure}', '',
                ]); continue

            # ── LISTA ITEMIZE ─────────────────────────────────────────────
            m = re.match(r'^\s*[*\-+]\s+(.+)$', linea)
            if m:
                flush_tabla(); flush_bq()
                if en_enumerate:
                    salida.extend(self._flush_lista('enumerate', enum_acum))
                    en_enumerate = False; enum_acum = []
                en_itemize = True
                items_acum.append(f'  \\item {self._convertir_inline(m.group(1))}'); continue

            # ── LISTA ENUMERATE ───────────────────────────────────────────
            m = re.match(r'^\s*\d+\.\s+(.+)$', linea)
            if m:
                flush_tabla(); flush_bq()
                if en_itemize:
                    salida.extend(self._flush_lista('itemize', items_acum))
                    en_itemize = False; items_acum = []
                en_enumerate = True
                enum_acum.append(f'  \\item {self._convertir_inline(m.group(1))}'); continue

            # ── REGLA HORIZONTAL ---, ***, ___ ────────────────────────────
            if re.match(r'^(-{3,}|\*{3,}|_{3,})$', linea.strip()):
                flush_todo()
                salida.extend(['', '\\vspace{4pt}\\hrule\\vspace{8pt}', '']); continue

            # ── PÁRRAFO NORMAL ────────────────────────────────────────────
            flush_todo()
            salida.append(self._convertir_inline(linea))

        flush_todo()
        return '\n'.join(salida)

    # ------------------------------------------------------------------
    # Encabezado y pie del documento
    # ------------------------------------------------------------------

    def _generar_encabezado(self) -> str:
        """
        Genera el preámbulo LaTeX y la portada institucional UCUENCA.

        Funcionalidad:
            Extrae metadatos del frontmatter (con valores por defecto si faltan),
            genera \\documentclass, \\input{Template/Template} y la portada
            con las franjas rojas, tipografía FiraSans y colores del Libro de Marca.

        Argumentos:
            None

        Salidas:
            str: Código LaTeX desde \\documentclass hasta \\clearpage.
        """
        fm        = self.frontmatter
        titulo    = fm.get('titulo',        'Título del Documento')
        subtitulo = fm.get('subtitulo',     '')
        autor     = fm.get('autor',         'Ing. Henry Maldonado')
        periodo   = fm.get('periodo',       '')
        carrera   = fm.get('carrera',       'Ingeniería en Telecomunicaciones')
        anio      = fm.get('anio',          str(datetime.date.today().year))
        dep       = fm.get('departamento',  'Departamento de Ingeniería Eléctrica, Electrónica y Telecomunicaciones')

        bloque_periodo   = (f'  {{\\fontsize{{10}}{{12}}\\selectfont\\bfseries\\color{{white!70!UCblue}}'
                            f'\\MakeUppercase{{{periodo}}}}}\\\\[14pt]\n') if periodo else ''
        bloque_subtitulo = (f'  {{\\fontsize{{22}}{{26}}\\selectfont\\bfseries\\color{{white!85!UCblue}}'
                            f'{subtitulo}}}\\\\[6pt]\n') if subtitulo else ''

        return (
            f'% =============================================================\n'
            f'% Generado por md_a_latex.py  ·  Fuente: {self.ruta_md.name}\n'
            f'% =============================================================\n'
            f'\\documentclass[12pt,a4paper,oneside,openany]{{book}}\n'
            f'\\let\\cleardoublepage=\\clearpage\n'
            f'\\input{{Template/Template}}\n\n'
            f'\\begin{{document}}\n\n'
            f'%--------------------------------------------------------------\n'
            f'%  PORTADA\n'
            f'%--------------------------------------------------------------\n'
            f'\\pagestyle{{empty}}\n'
            f'\\begin{{titlepage}}\n'
            f'  \\thispagestyle{{empty}}\n'
            f'  \\pagecolor{{UCblue}}\n'
            f'  \\color{{white}}\n'
            f'  \\begin{{tikzpicture}}[remember picture, overlay]\n'
            f'    \\fill[UCred] ([yshift=-3.8cm]current page.north west)\n'
            f'      rectangle ([yshift=-4.2cm]current page.north east);\n'
            f'    \\fill[UCred] ([yshift=3.6cm]current page.south west)\n'
            f'      rectangle ([yshift=3.2cm]current page.south east);\n'
            f'  \\end{{tikzpicture}}\n'
            f'  \\vspace*{{0.9cm}}\n'
            f'  \\begin{{flushleft}}\n'
            f'    {{\\fontsize{{42}}{{46}}\\selectfont\\bfseries\\textcolor{{white}}{{UCUENCA}}}}\\\\[-6pt]\n'
            f'    {{\\color{{UCred}}\\rule{{0.52\\linewidth}}{{3pt}}}}\\\\[4pt]\n'
            f'    {{\\small\\bfseries\\color{{white!80!UCblue}}\\MakeUppercase{{Ingeniería}}}}\\\\[2pt]\n'
            f'    {{\\fontsize{{7}}{{8}}\\selectfont\\bfseries\\color{{white!60!UCblue}}'
            f'\\MakeUppercase{{{carrera}}}}}\n'
            f'  \\end{{flushleft}}\n'
            f'  \\vspace{{3.8cm}}\n'
            f'  \\begin{{flushleft}}\n'
            f'{bloque_periodo}'
            f'    {{\\fontsize{{38}}{{44}}\\selectfont\\bfseries\\color{{white}}{titulo}}}\\\\[10pt]\n'
            f'{bloque_subtitulo}'
            f'  \\end{{flushleft}}\n'
            f'  \\vfill\n'
            f'  \\begin{{flushleft}}\n'
            f'    {{\\color{{UCred}}\\rule{{0.4\\linewidth}}{{1pt}}}}\\\\[8pt]\n'
            f'    {{\\normalsize\\bfseries\\color{{white}}{autor}}}\\\\[4pt]\n'
            f'    {{\\small\\color{{white!70!UCblue}}{dep}}}\\\\[16pt]\n'
            f'    {{\\footnotesize\\color{{white!50!UCblue}}Cuenca\\,--\\,Ecuador \\quad {anio}}}\n'
            f'  \\end{{flushleft}}\n'
            f'  \\vspace{{0.6cm}}\n'
            f'\\end{{titlepage}}\n'
            f'\\pagecolor{{white}}\\color{{black}}\n'
            f'\\pagestyle{{fancy}}\n\n'
            f'\\tableofcontents\n'
            f'\\clearpage\n'
        )

    def _generar_pie(self) -> str:
        """
        Genera el pie del documento LaTeX (bibliografía y cierre).

        Argumentos:
            None

        Salidas:
            str: Código LaTeX de cierre del documento.
        """
        return (
            '\n%--------------------------------------------------------------\n'
            '%  BIBLIOGRAFÍA\n'
            '%--------------------------------------------------------------\n'
            '\\newpage\n'
            '\\printbibliography\n\n'
            '\\end{document}\n'
        )

    # ------------------------------------------------------------------
    # Compilación a PDF
    # ------------------------------------------------------------------

    def _compilar_pdf(self) -> None:
        """
        Compila el .tex a PDF usando latexmk (preferido) o pdflatex.

        Funcionalidad:
            Detecta si latexmk está disponible (maneja biber y referencias
            automáticamente). Si no, recurre a pdflatex. Ejecuta en el
            directorio del .tex para que las rutas relativas funcionen.

        Argumentos:
            None

        Salidas:
            None (genera el PDF en disco).
        """
        cwd = self.ruta_salida.parent

        if shutil.which('latexmk'):
            cmd = ['latexmk', '-pdf', '-interaction=nonstopmode', self.ruta_salida.name]
            herramienta = 'latexmk'
        elif shutil.which('pdflatex'):
            cmd = ['pdflatex', '-interaction=nonstopmode', self.ruta_salida.name]
            herramienta = 'pdflatex'
        else:
            print('[!] No se encontró latexmk ni pdflatex. Instala TeX Live o MiKTeX.')
            return

        print(f'[INFO] Compilando con {herramienta}...')
        res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)

        pdf = self.ruta_salida.with_suffix('.pdf')
        if res.returncode == 0 and pdf.exists():
            print(f'[OK] PDF generado    : {pdf}')
        else:
            print(f'[ERROR] Error al compilar. Ultimas lineas del log:')
            print(res.stdout[-600:])


# =============================================================================
# Configuración del parser CLI
# =============================================================================

def configurar_parser() -> argparse.ArgumentParser:
    """
    Configura y retorna el parser de argumentos de línea de comandos.

    Argumentos:
        None

    Salidas:
        argparse.ArgumentParser: Parser configurado.
    """
    parser = argparse.ArgumentParser(
        prog='md_a_latex',
        description='Convierte Markdown a LaTeX con plantilla UCUENCA (auto-setup incluido).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Ejemplos:\n'
            '  python md_a_latex.py informe.md\n'
            '  python md_a_latex.py informe.md --salida practica1.tex\n'
            '  python md_a_latex.py informe.md --compilar\n'
            '  python md_a_latex.py informe.md --sin-setup\n'
        )
    )
    parser.add_argument('entrada', type=str,
                        help='Ruta al archivo Markdown de entrada (.md).')
    parser.add_argument('--salida', '-o', type=str, default=None, metavar='ARCHIVO.tex',
                        help='Archivo .tex de salida (por defecto: mismo nombre que entrada).')
    parser.add_argument('--compilar', '-c', action='store_true',
                        help='Compila a PDF con latexmk/pdflatex tras generar el .tex.')
    parser.add_argument('--sin-setup', action='store_true',
                        help='No copia Template/ ni crea images/. Usar si ya existen.')
    return parser


# =============================================================================
# Código main — Punto de entrada
# =============================================================================

def main(argv: Optional[list[str]] = None) -> int:
    """
    Ejecuta la interfaz de línea de comandos para convertir Markdown a LaTeX.

    Funcionalidad:
        Parsea argumentos de terminal, valida el archivo de entrada, ejecuta
        la conversión y retorna un código de salida para scripts.

    Argumentos:
        argv (Optional[list[str]]): Lista de argumentos para pruebas. Si es
                                    None, argparse usa sys.argv.

    Salidas:
        int: Código de salida del proceso.
    """

    parser = configurar_parser()
    args   = parser.parse_args(argv)

    ruta_entrada = Path(args.entrada)

    if not ruta_entrada.exists():
        print(f'[ERROR] El archivo "{ruta_entrada}" no existe.')
        return 1

    if ruta_entrada.suffix.lower() != '.md':
        print(f'[AVISO] El archivo no tiene extensión .md.')

    conversor = ConversorMdLatex(
        ruta_md    = ruta_entrada,
        ruta_salida= Path(args.salida) if args.salida else None,
        sin_setup  = args.sin_setup,
        compilar   = args.compilar,
    )

    try:
        conversor.convertir()
        return 0
    except Exception as e:
        print(f'[ERROR] {e}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
