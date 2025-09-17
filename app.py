import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rectpack import newPacker
import re

# Haagise mõõdud (meetrites)
TRAILER_LENGTH = 13.6
TRAILER_WIDTH = 2.45

# Standardaluste mõõdud (meetrites)
STD_SIZES = {
    "eur": (1.2, 0.8),
    "fin": (1.2, 1.0),
}

# --- Funktsioon: teksti parsimine ---
def parse_input(text):
    items = []
    for block in text.splitlines():
        if not block.strip():
            continue

        # Leia mahalaadimise järjekord (#N)
        order_match = re.search(r"#(\d+)", block)
        unload_order = int(order_match.group(1)) if order_match else 999

        # Leia kliendi nimi (esimene sõna)
        client = block.strip().split()[0]

        # Leia kõik mõõdud
        dims = re.findall(r"(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)", block)
        for (l, w, h) in dims:
            items.append({
                "client": client,
                "order": unload_order,
                "length": int(l)/100,
                "width": int(w)/100,
                "height": int(h)/100,
            })

        # Leia EUR/FIN märge
        if "eur" in block.lower():
            items.append({
                "client": client,
                "order": unload_order,
                "length": STD_SIZES["eur"][0],
                "width": STD_SIZES["eur"][1],
                "height": 1.5,  # suvaline kõrgus
            })
        if "fin" in block.lower():
            items.append({
                "client": client,
                "order": unload_order,
                "length": STD_SIZES["fin"][0],
                "width": STD_SIZES["fin"][1],
                "height": 1.5,
            })

        # Leia LDM (lineaarmeetrit)
        ldm_match = re.search(r"([\d.,]+)\s*ldm", block.lower())
        if ldm_match:
            ldm = float(ldm_match.group(1).replace(",", "."))
            items.append({
                "client": client,
                "order": unload_order,
                "length": ldm,
                "width": TRAILER_WIDTH,
                "height": 1.5,
            })

    return items

# --- Funktsioon: paigutus ---
def pack_items(items):
    # Sorteeri kliendid mahalaadimise järjekorra järgi
    items = sorted(items, key=lambda x: x["order"])

    packer = newPacker(rotation=True)

    for i, it in enumerate(items):
        packer.add_rect(it["length"], it["width"], i)

    packer.add_bin(TRAILER_LENGTH, TRAILER_WIDTH)
    packer.pack()

    placed, not_placed = [], []

    for rect in packer.rect_list():
        b, x, y, w, h, rid = rect
        it = items[rid]
        placed.append({
            **it,
            "x": x,
            "y": y,
            "length": w,
            "width": h,
        })

    placed_id_
