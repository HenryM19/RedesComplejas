# Contributing

Gracias por contribuir a Templates Library. Esta guía mantiene el proyecto
ordenado, testeable y listo para empaquetarse.

## Preparar el entorno

```bash
git clone https://github.com/henrr/Templates_Library.git
cd Templates_Library
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Convenciones de código

Cada archivo Python debe mantener esta estructura:

1. Documentación introductoria del propósito del módulo.
2. Carga de librerías estándar, externas y locales.
3. Constantes del módulo, si aplican.
4. Funciones o clases con docstrings completos.
5. Código `main` documentado solo cuando el módulo exponga CLI.

Agrupa funciones por funcionalidad, no por tamaño o dificultad. Por ejemplo:

- `modulos/proyectos.py`: creación y validación de proyectos.
- `modulos/resultados.py`: guardado, movimiento y listado de resultados.
- `modulos/conversion.py`: conversión Markdown a LaTeX.

## Pruebas

Antes de abrir un pull request:

```bash
pytest
python -m compileall src
```

Agrega pruebas cuando cambies comportamiento público, rutas de plantillas,
validaciones o entry points.

## Commits y pull requests

- Mantén los cambios enfocados en un solo propósito.
- Describe qué cambia y cómo se verificó.
- No incluyas archivos generados, builds ni cachés.
- Actualiza `README.md` o `CHANGELOG.md` si cambias la API pública.

## Publicación

Solo los mantenedores deben publicar versiones. Para una nueva versión:

1. Actualizar `version` en `pyproject.toml`.
2. Actualizar `__version__` en `src/templates_library/__init__.py`.
3. Agregar notas en `CHANGELOG.md`.
4. Ejecutar pruebas y construir con `python -m build`.
