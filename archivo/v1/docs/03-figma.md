# 3. Traslado a componentes de Figma

Guía para reconstruir estas landings como sistema de diseño en Figma, de modo que el
archivo y el código no se separen con el tiempo.

---

## 3.1 Estructura del archivo

```
📄 Fulbright — Posgrado Regular
├── 📑 00 · Fundamentos      variables, escala tipográfica, retícula, iconos
├── 📑 01 · Componentes      biblioteca publicada
├── 📑 02 · Modelo 1         Observatorio — 375 / 768 / 1440
├── 📑 03 · Modelo 2         Trayecto — 375 / 768 / 1440
├── 📑 04 · Volante          impreso 21,6 × 27,9 cm + zona de QR
└── 📑 05 · Entrega          specs, estados, notas de handoff
```

El volante vive en el mismo archivo que las landings **a propósito**: el *message match*
entre el impreso y la pantalla se rompe en cuanto viven en archivos distintos.

---

## 3.2 Variables (Figma Variables, no estilos sueltos)

Crear cuatro colecciones. Los nombres deben coincidir **carácter por carácter** con los
custom properties del CSS: es lo que permite que un cambio en Figma se traduzca a una sola
línea de código.

### Colección `color` — modos: `Claro` / `Oscuro`

| Variable | Claro | Oscuro |
|---|---|---|
| `paper` | `#F4F5F1` | `#0B1017` |
| `surface` | `#FFFFFF` | `#121A24` |
| `ink` | `#0E1D34` | `#E9EDF1` |
| `ink-2` | `#4B5B70` | `#A9B5C4` |
| `ink-3` | `#78859A` | `#7B8899` |
| `line` | `#DCDFD8` | `#232D3A` |
| `accent` | `#C41B60` | `#FF7BAA` |
| `accent-soft` | `#FAE9F0` | `#2A1421` |
| `halo` | `#2E6F9E` | `#7FB6DE` |

El Modelo 2 usa una colección aparte (`color-noct`) con un solo modo, porque es un diseño
comprometido con el tema oscuro: `bg #080A18`, `rosa #FF2E7E`, `violeta #6C4BFF`,
`ambar #FFC24B`, `jade #39E0A8`, `text #F3F4FB`.

> **Regla:** ningún componente lleva un hex escrito a mano. Si un color no está en la
> colección, no existe.

### Colección `espaciado`

`space-1 = 4` · `space-2 = 8` · `space-3 = 12` · `space-4 = 16` · `space-6 = 24` ·
`space-8 = 32` · `space-12 = 48` · `space-16 = 64`

### Colección `radio`

`r-sm = 12` · `r = 20` · `r-pill = 999` · `r-ficha = 2` (Modelo 1)

### Colección `tipografia` — modos: `Móvil` / `Escritorio`

Las variables fluidas de CSS (`clamp()`) no tienen equivalente en Figma. Se resuelve
declarando los **dos extremos** como modos y dejando que el desarrollo interpole:

| Variable | Móvil | Escritorio |
|---|---|---|
| `step--1` | 13 | 14 |
| `step-0` | 16 | 17 |
| `step-1` | 19 | 22 |
| `step-2` | 24 | 30 |
| `step-3` | 30 | 45 |
| `step-4` | 42 | 90 (M2) / 64 (M1) |

---

## 3.3 Componentes y sus variantes

Todo con **Auto Layout**. Nada posicionado a mano salvo la aurora decorativa del Modelo 2.

### `Boton`

| Propiedad | Valores |
|---|---|
| `jerarquia` | `primario` · `fantasma` |
| `estado` | `normal` · `hover` · `presionado` · `cargando` · `deshabilitado` |
| `ancho` | `hug` · `fill` |
| `icono` | booleano (flecha a la derecha) |

Auto Layout horizontal, padding `space-4 / space-6`, alto **fijo en 52**, gap `space-2`.
El estado `cargando` sustituye la etiqueta por "Enviando…" — no agrega un spinner encima,
porque el ancho cambiaría y el botón saltaría.

### `Campo`

| Propiedad | Valores |
|---|---|
| `tipo` | `texto` · `email` · `select` · `radio-pill` · `checkbox` |
| `estado` | `reposo` · `foco` · `error` · `deshabilitado` |
| `ayuda` | booleano |

Estructura interna (vertical, gap `space-1`): `Label` → `Input` → `Ayuda` / `Error`. El
slot de ayuda y el de error **ocupan la misma ranura**: así el formulario no cambia de alto
al aparecer un error, que es una de las fuentes más comunes de CLS.

### `TarjetaApoyo`

Slots: `nivel`, `monto`, `duracion`, `lista de inclusiones`.
Variantes: `nivel = maestria | doctorado` (cambia el color del monto).

### `FilaRequisito`

Auto Layout horizontal con `space-between`. Slots: `concepto`, `detalle` (opcional),
`valor`. Variante `enfasis = normal | critico` para GRE y para "no requerida".

### `Hito`

Slots: `fecha`, `titulo`, `nota`. Variante `estado = pasado | actual | futuro`, que cambia
el relleno del punto y el peso del título.

### `Tile` (exclusivo del Modelo 2)

El componente central del bento.

| Propiedad | Valores |
|---|---|
| `span` | `2` · `3` · `4` · `6` |
| `alto` | `auto` · `doble` |
| `estado` | `reposo` · `hover` |

Efecto de vidrio: relleno `#FFFFFF` al 5.5 % + **Background blur 22** + borde de 1 px
`#FFFFFF` al 13 % + sombra interior superior de 1 px al 9 %.

> El *background blur* de Figma solo se ve si hay algo detrás. Colocar el frame de aurora
> como capa de fondo del page **antes** de construir los tiles; si no, el vidrio se ve
> plano y el equipo pensará que el efecto está mal.

### `EstadoConvocatoria`

Variante `estado = abierta | cerrada`. Controla simultáneamente la píldora del header, el
texto del contador, la etiqueta del CTA y el texto del dock — los cuatro puntos que cambian
cuando pasa la fecha límite. Tenerlo como un solo componente evita que se actualicen tres
de cuatro.

---

## 3.4 Reglas de responsive en Figma

| Elemento | Constraint / Auto Layout |
|---|---|
| Secciones | `Fill container` horizontal, `Hug` vertical |
| Contenedor | Máx. 1184 px, centrado, padding lateral por variable |
| Bento | Grid de 6 columnas, gap 16, con variantes de span por breakpoint |
| Hero M1 | El canvas es un frame de placeholder con `Fill`, alto por variable `hero-h` |
| Dock | `Fixed position when scrolling`, anclado abajo, oculto en el frame de 1440 |

Crear los tres frames (375 / 768 / 1440) para cada modelo. No entregar solo el de 375
"porque escala": las decisiones de bento de 6 columnas y de ocultamiento del dock hay que
verlas.

---

## 3.5 Assets oficiales — pendiente bloqueante

Las dos landings usan hoy un **wordmark tipográfico provisional**. Antes de publicar:

1. Solicitar a COMEXUS el lockup oficial Fulbright-García Robles en SVG.
2. Respetar el área de resguardo y las proporciones de la guía de marca de Fulbright.
3. Sustituir el bloque marcado con el comentario `<!-- Sustituir por el lockup oficial -->`
   en ambos archivos HTML y el componente `Wordmark` en Figma.

No recolorear, no reproporcionar y no reconstruir el logotipo a partir de una imagen: el
uso de la marca Fulbright está regulado.

---

## 3.6 Handoff

- Publicar la página `01 · Componentes` como **biblioteca de equipo**.
- Anotar en `05 · Entrega` los cuatro estados que no se ven en el diseño estático:
  convocatoria cerrada, error de red en el envío, éxito de envío y `prefers-reduced-motion`.
- Los tokens de Figma y los custom properties del CSS comparten nombre; documentar esa
  correspondencia en la portada del archivo para que quien entre después no invente
  nombres nuevos.
