# Prospección

## 1. Lista base desde el DENUE (gratis, sin API key)

```bash
python3 prospeccion/buscar_leads.py --nicho dentistas --limite 40
python3 prospeccion/buscar_leads.py --nicho abogados --limite 40
```

- Fuente: [DENUE del INEGI](https://www.inegi.org.mx/app/descarga/?ti=6), el directorio oficial de negocios de México. La primera vez descarga el sector a `datos/` (ignorado por git).
- Zona por defecto: Guadalajara y Zapopan. Se cambia con `--municipios guadalajara,zapopan,tlaquepaque,tonala,tlajomulco`.
- Solo incluye negocios **con teléfono** y revisa en automático el sitio web de los que lo tienen registrado.
- Resultado: `salida/leads_<nicho>_<fecha>.csv`, ordenado por puntuación, con enlace de WhatsApp, enlace a Maps y hallazgos.

### Puntuación

| Señal | Puntos |
|---|---|
| Tiene teléfono | +3 |
| Tiene email | +1 |
| 6–10 empleados / 11 o más | +2 / +3 |
| El nombre indica ticket alto (implantes, ortodoncia, laboral…) | +2 |
| Sin sitio, o sitio con problemas | +2 |

### Limitaciones

- El DENUE no tiene calificación, reseñas ni posición en Maps → ver el paso 2.
- Pocos negocios registran su sitio web en el DENUE: que diga "sin sitio" no garantiza que no tengan uno. Hay que confirmarlo en Maps.
- "No cargó en la revisión automática" puede ser un bloqueo a bots: verificar a mano antes de mencionarlo en un mensaje.

## 2. Enriquecer con Google Maps

Ver [enriquecer_con_chrome.md](enriquecer_con_chrome.md): prompts para Claude in Chrome.
