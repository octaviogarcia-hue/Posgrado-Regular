# 4. Integración técnica

## 4.1 Exportar el código a GitHub

Las dos landings son archivos HTML autónomos: no hay build, no hay dependencias que
instalar, no hay paso de compilación. Eso hace la publicación trivial.

### Ya está hecho en este repositorio

```bash
git checkout -b claude/fulbright-phygital-campaign-6dllr9
git add .
git commit -m "Campaña phygital Fulbright-García Robles: dos modelos de landing"
git push -u origin claude/fulbright-phygital-campaign-6dllr9
```

### Publicar con GitHub Pages

1. En el repositorio → **Settings › Pages**.
2. *Source*: `Deploy from a branch`. Rama: `main` (o la rama de campaña). Carpeta: `/ (root)`.
3. Guardar. En un par de minutos las páginas quedan en:
   - `https://<usuario>.github.io/Posgrado-Regular/modelo-1-observatorio.html`
   - `https://<usuario>.github.io/Posgrado-Regular/modelo-2-trayecto.html`

### Dominio propio (recomendado para el QR impreso)

Un QR impreso **no se puede corregir después**. Conviene que apunte a un dominio bajo
control, no a `github.io`:

1. Crear el archivo `CNAME` en la raíz con el dominio, p. ej. `beca.comexus.org.mx`.
2. En el DNS, un registro `CNAME` de `beca` hacia `<usuario>.github.io`.
3. Activar **Enforce HTTPS** en Settings › Pages.

> **Regla del QR:** que el código impreso apunte siempre a una URL corta y estable propia
> (`beca.comexus.org.mx/qr`) que **redirija** a la landing. Si mañana hay que cambiar de
> modelo, de proveedor o de ciclo, se cambia la redirección y los volantes ya repartidos
> siguen funcionando. Un QR que apunta directo al HTML final es un QR desechable.

### Flujo de trabajo sugerido

| Rama | Uso |
|---|---|
| `main` | Lo que está publicado. Protegida. |
| `claude/fulbright-phygital-campaign-*` | Desarrollo de la campaña. |
| `ciclo/2027` | Actualización del siguiente ciclo (solo cambia `CONFIG`). |

Para el siguiente ciclo basta editar el bloque `CONFIG` al inicio del `<script>` de cada
página:

```js
const CONFIG = {
  CIERRE: new Date('2027-01-31T23:59:59-06:00'),
  APERTURA_SIGUIENTE: '1 de septiembre',
  ENDPOINT: 'https://hooks.zapier.com/hooks/catch/000000/abcdef/',
  VARIANTE: 'modelo-1-observatorio'
};
```

Contador, píldora de estado, etiqueta del CTA, texto del dock y mensaje de confirmación se
recalculan solos a partir de esa fecha.

---

## 4.2 Estructura de datos del pre-registro

### Payload que envían las landings

`POST` con `Content-Type: application/json` al *Catch Hook* de Zapier:

```json
{
  "nombre": "Ana Ruiz Molina",
  "correo": "ana.ruiz@ejemplo.mx",
  "nivel": "maestria",
  "area": "ciencias_sociales",
  "estatus_ingles": "agendado",
  "consentimiento_aviso": true,
  "fecha_cierre_objetivo": "2026-02-01T05:59:59.000Z",
  "utm_source": "volante_impreso",
  "utm_medium": "qr",
  "utm_campaign": "fulbright_posgrado_regular_2026",
  "utm_content": "hook_a",
  "qr_id": "feria_unam_01",
  "landing_variant": "modelo-1-observatorio",
  "referrer": "directo",
  "locale": "es-MX",
  "timestamp_iso": "2025-12-01T16:04:22.113Z"
}
```

### Diccionario de campos

| Campo | Tipo | Origen | Para qué sirve |
|---|---|---|---|
| `nombre` | string | Usuario | Personalización del correo |
| `correo` | string (email) | Usuario | Clave única del contacto |
| `nivel` | enum `maestria` \| `doctorado` | Usuario | Segmenta el monto y la duración que se menciona en cada recordatorio |
| `area` | enum (5 valores) | Usuario (solo M2) | Determina qué sección del GRE se le recuerda |
| `estatus_ingles` | enum `si` \| `agendado` \| `no` | Usuario (solo M2) | **El campo más accionable:** decide qué secuencia recibe |
| `consentimiento_aviso` | boolean | Usuario | Cumplimiento LFPDPPP. Sin `true` no se envía nada |
| `fecha_cierre_objetivo` | ISO 8601 | `CONFIG` | Permite a Zapier calcular las fechas de recordatorio sin codificarlas |
| `utm_*` | string | Query string | Atribución por hook y por punto de reparto |
| `qr_id` | string | Query string | Identifica el lote físico de volantes |
| `landing_variant` | string | `CONFIG` | Prueba A/B entre modelos |
| `referrer` / `locale` / `timestamp_iso` | string | Navegador | Diagnóstico y depuración |

**Nota sobre `estatus_ingles`:** es lo que convierte una lista de correos en una campaña
útil. Quien responde `no` está a meses de poder postular y necesita recordatorios sobre el
examen; quien responde `si` solo necesita recordatorios sobre la fecha de cierre. Enviar el
mismo correo a los dos desperdicia la mitad del impacto.

### Esquema formal

Ver [`preregistro.schema.json`](./preregistro.schema.json) — JSON Schema Draft 2020-12,
utilizable para validar en un paso de *Code by Zapier* antes de escribir en la hoja.

---

## 4.3 Zaps de recordatorio automático

### Zap 1 — Captura y alta

```
Disparador   Webhooks by Zapier · Catch Hook
             └─ URL que se pega en CONFIG.ENDPOINT

Paso 2       Filter by Zapier
             └─ Continuar solo si  consentimiento_aviso  es  true

Paso 3       Formatter · Date/Time  (Add/Subtract Time)
             ├─ recordatorio_1 = fecha_cierre_objetivo − 60 días
             ├─ recordatorio_2 = fecha_cierre_objetivo − 30 días
             └─ recordatorio_3 = fecha_cierre_objetivo −  7 días

Paso 4       Google Sheets · Create Spreadsheet Row
             └─ Hoja "Pre-registros 2026" (una columna por campo del payload
                + las tres fechas calculadas)

Paso 5       Gmail / Mailchimp · Send Email
             └─ Correo de bienvenida con la guía de requisitos en PDF
```

### Zap 2 — Recordatorios programados

```
Disparador   Schedule by Zapier · Every Day  (09:00 h, America/Mexico_City)

Paso 2       Google Sheets · Lookup Rows
             └─ filas donde recordatorio_1 = HOY  (y ramas para _2 y _3)

Paso 3       Paths by Zapier
             ├─ Path A · estatus_ingles = "no"
             │   → "Todavía puedes agendar tu TOEFL / IELTS / Duolingo"
             ├─ Path B · estatus_ingles = "agendado"
             │   → "Ve preparando el GRE: necesitas 152 en tu sección"
             └─ Path C · estatus_ingles = "si"
                 → "Solo te falta enviar el expediente. Quedan N días"

Paso 4       Gmail · Send Email
             └─ Plantilla con {{nombre}}, {{nivel}} y días restantes

Paso 5       Google Sheets · Update Row
             └─ marcar recordatorio_N_enviado = TRUE  (evita duplicados)
```

### Zap 3 — Aviso final

```
Disparador   Schedule by Zapier · Every Day
Paso 2       Filter · solo si faltan 2 días o menos para el cierre
Paso 3       Gmail  →  "Último aviso: la convocatoria cierra el 31 de enero"
Paso 3b      Twilio (opcional)  →  SMS/WhatsApp si se capturó teléfono
```

### Cadencia de la secuencia

| Momento | Contenido | Objetivo |
|---|---|---|
| Inmediato | Guía de requisitos en PDF | Cumplir la promesa del formulario |
| −60 días | Checklist de exámenes | Que agenden TOEFL/GRE a tiempo |
| −30 días | Documentación y cartas de recomendación | Preparar el expediente |
| −7 días | Recordatorio de cierre | Urgencia |
| −2 días | Último aviso | Rezagados |

### Consideraciones

- **Deduplicación:** usar `correo` como clave. Un paso de *Lookup Row* antes del *Create
  Row* evita altas repetidas si alguien envía el formulario dos veces.
- **Baja:** todo correo debe llevar enlace de baja; un Zap adicional marca
  `baja = TRUE` en la hoja y los pasos de envío filtran por esa columna.
- **Datos personales:** la hoja de cálculo contiene datos personales bajo la LFPDPPP.
  Restringir el acceso a las cuentas de COMEXUS que lo necesiten y fijar una política de
  retención (p. ej. borrado a los 12 meses del cierre).
- **CORS:** los *Catch Hooks* de Zapier aceptan `POST` desde el navegador. Si en el futuro
  el endpoint cambia a un backend propio, habrá que habilitar CORS para el dominio de la
  landing.
