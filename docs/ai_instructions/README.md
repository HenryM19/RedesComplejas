# AI Instructions Templates

Esta carpeta contiene plantillas de instrucciones para que distintas IAs usen
`templates_library` como herramienta local en otros proyectos.

La idea no es copiar el codigo de esta libreria en cada proyecto. La idea es
instalarla una vez con:

```powershell
cd C:\GitHub\Templates_Library
pip install -e .
```

Luego, en cada proyecto donde quieras trabajar con IA, copia el archivo que
corresponda:

| Herramienta | Copiar desde | Copiar hacia |
|---|---|---|
| Codex | `AGENTS.template.md` | `AGENTS.md` |
| Claude / Claude Code | `CLAUDE.template.md` | `CLAUDE.md` |
| GitHub Copilot | `copilot-instructions.template.md` | `.github/copilot-instructions.md` |
| Cualquier IA | `LOCAL_TOOLS.template.md` | `docs/local_tools.md` |

Ejemplo:

```powershell
Copy-Item C:\GitHub\Templates_Library\docs\ai_instructions\AGENTS.template.md .\AGENTS.md
Copy-Item C:\GitHub\Templates_Library\docs\ai_instructions\CLAUDE.template.md .\CLAUDE.md
New-Item -ItemType Directory -Force .github
Copy-Item C:\GitHub\Templates_Library\docs\ai_instructions\copilot-instructions.template.md .\.github\copilot-instructions.md
```

Despues de copiarlos, ajusta rutas, tipos de proyecto y reglas especificas del
proyecto actual.
