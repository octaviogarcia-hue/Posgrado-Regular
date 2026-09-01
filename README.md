# Campaña Phygital — Beca Fulbright-García Robles · Posgrado Regular

Del volante impreso al pre-registro digital. Un código QR en papel lleva a una landing page
orientada a conversión.

El 99 % del tráfico llega por teléfono, así que la página es **mobile-first en retrato**:
proporciones verticales, tipografía dimensionada para la mano, y gestos táctiles en lugar de
eventos de ratón.

---

## Contenido

```
modelo-1-scrollytelling.html         Relato guiado por scroll con mapa SVG animado
docs/
  01-copy.md                         Hook del volante y microcopy de la landing
  02-zapier.md                       Pre-registro y recordatorios automáticos
  preregistro.schema.json            Esquema del payload de pre-registro
tools/
  build_artifacts.py                 Genera fragmentos publicables desde el HTML
archivo/                             Versiones anteriores del encargo (v1: icosaedro;
                                     v2: globo y mapa 3D en WebGL), como referencia
```

El HTML es **autónomo**: CSS y JavaScript embebidos, sin build, sin dependencias
obligatorias más allá de las fuentes de Google. Se abre con doble clic.

---

## El modelo — Del Ángel a la Antorcha

Un relato guiado por el scroll. El escenario queda fijo bajo el encabezado mientras las
tarjetas de contenido pasan por debajo, y el desplazamiento mueve una **cámara sobre un mapa
SVG** de México y Estados Unidos: arranca cerrada sobre el origen, se abre a las tres
ciudades emisoras, cruza la frontera y termina en el noreste. Seis **trayectorias que se
trazan solas** unen las ciudades de salida con las de destino. El **Ángel de la
Independencia** cede el sitio a la **Estatua de la Libertad** a mitad del trayecto, en
SVG 2D.

- **Un solo cálculo gobierna todo.** El avance del scroll dentro del relato produce un valor
  entre 0 y 1, y de ahí salen el encuadre de la cámara, el trazado de cada arco, la
  transición entre monumentos y la barra de progreso. No hay animaciones sueltas que se
  desincronicen.
- **Diseño geográfico minimalista, sin rótulos.** Las ciudades son solo marcadores —punto y
  halo en azules institucionales— unidos por sus rutas; no llevan nombre en el mapa. Cada
  grupo de ciudad compensa la escala de la cámara y los trazos usan
  `vector-effect: non-scaling-stroke`, así que ni los marcadores ni las fronteras se
  deforman a 2.7 aumentos.
- **`prefers-reduced-motion`** entrega el mapa completo, los seis arcos trazados y los dos
  monumentos a la vez, sin movimiento.
- **Formulario de pre-registro de un paso, tres campos** — máxima tasa de conversión.

---

## Identidad oficial

Aplicada según la Fulbright Brand Guide:

| | |
|---|---|
| Titulares, cifras, interfaz | **Montserrat** (Google Fonts, pesos 400–800) |
| Citas y acentos formales | **Source Serif 4** en cursiva |
| Legacy Blue `#003DA5` | Corporativo primario |
| Azure Blue `#0077C8` | Secundario y transiciones |
| Sky Blue `#00A9E0` | Acentos y resaltados |
| Blanco, `#C7C9C7`, `#707372` | Fondos y textos de soporte |

**Una advertencia de contraste que conviene conocer.** Sky Blue es un color de acento: sobre
blanco da 2.5:1, por debajo del mínimo de la WCAG. En la página pinta **solo gráficos**
—arcos, halos, bordes, la antorcha, las reglas, la barra de progreso—; el texto usa Legacy
Blue, Azure Blue o blanco según el fondo. Se ve igual de vivo y se lee.

La página abre con un **sticky header** con un `<img class="logo-oficial">` listo para
recibir el logotipo oficial:

```html
<img class="logo-oficial" src="logo-fulbright-comexus.png"
     alt="Fulbright COMEXUS — Becas Fulbright-García Robles"
     onerror="...">
```

Para activarlo, **coloca el PNG que entregue COMEXUS junto al HTML** con el nombre
`logo-fulbright-comexus.png` —o cambia el `src` por su URL, si se va a alojar aparte—. No hay
que tocar nada más del encabezado. Mientras el archivo no exista, el `onerror` del propio
`<img>` lo oculta y muestra en su lugar un lockup de texto (`Fulbright COMEXUS · Becas
Fulbright-García Robles`) para que el encabezado nunca se vea roto.

### Contacto: formulario nativo, no `mailto:`

Los enlaces `mailto:` quedaban bloqueados en varios clientes, así que el contacto es una
**sección propia al final del relato** con el formulario maquetado a mano en HTML y CSS:
glassmorphism sobre una banda con el degradado corporativo, campos con línea inferior y
botón a todo el ancho en Legacy Blue.

El envío es un **POST nativo del propio `<form>`** a Jotform —sin iframe, sin SDK, sin
JavaScript de por medio—. Al enviar, el navegador sale a la pantalla de agradecimiento de
Jotform:

```html
<form action="https://submit.jotform.com/submit/262434743012045" method="POST">
  <input type="hidden" name="formID"     value="262434743012045">
  <input type="hidden" name="simple_spc" value="262434743012045-262434743012045">
  <input name="q3_name[first]" ...>   <!-- Nombre completo -->
  <input name="q4_email"       ...>   <!-- Correo          -->
  <input name="q6_typeA"       ...>   <!-- Asunto          -->
  <textarea name="q7_typeA7"   ...>   <!-- Mensaje         -->
```

`formID` y `simple_spc` son obligatorios para que Jotform acepte un envío directo. El campo
de nombre es de tipo *Full Name* en Jotform, así que el nombre completo llega en la columna
«First Name»; para separarlo hay que cambiar ese campo a *Short Text* en el editor. Los
`utm_*` viajan como campos ocultos pero **Jotform los descarta** mientras no existan campos
equivalentes en el formulario.

---

## Configuración por ciclo

La landing tiene un único bloque de configuración al inicio de su `<script>`:

```js
const CONFIG = {
  CIERRE: new Date('2027-01-15T23:59:59-06:00'),
  APERTURA_SIGUIENTE: '1 de septiembre',
  ENDPOINT: '',            // URL del Catch Hook de Zapier. Vacío = modo demo.
  VARIANTE: 'modelo-1-scrollytelling'
};
```

Cambiar `CIERRE` recalcula el contador, la píldora de estado, la etiqueta del CTA, el texto
del dock y el mensaje de confirmación. Las fechas escritas a mano —los tres hitos del
calendario y la `<meta description>`— sí hay que tocarlas aparte.

### Estado «convocatoria cerrada»

Cuando la fecha de cierre ya pasó, la página cambia sola de discurso: deja de prometer una
postulación imposible y ofrece aviso para la siguiente apertura. No hay que despublicar nada
ni editar textos con prisa.

`ENDPOINT` gobierna solo el **pre-registro**, no el formulario de contacto. Con `ENDPOINT`
vacío el pre-registro funciona en **modo demo**: valida, muestra la confirmación y escribe en
la consola el payload exacto que recibiría Zapier.

---

## Verificación

Probado en Chromium (Playwright) a 360, 390, 768 y 1280 px.

| Comprobación | Resultado |
|---|---|
| Errores de consola y de JavaScript | Ninguno |
| Desbordamiento horizontal (360, 390, 768, 1280 px) | Ninguno |
| Contacto: `action`, `method` y los cuatro campos de Jotform | Correctos y en orden |
| Contador con convocatoria abierta | Píldora en «Abierta», 136 días al 1 de septiembre de 2026 |
| Montos sin JavaScript | Se leen correctos: la cifra real vive en el HTML |
| Zonas táctiles por debajo de 44 px | Ninguna |

Un **envío de prueba real a Jotform está pendiente**: no se hizo para no dejar un registro
falso en el formulario de producción.

---

## Pendiente antes de publicar

- [ ] Hacer un envío de prueba del formulario de contacto y confirmar que llegan los cuatro
      campos.
- [ ] Renombrar en el editor de Jotform las etiquetas de los campos 6 y 7, que siguen como
      «Type a question» y así aparecen en los correos de aviso.
- [ ] Pegar la URL del Catch Hook de Zapier en `CONFIG.ENDPOINT` para el pre-registro.
- [ ] Enlazar el aviso de privacidad real de COMEXUS (hoy es un ancla interna).
- [ ] Confirmar cifras, fechas y criterios de elegibilidad contra la convocatoria oficial
      vigente.

---

## Dos notas

**Sobre el calendario.** El material usa el ciclo vigente: convocatoria del 1 de septiembre
de 2026 al 15 de enero de 2027, con inicio de estudios en otoño de 2028. Los montos se
enuncian siempre con «hasta», porque la cantidad varía según el programa.

**Sobre `user-scalable=no`.** El brief pide esa etiqueta de viewport y está puesta tal cual.
Conviene saber que bloquea el zoom del navegador, lo que incumple el criterio WCAG 1.4.4 y
afecta a quien necesita ampliar el texto. La página está construida para no necesitarlo
—cuerpo de 16 px mínimo, controles de 52–56 px—, así que quitar `maximum-scale=1.0,
user-scalable=no` no cambia nada del diseño y devuelve el zoom. Es una decisión de una línea.
