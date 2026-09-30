# Flujo de captación automatizado

```
1. Identificar → 2. Diagnosticar → 3. Calificar → 4. Contactar → 5. Agendar → 6. Notificarte
```

| Paso | Qué hace | Herramientas propuestas | Costo |
|---|---|---|---|
| **1. Identificar** | Buscar negocios por nicho y ciudad en Google Maps (nombre, teléfono, sitio, reseñas) | Google Places API | Crédito gratis mensual de Google Maps Platform |
| **2. Diagnosticar** | Revisar el sitio de cada negocio: velocidad, móvil, SEO básico, perfil de Google, presencia en IA | PageSpeed Insights API, Claude, Semrush/Ahrefs para los mejores leads | Gratis / tus licencias |
| **3. Calificar** | Puntuar el lead por nicho, oportunidad detectada y facilidad de contacto | Claude + CRM | Gratis |
| **4. Contactar** | Mensaje personalizado con 1–2 hallazgos reales de su negocio | Email (Gmail) + WhatsApp (ver nota) | Gratis |
| **5. Agendar** | Mandar enlace de agenda a quien responda con interés | Cal.com o Calendly (plan gratis) | Gratis |
| **6. Notificarte** | Aviso a tu WhatsApp con cada cita o lead caliente, con resumen del negocio | CallMeBot (gratis) o Twilio WhatsApp | Gratis / bajo |

## CRM

Propuesta: **HubSpot CRM gratis** (tiene API, pipeline visual y app móvil). Alternativa más simple para empezar: **Google Sheets**.

## Nota importante sobre WhatsApp

- **Para notificarte a ti:** es fácil y gratis con CallMeBot, o con Twilio si se necesita algo más robusto.
- **Para prospectar en frío:** WhatsApp **banea números** que envían mensajes masivos a desconocidos. La API oficial (WhatsApp Business Platform) solo permite iniciar conversaciones con plantillas aprobadas, y cobra por conversación. Recomendación:
  1. Primer contacto por **email** (y opcionalmente una llamada o un mensaje manual).
  2. WhatsApp **solo con quien ya respondió** o dio permiso.
  3. Si se usa WhatsApp en frío, que sea con un número secundario, a bajo volumen y con mensajes redactados por Claude pero enviados de forma manual o semiautomática.

### Modo elegido: WhatsApp Business con número nuevo, envío semiautomático

No se automatiza WhatsApp Web con bots (whatsapp-web.js, Baileys, extensiones de envío masivo): va contra los términos de WhatsApp y es la causa más común de baneo, sobre todo en números nuevos.

Así funciona:

1. El sistema prepara cada día una lista de leads con su mensaje personalizado, redactado por Claude.
2. Cada lead trae un enlace `https://wa.me/52XXXXXXXXXX?text=...` con el mensaje ya escrito.
3. Tú haces clic, revisas y envías desde WhatsApp Business. Cada envío toma unos 10 segundos.
4. Las respuestas las marcas en el CRM, o las clasifica Claude si le pegas la conversación.

Reglas para cuidar el número:

- **Calentamiento:** usar el número 1–2 semanas de forma normal antes de prospectar. Completar el perfil de empresa: foto, descripción, horario, sitio y catálogo.
- **Volumen:** empezar con 10–15 mensajes al día y subir poco a poco hasta un máximo de 30–40.
- **Mensajes únicos:** cada mensaje menciona algo específico del negocio. Nunca mandar el mismo texto a todos.
- **Sin enlaces en el primer mensaje:** enviar el diagnóstico o la agenda solo cuando respondan.
- **Salida fácil:** incluir algo como "si no le interesa, dígamelo y no le vuelvo a escribir".
- **Señal de alerta:** si varios contactos bloquean o reportan, bajar el volumen varios días.
- Tener un **número de respaldo** por si banean el principal.

## Contacto doble: WhatsApp + correo

Cada lead recibe **el mismo día** un WhatsApp corto y un correo con más detalle (los hallazgos de su sitio o de su perfil de Google). El WhatsApp puede decir "le acabo de enviar un correo con lo que encontré". Así cada canal refuerza al otro.

Para el correo en frío:
- **Dominio secundario:** por ejemplo `faridclienta.com` en vez de tu dominio principal, con Google Workspace o Zoho Mail. Si hay reportes de spam, tu dominio principal queda protegido.
- **Configurar SPF, DKIM y DMARC** en el dominio antes de enviar.
- **Calentamiento:** 2–3 semanas con volumen bajo y creciente, de 10 a 30 correos al día por buzón.
- **Texto plano,** sin imágenes ni enlaces en el primer correo, con una línea para darse de baja.
- **Rebotes:** algunos correos del DENUE pueden ser viejos; se quitan de la lista los que reboten.

## Métricas

- Leads identificados por semana
- Tasa de respuesta por nicho y por canal (WhatsApp vs. correo), para descubrir qué nicho y qué canal responden más rápido
- Citas por semana
- Tasa de cierre y ticket promedio

## Siguiente paso técnico

Pasos 1 y 2 hechos con el DENUE (ver `prospeccion/`). Falta: plantillas de mensaje (WhatsApp + correo), carga al CRM y notificaciones.
