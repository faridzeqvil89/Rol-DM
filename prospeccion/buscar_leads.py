#!/usr/bin/env python3
"""Busca y puntúa leads de un nicho en una zona usando el DENUE del INEGI.

Fuente gratuita y oficial: https://www.inegi.org.mx/app/descarga/?ti=6
No requiere API key. Solo usa la librería estándar de Python.

Ejemplos:
    python3 prospeccion/buscar_leads.py --nicho dentistas --limite 40
    python3 prospeccion/buscar_leads.py --nicho abogados --limite 40 --sin-revisar-sitios
"""

import argparse
import csv
import datetime
import glob
import io
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_DATOS = os.path.join(RAIZ, "datos")
DIR_SALIDA = os.path.join(RAIZ, "salida")
URL_DENUE = "https://www.inegi.org.mx/contenidos/masiva/denue/denue_00_{sector}_csv.zip"

# Códigos SCIAN por nicho. "palabras_ticket_alto" suben la puntuación si aparecen en el nombre.
NICHOS = {
    "dentistas": {
        "sector": "62",
        "codigos": {"621211"},  # Consultorios dentales del sector privado
        "palabras_ticket_alto": [
            "implant", "ortodon", "rehabilita", "estetic", "especialidad",
            "maxilo", "endodon", "periodon", "smile", "dental center", "clinica",
        ],
    },
    "abogados": {
        "sector": "54",
        "codigos": {"541110"},  # Bufetes jurídicos
        "palabras_ticket_alto": [
            "laboral", "familiar", "penal", "corporativ", "fiscal",
            "migratori", "litigio", "asociados", "abogados",
        ],
    },
}

# Zona metropolitana de Guadalajara (Jalisco = 14).
MUNICIPIOS = {
    "guadalajara": "039",
    "zapopan": "120",
    "tlaquepaque": "098",
    "tonala": "101",
    "tlajomulco": "097",
}

PUNTOS_TAMANO = {"6 a 10 personas": 2, "11 a 30 personas": 3, "31 a 50 personas": 3}


def descargar_sector(sector):
    """Descarga y cachea el CSV del sector en datos/. Devuelve la ruta del CSV."""
    destino = os.path.join(DIR_DATOS, f"denue_{sector}")
    existentes = glob.glob(os.path.join(destino, "conjunto_de_datos", "*.csv"))
    if existentes:
        return existentes[0]
    os.makedirs(destino, exist_ok=True)
    url = URL_DENUE.format(sector=sector)
    print(f"Descargando DENUE sector {sector}...", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=300) as resp:
        contenido = resp.read()
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        z.extractall(destino)
    return glob.glob(os.path.join(destino, "conjunto_de_datos", "*.csv"))[0]


def normalizar_telefono(tel):
    digitos = re.sub(r"\D", "", tel or "")
    return digitos[-10:] if len(digitos) >= 10 else ""


def normalizar_url(www):
    www = (www or "").strip().lower()
    if not www or "." not in www:
        return ""
    return www if www.startswith("http") else "http://" + www


def revisar_sitio(url):
    """Revisión rápida y gratuita del sitio. Devuelve (datos, hallazgos)."""
    datos = {"sitio_estado": "", "sitio_https": "", "sitio_segundos": "", "sitio_wordpress": ""}
    hallazgos = []
    peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; revision-seo)"})
    inicio = time.time()
    try:
        with urllib.request.urlopen(peticion, timeout=15) as resp:
            html = resp.read(500_000).decode("utf-8", errors="ignore").lower()
            final = resp.geturl()
            estado = resp.status
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
        razon = str(getattr(e, "reason", e))
        if "Name or service not known" in razon or "nodename nor servname" in razon:
            datos["sitio_estado"] = "dominio_no_existe"
            hallazgos.append("El dominio no existe o expiró")
        else:
            # Puede ser una caída real o un bloqueo a revisiones automáticas: confirmar a mano.
            datos["sitio_estado"] = "no_cargo"
            hallazgos.append(f"El sitio no cargó en la revisión automática ({razon[:40]}), verificar a mano")
        return datos, hallazgos

    segundos = round(time.time() - inicio, 1)
    datos.update({
        "sitio_estado": str(estado),
        "sitio_https": "si" if final.startswith("https") else "no",
        "sitio_segundos": str(segundos),
        "sitio_wordpress": "si" if "wp-content" in html else "no",
    })
    if not final.startswith("https"):
        hallazgos.append("Sin HTTPS (el navegador lo marca como no seguro)")
    if segundos > 3:
        hallazgos.append(f"Tarda {segundos}s en responder")
    if 'name="viewport"' not in html and "name=viewport" not in html:
        hallazgos.append("No está adaptado a celular")
    if "<title" not in html or re.search(r"<title>\s*</title>", html):
        hallazgos.append("Sin título SEO")
    if 'name="description"' not in html:
        hallazgos.append("Sin meta descripción")
    if "wa.me" not in html and "whatsapp" not in html:
        hallazgos.append("Sin botón de WhatsApp")
    if "application/ld+json" not in html:
        hallazgos.append("Sin datos estructurados (schema)")
    return datos, hallazgos


def puntuar(fila, nicho):
    puntos = 0
    if fila["telefono"]:
        puntos += 3
    if fila["email"]:
        puntos += 1
    puntos += PUNTOS_TAMANO.get(fila["personal"], 0)
    nombre = (fila["nombre"] + " " + fila["razon_social"]).lower()
    if any(p in nombre for p in NICHOS[nicho]["palabras_ticket_alto"]):
        puntos += 2
    # Sin sitio = oportunidad de venderle uno; sitio con problemas = oportunidad de SEO.
    if not fila["sitio"] or fila["hallazgos"]:
        puntos += 2
    return puntos


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nicho", choices=NICHOS, required=True)
    parser.add_argument("--municipios", default="guadalajara,zapopan",
                        help="Separados por coma: " + ",".join(MUNICIPIOS))
    parser.add_argument("--limite", type=int, default=40, help="Cuántos leads exportar (los de mayor puntuación)")
    parser.add_argument("--sin-revisar-sitios", action="store_true", help="No visitar los sitios web")
    args = parser.parse_args()

    config = NICHOS[args.nicho]
    claves_mun = {MUNICIPIOS[m.strip()] for m in args.municipios.split(",")}
    ruta_csv = descargar_sector(config["sector"])

    leads = []
    with open(ruta_csv, encoding="latin1") as f:
        for fila in csv.DictReader(f):
            if fila["cve_ent"] != "14" or fila["cve_mun"] not in claves_mun:
                continue
            if fila["codigo_act"] not in config["codigos"]:
                continue
            telefono = normalizar_telefono(fila["telefono"])
            if not telefono:
                continue  # Requisito del ICP: fácil de contactar
            direccion = " ".join(x for x in [fila["tipo_vial"], fila["nom_vial"], fila["numero_ext"]] if x)
            leads.append({
                "id_denue": fila["id"],
                "nombre": fila["nom_estab"].strip(),
                "razon_social": fila["raz_social"].strip(),
                "personal": fila["per_ocu"],
                "municipio": fila["municipio"],
                "colonia": fila["nomb_asent"],
                "direccion": direccion,
                "telefono": telefono,
                "whatsapp": f"https://wa.me/52{telefono}",
                "email": fila["correoelec"].strip().lower(),
                "sitio": normalizar_url(fila["www"]),
                "maps": f"https://www.google.com/maps/search/?api=1&query={fila['latitud']},{fila['longitud']}",
                "hallazgos": [],
            })

    print(f"{len(leads)} negocios con teléfono en la zona.", file=sys.stderr)

    if not args.sin_revisar_sitios:
        con_sitio = [l for l in leads if l["sitio"]]
        print(f"Revisando {len(con_sitio)} sitios web...", file=sys.stderr)
        for lead in con_sitio:
            datos, hallazgos = revisar_sitio(lead["sitio"])
            lead.update(datos)
            lead["hallazgos"] = hallazgos

    for lead in leads:
        if not lead["sitio"]:
            lead["hallazgos"] = ["Sin sitio web registrado"]
        lead["puntos"] = puntuar(lead, args.nicho)

    leads.sort(key=lambda l: l["puntos"], reverse=True)
    seleccion = leads[: args.limite]

    os.makedirs(DIR_SALIDA, exist_ok=True)
    fecha = datetime.date.today().isoformat()
    salida = os.path.join(DIR_SALIDA, f"leads_{args.nicho}_{fecha}.csv")
    columnas = [
        "puntos", "nombre", "razon_social", "personal", "municipio", "colonia", "direccion",
        "telefono", "whatsapp", "email", "sitio", "sitio_estado", "sitio_https", "sitio_segundos",
        "sitio_wordpress", "hallazgos", "maps", "id_denue",
    ]
    with open(salida, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        escritor.writeheader()
        for lead in seleccion:
            escritor.writerow({**lead, "hallazgos": "; ".join(lead["hallazgos"])})

    print(f"{len(seleccion)} leads guardados en {os.path.relpath(salida, RAIZ)}", file=sys.stderr)


if __name__ == "__main__":
    main()
