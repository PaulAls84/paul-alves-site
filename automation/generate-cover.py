#!/usr/bin/env python3
"""Génère une couverture d'article (1200x800) dans la charte Paul Alves.

Usage :
    python3 automation/generate-cover.py "<titre>" "<catégorie>" "<chemin_sortie.jpg>"

Comportement :
- Si la variable d'environnement OPENAI_API_KEY est définie, une image de fond
  est générée par IA (palette navy/or, sans texte), puis on superpose un voile
  navy + un cadre or + la catégorie + le titre pour garder la cohérence de marque.
- Sinon (ou en cas d'erreur API), on retombe sur une couverture pleine charte
  générée localement avec Pillow. La routine ne doit JAMAIS échouer faute d'image.

Dépendances : Pillow (déjà présent). Aucune dépendance réseau tierce (urllib stdlib).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import textwrap
import urllib.request
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 800
NAVY = (10, 29, 54)       # #0a1d36
NAVY_DARK = (6, 18, 34)
GOLD = (212, 164, 74)     # #d4a44a
CREAM = (250, 247, 242)   # #faf7f2
MUTED = (180, 190, 205)

SERIF_PATH = "/System/Library/Fonts/Supplemental/Didot.ttc"
SANS_PATH = "/System/Library/Fonts/Avenir Next.ttc"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def ai_background(title: str) -> Image.Image | None:
    """Tente de générer un fond via l'API images d'OpenAI. None si indisponible."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    prompt = (
        f"Editorial blog cover background illustrating the concept of: {title}. "
        "Elegant, professional, minimalist. Deep navy blue and warm gold color "
        "palette only. Abstract, no text, no letters, no words, no logos. "
        "Soft lighting, premium feel, plenty of empty space on the left."
    )
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1536x1024",
        "n": 1,
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        b64 = data["data"][0]["b64_json"]
        img = Image.open(BytesIO(base64.b64decode(b64))).convert("RGB")
        # Recadrage 3:2 -> 1200x800
        img = img.resize((1200, 800)) if img.size != (W, H) else img
        return img
    except Exception as e:  # réseau, quota, format inattendu...
        print(f"[cover] génération IA indisponible ({e}) -> fallback charte", file=sys.stderr)
        return None


def base_canvas(bg: Image.Image | None) -> Image.Image:
    if bg is not None:
        img = bg.copy()
        # Voile navy dégradé (gauche opaque -> droite plus léger) pour lisibilité du titre
        scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(scrim)
        for x in range(W):
            a = int(235 - (x / W) * 150)  # 235 à gauche -> ~85 à droite
            sd.line([(x, 0), (x, H)], fill=(NAVY[0], NAVY[1], NAVY[2], max(60, a)))
        img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
        return img
    # Pas d'IA : dégradé navy plein
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(NAVY[0] + (NAVY_DARK[0] - NAVY[0]) * t),
            int(NAVY[1] + (NAVY_DARK[1] - NAVY[1]) * t),
            int(NAVY[2] + (NAVY_DARK[2] - NAVY[2]) * t),
        ))
    return img


def render(title: str, category: str, out: str) -> None:
    img = base_canvas(ai_background(title))
    d = ImageDraw.Draw(img)

    # Cadre or
    m = 48
    d.rectangle([m, m, W - m, H - m], outline=GOLD, width=2)

    serif = _font(SERIF_PATH, 76)
    sans = _font(SANS_PATH, 26)
    sans_sm = _font(SANS_PATH, 22)

    # Label catégorie (lettres espacées) + trait
    label = " ".join(category.upper())
    d.text((90, 130), label, font=sans, fill=GOLD)
    lw = d.textlength(label, font=sans)
    d.line([(92, 175), (92 + lw, 175)], fill=GOLD, width=2)

    # Titre serif, wrap
    y = 250
    for line in textwrap.wrap(title, width=20)[:4]:
        d.text((90, y), line, font=serif, fill=CREAM)
        y += 92

    # Signature
    d.text((90, H - 130), "paul-alves.fr", font=sans_sm, fill=GOLD)
    d.text((90, H - 95), "Développeur Web & Consultant SEO — Soissons",
           font=sans_sm, fill=MUTED)

    # JPG : sert d'og:image / donnée structurée (aperçus sociaux fiables en JPG).
    img.save(out, "JPEG", quality=88)
    # WebP : version légère utilisée pour l'AFFICHAGE sur le site (helper webpCover).
    import os as _os
    webp_out = _os.path.splitext(out)[0] + ".webp"
    img.save(webp_out, "WEBP", quality=80)
    print(f"[cover] OK {out} + {webp_out} ({W}x{H})")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: generate-cover.py "<titre>" "<catégorie>" "<sortie.jpg>"',
              file=sys.stderr)
        sys.exit(1)
    render(sys.argv[1], sys.argv[2], sys.argv[3])
