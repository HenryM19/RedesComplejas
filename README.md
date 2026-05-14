# Templates Library

Templates Library es una librería Python para crear proyectos con estructura
estandarizada, organizar resultados generados por scripts y convertir documentos
Markdown a LaTeX usando plantillas académicas.

## Instalación

Desde el repositorio local:

```bash
pip install -e .
```

Con dependencias de desarrollo:

```bash
pip install -e ".[dev]"
```

## Uso rápido

Crear un proyecto:

```bash
create-project mi_analisis --type python
create-project practica_latex --type latex
create-project notebook_lab --type notebook
```

Convertir Markdown a LaTeX:

```bash
md-a-latex informe.md
md-a-latex informe.md --salida informe.tex --compilar
```

Usar la API desde Python:

```python
from templates_library import crear_proyecto, guardar_imagen, crear_estructura_resultados

crear_proyecto("mi_analisis", tipo="python")
crear_estructura_resultados()
guardar_imagen("grafico.png", agregar_timestamp=True)
```

## Módulos principales

### `templates_library.modulos.proyectos`

Crea proyectos base para distintos flujos de trabajo.

Tipos incluidos:

- `python`
- `latex`
- `julia`
- `notebook`
- `matlab`

Ejemplo:

```python
from templates_library.modulos.proyectos import crear_proyecto

ruta = crear_proyecto("control_lab", tipo="latex")
print(ruta)
```

### `templates_library.modulos.resultados`

Organiza archivos producidos por análisis, simulaciones o reportes.

Funciones públicas:

- `guardar_imagen()`
- `guardar_informe()`
- `guardar_md()`
- `crear_estructura_resultados()`
- `listar_resultados()`

### `templates_library.modulos.conversion`

Convierte archivos Markdown a documentos LaTeX completos.

```python
from pathlib import Path
from templates_library.modulos.conversion import ConversorMdLatex

conversor = ConversorMdLatex(Path("informe.md"), compilar=False)
tex = conversor.convertir()
```

## Estructura del repositorio

```text
Templates_Library/
├── src/
│   └── templates_library/
│       ├── __init__.py
│       ├── modulos/
│       │   ├── __init__.py
│       │   ├── conversion.py
│       │   ├── proyectos.py
│       │   └── resultados.py
│       ├── templates/
│       │   ├── guia_estilos_codigo.md
│       │   ├── latex_report/
│       │   └── slides_HTML/
│       └── utils/
│           ├── __init__.py
│           └── recursos.py
├── tests/
├── docs/
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── CHANGELOG.md
```

## Desarrollo

Ejecutar pruebas:

```bash
pytest
```

Verificar importación y entry points:

```bash
python -m templates_library.modulos.proyectos --list_type
python -m templates_library.modulos.conversion --help
```

## Publicación en PyPI

Construir el paquete:

```bash
python -m build
```

Publicar con Twine:

```bash
twine upload dist/*
```

## Licencia

MIT. Consulta `LICENSE` para más detalles.
