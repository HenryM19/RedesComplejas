# Herramientas Locales Disponibles

Este proyecto puede usar la libreria local `templates_library`.

Antes de generar manualmente carpetas, plantillas, reportes o estructuras de
resultados, revisa si existe un comando o funcion de `templates_library` que ya
resuelva la tarea.

## Instalacion Esperada

La libreria debe estar instalada en modo editable desde:

```powershell
cd C:\GitHub\Templates_Library
pip install -e .
```

Verificacion:

```powershell
python -c "import templates_library as tl; print(tl.__version__)"
crear_proyecto --help
md_a_latex --help
```

## Reglas De Uso

- No crees manualmente una estructura de proyecto si puedes usar `crear_proyecto`.
- No escribas manualmente una plantilla LaTeX completa si puedes usar `md_a_latex`.
- No organices resultados copiando archivos a mano si puedes usar `guardar_imagen`, `guardar_informe`, `guardar_md`, `crear_estructura_resultados` o `listar_resultados`.
- No generes PDFs completos en la respuesta de la IA. Genera Markdown o LaTeX y usa las herramientas locales para convertir o compilar.
- Antes de proponer codigo nuevo, revisa si la libreria ya expone una funcion equivalente.
- Si una herramienta falla, muestra el error y propone el siguiente paso minimo.

## Comandos Principales

Crear proyectos:

```powershell
crear_proyecto nombre_proyecto --type python
crear_proyecto nombre_proyecto --type latex
crear_proyecto nombre_proyecto --type julia
crear_proyecto nombre_proyecto --type notebook
crear_proyecto nombre_proyecto --type matlab
```

Crear en una ruta especifica:

```powershell
crear_proyecto nombre_proyecto --type python --base C:\GitHub\test
```

Organizar resultados:

```powershell
crear_estructura_resultados --base .
guardar_imagen grafico.png --base .
guardar_informe reporte.pdf --base .
guardar_md notas.md --base .
listar_resultados --base .
```

Convertir Markdown a LaTeX:

```powershell
md_a_latex informe.md
md_a_latex informe.md --salida informe.tex
md_a_latex informe.md --compilar
```

## Uso Desde Python

```python
import templates_library as tl

tl.crear_proyecto("mi_proyecto", tipo="python")
tl.crear_estructura_resultados()
tl.guardar_imagen("grafico.png", agregar_timestamp=True)
```

```python
from pathlib import Path
from templates_library import ConversorMdLatex

ConversorMdLatex(Path("informe.md")).convertir()
```

## Preferencias

- Usa comandos de terminal cuando la tarea sea crear estructuras, convertir documentos o guardar archivos.
- Usa imports de Python cuando estes escribiendo scripts reproducibles.
- Mantén los nombres principales con guion bajo, igual que las funciones Python: `crear_proyecto`, `md_a_latex`, `guardar_md`.
- Los alias con guion medio existen por compatibilidad, pero no son el estilo principal de este proyecto.
