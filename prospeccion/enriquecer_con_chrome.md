# Buscar y enriquecer leads con Claude in Chrome

El DENUE da la lista base gratis (nombre, teléfono, tamaño, dirección), pero no trae **calificación, reseñas ni posición en Google Maps**. Esos datos los obtenemos con la extensión Claude in Chrome, desde tu navegador.

Reglas para no tener bloqueos de Google:
- Lotes pequeños: 10–20 negocios por sesión.
- Deja que la extensión navegue a ritmo normal y no la pongas a correr en paralelo en varias pestañas.
- Si Google muestra un captcha, resuélvelo y baja el ritmo.

## Prompt A: buscar leads directo en Google Maps

Pega esto en Claude in Chrome (cambia la búsqueda y la zona):

```
Abre Google Maps y busca "implantes dentales Guadalajara". Recorre los primeros 20 resultados
del listado (hacia abajo en el panel izquierdo). Para cada negocio abre su ficha y anota:

- posicion (1, 2, 3… según el orden del listado)
- nombre
- calificacion (estrellas)
- num_resenas
- fecha_ultima_resena (aproximada, ej. "hace 2 semanas")
- responde_resenas (si/no: ¿el dueño contesta reseñas?)
- telefono
- sitio_web (URL o "no tiene")
- horario_completo (si/no)
- fotos (aprox. cuántas)
- categoria (la que muestra Google)

No hagas clic en anuncios. Al final dame TODO en una sola tabla CSV con esas columnas,
separada por comas, sin texto adicional.
```

Búsquedas sugeridas para dentistas en Guadalajara (una por sesión):
- implantes dentales Guadalajara
- ortodoncista Zapopan
- dentista Providencia Guadalajara
- clínica dental Chapalita
- dentist Guadalajara (resultados en inglés → clínicas de turismo dental)

## Prompt B: enriquecer los leads del DENUE

Abre el CSV de `salida/leads_dentistas_AAAA-MM-DD.csv`, copia 10–20 filas (nombre y municipio) y pega:

```
Para cada negocio de esta lista, búscalo en Google Maps por nombre y municipio.
Si lo encuentras, anota: nombre, calificacion, num_resenas, fecha_ultima_resena,
responde_resenas (si/no), sitio_web, y si aparece en el top 3 del mapa al buscar
"dentista <municipio>". Si no lo encuentras, pon "no_encontrado".
Devuélveme todo en una tabla CSV, sin texto adicional.

<pega aquí la lista>
```

## Prompt C: conseguir correos que faltan

El DENUE trae correo de cerca de un tercio de los negocios. Para los demás (o para confirmar un correo viejo):

```
Para cada negocio de esta lista, busca su correo electrónico en este orden y detente
en cuanto lo encuentres:
1. Su sitio web (página de inicio, pie de página y página de "Contacto").
2. Su página de Facebook, sección "Información" / "Detalles".
3. Su perfil de Instagram (biografía o botón "Correo").
4. Directorios como Doctoralia o Top Doctors (dentistas) o Abogados.com.mx (abogados).
Anota: nombre, email, fuente (sitio/facebook/instagram/directorio) y facebook_url.
Si no encuentras correo, pon "sin_email". Devuélveme todo en una tabla CSV, sin texto adicional.

<pega aquí la lista con nombre y municipio>
```

## Qué hacer con el resultado

Pega la tabla aquí, en Claude Code, y yo:
1. La combino con el CSV del DENUE.
2. Recalculo la puntuación con estas señales: más de 4.3 estrellas y más de 30 reseñas = negocio activo; no responde reseñas o está fuera del top 3 = oportunidad de SEO.
3. Redacto el mensaje de WhatsApp de cada lead con sus hallazgos reales.
