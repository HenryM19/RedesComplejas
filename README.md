# Templates Library

Templates Library es una librería Python para automatizar tareas repetitivas en
proyectos académicos y técnicos:

- crear proyectos con carpetas y archivos base;
- organizar imágenes, informes y notas Markdown en carpetas de resultados;
- convertir documentos Markdown a LaTeX usando plantillas incluidas;
- reutilizar plantillas HTML/LaTeX desde un único paquete local.

Por ahora está pensada para usarse desde este repositorio Git, sin publicarla en
PyPI.

## Instalación Local

Desde la raíz del repositorio:

```powershell
cd C:\GitHub\Templates_Library
pip install -e .
```

El modo editable hace que cualquier cambio en el código del repo se refleje sin
reinstalar. Solo necesitas repetir `pip install -e .` si cambias los comandos
de terminal definidos en `pyproject.toml`.

Para instalar también herramientas de prueba y desarrollo:

```powershell
pip install -e ".[dev]"
```

Para comprobar que quedó instalada:

```powershell
python -c "import templates_library as tl; print(tl.__version__)"
crear_proyecto --help
```

## Uso Desde Terminal

### Crear Proyectos

```powershell
crear_proyecto mi_analisis --type python
crear_proyecto practica_latex --type latex
crear_proyecto simulacion_julia --type julia
crear_proyecto cuaderno_lab --type notebook
crear_proyecto control_matlab --type matlab
```

Crear el proyecto en una carpeta específica:

```powershell
crear_proyecto mi_analisis --type python --base C:\GitHub\test
```

Listar tipos de proyectos disponibles:

```powershell
crear_proyecto --list_type
```

Opciones principales:

| Opción | Descripción |
|---|---|
| `nombre` | Nombre del proyecto a crear. |
| `--type`, `--tipo` | Tipo de proyecto: `python`, `latex`, `julia`, `notebook`, `matlab`. |
| `--base`, `--2route` | Carpeta donde se creará el proyecto. |
| `--list_type`, `--listar-tipos` | Muestra los tipos de proyecto disponibles. |
| `--quiet`, `--silencioso` | Oculta mensajes de progreso. |

### Organizar Resultados

Crear carpetas de resultados:

```powershell
crear_estructura_resultados --base .
```

Guardar archivos:

```powershell
guardar_imagen grafico.png --base .
guardar_informe reporte.pdf --base .
guardar_md notas.md --base .
```

Guardar con timestamp:

```powershell
guardar_imagen grafico.png --base . --agregar-timestamp
```

Mover en lugar de copiar:

```powershell
guardar_md notas.md --base . --mover
```

Listar resultados:

```powershell
listar_resultados --base .
```

Carpetas generadas:

```text
Resultados_imagenes/
Resultados_informes/
Resultados_md/
```

Opciones principales:

| Comando | Descripción |
|---|---|
| `crear_estructura_resultados` | Crea las carpetas estándar de resultados. |
| `guardar_imagen` | Copia o mueve imágenes a `Resultados_imagenes/`. |
| `guardar_informe` | Copia o mueve informes a `Resultados_informes/`. |
| `guardar_md` | Copia o mueve Markdown/texto a `Resultados_md/`. |
| `listar_resultados` | Lista archivos guardados por categoría. |

| Opción | Descripción |
|---|---|
| `--base`, `--directorio-base` | Directorio donde se crean o buscan resultados. |
| `--mover` | Mueve el archivo en lugar de copiarlo. |
| `--agregar-timestamp` | Agrega fecha y hora al nombre del archivo. |

### Convertir Markdown a LaTeX

```powershell
md_a_latex informe.md
md_a_latex informe.md --salida informe.tex
md_a_latex informe.md --compilar
md_a_latex informe.md --sin-setup
```

Opciones principales:

| Opción | Descripción |
|---|---|
| `entrada` | Archivo Markdown de entrada. |
| `--salida`, `-o` | Ruta del archivo `.tex` generado. |
| `--compilar`, `-c` | Intenta compilar a PDF con `latexmk` o `pdflatex`. |
| `--sin-setup` | No copia `Template/`, `images/` ni `references.bib`. |

El comando crea automáticamente, junto al `.tex`, los recursos necesarios para
compilar:

```text
Template/
images/
references.bib
```

## Uso Desde Python

Puedes importar la API principal desde el paquete raíz:

```python
import templates_library as tl

tl.crear_proyecto("mi_analisis", tipo="python")
tl.crear_estructura_resultados()
tl.guardar_imagen("grafico.png", agregar_timestamp=True)
```

También puedes importar funciones específicas:

```python
from templates_library import crear_proyecto, guardar_md, listar_resultados

crear_proyecto("demo", tipo="python")
guardar_md("notas.md")
listar_resultados()
```

### Crear Proyectos

```python
from pathlib import Path
from templates_library import crear_proyecto

ruta = crear_proyecto(
    nombre_proyecto="control_lab",
    tipo="latex",
    directorio_base=Path("C:/GitHub/test"),
    verbose=True,
)

print(ruta)
```

### Organizar Resultados

```python
from templates_library import (
    crear_estructura_resultados,
    guardar_imagen,
    guardar_informe,
    guardar_md,
    listar_resultados,
)

crear_estructura_resultados()
guardar_imagen("grafico.png", agregar_timestamp=True)
guardar_informe("reporte.pdf")
guardar_md("notas.md")
resultados = listar_resultados()
```

### Convertir Markdown a LaTeX

```python
from pathlib import Path
from templates_library import ConversorMdLatex

conversor = ConversorMdLatex(
    ruta_md=Path("informe.md"),
    ruta_salida=Path("informe.tex"),
    compilar=False,
)

tex = conversor.convertir()
print(tex)
```

## Nombres de Comandos

La regla recomendada es simple: el comando principal de terminal usa el mismo
nombre que la función Python.

Ejemplos:

| Python | Terminal |
|---|---|
| `crear_proyecto()` | `crear_proyecto` |
| `guardar_imagen()` | `guardar_imagen` |
| `guardar_informe()` | `guardar_informe` |
| `guardar_md()` | `guardar_md` |
| `crear_estructura_resultados()` | `crear_estructura_resultados` |
| `listar_resultados()` | `listar_resultados` |

También existen alias con guion medio por compatibilidad con estilos comunes de
CLI, por ejemplo `crear-proyecto`, `guardar-imagen` y `md-a-latex`.

## Desinstalar

Para quitar la instalación editable:

```powershell
pip uninstall templates-library
```

Luego puedes verificar que ya no está disponible:

```powershell
python -c "import templates_library"
```

## Instrucciones Para IA

Este repositorio incluye plantillas para que Codex, Claude, Copilot u otra IA
usen `templates_library` como herramienta local en tus otros proyectos.

Están en:

```text
docs/ai_instructions/
```

Archivos incluidos:

| Archivo | Uso recomendado |
|---|---|
| `AGENTS.template.md` | Copiar como `AGENTS.md` para Codex. |
| `CLAUDE.template.md` | Copiar como `CLAUDE.md` para Claude / Claude Code. |
| `copilot-instructions.template.md` | Copiar como `.github/copilot-instructions.md` para GitHub Copilot. |
| `LOCAL_TOOLS.template.md` | Copiar como `docs/local_tools.md` para documentar herramientas locales. |

Ejemplo:

```powershell
Copy-Item C:\GitHub\Templates_Library\docs\ai_instructions\AGENTS.template.md .\AGENTS.md
Copy-Item C:\GitHub\Templates_Library\docs\ai_instructions\CLAUDE.template.md .\CLAUDE.md
New-Item -ItemType Directory -Force .github
Copy-Item C:\GitHub\Templates_Library\docs\ai_instructions\copilot-instructions.template.md .\.github\copilot-instructions.md
```

## Estructura Técnica

```text
Templates_Library/
|-- src/
|   `-- templates_library/
|       |-- __init__.py
|       |-- modulos/
|       |   |-- conversion.py
|       |   |-- proyectos.py
|       |   `-- resultados.py
|       |-- templates/
|       |   |-- guia_estilos_codigo.md
|       |   |-- latex_report/
|       |   `-- slides_HTML/
|       `-- utils/
|           `-- recursos.py
|-- docs/
|   `-- ai_instructions/
|-- tests/
|-- pyproject.toml
|-- README.md
|-- CONTRIBUTING.md
|-- LICENSE
`-- CHANGELOG.md
```

## Desarrollo

Ejecutar pruebas:

```powershell
python -m pytest -q
```

Revisar estilo:

```powershell
python -m ruff check src tests
```

Construir paquete local:

```powershell
python -m build
```

Los artefactos `build/`, `dist/` y `*.egg-info/` no deben subirse al repo.

## Licencia

MIT. Consulta `LICENSE` para más detalles.
