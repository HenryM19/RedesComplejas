# GitHub Copilot Instructions

Este proyecto puede usar la libreria local `templates_library`.

Cuando generes codigo, scripts o instrucciones, prefiere reutilizar
`templates_library` antes de recrear logica manualmente.

## Reglas

- Para crear proyectos, usa o recomienda `crear_proyecto`.
- Para convertir Markdown a LaTeX, usa o recomienda `md_a_latex`.
- Para organizar archivos de salida, usa o recomienda:
  - `crear_estructura_resultados`
  - `guardar_imagen`
  - `guardar_informe`
  - `guardar_md`
  - `listar_resultados`
- No generes plantillas LaTeX completas si ya existe una plantilla local.
- No inventes una estructura de carpetas si `crear_proyecto` ya cubre el caso.
- Mantén el estilo de nombres con guion bajo para comandos y funciones.

## Comandos Locales

```powershell
crear_proyecto --help
md_a_latex --help
guardar_imagen --help
guardar_informe --help
guardar_md --help
crear_estructura_resultados --help
listar_resultados --help
```

## Uso Python Preferido

```python
import templates_library as tl

tl.crear_proyecto("mi_proyecto", tipo="python")
tl.guardar_md("notas.md")
```

## Notas

Si el usuario pide un resultado final en PDF, sugiere generar primero Markdown
o LaTeX y convertirlo con `md_a_latex`.
