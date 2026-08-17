# Campaña Phygital — Beca Fulbright-García Robles · Posgrado Regular

Del volante impreso al pre-registro digital. Un código QR en papel lleva a una landing page
orientada a conversión; **dos modelos de diseño distintos** compiten por el mismo objetivo.

El 99 % del tráfico llega por teléfono, así que las dos páginas son **mobile-first en
retrato**: proporciones verticales, tipografía dimensionada para la mano, y gestos táctiles
en lugar de eventos de ratón.

---

## Contenido

```
modelo-1-recorrido-binacional.html   Globo 3D interactivo (Three.js + respaldo propio)
modelo-2-bento-vertical.html         Bento apilado, glassmorphism, sin motores 3D
docs/
  01-copy.md                         Hook del volante y microcopy de las landings
  02-zapier.md                       Pre-registro y recordatorios automáticos
  preregistro.schema.json            Esquema del payload de pre-registro
tools/
  build_artifacts.py                 Genera fragmentos publicables desde los HTML
archivo/v1/                          Versión anterior del encargo (otra paleta y otro
                                     concepto de escena), conservada como referencia
```

Los dos HTML son **autónomos**: CSS y JavaScript embebidos, sin build, sin fuentes externas,
sin dependencias obligatorias. Se abren con doble clic.

---

## Los dos modelos

### Modelo 1 — Recorrido Binacional

Un globo terráqueo encuadrado para pantalla vertical, girando sobre el corredor
México–Estados Unidos. Dos arcos animados viajan entre las dos ciudades, uno en cada
sentido. En sus extremos, el **Ángel de la Independencia** y la **Estatua de la Libertad**,
construidos con geometrías simples. La información vive en un **bottom sheet** de tres
posiciones que se arrastra con el pulgar.

- **Gestos:** un dedo gira, dos dedos acercan, el toque en un marcador centra la cámara y
  abre la sección correspondiente.
- **Marcadores accesibles:** los monumentos llevan botones HTML anclados a su posición
  proyectada. Un glifo dibujado en el lienzo no es enfocable ni lo lee un lector de
  pantalla; un botón sí.
- **Formulario de un paso, tres campos** — máxima tasa de conversión.

Three.js se carga por CDN mediante *import map* (ESM). El punto importante es cómo:

> Un renderizador propio en Canvas 2D **pinta desde el primer fotograma**, con la misma
> geometría, el mismo encuadre y la misma interacción. Si Three.js llega antes de 3.5 s,
> releva el render sustituyendo el `<canvas>`. Si el CDN está bloqueado por CSP, por la red
> del campus o por falta de conexión, no ocurre nada visible. El hero nunca queda vacío y el
> LCP no depende de un tercero.

### Modelo 2 — Corredor Fulbright

Interfaz contemporánea sin motores 3D: **bento apilado en vertical** (1 columna en móvil,
4 a partir de 46rem, 6 a partir de 70rem), **glassmorphism** sobre una aurora en movimiento,
tipografía de peso 800 con tracking negativo y micro-interacciones —reflejo que sigue al
dedo, revelado escalonado, contadores de monto, reloj de cierre al segundo—.

- **Zonas táctiles de 56 px** en todos los controles.
- Control segmentado para alternar entre «Sí puedes» y «No aplica» en elegibilidad.
- **Formulario de dos pasos, seis campos** — menos conversión bruta, mucha mejor
  segmentación de la secuencia de correos.

---

## Configuración por ciclo

Cada landing tiene un único bloque de configuración al inicio de su `<script>`:

```js
const CONFIG = {
  CIERRE: new Date('2026-01-31T23:59:59-06:00'),
  APERTURA_SIGUIENTE: '1 de septiembre',
  ENDPOINT: '',            // URL del Catch Hook de Zapier. Vacío = modo demo.
  VARIANTE: 'modelo-1-recorrido-binacional'
};
```

Cambiar `CIERRE` recalcula el contador, la píldora de estado, la etiqueta del CTA, el texto
del dock y el mensaje de confirmación.

### Estado «convocatoria cerrada»

Cuando la fecha de cierre ya pasó, ambas páginas cambian solas de discurso: dejan de
prometer una postulación imposible y ofrecen aviso para la siguiente apertura. No hay que
despublicar nada ni editar textos con prisa.

Con `ENDPOINT` vacío el formulario funciona en **modo demo**: valida, muestra la
confirmación y escribe en la consola el payload exacto que recibiría Zapier.

---

## Verificación

Probado en Chromium (Playwright) a 390 × 844 con emulación táctil, y a 1440 px.

| Comprobación | Resultado |
|---|---|
| Errores de consola y de JavaScript | Ninguno |
| Desbordamiento horizontal (390 y 1440 px) | Ninguno |
| Modelo 1 con Three.js real (servido en local) | WebGL2, globo y monumentos en escena |
| Modelo 1 con el CDN bloqueado | Renderiza por el respaldo en Canvas 2D, sin salto visible |
| Toque en un marcador | Centra la cámara, abre la hoja y salta a su sección |
| Zonas táctiles por debajo de 44 px | Ninguna |
| Contador con convocatoria abierta | 61 d 13 h 59 m 12 s, avanza al segundo |
| Estado de convocatoria cerrada | Píldora, reloj, hito, dock, CTA y formulario cambian a la vez |
| Formulario: paso vacío, correo inválido, consentimiento | Bloquea y enfoca el primer campo con error |
| Formulario: envío completo | Muestra confirmación y mueve el foco |
| Montos sin JavaScript | Se leen correctos: la cifra real vive en el HTML |

---

## Pendiente antes de publicar

- [ ] Sustituir el wordmark tipográfico provisional por el lockup oficial de
      COMEXUS / Fulbright en SVG (marcado con un comentario en ambos HTML).
- [ ] Pegar la URL del Catch Hook de Zapier en `CONFIG.ENDPOINT`.
- [ ] Enlazar el aviso de privacidad real de COMEXUS (hoy es un ancla interna).
- [ ] Confirmar cifras, fechas y criterios de elegibilidad contra la convocatoria oficial
      vigente.

---

## Dos notas

**Sobre el calendario.** El material usa las fechas del brief: convocatoria del 1 de
septiembre de 2025 al 31 de enero de 2026, con inicio de estudios en agosto de 2027. Ese
periodo ya concluyó, de modo que hoy las páginas se muestran en su estado de convocatoria
cerrada. Para activar el ciclo vigente basta actualizar `CIERRE`.

**Sobre `user-scalable=no`.** El brief pide esa etiqueta de viewport y está puesta tal cual.
Conviene saber que bloquea el zoom del navegador, lo que incumple el criterio WCAG 1.4.4 y
afecta a quien necesita ampliar el texto. Las páginas están construidas para no necesitarlo
—cuerpo de 16 px mínimo, controles de 52–56 px—, así que quitar `maximum-scale=1.0,
user-scalable=no` no cambia nada del diseño y devuelve el zoom. Es una decisión de una línea.
