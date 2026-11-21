#!/usr/bin/env python3
"""Importa los datos y las fotos REALES de arimune.es (extraídos con Chrome el 21/11/2026):
- 16 habitaciones con su nombre, m², categoría y fotos (arimune.es/nuestras-habitaciones y /ux_room/*)
- fotos generales de la casa, del comedor, del jardín y de Bakio
Entrada: la carpeta con las fotos ya reducidas (img/) y rooms.json del raspado.
Uso: python3 tools/importar_arimune.py /tmp/ari"""
import json, os, re, shutil, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ari"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PUB = os.path.join(ROOT, "public", "fotos")
IMG = os.path.join(SRC, "img")
files = os.listdir(IMG)
def find(name):
    b = re.sub(r"-\d+x\d+(?=\.)", "", name)
    b = re.sub(r"\.(png|jpe?g)$", "", b, flags=re.I)
    b = re.sub(r"[^A-Za-z0-9._-]", "_", b)
    for f in files:
        if f[8:-4] == b or f.endswith("_" + b + ".jpg"):
            return f
    return None

R = json.load(open(os.path.join(SRC, "rooms.json")))
META = {  # nombre visible, m², categoría (arimune.es/nuestras-habitaciones, visto el 21/11/2026)
 "hondartza": ("Hondartza", 45, "Suite Deluxe Vistas Mar", "solo adultos"),
 "koba": ("Koba", 51, "Suite Deluxe Vistas Mar", "solo adultos"),
 "ama-arantza": ("Ama Arantza", 29, "Junior Suite con Terraza Privada", "solo adultos"),
 "aitxitxe-peli": ("Aitxitxe Peli", 29, "Junior Suite con Terraza Privada", "solo adultos"),
 "amama-kontxita": ("Amama Kontxita", 19, "Deluxe con Terraza Privada", ""),
 "atxulo": ("Atxulo", 21, "Doble Deluxe Vistas Mar", "2 o 3 personas"),
 "burgoa": ("Burgoa", 18, "Doble Deluxe Vistas Mar", "2 personas"),
 "jata": ("Jata", 18, "Doble Deluxe", "2 o 3 personas"),
 "bekoerrota": ("Bekoerrota", 27, "Doble Deluxe Superior", ""),
 "andino": ("Andiño", 17, "Doble Deluxe Vistas Mar", "2 personas"),
 "askada": ("Askada", 18, "Doble Deluxe Vistas Mar", "2 personas"),
 "basigo": ("Basigo", 29, "Doble Deluxe Superior", ""),
 "la-benta": ("La Benta", 18, "Doble Deluxe", "2 personas"),
 "gaztelugatxe": ("Gaztelugatxe", 17, "Doble Deluxe Vistas Mar", "2 personas"),
 "akatz": ("Akatz", 15, "Individual Superior Vistas Mar", "1 persona"),
 "san-pelaio": ("San Pelaio", 20, "Doble Deluxe Vistas Mar", "adaptada (PMR)"),
}
os.makedirs(os.path.join(PUB, "hab"), exist_ok=True)
rooms = []
for slug, (nombre, m2, cat, nota) in META.items():
    lst = R[slug]["imgs"]
    keep = []
    for u in lst:
        n = u.split("/")[-1]
        if re.search(r"logo|Diseno-sin|Travel-Proud|TC-Badge|kit\d|logos-kit", n):
            continue
        if "-510x360" in n:   # miniaturas de «otras habitaciones»
            continue
        f = find(n)
        if f and f not in keep:
            keep.append(f)
    fotos = []
    for i, f in enumerate(keep, 1):
        dst = f"{slug}-{i}.jpg"
        shutil.copy(os.path.join(IMG, f), os.path.join(PUB, "hab", dst))
        fotos.append(f"/fotos/hab/{dst}")
    vistas = "Vistas Mar" in cat
    cap = 1 if cat.startswith("Individual") else (3 if "3" in nota else 2)
    adultos = nota == "solo adultos"
    pax = ", para 2 o 3 personas" if "3" in nota else ""
    if cat.startswith("Suite"): story = f"Suite de {m2} m² frente al mar, con cama King Size. Solo adultos."
    elif cat.startswith("Junior"): story = f"Junior suite de {m2} m² con terraza privada y cama de 160. Solo adultos."
    elif cat.startswith("Deluxe con Terraza"): story = f"Habitación de {m2} m² con terraza privada y cama de 160."
    elif cat.startswith("Individual"): story = f"Individual de {m2} m² con vistas al mar."
    elif nota == "adaptada (PMR)": story = f"Doble de {m2} m² con vistas al mar, adaptada para movilidad reducida."
    elif "Superior" in cat: story = f"Doble superior de {m2} m², de las más amplias de la casa."
    elif vistas: story = f"Doble de {m2} m² con vistas al mar{pax}."
    else: story = f"Doble de {m2} m²{pax}."
    rooms.append({
        "id": slug, "nombre": nombre, "significado": "", "concepto": cat,
        "planta": "baja" if adultos else "superior", "tipo": cat.lower(),
        "capacidad": cap, "m2": m2, "cama": "King Size" if cat.startswith("Suite") else ("160" if "Terraza" in cat else ("individual" if cap == 1 else "doble")),
        "precio": 0, "activa": True, "fotos": fotos,
        "lema": cat, "storytelling": story,
        "vistas_mar": vistas, "solo_adultos": adultos,
    })
data = {"_meta": {
    "descripcion": "Las 16 habitaciones REALES de Arimune (nombre, m² y categoría tal como aparecen en arimune.es/nuestras-habitaciones, vistos el 21/11/2026). Web pública y panel leen de aquí; la web solo muestra las activa:true.",
    "precios": "Sin precio publicado: arimune.es no muestra tarifas (su motor marca 0 por noche). precio:0 = «precio según fechas»; se fija desde el panel cuando el hotel dé sus tarifas.",
    "fotos": "Fotos reales de cada habitación, de arimune.es (public/fotos/hab/)."}, "rooms": rooms}
json.dump(data, open(os.path.join(ROOT, "src", "data", "rooms.json"), "w"), ensure_ascii=False, indent=1)

# Fotos generales (elegidas a mano mirando la hoja de contactos)
G = {
 "hero-terraza-mar": "2022_10_76-ARIMUNE-IMG_6969.jpg", "fachada": "2022_10_95-ARIMUNE-IMG_6989.jpg",
 "entrada": "2022_10_17-ARIMUNE-IMG_6888.jpg", "escalera": "2022_10_15-ARIMUNE-IMG_6886.jpg",
 "comedor-mar": "2022_10_134-ARIMUNE-IMG_7059.jpg", "comedor": "2022_10_190-ARIMUNE-IMG_7166.jpg",
 "salon": "2022_10_08-ARIMUNE-IMG_6872.jpg", "salon-piano": "2022_10_09-ARIMUNE-IMG_6875.jpg", "chimenea": "2022_10_20-ARIMUNE-IMG_6891.jpg",
 "terraza-arboles": "2022_10_48-ARIMUNE-IMG_6928.jpg", "terraza-2": "2022_10_54-ARIMUNE-IMG_6940.jpg", "patio": "2022_10_57-ARIMUNE-IMG_6942.jpg",
 "gaztelugatxe": "2022_10_Hotel-cerca-de-san-juan-de-gaztelugatxe.jpg", "bakio-costa": "2022_10_Descubre-Bakio.jpg",
 "gaztelugatxe-mar": "2022_10_Entorno-de-Bakio.jpg", "playa": "2022_10_Hotel-en-la-playa-de-Bakio-2.jpg", "txakoli": "2022_10_Txakoli-en-Bakio.jpg",
 "bakio-vista": "2023_01_Hotel-arimune-familiar.jpg", "fachada-2": "2022_10_Sin-titulo-510-_C3_97-335-px.jpg",
 "playa-ventana": "2022_11_Hotel-Arimune.jpg", "habitacion-mar": "2022_11_263-ARIMUNE-IMG_7267-scaled.jpg",
 "habitacion": "2022_11_239-ARIMUNE-IMG_7229-scaled.jpg", "bano": "2022_11_241-ARIMUNE-IMG_7237-scaled.jpg",
 "amenities-re": "elementor_thumbs_Hotel-ecologico-q19xtyl3x5fq1khwkc5ll991l7odzimtn5zot1b3w0.jpg",
 "jardin-mar": "elementor_thumbs_Diseno-sin-titulo-2023-05-29T105106.174-q764td7wy6d9dgpetkmpklsekow28a3ffnhky90lf4.jpg",
 "pintxos": "2026_09_Fotos-Web.jpg", "etikoa": "2021_06_Diseno-sin-titulo-13.jpg",
}
shutil.rmtree(os.path.join(PUB, "casa"), ignore_errors=True)
os.makedirs(os.path.join(PUB, "casa"), exist_ok=True)
for k, f in G.items():
    shutil.copy(os.path.join(IMG, f), os.path.join(PUB, "casa", k + ".jpg"))
print(len(rooms), "habitaciones;", sum(len(r["fotos"]) for r in rooms), "fotos de habitación;", len(G), "generales")
for r in rooms: print(" ", r["nombre"], len(r["fotos"]), r["storytelling"])
