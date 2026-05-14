# Guía de Estilos y Convenciones de Código

> Documento de referencia personal para la estructura, documentación y organización
> de programas en distintos lenguajes y formatos de archivo.  
> **Autor:** Henry Maldonado · **Actualizado:** 2026-05-12

---

## Tabla de contenidos

1. [Python — Archivos `.py`](#1-python--archivos-py)
2. [Jupyter Notebook — Archivos `.ipynb`](#2-jupyter-notebook--archivos-ipynb)
3. [Julia — Archivos `.jl`](#3-julia--archivos-jl)
4. [C++ — Archivos `.cpp` / `.h`](#4-c--archivos-cpp--h)
5. [Arduino — Archivos `.ino`](#5-arduino--archivos-ino)
6. [JavaScript — Archivos `.js`](#6-javascript--archivos-js)
7. [Dart — Archivos `.dart`](#7-dart--archivos-dart)
8. [Organización de resultados](#8-organización-de-resultados)

---

## 1. Python — Archivos `.py`

Todo archivo `.py` sigue **cuatro bloques ordenados**: documentación general,
carga de librerías, definición de funciones y código `main`.

### 1.1 Estructura general

```
archivo.py
├── [1] Docstring general del módulo
├── [2] Carga de librerías
├── [3] Definición de funciones (cada una con su docstring)
└── [4] Bloque main (if __name__ == "__main__":)
```

### 1.2 Bloque 1 — Docstring general del módulo

El docstring va al inicio del archivo, **antes** de cualquier `import`.
Describe qué hace el programa, cómo ejecutarlo y quién lo escribió.

```python
"""
nombre_archivo.py
=================
Descripción breve del propósito del programa en una o dos oraciones.

Descripción extendida opcional: contexto del problema, metodología
empleada, limitaciones conocidas o supuestos importantes.

Uso:
    python nombre_archivo.py [argumentos]

Ejemplo:
    python nombre_archivo.py --entrada datos.csv --salida resultados/

Autor: Henry Maldonado
Fecha: YYYY-MM-DD
"""
```

### 1.3 Bloque 2 — Carga de librerías

Las librerías se importan en el siguiente orden, separadas por un comentario
de sección y una línea en blanco entre grupos:

1. Librerías de la **biblioteca estándar** de Python
2. Librerías de **terceros** (numpy, pandas, matplotlib…)
3. Módulos **propios** del proyecto

```python
# =============================================================================
# Carga de librerías
# =============================================================================

# Biblioteca estándar
import os
import sys
from pathlib import Path

# Terceros
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Módulos propios
import funciones_template as ft
from src.functions import mi_funcion
```

### 1.4 Bloque 3 — Definición de funciones

Cada función lleva un **docstring con cuatro campos obligatorios**:
*Funcionalidad*, *Argumentos* (nombre, tipo y descripción), *Salidas*
(nombre, tipo y descripción) y *Excepciones* si aplica.

```python
# =============================================================================
# Definición de funciones
# =============================================================================

def nombre_funcion(parametro_1: tipo_1, parametro_2: tipo_2) -> tipo_retorno:
    """
    Título breve de una línea.

    Funcionalidad:
        Explicación detallada de qué hace la función, el algoritmo que usa
        o el proceso que ejecuta. Puede ocupar varias líneas.

    Argumentos:
        parametro_1 (tipo_1): Descripción del primer parámetro.
        parametro_2 (tipo_2): Descripción del segundo parámetro.

    Salidas:
        tipo_retorno: Descripción de lo que retorna la función.

    Excepciones:
        ValueError     : Cuándo y por qué se lanza este error.
        FileNotFoundError: Si aplica, describir la condición.

    Ejemplo:
        >>> resultado = nombre_funcion(valor_1, valor_2)
    """
    # Implementación
    pass
```

### 1.5 Bloque 4 — Código `main`

El bloque `main` documenta cada procedimiento significativo con comentarios
de sección y comentarios en línea para las decisiones no obvias.

```python
# =============================================================================
# Código main
# =============================================================================

if __name__ == "__main__":

    # --- Configuración inicial ---
    RUTA_DATOS    = Path("src/data/dataset.csv")
    RUTA_SALIDA   = Path("results/")

    # --- Carga de datos ---
    # Se usa encoding utf-8 porque el CSV puede tener tildes
    datos = pd.read_csv(RUTA_DATOS, encoding="utf-8")

    # --- Procesamiento ---
    resultado = nombre_funcion(datos["columna_a"], datos["columna_b"])

    # --- Guardar resultados ---
    ft.guardar_imagen("grafico_resultado.png")
    ft.guardar_informe("reporte_final.pdf")
```

---

## 2. Jupyter Notebook — Archivos `.ipynb`

Los notebooks alternan celdas **Markdown** y celdas de **código** siguiendo
un patrón narrativo: primero se explica, luego se ejecuta.

### 2.1 Estructura general del notebook

```
notebook.ipynb
├── [Markdown] Título, descripción y objetivo
├── [Markdown] 1. Carga de librerías          → [Código] imports
├── [Markdown] 2. Carga de datos              → [Código] lectura
├── [Markdown] 3. Descripción del problema    → [Código] exploración
├── [Markdown] 4. Metodología / solución      → [Código] procesamiento
├── [Markdown] 5. Resultados                  → [Código] gráficas + guardado
└── [Markdown] 6. Conclusiones
```

### 2.2 Celda Markdown de apertura (obligatoria)

La primera celda siempre es Markdown con el encabezado del notebook:

```markdown
# Título del Análisis o Experimento

**Autor:** Henry Maldonado  
**Fecha:** YYYY-MM-DD  
**Descripción:** Párrafo breve explicando el objetivo del notebook,
el dataset utilizado y el resultado esperado.

---
```

### 2.3 Par Markdown → Código (patrón base)

Cada sección de código va **precedida obligatoriamente** por una celda
Markdown que describe el problema que resuelve el bloque siguiente:

```markdown
## 2. Carga de datos

Se carga el archivo `dataset.csv` desde la carpeta `src/data/`.
Se verifica la forma del DataFrame y se muestran las primeras filas
para confirmar que la carga fue exitosa.
```

```python
# Carga del dataset
df = pd.read_csv("src/data/dataset.csv", encoding="utf-8")

print(f"Shape: {df.shape}")
df.head()
```

### 2.4 Celdas de visualización — guardar siempre los resultados

Toda celda que genere una gráfica debe guardarla en `Resultados_imagenes/`
antes de mostrarla, usando `funciones_template` o directamente con
`savefig`. El nombre del archivo debe ser descriptivo.

```markdown
## 5. Distribución de la variable objetivo

Se grafica el histograma de la variable `precio` para identificar
si sigue una distribución normal o presenta sesgo.
```

```python
import matplotlib.pyplot as plt
import funciones_template as ft

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["precio"], bins=30, color="steelblue", edgecolor="white")
ax.set_title("Distribución de Precio")
ax.set_xlabel("Precio (USD)")
ax.set_ylabel("Frecuencia")
plt.tight_layout()

# Guardar antes de mostrar
fig.savefig("distribucion_precio.png", dpi=150, bbox_inches="tight")
ft.guardar_imagen("distribucion_precio.png")

plt.show()
```

### 2.5 Celda de conclusiones (obligatoria al final)

```markdown
## 6. Conclusiones

- **Hallazgo 1:** Descripción del resultado principal.
- **Hallazgo 2:** Observación secundaria relevante.
- **Próximos pasos:** Qué se haría a continuación.
```

### 2.6 Buenas prácticas para notebooks

- Ejecutar siempre el notebook completo (`Kernel → Restart & Run All`) antes de guardar.
- No dejar celdas con errores o salidas desactualizadas.
- Cada celda de código debe tener **un único propósito**; si hace demasiado, dividirla.
- Usar `display()` en lugar de `print()` para DataFrames y objetos ricos.
- Limpiar las salidas antes de hacer commit a Git (`Kernel → Clear All Outputs`).

---

## 3. Julia — Archivos `.jl`

### 3.1 Estructura general

```
archivo.jl
├── [1] Comentario de cabecera (descripción, autor, fecha)
├── [2] Carga de paquetes (using / import)
├── [3] Definición de funciones con docstrings
└── [4] Bloque principal (función main() o código directo)
```

### 3.2 Cabecera del archivo

```julia
# ==============================================================================
# nombre_archivo.jl
# ==============================================================================
# Descripción: Qué hace este script.
# Autor      : Henry Maldonado
# Fecha      : YYYY-MM-DD
# Uso        : julia nombre_archivo.jl
# ==============================================================================
```

### 3.3 Carga de paquetes

```julia
# ------------------------------------------------------------------------------
# Carga de paquetes
# ------------------------------------------------------------------------------
using CSV
using DataFrames
using Plots
using Statistics
```

### 3.4 Definición de funciones

El docstring en Julia se escribe **antes** de la función con comillas triples:

```julia
"""
    nombre_funcion(param1::Tipo1, param2::Tipo2) -> TipoRetorno

Descripción breve de la función.

# Argumentos
- `param1::Tipo1`: Descripción del primer parámetro.
- `param2::Tipo2`: Descripción del segundo parámetro.

# Retorna
- `TipoRetorno`: Descripción del valor de retorno.

# Ejemplo
```julia
resultado = nombre_funcion(valor1, valor2)
```
"""
function nombre_funcion(param1::Tipo1, param2::Tipo2)::TipoRetorno
    # Implementación
end
```

### 3.5 Bloque principal

```julia
# ------------------------------------------------------------------------------
# Código principal
# ------------------------------------------------------------------------------

function main()
    # Carga de datos
    df = CSV.read("src/data/datos.csv", DataFrame)

    # Procesamiento
    resultado = nombre_funcion(df.columna1, df.columna2)

    # Guardar figura
    p = plot(resultado, title="Mi gráfica")
    savefig(p, "Resultados_imagenes/mi_grafica.png")
end

main()
```

---

## 4. C++ — Archivos `.cpp` / `.h`

### 4.1 Estructura general

```
proyecto_cpp/
├── src/
│   ├── main.cpp         ← Punto de entrada
│   ├── modulo.h         ← Declaraciones
│   └── modulo.cpp       ← Implementaciones
```

### 4.2 Cabecera de archivo (`.cpp` y `.h`)

```cpp
/**
 * @file    nombre_archivo.cpp
 * @brief   Descripción breve del propósito del archivo.
 *
 * Descripción extendida opcional del módulo.
 *
 * @author  Henry Maldonado
 * @date    YYYY-MM-DD
 */
```

### 4.3 Includes y namespaces

```cpp
// ----------------------------------------------------------------------------
// Includes
// ----------------------------------------------------------------------------
#include <iostream>
#include <vector>
#include <string>
#include "modulo.h"

// Evitar `using namespace std;` en archivos de cabecera
using namespace std;
```

### 4.4 Documentación de funciones (estilo Doxygen)

```cpp
/**
 * @brief   Descripción breve de la función.
 *
 * Descripción detallada del comportamiento, algoritmo o proceso.
 *
 * @param   param1  Descripción del primer parámetro (tipo: int).
 * @param   param2  Descripción del segundo parámetro (tipo: string).
 * @return  Descripción del valor retornado (tipo: double).
 *
 * @throws  std::invalid_argument  Cuándo se lanza esta excepción.
 */
double nombre_funcion(int param1, const string& param2) {
    // Implementación
    return 0.0;
}
```

### 4.5 Función `main`

```cpp
// ----------------------------------------------------------------------------
// Función principal
// ----------------------------------------------------------------------------
int main(int argc, char* argv[]) {

    // --- Configuración inicial ---
    string ruta_datos = "src/data/datos.txt";

    // --- Procesamiento ---
    double resultado = nombre_funcion(42, ruta_datos);

    // --- Salida ---
    cout << "Resultado: " << resultado << endl;

    return 0;
}
```

---

## 5. Arduino — Archivos `.ino`

### 5.1 Estructura general

```
sketch_nombre/
└── sketch_nombre.ino
    ├── [1] Cabecera comentada
    ├── [2] Includes de librerías
    ├── [3] Definición de pines y constantes
    ├── [4] Variables globales
    ├── [5] Definición de funciones auxiliares
    ├── [6] setup()
    └── [7] loop()
```

### 5.2 Cabecera del sketch

```cpp
/**
 * Proyecto : Nombre del Proyecto
 * Archivo  : sketch_nombre.ino
 * Descripción: Qué hace el sketch, qué hardware controla y cómo.
 *
 * Hardware:
 *   - Placa  : Arduino Uno / Mega / ESP32 (especificar)
 *   - Sensor : Nombre y modelo del sensor
 *   - Actuador: Nombre y modelo del actuador
 *
 * Conexiones:
 *   PIN 2  → Sensor de temperatura (DATA)
 *   PIN 13 → LED indicador
 *
 * Autor    : Henry Maldonado
 * Fecha    : YYYY-MM-DD
 */
```

### 5.3 Definición de pines, constantes y variables

```cpp
// ----------------------------------------------------------------------------
// Librerías
// ----------------------------------------------------------------------------
#include <DHT.h>
#include <Wire.h>

// ----------------------------------------------------------------------------
// Pines y constantes
// ----------------------------------------------------------------------------
#define PIN_SENSOR    2       // Pin de datos del sensor DHT22
#define PIN_LED       13      // LED indicador de estado
#define INTERVALO_MS  1000    // Intervalo de muestreo en milisegundos

// ----------------------------------------------------------------------------
// Variables globales
// ----------------------------------------------------------------------------
DHT dht(PIN_SENSOR, DHT22);
float temperatura   = 0.0;
float humedad       = 0.0;
unsigned long ultimaLectura = 0;
```

### 5.4 Documentación de funciones auxiliares

```cpp
/**
 * @brief  Lee temperatura y humedad del sensor DHT22.
 *
 * @param  temp   Referencia a variable float donde se guarda la temperatura (°C).
 * @param  hum    Referencia a variable float donde se guarda la humedad (%).
 * @return true   Si la lectura fue exitosa.
 * @return false  Si el sensor devolvió NaN.
 */
bool leerSensor(float& temp, float& hum) {
    temp = dht.readTemperature();
    hum  = dht.readHumidity();
    return !(isnan(temp) || isnan(hum));
}
```

### 5.5 `setup()` y `loop()`

```cpp
// ----------------------------------------------------------------------------
// Configuración inicial
// ----------------------------------------------------------------------------
void setup() {
    Serial.begin(9600);
    pinMode(PIN_LED, OUTPUT);
    dht.begin();
    Serial.println("Sistema iniciado.");
}

// ----------------------------------------------------------------------------
// Ciclo principal
// ----------------------------------------------------------------------------
void loop() {
    unsigned long ahora = millis();

    // Leer sensor cada INTERVALO_MS milisegundos
    if (ahora - ultimaLectura >= INTERVALO_MS) {
        ultimaLectura = ahora;

        if (leerSensor(temperatura, humedad)) {
            Serial.print("Temp: ");   Serial.print(temperatura); Serial.print(" °C | ");
            Serial.print("Hum: ");    Serial.print(humedad);     Serial.println(" %");
            digitalWrite(PIN_LED, HIGH);
        } else {
            Serial.println("[ERROR] Fallo en la lectura del sensor.");
            digitalWrite(PIN_LED, LOW);
        }
    }
}
```

---

## 6. JavaScript — Archivos `.js`

### 6.1 Estructura general

```
archivo.js
├── [1] Comentario de cabecera
├── [2] Imports / requires
├── [3] Constantes y configuración
├── [4] Definición de funciones (con JSDoc)
└── [5] Código de ejecución principal
```

### 6.2 Cabecera del archivo

```javascript
/**
 * @file    nombre_archivo.js
 * @description Descripción breve del propósito del módulo o script.
 *
 * @author  Henry Maldonado
 * @date    YYYY-MM-DD
 */
```

### 6.3 Imports y constantes

```javascript
// ----------------------------------------------------------------------------
// Imports
// ----------------------------------------------------------------------------
const fs   = require('fs');
const path = require('path');

// ----------------------------------------------------------------------------
// Constantes de configuración
// ----------------------------------------------------------------------------
const RUTA_DATOS  = path.join(__dirname, 'src', 'data', 'datos.json');
const RUTA_SALIDA = path.join(__dirname, 'results');
```

### 6.4 Documentación de funciones (JSDoc)

```javascript
/**
 * Descripción breve de la función.
 *
 * @param  {number} param1 - Descripción del primer parámetro.
 * @param  {string} param2 - Descripción del segundo parámetro.
 * @returns {Object} Descripción del objeto retornado.
 *
 * @throws {Error} Cuándo y por qué se lanza el error.
 *
 * @example
 * const resultado = nombreFuncion(42, "hola");
 */
function nombreFuncion(param1, param2) {
    // Implementación
    return {};
}
```

### 6.5 Bloque principal

```javascript
// ----------------------------------------------------------------------------
// Ejecución principal
// ----------------------------------------------------------------------------

(async function main() {

    // Carga de datos
    const datos = JSON.parse(fs.readFileSync(RUTA_DATOS, 'utf-8'));

    // Procesamiento
    const resultado = nombreFuncion(datos.valor, datos.nombre);

    // Guardar resultado
    fs.writeFileSync(
        path.join(RUTA_SALIDA, 'resultado.json'),
        JSON.stringify(resultado, null, 2),
        'utf-8'
    );

    console.log('Proceso finalizado.');
})();
```

---

## 7. Dart — Archivos `.dart`

### 7.1 Estructura general

```
archivo.dart
├── [1] Comentario de cabecera
├── [2] Imports
├── [3] Constantes y configuración
├── [4] Definición de clases y funciones (con doc-comments ///)
└── [5] Función main()
```

### 7.2 Cabecera del archivo

```dart
// =============================================================================
// nombre_archivo.dart
// =============================================================================
// Descripción: Qué hace este archivo o módulo.
// Autor      : Henry Maldonado
// Fecha      : YYYY-MM-DD
// =============================================================================
```

### 7.3 Imports

```dart
// ----------------------------------------------------------------------------
// Imports
// ----------------------------------------------------------------------------
import 'dart:io';
import 'dart:convert';
import 'package:path/path.dart' as path;
```

### 7.4 Documentación de funciones y clases (`///`)

```dart
/// Descripción breve de la clase.
///
/// Descripción extendida del comportamiento de la clase,
/// su propósito dentro del sistema y sus responsabilidades.
class NombreClase {

  /// Descripción breve del atributo.
  final String atributo;

  /// Constructor principal de [NombreClase].
  ///
  /// Parámetros:
  /// - [atributo]: Descripción del valor requerido.
  NombreClase({required this.atributo});

  /// Descripción breve del método.
  ///
  /// Parámetros:
  /// - [param1] (`int`): Descripción del primer parámetro.
  /// - [param2] (`String`): Descripción del segundo parámetro.
  ///
  /// Retorna:
  /// - `double`: Descripción del valor retornado.
  ///
  /// Lanza:
  /// - [ArgumentError]: Cuándo y por qué se lanza.
  double nombreMetodo(int param1, String param2) {
    // Implementación
    return 0.0;
  }
}
```

### 7.5 Función `main`

```dart
// ----------------------------------------------------------------------------
// Función principal
// ----------------------------------------------------------------------------

Future<void> main() async {

  // --- Configuración inicial ---
  final rutaDatos  = path.join('src', 'data', 'datos.json');
  final rutaSalida = path.join('results', 'resultado.json');

  // --- Carga de datos ---
  final archivo = File(rutaDatos);
  final contenido = await archivo.readAsString();
  final datos = jsonDecode(contenido) as Map<String, dynamic>;

  // --- Procesamiento ---
  final objeto = NombreClase(atributo: datos['nombre'] as String);
  final resultado = objeto.nombreMetodo(datos['valor'] as int, 'hola');

  // --- Guardar resultado ---
  await File(rutaSalida).writeAsString(
    jsonEncode({'resultado': resultado}),
  );

  print('Proceso finalizado. Resultado: $resultado');
}
```

---

## 8. Organización de resultados

Independientemente del lenguaje, todos los resultados se guardan en carpetas
estandarizadas usando la librería `funciones_template.py` (cuando el entorno
es Python) o creando manualmente las carpetas equivalentes.

| Tipo de archivo             | Carpeta destino          | Extensiones              |
|-----------------------------|--------------------------|--------------------------|
| Gráficas e imágenes         | `Resultados_imagenes/`   | `.png` `.jpg` `.svg`     |
| Informes y presentaciones   | `Resultados_informes/`   | `.pdf` `.pptx` `.docx`   |
| Documentos Markdown         | `Resultados_md/`         | `.md` `.txt`             |

### Regla de nombrado de archivos de resultados

```
{descriptor}_{version_o_fecha}.extension

Ejemplos:
  distribucion_precio_v1.png
  reporte_final_2026-05-12.pdf
  notas_experimento_01.md
```

### Guardar resultados en Python

```python
import funciones_template as ft

# Imagen generada con matplotlib
fig.savefig("mi_grafica.png", dpi=150, bbox_inches="tight")
ft.guardar_imagen("mi_grafica.png")

# Informe PDF
ft.guardar_informe("reporte.pdf")

# Documento Markdown
ft.guardar_md("notas.md")
```

### Guardar resultados en Jupyter Notebook

```python
# Siempre guardar ANTES de plt.show()
fig.savefig("nombre_descriptivo.png", dpi=150, bbox_inches="tight")
ft.guardar_imagen("nombre_descriptivo.png")
plt.show()
```

---

## 9. Informes finales — flujo Markdown → LaTeX → PDF

La idea es escribir el informe una sola vez en Markdown (rápido, sin
preocuparse por formato) y luego convertirlo automáticamente al formato
LaTeX UCUENCA para entregarlo como PDF. El programa `md_a_latex.py`
hace esa conversión.

### 9.1 Crear el proyecto base

```bash
# Crea la carpeta con el Template UCUENCA ya dentro
python crear_proyecto.py practica1_control --tipo proyecto_latex
cd practica1_control
```

### 9.2 Estructura del informe en Markdown

Crear el archivo `informe.md` en la raíz del proyecto con la siguiente
estructura. El bloque `---` al inicio es el **frontmatter YAML** y define
los metadatos de la portada.

```markdown
---
titulo: "Control PID de un Motor DC"
subtitulo: "Práctica 1 — Control Digital"
autor: "Ing. Henry Maldonado"
periodo: "2026-1 · Mar 2026 – Ago 2026"
carrera: "Ingeniería en Telecomunicaciones"
anio: "2026"
---

# Introducción

Texto introductorio del informe...

## Objetivos

> [!OBJECTIVE]
> Al finalizar esta práctica el estudiante será capaz de...
> - Diseñar un controlador PID.
> - Validar el diseño mediante simulación.

## Marco teórico

Texto con ecuaciones inline $G(s) = \frac{K}{Ts+1}$ o en bloque:

$$
G(s) = \frac{K_p \cdot (T_i s + 1)}{T_i s}
$$

## Materiales y equipos

> [!WARNING]
> Verificar que el equipo esté apagado antes de realizar conexiones.

| Elemento       | Cantidad | Descripción                  |
|----------------|:--------:|------------------------------|
| QUBE-Servo 3   | 1        | Planta de control            |
| Cable USB      | 1        | Conexión PC–planta            |
| MATLAB/Simulink| —        | Software de control          |

## Procedimiento

### Paso 1 — Configuración del modelo

Texto descriptivo del paso...

![Diagrama del modelo](images/diagrama_modelo.png)

### Paso 2 — Código de adquisición

```python
import quanser_sdk as qs
board = qs.HIL("qube_servo3_usb", "0")
```

## Resultados

Guardar todas las gráficas en `images/` antes de referenciarlas.

![Respuesta al escalón con Kp=1](images/respuesta_escalon.png)

![Respuesta con controlador PID sintonizado](images/respuesta_pid.png){0.7\linewidth}

## Análisis y discusión

Texto del análisis...

> [!NOTE]
> Un sobreimpulso mayor al 20% indica que la ganancia derivativa es insuficiente.

## Entregables

> [!DELIVERABLE]
> - Informe en PDF generado desde este Markdown.
> - Archivo `.m` o `.py` con el código de simulación.
> - Capturas de las respuestas obtenidas en `images/`.

## Conclusiones

- **Conclusión 1:** ...
- **Conclusión 2:** ...

## Referencias

Se usan citaciones BibTeX en el texto: según \cite{katsuhiko2003teoria}, el
método de Ziegler-Nichols permite una sintonización inicial rápida.
```

### 9.3 Cajas especiales disponibles

Usar dentro de blockquotes (`>`). El conversor las mapea al estilo UCUENCA:

| Marcador Markdown    | Caja LaTeX generada       | Color / Ícono               |
|----------------------|---------------------------|-----------------------------|
| `> [!OBJECTIVE]`     | `objetivebox`             | Azul — Objetivos            |
| `> [!NOTE]`          | `infobox`                 | Azul claro — Nota           |
| `> [!WARNING]`       | `warningbox`              | Amarillo — Advertencia      |
| `> [!DELIVERABLE]`   | `entregabox`              | Verde — Entregables         |
| `> [!EXERCISE]`      | `exercisebox`             | Azul oscuro — Ejercicio     |
| `> texto libre`      | `quote`                   | Cursiva                     |

### 9.4 Imágenes — reglas de uso

Todas las imágenes deben estar en la carpeta `images/` del proyecto antes
de referenciarlas. El ancho por defecto es `0.85\linewidth`. Para cambiar
el ancho, agregarlo entre llaves después del paréntesis:

```markdown
![Descripción](images/figura.png)               <- ancho por defecto (85%)
![Descripción](images/figura.png){0.5\linewidth} <- ancho personalizado (50%)
```

Al generar resultados desde Python, usar `funciones_template` y luego copiar
a `images/` o guardar directamente ahí:

```python
fig.savefig("images/respuesta_pid.png", dpi=150, bbox_inches="tight")
```

### 9.5 Tablas

Las tablas en Markdown se convierten a `tabularx` con `booktabs`. La
alineación se controla con los dos puntos en la fila separadora:

```markdown
| Columna izq | Centro | Derecha |
|-------------|:------:|--------:|
| dato a      |   42   |   3.14  |
| dato b      |   17   |   2.71  |
```

### 9.6 Código — lenguajes soportados

El bloque de código se convierte a `lstlisting` con el lenguaje correspondiente:

````markdown
```python
# código Python
```

```matlab
% código MATLAB
```

```arduino
// código Arduino
```
````

Lenguajes soportados: `python`, `julia`, `cpp`/`c++`, `c`, `javascript`/`js`,
`dart`, `matlab`, `bash`/`sh`, `latex`/`tex`, `arduino`.

### 9.7 Bibliografía

Las referencias se definen en `references.bib` (formato BibTeX/IEEE).
En el texto Markdown se pueden insertar comandos LaTeX directamente:

```markdown
Como se muestra en \cite{katsuhiko2003teoria}, el método PID...
```

El conversor no toca el interior de los bloques LaTeX literales.

### 9.8 Convertir a LaTeX y a PDF

```bash
# Desde la raíz del proyecto (donde está Template/)
python md_a_latex.py informe.md

# Especificar nombre de salida
python md_a_latex.py informe.md --salida practica1_control.tex

# Convertir Y compilar a PDF directamente
python md_a_latex.py informe.md --compilar

# Si el Template está en otra ruta
python md_a_latex.py informe.md --template-dir ../Formatos_repos/templates/latex/Template
```

### 9.9 Flujo completo de trabajo

```
1. python crear_proyecto.py practica1 --tipo proyecto_latex
2. cd practica1
3. Escribir informe.md  (texto + imágenes en images/)
4. python ../md_a_latex.py informe.md
5. Abrir practica1/informe.tex en VS Code → compilar con LaTeX Workshop
   — o bien —
   python ../md_a_latex.py informe.md --compilar
6. Guardar PDF final:
   python ../funciones_template.py  (o ft.guardar_informe("informe.pdf"))
```

---

*Guía mantenida en `C:\GitHub\Formatos_repos\guia_estilos_codigo.md`*
