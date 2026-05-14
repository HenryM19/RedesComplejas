# Template Slides HTML

Template de diapositivas HTML reutilizable, pensado para presentar teoría, resultados, embeds interactivos y simulaciones sin depender de frameworks externos. El deck está contenido en un solo archivo principal y usa `embeds/` para insertar visualizaciones o bloques autónomos con su propio `HTML`, `CSS` y `JavaScript`.

## Estructura del template

- `index.html`: deck principal de slides.
- `embeds/demo-a.html`: ejemplo de embed simple.
- `embeds/demo-b.html`: segundo ejemplo de embed para tabs.
- `embeds/simulation.html`: ejemplo de bloque autónomo para simulaciones interactivas.

## Qué hace este template

- navegación por slides con botones inferiores;
- soporte de teclado con flechas y barra espaciadora;
- soporte táctil con swipe horizontal;
- diseño responsive para escritorio y celular;
- renderizado de ecuaciones LaTeX con `MathJax`;
- bloques reutilizables para teoría, resultados, KPIs, tablas, código, tabs y simulaciones;
- embeds independientes para contenido interactivo o visualizaciones complejas.

## Cómo editarlo

1. Abre `index.html`.
2. Duplica cualquier bloque `<div class="slide"> ... </div>` para crear una nueva diapositiva.
3. Sustituye títulos, textos, tablas, tarjetas o iframes por tu contenido.
4. Si necesitas un bloque interactivo complejo, crea un archivo dentro de `embeds/` y cárgalo con un `iframe`.
5. Mantén las clases existentes siempre que quieras conservar el mismo estilo visual y el mismo comportamiento responsive.

## Cómo funciona cada slide

Cada slide usa la clase base `slide`.

Ejemplo mínimo:

```html
<div class="slide">
	<h2>Título del slide</h2>
	<div class="card">
		<p>Contenido.</p>
	</div>
</div>
```

El script del template muestra solo una slide a la vez usando la clase `active`.

## Tipos de slide incluidos

### 1. Portada

Usa la clase `slide cover`.

```html
<div class="slide cover active">
	<h1>Título de la Presentación<br>Subtítulo o Proyecto</h1>
	<div class="sub">Plantilla base de diapositivas HTML</div>
	<div class="meta">Autor o curso · Fecha · Institución</div>
</div>
```

### 2. Separador de sección

Usa la clase `slide sdiv`.

```html
<div class="slide sdiv" style="background:linear-gradient(135deg,#1e3a5f,#2563eb)">
	<div class="snum">01</div>
	<div class="stitle">Sección Principal</div>
	<div class="ssub">Tema · contexto · ideas clave</div>
</div>
```

### 3. Slide conceptual

Usa `slide concept-slide` para aprovechar mejor el alto disponible sin generar scroll innecesario.

### 4. Slide de resultados

Usa `slide spread` para repartir contenido superior e inferior de forma más equilibrada.

### 5. Slide de simulación

Usa `slide simulation-slide` para que un bloque embebido ocupe la altura útil del slide.

## Clases principales del layout

### Layout general

- `slide`: slide base.
- `slide fill`: centra verticalmente el contenido.
- `slide end`: empuja el contenido hacia la parte inferior.
- `slide spread`: distribuye el contenido entre arriba y abajo.
- `concept-slide`: optimiza slides conceptuales para que no dejen huecos ni scroll sobrante.
- `simulation-slide`: optimiza slides con simulaciones o embeds altos.

### Contenedores reutilizables

- `card`: tarjeta visual base.
- `fill-card`: hace que una tarjeta ocupe la altura disponible.
- `grow`: hace que un contenedor crezca dentro del slide.
- `fill-main`: marca el área principal que debe estirarse dentro de un bloque.
- `stack`: apila bloques verticalmente con separación consistente.
- `flow`: flujo vertical simple de elementos.

### Grids

- `g2`: grid de 2 columnas.
- `g3`: grid de 3 columnas.
- `slide-layout`: grid de 12 columnas para layouts más libres.
- `span-4`, `span-5`, `span-6`, `span-7`, `span-8`, `span-12`: ancho de columna en desktop.
- `self-start`, `self-center`, `self-end`: alineación vertical dentro del grid.

En móvil, los grids se apilan automáticamente a una sola columna.

## Bloques visuales disponibles

### Texto y teoría

- `card`: texto general.
- `note`: notas, advertencias o comentarios rápidos.
- `ans`: bloque de respuesta o conclusión destacada.

### Ecuaciones

- `eq`: bloque para ecuaciones LaTeX.

Ejemplo:

```html
<div class="eq">\[E = mc^2\]</div>
```

También puedes escribir solo el contenido de la fórmula y el script lo envuelve automáticamente como ecuación en bloque.

### Tablas y variables

- `vars`: tabla compacta de variables.
- `rt`: tabla de resultados.

### KPIs o métricas

- `stat`: tarjeta pequeña para métricas, porcentajes, estados o contadores.

### Código

- `code`: bloque visual para fragmentos de código.

### Badges

- `badge`: etiqueta visual base.
- `b-blue`, `b-green`, `b-red`, `b-orange`, `b-purple`, `b-yellow`: variantes de color.

## Navegación del deck

La navegación está integrada en la barra inferior.

Incluye:

- botón `Anterior`;
- botón `Siguiente`;
- contador de slide actual;
- barra de progreso.

También puedes navegar con:

- `ArrowRight`, `ArrowDown` o espacio para avanzar;
- `ArrowLeft` o `ArrowUp` para retroceder;
- swipe horizontal en pantallas táctiles.

## Responsive

El template ya está preparado para escritorio y móvil.

Comportamientos importantes:

- los grids pasan a una sola columna en pantallas pequeñas;
- los botones inferiores aumentan su área táctil;
- la navegación soporta taps y swipe;
- los bloques de simulación o embeds ajustan su altura en móvil;
- el contenido intenta ocupar el alto disponible antes de introducir scroll.

## Tipografía

La tipografía actual busca un estilo más moderno y menos formal:

- cuerpo: `Aptos`, `Segoe UI Variable Text`, `Segoe UI`, `sans-serif`;
- títulos: `Aptos Display`, `Segoe UI Variable Display`, `Aptos`, `Segoe UI`, `sans-serif`.

## Ecuaciones en LaTeX

Las ecuaciones se renderizan con `MathJax`.

Soporta:

- inline math con `$...$` o `\(...\)`;
- block math con `$$...$$` o `\[...\]`.

Ejemplo:

```html
<div class="eq">\[\text{Métrica} = \frac{\text{valor}}{\text{referencia}}\]</div>
```

## Embeds interactivos

Si quieres insertar una visualización o miniaplicación, crea un archivo HTML en `embeds/`.

Ese archivo puede tener:

- `HTML` completo;
- `CSS` propio;
- `JavaScript` propio;
- `canvas`;
- animaciones;
- sliders;
- botones;
- cálculos;
- dashboards o simulaciones.

Ejemplo simple:

```html
<div class="simulation span-8 fill-card">
	<div class="sim-head">
		<div>
			<div class="sim-title">Simulation</div>
			<p class="sim-copy">Descripción corta del bloque.</p>
		</div>
		<span class="badge b-blue">Embed autónomo</span>
	</div>
	<iframe src="embeds/simulation.html" loading="lazy" title="Simulation demo"></iframe>
</div>
```

## Tabs con iframes

El template incluye un ejemplo de tabs que alternan distintos iframes sin salir del slide.

Úsalo cuando quieras mostrar varias vistas de un mismo tema.

Ejemplo:

```html
<div class="ifw fill-card grow">
	<div class="tabs">
		<button type="button" class="tbn on" onclick="ct('demo-a',this,'demo-frame')">Vista A</button>
		<button type="button" class="tbn" onclick="ct('demo-b',this,'demo-frame')">Vista B</button>
	</div>
	<iframe id="demo-a" class="demo-frame fill-main" src="embeds/demo-a.html" style="display:block"></iframe>
	<iframe id="demo-b" class="demo-frame fill-main" src="embeds/demo-b.html" style="display:none"></iframe>
</div>
```

## Cómo aprovechar mejor el espacio

El template está ajustado para reducir espacios vacíos innecesarios.

Reglas prácticas:

1. Usa `fill-card` cuando un bloque deba ocupar la altura disponible.
2. Usa `grow` en contenedores que deban expandirse dentro del slide.
3. Usa `fill-main` en el contenido principal de la tarjeta, por ejemplo un grid, un bloque de código o un `iframe`.
4. Usa `concept-slide` o `simulation-slide` cuando el slide necesite un comportamiento de altura más controlado.
5. Si un slide tiene poco contenido, evita apilar demasiados bloques pequeños: combina elementos o usa un layout más compacto.

## Flujo recomendado para crear una nueva slide

1. Duplica una slide existente parecida a lo que quieres.
2. Cambia solo el contenido, no la estructura base.
3. Si necesitas más altura útil, añade `grow`, `fill-card` o `fill-main`.
4. Si necesitas interacción compleja, mueve esa lógica a un archivo en `embeds/`.
5. Verifica en desktop y móvil.

## Resumen rápido

- `index.html` controla el deck.
- `embeds/` contiene bloques externos reutilizables.
- `MathJax` renderiza las ecuaciones.
- los slides son responsive;
- la navegación funciona con botones, teclado y swipe;
- los bloques están preparados para aprovechar la altura disponible.