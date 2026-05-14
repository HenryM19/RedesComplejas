# Templates_Library MCP Server — Guía de Despliegue

## 📋 Descripción

Este es un **servidor MCP (Model Context Protocol)** que expone todas las funciones de tu Templates_Library como herramientas disponibles para Claude.

Con esto, Claude puede:
- ✅ Crear proyectos con estructura automática (python, latex, julia, notebook, matlab)
- ✅ Guardar imágenes, informes y documentos en carpetas organizadas
- ✅ Convertir Markdown a LaTeX
- ✅ Listar archivos de resultados

---

## 🚀 Despliegue en Render (5 minutos)

### Paso 1: Preparar tu repositorio GitHub

En tu repositorio `Templates_Library`, coloca estos archivos en la **raíz**:

```
Templates_Library/
├── mcp_server.py              ← Servidor MCP
├── requirements.txt           ← Dependencias Python
├── crear_proyecto.py          ← Tu código (ya existe)
├── funciones_template.py      ← Tu código (ya existe)
├── md_a_latex.py              ← Tu código (ya existe)
├── README.md                  ← Tu documentación
└── templates/                 ← Tu carpeta (ya existe)
```

### Paso 2: Configurar Render

1. Ve a https://render.com
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio GitHub
4. Rellena la siguiente información:

```
Name:                    templates-library-mcp
Environment:             Python 3.11
Region:                  Selecciona la más cercana

Build Command:           pip install -r requirements.txt
Start Command:           python mcp_server.py

Environment Variables:   (Ninguna necesaria por ahora)
Health Check Path:       /health
```

5. Click en **"Deploy"**

**¡Listo!** Tu servidor estará en vivo en: `https://templates-library-mcp.onrender.com`

---

## 🔗 Conectar con Claude

### Opción A: Claude Desktop App (Recomendado)

1. Descargar [Claude Desktop](https://claude.ai/download)
2. Abrir la carpeta de configuración:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

3. Editar el archivo y agregar:

```json
{
  "mcpServers": {
    "templates-library": {
      "command": "curl",
      "args": ["https://templates-library-mcp.onrender.com/tools"]
    }
  }
}
```

4. Reiniciar Claude Desktop
5. ¡Ya está disponible! Puedes usar comandos como:
   - "Crea un proyecto Python llamado mi_analisis"
   - "Guarda esta imagen en los resultados"
   - "Dame la lista de tipos de proyectos disponibles"

### Opción B: Claude en Web (claude.ai)

Por ahora, Claude.ai no soporta MCP servers directamente, pero puedes:
1. Usar Claude Desktop App (Opción A)
2. O llamar al API manualmente desde tus scripts

---

## 📡 Endpoints disponibles

### Health Check
```
GET /health
```
Verifica que el servidor está vivo.

### Crear Proyecto
```
POST /tools/crear_proyecto
```
**Body:**
```json
{
  "nombre_proyecto": "mi_analisis",
  "tipo": "python",
  "directorio_base": "/home/user/projects"
}
```
**Tipos:** `python`, `latex`, `julia`, `notebook`, `matlab`

### Guardar Imagen
```
POST /tools/guardar_imagen
```
**Body:**
```json
{
  "archivo_origen": "/ruta/a/grafico.png",
  "directorio_base": "/home/user/mi_proyecto",
  "agregar_timestamp": false
}
```

### Guardar Informe
```
POST /tools/guardar_informe
```
Igual que guardar_imagen, pero para PDF, PPTX, DOCX, etc.

### Guardar Markdown
```
POST /tools/guardar_md
```
Igual que guardar_imagen, pero para .md y .txt.

### Listar Tipos de Proyectos
```
GET /tools/listar_tipos
```

### Crear Estructura de Resultados
```
POST /tools/crear_estructura_resultados
```

### Listar Resultados
```
GET /tools/listar_resultados?directorio_base=/ruta
```

### Ver todas las herramientas
```
GET /tools
```

---

## 🔧 Troubleshooting

### El servidor no inicia
- Verifica que `requirements.txt` está en la raíz
- Verifica que `crear_proyecto.py`, `funciones_template.py` y `templates/` están en la raíz

### Error 404 en `/health`
- Espera 30 segundos después del deploy
- Recarga la página

### El servidor "duerme" (Free tier)
- Es normal, se activa automáticamente cuando accedes
- Espera 30 segundos el primer acceso

### Quiero despliegue 24/7 sin delays
- Upgrade a un tier de pago en Render (desde $7/mes)
- O usa Railway.app en su lugar

---

## 📝 Ejemplos de uso

### Con cURL

```bash
# Crear proyecto Python
curl -X POST https://templates-library-mcp.onrender.com/tools/crear_proyecto \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_proyecto": "analisis_datos",
    "tipo": "python",
    "directorio_base": "/home/user/projects"
  }'

# Guardar imagen
curl -X POST https://templates-library-mcp.onrender.com/tools/guardar_imagen \
  -H "Content-Type: application/json" \
  -d '{
    "archivo_origen": "/home/user/projects/analisis_datos/grafico.png"
  }'

# Listar tipos disponibles
curl https://templates-library-mcp.onrender.com/tools/listar_tipos
```

### Con Python

```python
import requests

API_URL = "https://templates-library-mcp.onrender.com"

# Crear proyecto
response = requests.post(
    f"{API_URL}/tools/crear_proyecto",
    json={
        "nombre_proyecto": "mi_proyecto",
        "tipo": "python"
    }
)
print(response.json())

# Guardar imagen
response = requests.post(
    f"{API_URL}/tools/guardar_imagen",
    json={"archivo_origen": "grafico.png"}
)
print(response.json())
```

### Con Claude (usando Claude Desktop)

```
Usuario: Crea un proyecto LaTeX llamado "practica1" en /home/user/proyectos
Claude: [Usa la herramienta crear_proyecto]
```

---

## 🔐 Seguridad

- **No hay autenticación por defecto** (perfecta para uso local)
- Si quieres agregar autenticación, edita `mcp_server.py` y agrega middleware
- Los archivos se guardan **localmente en tu máquina/servidor**, no en la nube

---

## 📦 Versiones

- Python ≥ 3.10
- FastAPI 0.104.1
- Uvicorn 0.24.0

---

## 🆘 Soporte

Para problemas:
1. Revisa los logs en Render (dashboard → tu servicio → Logs)
2. Verifica que todos los archivos están en la raíz del repositorio
3. Intenta `/health` para confirmar que el servidor está vivo

---

**¡Listo para usar!** 🎉 Ya puedes crear proyectos y guardar resultados automáticamente desde Claude.
