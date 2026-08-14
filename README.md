# Campaña Phygital — Beca Fulbright-García Robles · Posgrado Regular

Del volante impreso al pre-registro digital. Un código QR en papel lleva a una landing
page orientada a conversión; dos modelos de diseño distintos compiten por el mismo
objetivo.

---

## Contenido

```
modelo-1-observatorio.html    Landing con objeto 3D interactivo (Three.js + respaldo propio)
modelo-2-trayecto.html        Landing bento grid / glassmorphism, sin dependencias
docs/
  01-copy.md                  Hook del volante y microcopy de las landings
  02-arquitectura-ux.md       Wireframe mobile-first, sistema de diseño, accesibilidad
  03-figma.md                 Traslado a variables y componentes de Figma
  04-github-zapier.md         Publicación en GitHub y automatización con Zapier
  preregistro.schema.json     Esquema del payload de pre-registro
tools/
  build_artifacts.py          Genera fragmentos publicables desde los HTML autónomos
```

Los dos HTML son **autónomos**: CSS y JavaScript embebidos, sin build, sin fuentes
externas, sin dependencias obligatorias. Se abren con doble clic.

---

## Los dos modelos

### Modelo 1 — Observatorio

Base tipográfica sobria en tonos claros (con modo oscuro completo) para que el único
protagonista sea un **icosaedro de aristas** que gira con el giroscopio del teléfono o con
el cursor. La figura representa la red binacional de universidades: una forma cerrada,
muchos nodos.

Three.js se carga por CDN mediante *import map* (ESM). El punto importante es cómo:

> Un renderizador propio en Canvas 2D **pinta desde el primer frame**, con la misma silueta
> y la misma interacción. Si Three.js llega antes de 3.5 s, releva el render sustituyendo
> el `<canvas>`. Si el CDN está bloqueado por CSP, por la red del campus o por falta de
> conexión, no ocurre nada visible. El hero nunca queda vacío y el LCP nunca depende de un
> tercero.

Formulario de **un paso, tres campos** — máxima tasa de conversión.

### Modelo 2 — Trayecto

Diseño de interfaz contemporáneo, sin motores 3D: **bento grid** de 6 columnas,
**glassmorphism** sobre una aurora en movimiento, tipografía display de peso 800 con
tracking negativo, y micro-interacciones (reflejo que sigue al puntero, revelado
escalonado, contadores de monto, reloj de cierre al segundo).

Tema oscuro por decisión de diseño: el vidrio necesita luz detrás para leerse. Todos los
colores están declarados de forma explícita.

Formulario de **dos pasos, seis campos** — menos conversión bruta, mucha mejor
segmentación de la secuencia de correos.

La comparación completa, con la métrica que debe decidir el ganador, está en
[`docs/02-arquitectura-ux.md`](docs/02-arquitectura-ux.md#26-qué-diferencia-a-los-dos-modelos-para-la-decisión-del-cliente).

---

## Configuración por ciclo

Cada landing tiene un único bloque de configuración al inicio de su `<script>`:

```js
const CONFIG = {
  CIERRE: new Date('2026-01-31T23:59:59-06:00'),
  APERTURA_SIGUIENTE: '1 de septiembre',
  ENDPOINT: '',            // URL del Catch Hook de Zapier. Vacío = modo demo.
  VARIANTE: 'modelo-1-observatorio'
};
```

Cambiar `CIERRE` recalcula el contador, la píldora de estado, la etiqueta del CTA, el texto
del dock y el mensaje de confirmación.

### Estado "convocatoria cerrada"

Cuando la fecha de cierre ya pasó, ambas páginas cambian solas de discurso: dejan de
prometer una postulación imposible y ofrecen aviso para la siguiente apertura. No hay que
despublicar nada ni editar textos con prisa.

Con `ENDPOINT` vacío el formulario funciona en **modo demo**: valida, muestra la
confirmación y escribe en la consola el payload exacto que recibiría Zapier.

---

## Verificación

Ambas páginas se probaron en Chromium (Playwright) a 375, 390 y 1440 px:

| Comprobación | Resultado |
|---|---|
| Errores de consola y de JavaScript | Ninguno |
| Desbordamiento horizontal | Ninguno en los tres anchos |
| Objeto 3D con el CDN bloqueado | Renderiza por el respaldo en Canvas 2D |
| Contador con convocatoria abierta | 61 d 19 h 59 m 54 s, avanza al segundo |
| Estado de convocatoria cerrada | Titular, CTA, dock y píldora cambian a la vez |
| Formulario: paso vacío, correo inválido, consentimiento | Bloquea y enfoca el primer campo con error |
| Formulario: envío completo | Muestra confirmación y mueve el foco |

---

## Publicación

Ver [`docs/04-github-zapier.md`](docs/04-github-zapier.md). En resumen: GitHub Pages desde
la raíz del repositorio, dominio propio vía `CNAME`, y —regla importante— **que el QR
impreso apunte a una URL corta propia que redirija**, nunca directo al archivo HTML. Un
volante ya repartido no se puede corregir.

---

## Pendiente antes de publicar

- [ ] Sustituir el wordmark tipográfico provisional por el lockup oficial de
      COMEXUS / Fulbright en SVG (marcado con un comentario en ambos HTML).
- [ ] Pegar la URL del Catch Hook de Zapier en `CONFIG.ENDPOINT`.
- [ ] Enlazar el aviso de privacidad real de COMEXUS (hoy es un ancla interna).
- [ ] Confirmar las cifras y fechas contra la convocatoria oficial vigente.

---

## Nota sobre el calendario

El material se construyó con las fechas del brief: convocatoria del **1 de septiembre de
2025 al 31 de enero de 2026**, con inicio de estudios en **agosto de 2027**. Ese periodo ya
concluyó, de modo que las páginas se muestran hoy en su estado de convocatoria cerrada.
Para activar el ciclo vigente basta actualizar `CIERRE` en el bloque `CONFIG` de cada
página.
