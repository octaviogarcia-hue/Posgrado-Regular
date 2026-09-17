# Handoff — Campaña Phygital

> **Qué es este documento.** Registro de cierre de una campaña phygital (volante impreso con
> QR → landing de conversión). Tiene dos lectores distintos: quien retoma *esta* campaña
> (Fulbright-García Robles) necesita el estado y los pendientes; quien arranca la *siguiente*
> campaña con esta misma plantilla necesita las lecciones aprendidas y el flujo de trabajo,
> sin repetir los mismos errores.
>
> **Cómo reutilizarlo.** La estructura de este archivo está pensada para copiarse en el
> repositorio de la próxima campaña y llenarse con sus propios datos. Las secciones 1 a 4
> son la ficha específica de *esta* campaña — se reemplazan por completo. Las secciones 5 a 7
> (errores, lecciones y flujo de trabajo) son la parte que vale la pena conservar casi igual:
> son los tropiezos que le van a pasar a cualquier campaña con esta misma arquitectura
> (HTML autónomo + Git + PR + formulario externo), no solo a esta.

---

## 1 · Ficha de la campaña

| Campo | Valor |
|---|---|
| Institución | COMEXUS (Comisión México-Estados Unidos para el Intercambio Educativo y Cultural) |
| Programa | Beca Fulbright-García Robles — Posgrado Regular |
| Repositorio | `octaviogarcia-hue/Posgrado-Regular` |
| Rama de trabajo por defecto | `claude/fulbright-phygital-campaign-6dllr9` (histórica; los cambios recientes se hicieron en ramas nuevas por tema — ver §7) |
| Página publicada | `index.html` (raíz del repo, listo para cualquier hosting estático) |
| Autoría (crédito en el pie) | Etienne GC · O.E.G.C |
| Convocatoria vigente al cierre de este handoff | Abre 1 sep 2026 · Cierra 15 ene 2027 · Inicio de estudios otoño 2028 |
| Montos | Maestría: hasta $37,000 USD/año · Doctorado: hasta $25,000 USD/año |
| Formulario de contacto | Nativo HTML/CSS (glassmorphism), `POST` directo a Jotform, sin iframe ni SDK |
| Endpoint de contacto | `https://submit.jotform.com/submit/262434743012045` |
| Automatización de pre-registro | **Descartada.** Existió un formulario de pre-registro con destino a un *Catch Hook* de Zapier; se retiró por completo (ver §5.4) porque Zapier quedó fuera del proyecto |
| Hosting de producción | **Sin definir al cierre de este handoff.** El dueño del repo no usa su propio Hostinger porque la institución no cubre ese costo; queda pendiente que COMEXUS aloje el sitio con su propio hosting o dominio |

---

## 2 · Qué se entregó

- Una landing de una sola página (`index.html`), autónoma: CSS y JavaScript embebidos, sin
  build, sin dependencias más allá de Google Fonts. Se abre con doble clic o se sube tal cual
  a cualquier hosting estático.
- Relato guiado por scroll con un mapa SVG animado (cámara que recorre México–Estados Unidos)
  como pieza central del storytelling de marca.
- Un único formulario en toda la página — el de contacto — después de retirar el de
  pre-registro. Todos los llamados a la acción de la página apuntan a él.
- Identidad de marca aplicada desde la guía oficial (colores, tipografía, reglas de
  contraste) documentada dentro del propio HTML como comentarios.
- Deck de copy (`docs/01-copy.md`) que documenta cada texto de la página como fuente de
  verdad editorial, sincronizado a mano cada vez que el copy cambia.
- Herramienta de build (`tools/build_artifacts.py`) que convierte la landing en un fragmento
  publicable como Artifact de Claude, para compartir previews sin depender de hosting.

## 3 · Qué se descartó y por qué

| Elemento retirado | Razón |
|---|---|
| Segundo modelo de landing (`modelo-2-bento-vertical.html`) | Decisión explícita del cliente de quedarse solo con el modelo de scrollytelling |
| Formulario de pre-registro (nombre, correo, nivel, elegibilidad) | Enviaba a un *Catch Hook* de Zapier que el cliente decidió no pagar/mantener; un formulario sin destino real habría prometido un envío que nunca iba a llegar |
| Widget embebido de Jotform (iframe/SDK) | No coincidía con la estética de la página; se sustituyó por un formulario nativo en HTML/CSS que solo reutiliza el `action` de Jotform |
| `mailto:` en el pie de página | Quedaba bloqueado en varios clientes de correo |

## 4 · Estado al cierre de este handoff

- **Todo el código está fusionado en `main`** a través de los PR #1 al #6 (ver §7 para la
  lista completa con enlaces).
- **Pendiente de la institución**, no del código:
  1. Envío de prueba real al formulario de contacto (no se hizo antes para no dejar un
     registro falso en el Jotform de producción).
  2. Enlazar el aviso de privacidad real de COMEXUS (hoy es un ancla interna).
  3. Confirmar cifras, fechas y criterios de elegibilidad contra la convocatoria oficial
     vigente al momento de publicar.
  4. Decidir y configurar el hosting de producción (GitHub Pages, Netlify, Cloudflare Pages
     o el hosting propio de COMEXUS) — el archivo ya está listo para cualquiera de ellos.

---

## 5 · Errores y lecciones aprendidas

*Cada entrada: qué pasó → por qué → cómo se resolvió → qué hacer distinto la próxima vez.
Esta sección es la que más vale la pena copiar completa a la siguiente campaña.*

### 5.1 — El repositorio remoto tenía una historia de Git no relacionada
**Qué pasó:** al abrir el primer PR, GitHub rechazó la fusión con *"the branch has no
history in common with main"*. La rama `main` tenía únicamente un `index.html` y un logo
subidos manualmente desde la web de GitHub, sin relación con la rama de trabajo.
**Por qué:** alguien había subido archivos sueltos a `main` con la interfaz web de GitHub, en
paralelo al desarrollo por rama.
**Cómo se resolvió:** `git merge origin/main --allow-unrelated-histories`, sin conflictos, y
se retiró el `index.html` viejo (contenido desactualizado) conservando el logo (útil, pasó a
ser el logo oficial del encabezado).
**Para la próxima campaña:** antes de abrir el primer PR, verificar con
`git merge-base <rama> origin/main` que existe historia común. Si el repositorio se creó
subiendo archivos por la web en vez de por git, resolverlo temprano, no al momento de abrir
el PR.

### 5.2 — Un PR se fusionó antes de que llegara el último commit
**Qué pasó:** el cliente fusionó el PR #5 justo después de que se abrió con los primeros
cambios de copy, pero un commit adicional (unificar el texto de varios botones) se subió a
la misma rama *después* de esa fusión y se quedó fuera de `main` sin que nadie lo notara de
inmediato.
**Por qué:** un Pull Request se fusiona en el estado de la rama en el momento del merge, no
en su estado final; seguir empujando commits a una rama con un PR abierto no garantiza que
lleguen a tiempo si el cliente aprueba antes de avisar que hay más cambios en camino.
**Cómo se resolvió:** se identificó el commit faltante con
`git merge-base --is-ancestor <commit> origin/main`, se hizo `cherry-pick` de ese commit
sobre una rama nueva partiendo de `main` actualizado, y se abrió un PR nuevo y limpio solo
con ese cambio.
**Para la próxima campaña:** avisar explícitamente "todavía viene un commit más, no fusiones
todavía" cuando se sepa que hay cambios en curso sobre una rama con PR abierto. Si de todos
modos se fusiona antes de tiempo, no hay que revertir nada: aislar el commit faltante con
`cherry-pick` sobre la rama base actualizada es más limpio que reabrir la rama vieja.

### 5.3 — Desbordamiento horizontal al anteponer texto a una cifra
**Qué pasó:** una regla de copy pedía anteponer la palabra "hasta" a cada monto en dólares.
Escribirla como texto en línea justo antes de la cifra (`<small>hasta</small>$37,000`) generó
desbordamiento horizontal a 390px de ancho, porque el conjunto ya no cabía en una sola línea
y el contenedor no estaba pensado para que esa etiqueta creciera.
**Por qué:** un `<small>` en línea antes de un número grande no tiene su propio espacio
reservado; a texturas de columna angosta empuja el ancho total del bloque.
**Cómo se resolvió:** se convirtió esa etiqueta en un elemento de bloque (`display:block`)
por encima del número, no en línea antes de él.
**Para la próxima campaña:** cualquier prefijo o sufijo de texto que se agregue a una cifra
grande debe probarse de inmediato en el ancho más angosto soportado (aquí, 360–390px) antes
de darlo por bueno; un cambio de copy que parece trivial puede romper el layout.

### 5.4 — Retirar una función a medias deja código muerto
**Qué pasó:** al principio se pidió solo "quita el botón de pre-registro"; en una iteración
posterior se pidió formalmente retirar todo el formulario. Si se hubiera hecho solo lo
primero, habrían quedado huérfanos: ~40 líneas de CSS exclusivas del formulario, 87 líneas de
JavaScript de validación, dos claves de configuración (`ENDPOINT`, `VARIANTE`) sin uso, y dos
documentos (`02-zapier.md`, `preregistro.schema.json`) describiendo algo que ya no existía.
**Por qué:** un formulario no es solo su `<form>` visible: tiene CSS propio, JS propio,
configuración propia y documentación propia. Borrar solo el HTML visible dejaría el resto
como deuda técnica invisible.
**Cómo se resolvió:** al recibir la instrucción de retirar la función completa, se buscó
sistemáticamente cada rastro (`grep` de ids, clases y nombres de configuración referenciados
desde JS) antes de dar el cambio por terminado.
**Para la próxima campaña:** al retirar cualquier función, hacer una pasada de búsqueda de
sus identificadores (`id`, clases CSS, claves de `CONFIG`, archivos de `docs/`) antes de
cerrar el cambio, no asumir que borrar el bloque visible es suficiente.

### 5.5 — Verificar más allá de "no truena": comprobar cada afirmación
**Qué pasó:** en más de una ocasión se pidió confirmar que "todo funciona". La respuesta
correcta no fue una revisión de memoria del código escrito, sino correr la página real en un
navegador headless (Chromium vía Playwright) y comprobar, con datos concretos: ausencia de
errores de consola, ausencia de desbordamiento horizontal en 4 anchos de pantalla, que cada
`id` referenciado desde JavaScript existe en el HTML, y que el `action`/`method`/campos del
formulario son exactamente los que se pactaron.
**Para la próxima campaña:** cuando se pregunte "¿funciona?", verificar con la herramienta
adecuada (navegador headless para el frontend, linter/validador para JSON, etc.) en vez de
responder solo con una relectura del código. Guardar un script de verificación reutilizable
en el scratchpad de la sesión ahorra tiempo en cada ronda de cambios.

### 5.6 — Entorno efímero: las herramientas de verificación no persisten
**Qué pasó:** entre una sesión y otra, `node_modules` (con Playwright) dejó de existir porque
el contenedor de ejecución se reinicia entre sesiones.
**Cómo se resolvió:** Playwright también está instalado de forma global en
`/opt/node22/lib/node_modules`; apuntar `NODE_PATH` ahí evita depender de una instalación
local que no sobrevive entre sesiones.
**Para la próxima campaña:** no asumir que un entorno de verificación configurado en una
sesión sigue disponible en la siguiente; comprobar primero (`ls node_modules` o equivalente)
y tener un plan B (instalación global) listo.

---

## 6 · Decisiones de producto que conviene recordar

- **Un solo llamado a la acción por página**, no dos formularios compitiendo. Cuando la
  automatización de un formulario se cae (aquí, Zapier), es mejor retirarlo por completo que
  dejarlo mudo: un botón que no lleva a ningún lado es peor que no tener el botón.
- **El contador de cierre no promete nada** y por eso se conservó incluso al retirar el
  formulario que lo acompañaba: transmite urgencia sin depender de una integración externa.
- **Todas las cifras de dinero llevan "hasta" como prefijo**, porque el monto real varía según
  el programa — evita que alguien lea la cifra máxima como una cifra garantizada.
- **El pie de página es el lugar correcto para el crédito de autoría**: discreto, separado por
  una regla fina, sin competir con la información oficial de la institución.
- **El `<title>` de la pestaña debe identificar la institución/programa**, no repetir el lema
  creativo de la campaña (aquí, "Del Ángel a la Antorcha" quedó como ceja visual del hero,
  pero no como título de pestaña).

## 7 · Flujo de trabajo de Git y PR usado en esta campaña

1. **Una rama por tema de cambio**, no una sola rama acumulando todo. Facilita que un PR se
   revise y apruebe sin arrastrar cambios de otro tema.
2. **Nunca push directo a `main`.** Todo cambio pasa por Pull Request, incluso ajustes de una
   línea, para que el cliente decida cuándo fusionar.
3. **Verificar antes de abrir el PR**: build de la herramienta correspondiente
   (`tools/build_artifacts.py` en este proyecto), pruebas en navegador headless a varios
   anchos, y `grep` de que el texto pedido quedó exactamente como se pidió.
4. **Describir el PR con el "por qué", no solo el "qué"**: cada PR de esta campaña incluyó una
   sección explicando decisiones que el revisor podría cuestionar, para que apruebe con
   contexto completo en vez de a ciegas.
5. **Confirmar el estado de `main` después de cada fusión** (`git fetch` + `git log
   origin/main`) antes de asumir que un cambio ya está integrado — ver el error de §5.2.
6. **Nunca abrir un Pull Request sin que el usuario lo pida explícitamente** salvo que el
   propio flujo de trabajo pactado con el cliente ya lo dé por hecho (como en esta campaña,
   donde cada tanda de cambios terminaba en un PR nuevo).

---

## 8 · Referencias de esta campaña

| PR | Contenido |
|---|---|
| #1 | Formulario de contacto nativo en vidrio, conectado a Jotform |
| #2 | Renombrar la landing a `index.html` (raíz del sitio) |
| #3 | Retirar el pre-registro y dejar el contacto como único formulario |
| #4 | Crédito de autoría y título de pestaña general |
| #5 | Ajustes de copy institucional (EE.UU., contacto, requisitos, elegibilidad, FAQ) |
| #6 | Unificar los botones de contacto — commit que quedó fuera del #5 (ver §5.2) |

Todos los PR están en `octaviogarcia-hue/Posgrado-Regular`, fusionados contra `main`.

---

*Documento generado como cierre de campaña. Al iniciar la siguiente, copiar este archivo,
conservar las secciones 5 a 7 casi sin cambios, y reescribir las secciones 1 a 4 y 8 con los
datos de la nueva campaña.*
