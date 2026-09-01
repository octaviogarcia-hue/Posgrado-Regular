# 3. Integración técnica — pre-registro y recordatorios con Zapier

El formulario no intenta cerrar la postulación. Quien acaba de escanear un papel en un
pasillo no llena una solicitud de beca ahí mismo: deja un correo. La conversión primaria es
la captura del contacto, y **el trabajo de convertir lo hace la secuencia de recordatorios**,
no la landing.

De ahí que el formulario esté diseñado para dos cosas a la vez: pedir lo mínimo, y capturar
los dos campos que permiten segmentar los recordatorios (`nivel` y `estatus_ingles`).

---

## 3.1 Qué envía la landing

`POST` con `Content-Type: application/json` al *Catch Hook* de Zapier. La URL se pega en un
solo sitio: `CONFIG.ENDPOINT`, al inicio del `<script>` de cada página. Con ese campo vacío
las páginas funcionan en **modo demo**: validan, muestran la confirmación y escriben en la
consola el payload exacto que recibiría Zapier.

```json
{
  "nombre": "Ana Ruiz Molina",
  "correo": "ana.ruiz@ejemplo.mx",
  "nivel": "maestria",
  "area": "ciencias_ingenieria",
  "estatus_ingles": "agendado",
  "elegibilidad_confirmada": true,
  "consentimiento_aviso": true,
  "convocatoria_abierta": true,
  "fecha_cierre_objetivo": "2027-01-16T05:59:59.000Z",
  "utm_source": "volante_impreso",
  "utm_medium": "qr",
  "utm_campaign": "fulbright_posgrado_regular_2026",
  "utm_content": "hook_a",
  "qr_id": "feria_unam_01",
  "landing_variant": "modelo-1-scrollytelling",
  "referrer": "directo",
  "locale": "es-MX",
  "timestamp_iso": "2025-12-01T16:04:22.113Z"
}
```

Esquema formal en [`preregistro.schema.json`](./preregistro.schema.json) (JSON Schema Draft
2020-12), utilizable en un paso de *Code by Zapier* para validar antes de escribir en la hoja.

### Diccionario de campos

| Campo | Origen | Para qué sirve |
|---|---|---|
| `nombre` | Usuario | Personalización del correo |
| `correo` | Usuario | **Clave única** del contacto y de la deduplicación |
| `nivel` | Usuario | Segmenta el monto y la duración que se cita en cada recordatorio |
| `area` | Usuario (M2) | Permite priorizar STEM y estudios sobre EE. UU. en la comunicación |
| `estatus_ingles` | Usuario (M2) | **El campo más accionable:** decide qué secuencia recibe |
| `elegibilidad_confirmada` | Usuario | Filtra a quien no puede postular antes de gastarle un correo |
| `consentimiento_aviso` | Usuario | Cumplimiento LFPDPPP. Sin `true` no se envía nada |
| `convocatoria_abierta` | `CONFIG` | Separa «recordar el cierre» de «avisar la apertura» |
| `fecha_cierre_objetivo` | `CONFIG` | Deja que Zapier calcule las fechas en vez de codificarlas |
| `utm_*`, `qr_id` | Query string | Atribución por hook impreso y por punto de reparto |
| `landing_variant` | `CONFIG` | Prueba A/B entre los dos modelos |
| `referrer`, `locale`, `timestamp_iso` | Navegador | Diagnóstico |

> **Por qué `fecha_cierre_objetivo` viaja en el payload.** Si la fecha de cierre vive dentro
> del Zap, cada año hay que editar el Zap y la landing. Viajando en el dato, el año que viene
> se cambia una línea en `CONFIG` y toda la automatización se recalcula sola.

---

## 3.2 Los tres Zaps

### Zap 1 — Captura y alta

```
Disparador   Webhooks by Zapier · Catch Hook
             └─ La URL que se pega en CONFIG.ENDPOINT

Paso 2       Filter by Zapier
             └─ Continuar solo si  consentimiento_aviso = true
                                Y  elegibilidad_confirmada = true

Paso 3       Google Sheets · Lookup Row          (deduplicación)
             └─ Buscar  correo  en la hoja "Pre-registros 2026"

Paso 4       Formatter · Date/Time · Add/Subtract Time
             ├─ recordatorio_1 = fecha_cierre_objetivo − 60 días
             ├─ recordatorio_2 = fecha_cierre_objetivo − 30 días
             ├─ recordatorio_3 = fecha_cierre_objetivo −  7 días
             └─ recordatorio_4 = fecha_cierre_objetivo −  2 días

Paso 5       Google Sheets · Create or Update Row
             └─ Una columna por campo del payload, más las cuatro fechas
                calculadas y cuatro casillas  recordatorio_N_enviado

Paso 6       Gmail / Mailchimp · Send Email
             └─ Bienvenida con la guía de requisitos en PDF
                (cumple de inmediato la promesa del formulario)
```

### Zap 2 — Recordatorios programados

Un solo Zap diario cubre las cuatro fechas. Es el que hace el trabajo.

```
Disparador   Schedule by Zapier · Every Day   09:00 h America/Mexico_City

Paso 2       Google Sheets · Lookup Rows
             └─ Filas donde  recordatorio_N = HOY
                        Y   recordatorio_N_enviado = FALSE
                        Y   baja = FALSE

Paso 3       Paths by Zapier — ramifica por estatus_ingles
             ├─ Ruta A · "no"        → "Todavía te da tiempo de agendar tu
             │                          TOEFL, IELTS o Duolingo"
             ├─ Ruta B · "agendado"  → "Ve preparando el GRE: es obligatorio
             │                          y el mínimo depende de tu área"
             └─ Ruta C · "si"        → "Solo te falta el expediente.
                                        Quedan N días"

Paso 4       Gmail · Send Email
             └─ Plantilla con {{nombre}}, el monto que corresponde a
                {{nivel}} y los días restantes

Paso 5       Google Sheets · Update Row
             └─ recordatorio_N_enviado = TRUE     (evita duplicados)
```

### Zap 3 — Aviso de apertura del siguiente ciclo

Para los contactos que llegaron con la convocatoria ya cerrada.

```
Disparador   Schedule by Zapier · Every Day
Paso 2       Filter · solo el 1 de septiembre
Paso 3       Google Sheets · Lookup Rows  →  convocatoria_abierta = FALSE
Paso 4       Gmail  →  "Ya abrió la convocatoria que estabas esperando"
```

---

## 3.3 Cadencia de la secuencia

| Momento | Contenido | Objetivo |
|---|---|---|
| Inmediato | Guía de requisitos en PDF | Cumplir la promesa del formulario |
| −60 días | Checklist de exámenes | Que agenden TOEFL / GRE a tiempo |
| −30 días | Documentación y cartas de recomendación | Preparar el expediente |
| −7 días | Recordatorio de cierre | Urgencia |
| −2 días | Último aviso | Rezagados |

Los −60 días no son arbitrarios: son el tiempo mínimo razonable para agendar y presentar un
examen de inglés y el GRE. Un recordatorio que llega a −7 días a alguien que respondió «no»
en `estatus_ingles` llega tarde para servir de algo.

---

## 3.4 Consideraciones

- **Deduplicación.** `correo` es la clave. El *Lookup Row* antes del *Create or Update*
  evita altas repetidas si alguien envía el formulario dos veces.
- **Baja.** Todo correo lleva enlace de baja; un Zap adicional marca `baja = TRUE` y el
  Paso 2 del Zap 2 filtra por esa columna.
- **Datos personales.** La hoja contiene datos personales bajo la LFPDPPP: restringir el
  acceso a las cuentas de COMEXUS que lo necesiten y fijar una política de retención
  (por ejemplo, borrado a los 12 meses del cierre).
- **CORS.** Los *Catch Hooks* de Zapier aceptan `POST` desde el navegador. Si el endpoint
  cambiara a un backend propio, habría que habilitar CORS para el dominio de la landing.
- **Volumen.** Un reparto de volantes concentra los envíos en pocas horas. Los planes de
  Zapier se cobran por tarea: conviene revisar el límite mensual antes de una feria grande.
- **El QR impreso no se puede corregir.** Que apunte siempre a una URL corta propia que
  **redirija** a la landing (`beca.comexus.org.mx/qr`). Si mañana hay que cambiar de modelo,
  de proveedor o de ciclo, se cambia la redirección y los volantes ya repartidos siguen
  sirviendo.
