# Instrucciones Para Codex

Este proyecto usa la libreria local `templates_library` como caja de herramientas.

Antes de crear manualmente carpetas, plantillas, reportes o estructuras de
resultados, intenta usar sus comandos o funciones.

## Contexto Local

La libreria se instala desde:

```powershell
C:\GitHub\Templates_Library
```

Instalacion esperada:

```powershell
cd C:\GitHub\Templates_Library
pip install -e .
```

## Reglas Para Codex

- Si el usuario pide crear un proyecto, usa `crear_proyecto`.
- Si el usuario pide una estructura de proyecto, no la generes archivo por archivo si `crear_proyecto` puede hacerlo.
- Si el usuario pide convertir un informe Markdown a LaTeX, usa `md_a_latex`.
- Si el usuario pide organizar resultados, usa `crear_estructura_resultados`, `guardar_imagen`, `guardar_informe`, `guardar_md` o `listar_resultados`.
- Si el usuario pide un PDF, no escribas un PDF en texto. Genera Markdown/LaTeX y usa la herramienta local de conversion.
- Si necesitas saber opciones exactas, ejecuta `<comando> --help`.
- Mantén cambios pequenos y verificables.
- Antes de cerrar una tarea de codigo, ejecuta las pruebas relevantes del proyecto actual.

## Comandos Disponibles

```powershell
crear_proyecto --help
md_a_latex --help
guardar_imagen --help
guardar_informe --help
guardar_md --help
crear_estructura_resultados --help
listar_resultados --help
```

## Ejemplos

Crear un proyecto Python:

```powershell
crear_proyecto mi_analisis --type python --base C:\GitHub\test
```

Crear un proyecto LaTeX:

```powershell
crear_proyecto practica_1 --type latex --base C:\GitHub\test
```

Convertir un informe:

```powershell
md_a_latex informe.md --salida informe.tex
```

Guardar resultados:

```powershell
guardar_imagen grafico.png --base .
guardar_md notas.md --base .
listar_resultados --base .
```

## Uso Desde Python

```python
import templates_library as tl

tl.crear_proyecto("demo", tipo="python")
tl.guardar_md("notas.md")
```
