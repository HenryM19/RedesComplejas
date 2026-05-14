# Formatos\_repos — Librería de Automatización de Proyectos

Colección de scripts Python para la creación, organización y documentación
de proyectos académicos e investigativos. Elimina el trabajo repetitivo de
configurar carpetas, aplicar formatos y generar documentos, permitiendo
enfocarse en el contenido.

**Autor:** Ing. Henry Maldonado · Universidad de Cuenca  
**Repositorio:** `C:\GitHub\Formatos_repos`

---

## Estructura del repositorio

```
Formatos_repos/
│
├── crear_proyecto.py       → Crea la estructura de carpetas de un proyecto nuevo
├── funciones_template.py   → Librería para guardar resultados en carpetas organizadas
├── md_a_latex.py           → Convierte un informe .md a LaTeX con plantilla UCUENCA
│
└── templates/
    ├── guia_estilos_codigo.md      → Convenciones de código por lenguaje
    └── latex/
        ├── main.tex                → Documento principal de referencia
        ├── references.bib          → Plantilla de bibliografía BibTeX
        ├── images/                 → Carpeta de imágenes (vacía)
        └── Template/
            ├── Template.tex        → Estilos, paquetes y cajas UCUENCA
            ├── Portada.tex         → Portada institucional editable
            └── ucuenca_logo.png    → Logo oficial UCUENCA
```

---

## Requisitos

- **Python** ≥ 3.10
- **LaTeX**: TeX Live o MiKTeX (para compilar a PDF)
  - Paquetes necesarios: `FiraSans`, `FiraMono`, `tcolorbox`, `biblatex`,
    `fontawesome5`, `tikz`, `listings`, `geometry`, `fancyhdr`

---

## Guía rápida

### 1 · Crear un proyecto nuevo

```bash
# Python project (main.py + docs/, src/data/, src/functions/, results/reports/, results/images/)
python crear_proyecto.py my_analysis --type python

# LaTeX UCUENCA project (Template/, images/, references.bib, main.tex)
python crear_proyecto.py control_lab --type latex

# Julia project (main.jl + Project.toml + shared resource folders)
python crear_proyecto.py pde_solver --type julia

# Jupyter Notebook project (main.ipynb + shared resource folders)
python crear_proyecto.py notebook_analysis --type notebook

# MATLAB project (main.m + shared resource folders)
python crear_proyecto.py signal_processing --type matlab

# In a specific location
python crear_proyecto.py my_project --type python --2route C:/Projects

# List all available types
python crear_proyecto.py --list_type
```

### Instalacion global en Windows

Si quieres invocar los comandos desde cualquier carpeta de la terminal,
ejecuta una vez:

```bat
install_temaplate_library.bat
```

Eso crea los lanzadores `create_project` y `md-a-latex` en `%USERPROFILE%\bin`
y agrega esa carpeta al `PATH` de tu usuario. Tambien agrega la raiz del
repositorio a `PYTHONPATH`, para que puedas hacer `import funciones_template as ft`
desde cualquier proyecto Python.

Luego, en una terminal nueva, podras usar:

```bat
create_project my_analysis --type python
create_project control_lab --type latex
create_project pde_solver --type julia
create_project notebook_analysis --type notebook
create_project signal_processing --type matlab
md-a-latex informe.md --compilar
```

Despues de abrir una terminal nueva, tambien podras importar la libreria asi:

```python
import funciones_template as ft
```

### 2 · Guardar resultados desde Python

```python
import funciones_template as ft

# Inicializar carpetas de resultados (opcional, se crean solas al guardar)
ft.crear_estructura_resultados()

# Guardar imagen generada con matplotlib
fig.savefig("grafico.png", dpi=150, bbox_inches="tight")
ft.guardar_imagen("grafico.png")                  # → Resultados_imagenes/

# Guardar informe PDF
ft.guardar_informe("reporte.pdf")                 # → Resultados_informes/

# Guardar documento Markdown
ft.guardar_md("notas.md")                         # → Resultados_md/

# Guardar con timestamp para evitar colisiones
ft.guardar_imagen("grafico.png", agregar_timestamp=True)

# Ver qué hay en cada carpeta
ft.listar_resultados()
```

### 3 · Escribir y convertir un informe

```bash
# Desde la carpeta de un proyecto LaTeX:
cd practica1_control

# Escribir el informe en Markdown (ver sección "Formato del informe")
# ...editar informe.md...

# Convertir a LaTeX (crea Template/, images/ y references.bib si no existen)
python ../md_a_latex.py informe.md

# Convertir y compilar a PDF directamente
python ../md_a_latex.py informe.md --compilar

# Si Template/ ya existe, saltar el setup
python ../md_a_latex.py informe.md --sin-setup

# Especificar nombre de salida
python ../md_a_latex.py informe.md --salida practica1_control.tex
```

---

## Referencia de scripts

### `crear_proyecto.py`

Crea la estructura de carpetas y archivos base de un proyecto.

| Argumento      | Descripción                                         |
|----------------|-----------------------------------------------------|
| `nombre`       | Nombre de la carpeta raíz del proyecto              |
| `--type`       | Tipo de proyecto (`python`, `latex`, `julia`, `notebook`, `matlab`) |
| `--2route RUTA`| Directorio donde crear el proyecto (default: cwd)   |
| `--list_type`  | Muestra los tipos disponibles y su estructura       |
| `--quiet`      | Suprime la salida en consola                        |

**Estructura `python`:**

```
mi_proyecto/
    main.py
    src/data/
    src/functions/
    docs/
    results/reports/
    results/images/
    README.md
```

**Estructura `latex`:**

```
mi_practica/
    main.tex
    references.bib
    images/
    Template/
        Template.tex
        Portada.tex
        ucuenca_logo.png
```

**Estructura `julia`:**

```
mi_julia_project/
    Project.toml
    main.jl
    src/data/
    src/functions/
    docs/
    results/reports/
    results/images/
    README.md
```

**Estructura `notebook`:**

```
mi_notebook_project/
    main.ipynb
    src/data/
    src/functions/
    docs/
    results/reports/
    results/images/
    requirements.txt
    README.md
```

**Estructura `matlab`:**

```
mi_matlab_project/
    main.m
    src/data/
    src/functions/
    docs/
    results/reports/
    results/images/
    README.md
```

---

### `funciones_template.py`

Librería importable para guardar resultados en carpetas organizadas.

| Función                         | Descripción                                      |
|---------------------------------|--------------------------------------------------|
| `guardar_imagen(archivo, ...)`  | Copia imagen a `Resultados_imagenes/`            |
| `guardar_informe(archivo, ...)` | Copia PDF/PPTX/DOCX a `Resultados_informes/`    |
| `guardar_md(archivo, ...)`      | Copia .md/.txt a `Resultados_md/`               |
| `crear_estructura_resultados()` | Crea las tres carpetas de resultados de una vez  |
| `listar_resultados()`           | Muestra los archivos en cada carpeta             |

Todas las funciones aceptan los parámetros opcionales:

- `directorio_base` → dónde crear las carpetas (default: cwd)
- `mover=True` → mover en lugar de copiar
- `agregar_timestamp=True` → añade fecha/hora al nombre del archivo

---

### `md_a_latex.py`

Convierte un archivo Markdown a LaTeX con plantilla UCUENCA. Al ejecutarse,
crea automáticamente `Template/`, `images/` y `references.bib` en el
directorio de salida si no existen.

| Argumento            | Descripción                                             |
|----------------------|---------------------------------------------------------|
| `entrada`            | Archivo `.md` de entrada                               |
| `--salida ARCHIVO`   | Nombre del `.tex` de salida (default: mismo nombre)    |
| `--compilar`         | Compila a PDF con latexmk o pdflatex                   |
| `--sin-setup`        | No copia Template/ ni crea imágenes/bib                |

**Conversiones soportadas:**

| Markdown                 | LaTeX generado                          |
|--------------------------|-----------------------------------------|
| Frontmatter `---`        | Portada UCUENCA completa                |
| `# Título`               | `\chapter{}`                            |
| `## Sección`             | `\section{}`                            |
| `### Sub`                | `\subsection{}`                         |
| `#### Sub-sub`           | `\subsubsection{}`                      |
| `**negrita**`            | `\textbf{}`                             |
| `*cursiva*`              | `\textit{}`                             |
| `` `código` ``           | `\texttt{}`                             |
| `$math$`                 | `$math$` (preservado)                   |
| `$$` ... `$$`            | `\[` ... `\]`                           |
| ` ```python `            | `\begin{lstlisting}[language=Python]`   |
| `![alt](img.png)`        | `\begin{figure}[H]...\includegraphics`  |
| `![alt](img.png){0.5\linewidth}` | Figura con ancho personalizado  |
| Tabla Markdown           | `tabularx` + `booktabs`                 |
| `> [!NOTE]`              | `\begin{infobox}`                       |
| `> [!WARNING]`           | `\begin{warningbox}`                    |
| `> [!OBJECTIVE]`         | `\begin{objetivebox}`                   |
| `> [!DELIVERABLE]`       | `\begin{entregabox}`                    |
| `> [!EXERCISE]`          | `\begin{exercisebox}`                   |
| `[texto](url)`           | `\href{url}{texto}`                     |

---

## Formato del informe Markdown

### Frontmatter YAML (metadatos de portada)

```markdown
---
titulo: "Control PID de un Motor DC"
subtitulo: "Práctica 1 — Control Digital"
autor: "Ing. Henry Maldonado"
periodo: "2026-1 · Mar 2026 – Ago 2026"
carrera: "Ingeniería en Telecomunicaciones"
anio: "2026"
departamento: "Departamento de Ingeniería Eléctrica, Electrónica y Telecomunicaciones"
---
```

Todos los campos son opcionales; si se omiten se usan valores por defecto.

### Estructura recomendada del informe

```markdown
---
titulo: "..."
subtitulo: "..."
autor: "..."
---

# Introducción

> [!OBJECTIVE]
> Al finalizar esta práctica el estudiante será capaz de...

## Marco teórico

Ecuación inline: $G(s) = K/(Ts+1)$

Ecuación en bloque:
$$
u(t) = K_p e(t) + K_i \int e \, dt
$$

## Materiales

| Elemento | Cantidad | Descripción |
|----------|:--------:|-------------|
| Arduino  | 1        | Controlador |

## Procedimiento

> [!WARNING]
> Verificar conexiones antes de energizar el sistema.

### Paso 1 — Código

```python
Kp = 1.0
Ki = 0.5
```

## Resultados

![Respuesta al escalón](images/respuesta.png)
![Figura ajustada al 60%](images/detalle.png){0.6\linewidth}

## Conclusiones

- **Punto 1:** descripción.
- **Punto 2:** descripción.

> [!DELIVERABLE]
> - Informe en PDF.
> - Código fuente comentado.
```

### Imágenes

Guardar siempre en `images/` antes de referenciar en el Markdown:

```python
# En Jupyter o script Python
fig.savefig("images/respuesta.png", dpi=150, bbox_inches="tight")
```

---

## Flujos de trabajo típicos

### Informe de práctica de laboratorio

```
1. create_project practica1 --type latex
2. cd practica1
3. Escribir código → guardar gráficas en images/
4. Escribir informe.md
5. python ../md_a_latex.py informe.md --compilar
```

### Análisis de datos en Python

```
1. create_project analisis_datos --type python
2. cd analisis_datos
3. Editar main.py  (importar funciones_template as ft)
4. Al guardar resultados:
      ft.guardar_imagen("grafico.png")
      ft.guardar_informe("reporte.pdf")
5. python ../md_a_latex.py notas.md  (si se quiere informe LaTeX)
```

### Agregar un nuevo tipo de proyecto

Para agregar un tipo (ej. `latex_article`):

1. Crear la carpeta `templates/latex_articulo/` con los archivos base.
2. En `crear_proyecto.py`, agregar una entrada al diccionario `TIPOS_PROYECTO`:

```python
"latex_article": {
    "descripcion": "Artículo LaTeX UCUENCA de una columna.",
    "carpetas": ["images"],
    "archivos_texto": {},
    "directorio_plantilla": "latex_articulo",   # subcarpeta en templates/
},
```

---

## Templates disponibles

Los templates están en `templates/` y pueden editarse libremente:

| Archivo / Carpeta                        | Propósito                             |
|------------------------------------------|---------------------------------------|
| `templates/guia_estilos_codigo.md`       | Convenciones de código por lenguaje y flujo de informes |
| `templates/latex/Template/Template.tex`  | Paquetes, colores y estilos UCUENCA   |
| `templates/latex/Template/Portada.tex`   | Portada institucional editable        |
| `templates/latex/references.bib`         | Plantilla de referencias BibTeX       |
| `templates/latex/main.tex`               | Documento principal de referencia     |

---

*Documentación generada el 2026-05-13 · `C:\GitHub\Formatos_repos\README.md`*
