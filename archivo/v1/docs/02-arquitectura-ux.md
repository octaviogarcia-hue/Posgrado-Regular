# 2. Arquitectura UI/UX — Wireframe mobile-first

## 2.1 Premisa: el contexto del escaneo manda

Quien llega a estas páginas **acaba de escanear un papel**. Eso define tres restricciones
que no son negociables:

1. **Es tráfico 100 % móvil.** No hay versión "de escritorio con adaptación móvil": hay una
   versión móvil que escala hacia arriba.
2. **La sesión es corta y de pie.** Pasillo de facultad, feria de posgrados, cafetería. El
   usuario decide en segundos si guarda la página o la cierra.
3. **La intención es media, no alta.** Nadie escanea un QR decidido a llenar una solicitud
   de beca. Por eso la conversión primaria **no es postular**: es **dejar un correo**.

De ahí la decisión de producto más importante del proyecto: **la landing no intenta cerrar
la postulación, intenta capturar el contacto** y entregar valor inmediato (la guía de
requisitos) a cambio.

---

## 2.2 Wireframe mobile-first (375 px de referencia)

```
┌─────────────────────────────────────┐
│ ▸ HEADER                      56 px │  Wordmark COMEXUS/Fulbright + estado
│   [wordmark]        ● Abierta       │  de convocatoria (píldora viva)
├─────────────────────────────────────┤
│                                     │
│ ▸ HERO                              │  M1: canvas 3D a sangre (54 svh)
│   ┌───────────────────────────┐     │  M2: tile de vidrio con titular
│   │                           │     │      display sobre aurora
│   │      [objeto 3D  /        │     │
│   │       tile de vidrio]     │     │  Regla: el titular y el CTA
│   │                           │     │  primario caben en el primer
│   └───────────────────────────┘     │  viewport sin scroll
│   eyebrow · ciclo 2026              │
│   H1 (2–3 líneas, máx. 28 car./lín) │
│   subtítulo (máx. 3 líneas)         │
│   ┌─────────────────────────────┐   │
│   │  CTA PRIMARIO      52 px    │◄──┼── ancho completo, ≥52 px de alto
│   └─────────────────────────────┘   │
│   [ CTA secundario: requisitos ]    │
│   ✓ sin carta  ✓ 4–5 univ.  ✓ visa  │◄── tira de confianza sobre el pliegue
│                                     │
├─────────────────────────────────────┤
│ ▸ APOYO                             │  2 tarjetas apiladas.
│   ┌──────────┐ ┌──────────┐         │  La cifra es el elemento
│   │ $37,000  │ │ $25,000  │         │  tipográfico más grande
│   │ Maestría │ │Doctorado │         │  después del H1.
│   └──────────┘ └──────────┘         │
├─────────────────────────────────────┤
│ ▸ REQUISITOS                        │  Ficha de 2 columnas:
│   Promedio ·············· 8.0 mín.  │  concepto a la izquierda,
│   TOEFL iBT ············· 80 mín.   │  valor tabular a la derecha.
│   IELTS ················· 6.5 mín.  │  GRE resaltado en acento.
│   Duolingo ·············· 120 mín.  │
│   GRE ················ OBLIGATORIO  │
├─────────────────────────────────────┤
│ ▸ FECHAS                            │  Contador arriba (dato vivo),
│   ┌─────────────────────────────┐   │  línea de tiempo abajo
│   │  62 días para el cierre     │   │  (3 hitos, hito activo marcado).
│   └─────────────────────────────┘   │
│   ● 1 sep 2025 — abre               │
│   ○ 31 ene 2026 — cierra            │
│   ○ ago 2027 — inicias              │
├─────────────────────────────────────┤
│ ▸ PROCESO                           │  4 pasos numerados.
│   01 Verifica tu perfil             │  La numeración es legítima:
│   02 Envía tu postulación           │  es una secuencia real donde
│   03 COMEXUS gestiona admisión      │  el orden importa.
│   04 Trámite de visa                │
├─────────────────────────────────────┤
│ ▸ PRE-REGISTRO          ◄ CONVERSIÓN│  M1: 1 paso (3 campos)
│   [ Nombre completo          ]      │  M2: 2 pasos (2 + 4 campos)
│   [ Correo electrónico       ]      │
│   ( ) Maestría   ( ) Doctorado      │
│   [x] Aviso de privacidad           │
│   ┌─────────────────────────────┐   │
│   │  ENVIAR                     │   │
│   └─────────────────────────────┘   │
│   🔒 nota de uso de datos           │
├─────────────────────────────────────┤
│ ▸ FAQ                               │  Acordeón. Cerrado por defecto:
│   ▸ ¿Necesito carta de aceptación?  │  divulgación progresiva.
│   ▸ ¿El GRE es obligatorio?         │
├─────────────────────────────────────┤
│ ▸ FOOTER + aviso legal              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ ▸ DOCK FIJO      (aparece tras hero)│  Persiste el CTA sin robar
│  Hasta $37,000 USD  [Pre-registrarme]│ pantalla en el hero, y se
│  Quedan 62 días                     │  retira cuando el formulario
└─────────────────────────────────────┘  ya está a la vista.
```

### Orden de secciones y por qué

El orden responde a las preguntas del usuario **en la secuencia en que se las hace**:

| # | Sección | Pregunta que responde |
|---|---|---|
| 1 | Hero | ¿De qué se trata y me conviene? |
| 2 | Apoyo | ¿Cuánto dinero es? |
| 3 | Requisitos | ¿Califico? |
| 4 | Fechas | ¿Cuánto tiempo tengo? |
| 5 | Proceso | ¿Qué tengo que hacer? |
| 6 | Pre-registro | *(conversión — llega ya calificado y con urgencia)* |
| 7 | FAQ | Manejo de objeciones residuales |

Los requisitos van **antes** del formulario a propósito. Auto-filtran: quien no cumple, se
va sin registrarse, y quien sí cumple llega al formulario ya convencido. Un pre-registro
menos, pero de mejor calidad.

---

## 2.3 Sistema de diseño

### Breakpoints

| Nombre | Ancho | Comportamiento |
|---|---|---|
| `base` | 375–559 px | Columna única. Todo apilado. |
| `sm` | 560 px (`30rem`) | Etiquetas largas del header, gutters mayores. |
| `md` | 736 px (`46rem`) | M1: tarjetas de apoyo a 2 columnas. M2: bento a 4 columnas. |
| `lg` | 1120 px (`70rem`) | M1: contenedor máx. 74rem. M2: bento a 6 columnas, dock oculto. |

### Escala tipográfica

Fluida con `clamp()` en seis escalones (`--step--1` … `--step-4`). Nunca se interpola un
tamaño fuera de la escala.

| Rol | Modelo 1 | Modelo 2 |
|---|---|---|
| Display | Serif old-style (Iowan/Palatino/Georgia) | Sans grotesque, peso 800, tracking −0.035em |
| Cuerpo | Sans de sistema, 16 px mín., interlínea 1.6 | Sans de sistema, 16 px mín., interlínea 1.55 |
| Datos | Monoespaciada, `tabular-nums` | Monoespaciada, `tabular-nums` |

Toda cifra que se alinee en columna (montos, puntajes, contador) usa
`font-variant-numeric: tabular-nums`, para que no baile al actualizarse.

### Retícula y espaciado

- Ritmo base de 4/8 px; `--gap` y `--pad` fluidos.
- Medida de lectura acotada a `--measure: 34rem` (~65 caracteres).
- Ancho máximo de contenedor: 74rem (M1) / 80rem (M2).

### Objetivos táctiles

Todo elemento interactivo mide **≥ 52 px de alto** (por encima de los 44 pt de Apple y los
48 dp de Material), con separación mínima de 8 px. Los `<summary>` del FAQ y las píldoras
de radio también.

---

## 2.4 Accesibilidad — decisiones concretas

| Requisito | Cómo se resuelve |
|---|---|
| Contraste | Texto principal ≥ 7:1; secundario ≥ 4.5:1 en ambos temas |
| Foco visible | `:focus-visible` con anillo de 3 px en color de acento y `outline-offset` |
| Salto de navegación | Enlace "Saltar al pre-registro" como primer elemento tabulable |
| Errores de formulario | `aria-invalid` + `aria-describedby` en el campo, mensaje adyacente, foco automático al primer campo inválido |
| Confirmación | `role="status"` + `aria-live="polite"`, y foco movido al encabezado de éxito |
| Movimiento | `prefers-reduced-motion` desactiva rotación automática, aurora, revelados y contadores. La interacción sigue funcionando |
| Color no exclusivo | Estado de convocatoria = punto de color **+ texto**; requisito crítico = color **+ palabra "Obligatorio"** |
| Iconografía | SVG en línea, trazo 1.8–2.4 uniforme. Cero emoji |
| Jerarquía | `h1` → `h2` → `h3` sin saltos; secciones con `aria-labelledby` donde el encabezado no es literal |
| Zoom | `viewport` sin `maximum-scale`; ningún bloqueo de zoom |

---

## 2.5 Rendimiento

Objetivos para tráfico de QR, que suele llegar por datos móviles:

| Métrica | Objetivo | Cómo se logra |
|---|---|---|
| LCP | < 2.5 s | Cero imágenes de mapa de bits. El hero es tipografía + canvas |
| CLS | < 0.1 | Alturas reservadas con `clamp()`; el canvas ocupa una caja fija; ningún contenido se inyecta por encima |
| Peso | < 60 KB por página sin Three.js | CSS y JS embebidos, sin fuentes externas, sin librerías salvo el 3D opcional |
| INP | < 200 ms | Escuchas pasivas, animaciones sobre `transform`/`opacity`, `IntersectionObserver` en lugar de `scroll` |

**Sobre Three.js:** son ~600 KB adicionales y solo los carga el Modelo 1. Se cargan **de
forma diferida y no bloqueante**: el respaldo en Canvas 2D pinta desde el primer frame, y
Three.js releva el render solo si llega antes de 3.5 s. El LCP nunca depende del CDN.

---

## 2.6 Qué diferencia a los dos modelos (para la decisión del cliente)

No son dos maquetaciones del mismo diseño; son dos apuestas distintas.

| | **Modelo 1 — Observatorio** | **Modelo 2 — Trayecto** |
|---|---|---|
| Apuesta | Autoridad institucional | Energía y modernidad |
| Riesgo | El 3D puede leerse como adorno | El tono puede leerse como poco institucional |
| Tema | Claro, con modo oscuro completo | Oscuro por decisión de diseño |
| Formulario | 1 paso, 3 campos → conversión máxima | 2 pasos, 6 campos → segmentación más rica |
| Dependencias | Three.js (opcional) | Ninguna |
| Público donde rinde mejor | Egresados, posgrado, contexto académico formal | Estudiantes de últimos semestres, campus, redes |
| Métrica a vigilar | Tiempo hasta el primer scroll | Tasa de abandono entre paso 1 y paso 2 |

**Recomendación de medición:** repartir los QR al 50/50 con `?utm_content=m1` y
`?utm_content=m2` durante las primeras 4 semanas y decidir por **pre-registros por
escaneo**, no por permanencia en página.
