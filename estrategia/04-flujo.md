# Flujo de captación automatizado

> Borrador de la arquitectura. Las herramientas son propuestas y se eligen en la siguiente etapa.

```
1. Identificar → 2. Enriquecer → 3. Calificar → 4. Contactar → 5. Agendar → 6. Notificar
```

| Paso | Qué hace | Cómo interviene Claude | Herramientas posibles |
|---|---|---|---|
| **1. Identificar** | Encontrar empresas que encajan en el ICP y muestran señales de compra | Busca empresas según los criterios del ICP y detecta señales (rondas, vacantes, migraciones) | Apollo, LinkedIn Sales Navigator, Crunchbase, búsqueda web |
| **2. Enriquecer** | Conseguir decisor, email y datos del sitio | Revisa el sitio: stack, Core Web Vitals, presencia en IA | Apollo, Hunter, PageSpeed Insights API, Ahrefs/Semrush |
| **3. Calificar** | Puntuar cada lead según encaje y señales | Asigna una puntuación y descarta los que no encajan | Hoja de cálculo o CRM |
| **4. Contactar** | Enviar mensajes personalizados con un hallazgo concreto de su sitio | Redacta cada email con 1–2 problemas reales detectados | Instantly, Lemlist, Gmail |
| **5. Agendar** | Convertir respuestas positivas en llamadas | Clasifica respuestas y contesta con el enlace de agenda | Calendly, Cal.com |
| **6. Notificar** | Avisarte de citas nuevas y leads calientes | Envía un resumen del lead antes de cada llamada | Email, Slack, WhatsApp, Telegram |

## Métricas a seguir

- Leads identificados por semana
- Tasa de respuesta
- Citas agendadas por semana
- Tasa de cierre (cita → cliente)

## Consideraciones

- **Cumplimiento:** respetar CAN-SPAM y GDPR (opción de baja, datos de contacto profesionales).
- **Entregabilidad:** usar un dominio secundario para el email en frío y calentarlo antes de enviar volumen.
- **Revisión humana:** al principio, aprobar los mensajes antes de enviarlos y automatizar por completo cuando la calidad sea consistente.
