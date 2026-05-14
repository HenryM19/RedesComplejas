# Claude Instructions

Usa `templates_library` como herramienta local cuando el usuario pida crear
proyectos, organizar resultados o convertir documentos.

## Principio Principal

No recrees manualmente lo que ya existe en `templates_library`.

Antes de generar archivos extensos o estructuras completas, revisa si puedes
usar un comando local.

## Herramientas Locales

```powershell
crear_proyecto
md_a_latex
guardar_imagen
guardar_informe
guardar_md
crear_estructura_resultados
listar_resultados
```

Consulta ayuda cuando tengas dudas:

```powershell
crear_proyecto --help
md_a_latex --help
guardar_md --help
```

## Casos De Uso

Si el usuario pide crear un proyecto:

```powershell
crear_proyecto nombre --type python --base RUTA
```

Si el usuario pide un proyecto LaTeX:

```powershell
crear_proyecto nombre --type latex --base RUTA
```

Si el usuario pide convertir Markdown a LaTeX:

```powershell
md_a_latex informe.md --salida informe.tex
```

Si el usuario pide organizar resultados:

```powershell
crear_estructura_resultados --base .
guardar_imagen grafico.png --base .
guardar_informe reporte.pdf --base .
guardar_md notas.md --base .
```

## Reglas

- Usa los comandos principales con guion bajo.
- No generes PDFs como texto en la conversacion.
- No copies plantillas completas si la herramienta local puede crearlas.
- Si una accion modifica archivos, explica brevemente que comando usaste.
- Si el comando falla, muestra el error relevante y sugiere una correccion concreta.

## Python

Cuando sea mejor dejar un script reproducible, usa:

```python
import templates_library as tl

tl.crear_proyecto("mi_proyecto", tipo="python")
tl.crear_estructura_resultados()
```
