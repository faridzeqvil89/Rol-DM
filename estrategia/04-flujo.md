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

## Métricas

- Leads identificados por semana
- Tasa de respuesta por nicho (para descubrir qué nicho responde más rápido)
- Citas por semana
- Tasa de cierre y ticket promedio

## Siguiente paso técnico

Construir el paso 1 + 2: un script que, dado un nicho y una ciudad, saque negocios de Google Maps, analice su sitio y deje una lista calificada en el CRM.
