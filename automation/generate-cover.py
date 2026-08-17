#!/usr/bin/env python3
"""Génère une couverture d'article (1200x800) dans la charte Paul Alves.

Usage :
    python3 automation/generate-cover.py "<titre>" "<catégorie>" "<chemin_sortie.jpg>" [config.json]

Comportement (routine auto) :
1. **Vignette « YouTube-style »** (pipeline principal) : une config est déduite
   automatiquement du titre et de la catégorie — badge, titre découpé en
   3 lignes percutantes, sous-titre, étapes et visuel thématique (serveur,
   bouclier, PageSpeed, SERP, match « X vs Y »…) choisi par mots-clés.
   Rendu HTML/CSS via Chrome/Chromium headless (cf. cover_template.py).
   Un fichier `config.json` optionnel permet d'affiner : toute clé fournie
   (`badge`, `lines` [[texte, "cream"|"gold", taille]…], `sub`, `steps`,
   `notif`, `preset`, `visual`) remplace la valeur déduite.
2. **Repli charte** : si Chrome est introuvable (environnement cloud minimal)
   ou si le rendu échoue, on retombe sur la couverture sobre générée avec
   Pillow (fond navy + titre serif, optionnellement fond IA si
   OPENAI_API_KEY est défini). La routine ne doit JAMAIS échouer faute d'image.

Dans tous les cas, deux fichiers sont produits : <slug>.jpg (og:image) et
<slug>.webp (affichage site).
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import textwrap
import urllib.request
from datetime import date
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cover_template import PRESETS, lines, make_vs_visual, render_cover, steps  # noqa: E402

W, H = 1200, 800
NAVY = (10, 29, 54)       # #0a1d36
NAVY_DARK = (6, 18, 34)
GOLD = (212, 164, 74)     # #d4a44a
CREAM = (250, 247, 242)   # #faf7f2
MUTED = (180, 190, 205)

# Plusieurs candidats par famille : macOS d'abord (poste de Paul), puis les
# polices Linux courantes pour que la routine cloud produise la même couverture.
SERIF_PATH = [
    "/System/Library/Fonts/Supplemental/Didot.ttc",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
]
SANS_PATH = [
    "/System/Library/Fonts/Avenir Next.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]


# ---------------------------------------------------------------------------
# Pipeline principal : vignette YouTube-style auto-composée
# ---------------------------------------------------------------------------

# Ordre important : le premier motif qui matche le titre gagne.
PRESET_KEYWORDS = [
    (r"pirat", "shield"),
    (r"sécuris|securis", "shield"),
    (r"sauvegard", "backup"),
    (r"vitesse|rapide|accélér|acceler|performance", "speed"),
    # Avant `plugin` : un plugin de cache relève du visuel « vitesse », pas du
    # visuel générique « plugins » (cas WP Rocket, LiteSpeed, W3 Total Cache…).
    (r"cache|wp rocket|litespeed|w3 total|web vitals|lazy", "speed"),
    (r"prix|coûte|coute|budget|tarif", "budget"),
    (r"migr", "migrate"),
    (r"refonte", "revamp"),
    (r"maintenance|entretenir", "dashboard"),
    (r"boutique|woocommerce|e-commerce|commerce", "shop"),
    (r"plugin|extension", "plugins"),
    (r"thème|theme", "themes"),
    (r"hébergeur|hebergeur|hébergement|hebergement|héberger|heberger", "server"),
    (r"seo|référenc|referenc|google", "serp"),
    (r"rgpd|cookie|mentions légales", "shield"),
]

BADGE_KEYWORDS = [
    (r"pirat", "URGENCE"),
    (r"comparatif|meilleur|classement", "COMPARATIF"),
    (r"\bavis\b|\btest\b|vaut-il", "AVIS TESTÉ"),
    (r"sécuris|securis", "SÉCURITÉ"),
    (r"vitesse|accélér|acceler|performance", "PERFORMANCE"),
    (r"prix|coûte|coute|budget|tarif", "BUDGET"),
    (r"guide", "GUIDE COMPLET"),
]

BADGE_BY_CATEGORY = {
    "WordPress": "LE GUIDE",
    "SEO": "SEO",
    "Plugins": "SÉLECTION",
    "Maintenance": "MAINTENANCE",
}

# Couleurs de marque pour les colonnes du match « X vs Y ».
VS_COLORS = {
    "wordpress": "#0e2444",
    "gutenberg": "#0073aa",
    "elementor": "#e2498a",
    "divi": "#7c3aed",
    "wix": "#0f9bd7",
    "shopify": "#5e8e3e",
    "yoast": "#a4286a",
    "rank math": "#6d28d9",
    "squarespace": "#1c1c1c",
}


def _clean(text: str) -> str:
    """Retire les tags [2026] et les espaces/ponctuations superflus."""
    text = re.sub(r"\[[^\]]*\]", "", text)
    return re.sub(r"\s+", " ", text).strip(" \t:;—–-|")


def _line_size(text: str, gold: bool) -> int:
    """Taille de police pour que la ligne (Arial Black ~0.80×taille/char) tienne."""
    cap = 118 if gold else 84
    return max(42, min(cap, int(620 / (0.80 * max(1, len(text))))))


def _pick_gold(ls: list[str]) -> int:
    """Ligne à passer en or : la plus « accroche », jamais un simple WORDPRESS."""
    if len(ls) == 1:
        return 0
    mid = len(ls) // 2 if len(ls) == 3 else 1
    if ls[mid].strip("?! ").upper() != "WORDPRESS":
        return mid
    for i in range(len(ls) - 1, -1, -1):
        if ls[i].strip("?! ").upper() != "WORDPRESS":
            return i
    return mid


def auto_config(title: str, category: str) -> dict:
    """Déduit une config de vignette complète depuis le titre et la catégorie."""
    low = title.lower()
    year_m = re.search(r"\[(\d{4})\]", title)
    year = year_m.group(1) if year_m else str(date.today().year)

    # Découpe titre principal / traîne (après « : »)
    main, _, tail = title.partition(":")
    main, tail = _clean(main), _clean(tail)

    # Titre trop long : bascule la fin dans le sous-titre
    moved = ""
    if len(main) > 30:
        m = re.search(r"\s(sans|pour|avec|et)\s", main)
        if m:
            moved = main[m.start() + 1:]
            main = main[:m.start()]

    # Mode « X vs Y » ?
    vs_m = re.fullmatch(r"(.{2,16})\s+ou\s+(.{2,16})", main, flags=re.IGNORECASE)

    # Préréglage visuel par mots-clés
    preset_key = "site"
    if vs_m:
        preset_key = "vs"
    else:
        for pat, key in PRESET_KEYWORDS:
            if re.search(pat, low):
                preset_key = key
                break
    preset = PRESETS[preset_key]

    # Lignes du titre
    if vs_m:
        a, b = vs_m.group(1).strip(), vs_m.group(2).strip()
        title_lines = [
            (a.upper(), "cream", min(70, int(620 / (0.80 * len(a))))),
            ("VS", "gold", 118),
            (b.upper(), "cream", min(70, int(620 / (0.80 * len(b))))),
        ]
        visual = make_vs_visual(
            a, b,
            VS_COLORS.get(a.lower(), "#0e2444"),
            VS_COLORS.get(b.lower(), "#0f9bd7"),
        )
    else:
        wrapped = [main.upper()]
        for width in range(10, 25):
            wrapped = textwrap.wrap(main.upper(), width) or wrapped
            if len(wrapped) <= 3:
                break
        gold_i = _pick_gold(wrapped)
        title_lines = [
            (t, "gold" if i == gold_i else "cream", _line_size(t, i == gold_i))
            for i, t in enumerate(wrapped)
        ]
        visual = preset["visual"]

    # Badge
    badge_label = "LE MATCH" if vs_m else None
    if badge_label is None:
        for pat, label in BADGE_KEYWORDS:
            if re.search(pat, low):
                badge_label = label
                break
    if badge_label is None:
        badge_label = BADGE_BY_CATEGORY.get(category, category.upper() or "LE GUIDE")

    # Sous-titre : traîne du titre si exploitable, sinon celui du preset
    sub = moved or tail
    sub = sub[:1].lower() + sub[1:] if sub else ""
    if not 8 <= len(sub) <= 44:
        sub = preset["sub"]

    return {
        "badge": f"{badge_label} · {year}",
        "title": lines(*title_lines),
        "sub": sub,
        "steps": steps(*preset["steps"]),
        "notif": tuple(preset["notif"]),
        "visual": visual,
    }


def apply_overrides(cfg: dict, path: str) -> dict:
    """Applique un config.json optionnel (clés : badge, lines, sub, steps, notif, preset, visual)."""
    with open(path) as f:
        over = json.load(f)
    if "preset" in over:
        p = PRESETS[over["preset"]]
        cfg.update({
            "sub": p["sub"],
            "steps": steps(*p["steps"]),
            "notif": tuple(p["notif"]),
            "visual": p["visual"],
        })
    if "lines" in over:
        cfg["title"] = lines(*[tuple(l) for l in over["lines"]])
    if "steps" in over:
        cfg["steps"] = steps(*over["steps"])
    if "notif" in over:
        cfg["notif"] = tuple(over["notif"])
    for key in ("badge", "sub", "visual"):
        if key in over:
            cfg[key] = over[key]
    return cfg


# ---------------------------------------------------------------------------
# Repli : couverture charte Pillow (ex-pipeline, conservé tel quel)
# ---------------------------------------------------------------------------

def _font(paths, size):
    """Première police disponible parmi `paths` (str ou liste), à la taille voulue."""
    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    try:  # Pillow >= 10.1 sait redimensionner la police par défaut
        return ImageFont.load_default(size)
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


def render_charte(title: str, category: str, out: str) -> None:
    """Couverture sobre pleine charte (repli sans Chrome)."""
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

    img.save(out, "JPEG", quality=88)
    img.save(os.path.splitext(out)[0] + ".webp", "WEBP", quality=80)


def render(title: str, category: str, out: str, config_path: str | None = None) -> None:
    try:
        cfg = auto_config(title, category)
        if config_path:
            cfg = apply_overrides(cfg, config_path)
        if render_cover(cfg, out):
            print(f"[cover] OK vignette {out} + .webp ({W}x{H})")
            return
        print("[cover] Chrome indisponible -> couverture charte", file=sys.stderr)
    except Exception as e:  # le pipeline vignette ne doit jamais bloquer la routine
        print(f"[cover] pipeline vignette en échec ({e}) -> couverture charte", file=sys.stderr)
    render_charte(title, category, out)
    print(f"[cover] OK charte {out} + .webp ({W}x{H})")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: generate-cover.py "<titre>" "<catégorie>" "<sortie.jpg>" [config.json]',
              file=sys.stderr)
        sys.exit(1)
    render(sys.argv[1], sys.argv[2], sys.argv[3],
           sys.argv[4] if len(sys.argv) > 4 else None)
