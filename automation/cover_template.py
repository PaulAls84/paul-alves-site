"""Bibliothèque partagée des vignettes « YouTube-style » du blog.

Contient le template HTML/CSS commun (badge, titre 3 lignes, sous-titre,
étapes, notification + flèche), les visuels thématiques réutilisables et le
rendu via Chrome headless (PNG → JPG og:image + WebP affichage).

Utilisée par :
- generate-cover.py      (routine auto : config déduite du titre/catégorie)
- generate-thumbnails.py (configs manuelles des articles existants)
"""
from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

W, H = 1200, 800

# Polices : macOS d'abord (poste de Paul), puis équivalents Linux (routine
# cloud) — DejaVu/Liberation en gras 900 restent percutants pour le titre.
TEMPLATE = """<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1200px; height: 800px; overflow: hidden; }
  body {
    position: relative;
    font-family: "Avenir Next", "Helvetica Neue", "DejaVu Sans", "Liberation Sans", sans-serif;
    background:
      radial-gradient(1000px 700px at 88% 12%, rgba(212,164,74,.28), transparent 60%),
      radial-gradient(900px 900px at -10% 110%, rgba(29,78,137,.55), transparent 60%),
      linear-gradient(135deg, #0e2444 0%, #0a1d36 45%, #061222 100%);
    color: #faf7f2;
  }
  .dots {
    position: absolute; inset: 0;
    background-image: radial-gradient(rgba(250,247,242,.10) 2px, transparent 2px);
    background-size: 34px 34px;
    -webkit-mask-image: linear-gradient(115deg, rgba(0,0,0,.9), transparent 55%);
  }
  .beam {
    position: absolute; top: -220px; right: -140px; width: 560px; height: 1300px;
    background: linear-gradient(90deg, transparent, rgba(212,164,74,.10), transparent);
    transform: rotate(24deg);
  }
  .left {
    position: absolute; left: 64px; top: 0; height: 100%; width: 620px; z-index: 3;
    display: flex; flex-direction: column; justify-content: center; align-items: flex-start;
  }
  .badge {
    display: inline-block;
    background: #d4a44a; color: #0a1d36;
    font-weight: 700; font-size: 26px; letter-spacing: 2px;
    padding: 10px 22px; border-radius: 999px;
    box-shadow: 0 8px 24px rgba(212,164,74,.35);
  }
  h1 {
    margin-top: 34px;
    font-family: "Arial Black", "Avenir Next", "DejaVu Sans", "Liberation Sans", sans-serif;
    font-weight: 900;
    line-height: .98; letter-spacing: -1px;
    text-shadow: 0 10px 30px rgba(0,0,0,.55);
  }
  h1 .ln { display: block; white-space: nowrap; }
  h1 .cream { color: #faf7f2; }
  h1 .gold { color: #d4a44a; }
  .sub { margin-top: 26px; font-size: 34px; font-weight: 600; color: #cfd9e6; }
  .sub b.gold { color: #d4a44a; font-weight: 700; }
  .sub b.purple { color: #b48ce0; font-weight: 700; }
  .sub b.green { color: #4ade80; font-weight: 700; }
  .steps {
    margin-top: 30px; display: flex; align-items: center; gap: 14px;
    font-weight: 700; font-size: 25px; color: #0a1d36;
  }
  .step { background: #faf7f2; border-radius: 12px; padding: 10px 18px; box-shadow: 0 6px 18px rgba(0,0,0,.35); white-space: nowrap; }
  .chev { color: #d4a44a; font-size: 30px; }

  /* ---- Panneau blanc générique (droite) ---- */
  .panel {
    position: absolute; right: 42px; top: 160px; width: 470px; z-index: 2;
    background: #fff; border-radius: 18px; padding: 22px 24px;
    transform: rotate(4deg);
    box-shadow: 0 40px 80px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.08);
    color: #1c2733;
  }
  .panel h3 { font-size: 21px; font-weight: 700; margin-bottom: 14px; display: flex; align-items: center; gap: 10px; }
  .row {
    display: flex; align-items: center; gap: 12px; padding: 11px 14px;
    border: 1px solid #e4e8ee; border-radius: 12px; margin-bottom: 10px;
    font-weight: 600; font-size: 17px; color: #33404d;
  }
  .row:last-child { margin-bottom: 0; }
  .row .ico { font-size: 24px; }
  .row .grow { flex: 1; }
  .pill { font-weight: 700; font-size: 14px; padding: 4px 12px; border-radius: 999px; white-space: nowrap; }
  .pill.green { background: #e7f6ee; color: #1f7a4d; }
  .pill.gold { background: #f9efdb; color: #9a6d1c; }
  .pill.red { background: #fdeaea; color: #c0392b; }
  .stars { color: #f5a623; letter-spacing: 2px; font-size: 15px; }

  /* Navigateur (mockup site) */
  .browser {
    position: absolute; right: 42px; top: 150px; width: 470px; z-index: 2;
    background: #fff; border-radius: 18px; overflow: hidden;
    transform: rotate(4deg);
    box-shadow: 0 40px 80px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.08);
    color: #1c2733;
  }
  .bbar { display: flex; gap: 8px; align-items: center; background: #eceff3; padding: 12px 16px; }
  .bdot { width: 13px; height: 13px; border-radius: 50%; }
  .burl { flex: 1; margin-left: 8px; background: #fff; border-radius: 8px; font-size: 15px; color: #7a8794; padding: 5px 12px; }

  /* Score PageSpeed */
  .score-wrap { display: flex; align-items: center; gap: 22px; }
  .score {
    width: 170px; height: 170px; border-radius: 50%; flex: none;
    background: conic-gradient(#2fac66 0 96%, #e8ecf1 96% 100%);
    display: grid; place-items: center;
  }
  .score b {
    width: 122px; height: 122px; background: #fff; border-radius: 50%;
    display: grid; place-items: center;
    font-size: 52px; color: #1f7a4d; font-family: "Arial Black", "DejaVu Sans", sans-serif;
  }
  /* Donut parts de marché */
  .donut {
    width: 170px; height: 170px; border-radius: 50%; flex: none;
    background: conic-gradient(#d4a44a 0 43%, #1d4e89 43% 65%, #e8ecf1 65% 100%);
    display: grid; place-items: center;
  }
  .donut b {
    width: 110px; height: 110px; background: #fff; border-radius: 50%;
    display: grid; place-items: center;
    font-size: 34px; color: #9a6d1c; font-family: "Arial Black", "DejaVu Sans", sans-serif;
  }
  .legend { font-size: 16px; font-weight: 600; color: #33404d; }
  .legend div { display: flex; align-items: center; gap: 9px; margin-bottom: 9px; }
  .swatch { width: 15px; height: 15px; border-radius: 4px; flex: none; }

  /* Barre de progression */
  .progress { height: 14px; background: #e8ecf1; border-radius: 999px; overflow: hidden; }
  .progress i { display: block; height: 100%; background: #2fac66; border-radius: 999px; }

  /* Mini-aperçus de sites (thèmes, avant/après) */
  .minis { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .mini { border: 1px solid #e4e8ee; border-radius: 12px; overflow: hidden; }
  .mini .cap { padding: 8px 10px; font-size: 14px; font-weight: 700; color: #33404d; display: flex; justify-content: space-between; align-items: center; }
  .mini .hero { height: 84px; padding: 12px; }
  .mini .hbar { height: 9px; border-radius: 5px; background: rgba(255,255,255,.85); margin-bottom: 7px; }
  .mini .hbtn { width: 52px; height: 16px; border-radius: 6px; margin-top: 10px; }

  /* SERP Google */
  .serp-search { display: flex; align-items: center; gap: 10px; border: 1px solid #dfe1e5; border-radius: 999px; padding: 10px 16px; font-size: 16px; color: #5f6a75; margin-bottom: 14px; }
  .serp-res { border: 1px solid #e4e8ee; border-radius: 12px; padding: 12px 14px; margin-bottom: 10px; }
  .serp-res.win { border: 2px solid #d4a44a; background: #fffaf0; position: relative; }
  .serp-res .stitle { color: #1a0dab; font-weight: 700; font-size: 17px; }
  .serp-res .surl { color: #1f7a4d; font-size: 13px; margin-bottom: 3px; }
  .gbar { height: 10px; border-radius: 5px; background: #e8ecf1; margin-top: 6px; }
  .rank1 {
    position: absolute; top: -14px; right: 12px; background: #d4a44a; color: #0a1d36;
    font-family: "Arial Black", "DejaVu Sans", sans-serif; font-size: 15px; padding: 4px 12px; border-radius: 999px;
  }

  /* Match VS */
  .vs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; position: relative; }
  .vs-col { border: 1px solid #e4e8ee; border-radius: 12px; overflow: hidden; }
  .vs-col .head { padding: 10px; text-align: center; font-family: "Arial Black", "DejaVu Sans", sans-serif; font-size: 18px; color: #fff; }
  .vs-col ul { list-style: none; padding: 10px 12px; font-size: 15px; font-weight: 600; color: #33404d; }
  .vs-col li { padding: 5px 0; }
  .vs-badge {
    position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-8deg);
    background: #d4a44a; color: #0a1d36; font-family: "Arial Black", "DejaVu Sans", sans-serif;
    font-size: 26px; padding: 12px 16px; border-radius: 50%;
    box-shadow: 0 10px 24px rgba(0,0,0,.35); z-index: 2;
  }

  /* Notification + flèche */
  .notif {
    position: absolute; right: 96px; top: 96px; z-index: 4;
    background: #fff; border-radius: 14px; padding: 14px 20px;
    display: flex; gap: 12px; align-items: center;
    transform: rotate(-3deg);
    box-shadow: 0 24px 48px rgba(0,0,0,.5);
    color: #1c2733;
  }
  .notif .check {
    width: 40px; height: 40px; border-radius: 50%; background: #2fac66;
    color: #fff; font-size: 24px; font-weight: 800; display: grid; place-items: center; flex: none;
  }
  .notif .check.red { background: #e5484d; }
  .notif .check.gold { background: #d4a44a; }
  .notif .t { font-size: 17px; font-weight: 700; }
  .notif .s { font-size: 15px; color: #6a7684; }
  svg.arrow { position: absolute; right: 470px; top: 78px; z-index: 5; filter: drop-shadow(0 6px 12px rgba(0,0,0,.45)); }
</style>

<div class="dots"></div>
<div class="beam"></div>

<div class="left">
  <div class="badge">%%BADGE%%</div>
  <h1>%%TITLE%%</h1>
  <div class="sub">%%SUB%%</div>
  <div class="steps">%%STEPS%%</div>
</div>

%%VISUAL%%

<div class="notif">
  <div class="check %%NOTIF_COLOR%%">%%NOTIF_ICON%%</div>
  <div>
    <div class="t">%%NOTIF_T%%</div>
    <div class="s">%%NOTIF_S%%</div>
  </div>
</div>

<svg class="arrow" width="150" height="110" viewBox="0 0 150 110">
  <path d="M8 100 C 40 60, 80 40, 122 26" fill="none" stroke="#d4a44a" stroke-width="11" stroke-linecap="round"/>
  <path d="M96 14 L 132 22 L 112 52 Z" fill="#d4a44a"/>
</svg>
"""


def lines(*ls):
    """Lignes du titre : tuples (texte, "cream"|"gold", taille_px)."""
    return "".join(
        f'<span class="ln {cls}" style="font-size:{size}px">{txt}</span>'
        for txt, cls, size in ls
    )


def steps(*ss):
    """Pastilles d'étapes séparées par des chevrons or."""
    parts = []
    for i, s in enumerate(ss):
        if i:
            parts.append('<div class="chev">➜</div>')
        parts.append(f'<div class="step">{s}</div>')
    return "".join(parts)


def build_html(cfg: dict) -> str:
    notif_color, notif_icon, notif_t, notif_s = cfg["notif"]
    return (
        TEMPLATE
        .replace("%%BADGE%%", cfg["badge"])
        .replace("%%TITLE%%", cfg["title"])
        .replace("%%SUB%%", cfg["sub"])
        .replace("%%STEPS%%", cfg["steps"])
        .replace("%%VISUAL%%", cfg["visual"])
        .replace("%%NOTIF_COLOR%%", notif_color)
        .replace("%%NOTIF_ICON%%", notif_icon)
        .replace("%%NOTIF_T%%", notif_t)
        .replace("%%NOTIF_S%%", notif_s)
    )


def _chrome_cache_dir() -> str:
    """Dossier où l'on dépose un Chrome téléchargé (surchargeable via env)."""
    return os.environ.get(
        "CHROME_CACHE_DIR",
        os.path.join(os.path.expanduser("~"), ".cache", "paul-alves-covers"),
    )


def _cached_download() -> str | None:
    """Chrome déjà téléchargé par une exécution précédente, s'il y en a un."""
    pattern = os.path.join(_chrome_cache_dir(), "chrome-headless-shell", "*", "*",
                           "chrome-headless-shell")
    hits = sorted(p for p in glob.glob(pattern) if os.access(p, os.X_OK))
    return hits[-1] if hits else None


def _download_chrome() -> str | None:
    """Télécharge un chrome-headless-shell via npx (~15 s).

    Sert dans l'environnement cloud de la routine : Ubuntu 24.04 n'y fournit
    aucun Chrome utilisable (le paquet `chromium` n'est qu'un stub snap, et
    snap ne tourne pas en conteneur). Le téléchargement passe par
    registry.npmjs.org, autorisé dans le bac à sable. Poser
    `COVER_NO_DOWNLOAD=1` pour l'interdire et forcer le repli charte.
    """
    if os.environ.get("COVER_NO_DOWNLOAD"):
        return None
    if shutil.which("npx") is None:
        return None
    print("[cover] Chrome absent -> téléchargement de chrome-headless-shell…",
          file=sys.stderr)
    try:
        proc = subprocess.run(
            ["npx", "--yes", "@puppeteer/browsers", "install",
             "chrome-headless-shell@stable", "--path", _chrome_cache_dir()],
            capture_output=True, text=True, timeout=600,
        )
    except Exception as e:
        print(f"[cover] téléchargement impossible ({e})", file=sys.stderr)
        return None
    # stdout attendu : "chrome-headless-shell@<version> <chemin absolu>"
    for line in proc.stdout.splitlines():
        _, _, path = line.strip().partition(" ")
        if path and os.path.exists(path):
            return path
    print(f"[cover] téléchargement échoué (code {proc.returncode})", file=sys.stderr)
    return None


def find_chrome() -> str | None:
    """Binaire Chrome/Chromium disponible, ou None (→ repli charte)."""
    env = os.environ.get("CHROME_BIN")
    if env and os.path.exists(env):
        return env
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac):
        return mac
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return _cached_download() or _download_chrome()


def render_cover(cfg: dict, out_jpg: str) -> bool:
    """Rend la vignette en <out>.jpg + <out>.webp. False si Chrome indisponible."""
    chrome = find_chrome()
    if chrome is None:
        return False
    tmp = tempfile.mkdtemp(prefix="cover-")
    html_path = os.path.join(tmp, "cover.html")
    png_path = os.path.join(tmp, "cover.png")
    with open(html_path, "w") as f:
        f.write(build_html(cfg))
    try:
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--window-size={W},{H}", f"--screenshot={png_path}",
             f"file://{html_path}"],
            check=True, capture_output=True, timeout=120,
        )
        img = Image.open(png_path).convert("RGB")
    except Exception:
        return False
    if img.size != (W, H):
        img = img.resize((W, H))
    img.save(out_jpg, "JPEG", quality=88)
    img.save(os.path.splitext(out_jpg)[0] + ".webp", "WEBP", quality=80)
    return True


def make_vs_visual(a: str, b: str, color_a: str = "#0e2444", color_b: str = "#0f9bd7") -> str:
    """Face-à-face générique « A vs B » (barres neutres, pas de faux arguments)."""
    def col(name, color, marks):
        items = "".join(
            f'<li style="display:flex;align-items:center;gap:8px">{m}'
            f'<span style="flex:1;height:9px;border-radius:5px;background:#e8ecf1"></span></li>'
            for m in marks
        )
        return (f'<div class="vs-col"><div class="head" style="background:{color}">{name}</div>'
                f'<ul>{items}</ul></div>')
    return (f'<div class="panel"><h3>⚔️ Le face-à-face</h3><div class="vs-grid">'
            f'{col(a, color_a, ["✓", "✓", "✓"])}'
            f'{col(b, color_b, ["✓", "✗", "✗"])}'
            f'<div class="vs-badge">VS</div></div></div>')


# ---------------------------------------------------------------------------
# Visuels thématiques prêts à l'emploi pour la génération automatique.
# Chaque preset : sub / steps / notif par défaut + bloc visuel de droite.
# ---------------------------------------------------------------------------
PRESETS: dict[str, dict] = {
    "site": {
        "sub": "le guide pas à pas",
        "steps": ["Préparer", "Créer", "Publier"],
        "notif": ("", "✓", "Site en ligne !", "prêt à accueillir vos visiteurs"),
        "visual": """
<div class="browser">
  <div class="bbar">
    <div class="bdot" style="background:#ff5f57"></div>
    <div class="bdot" style="background:#febc2e"></div>
    <div class="bdot" style="background:#28c840"></div>
    <div class="burl">votre-site.fr</div>
  </div>
  <div style="padding:18px 20px 22px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <b style="font-size:19px">Votre Site</b>
      <div style="display:flex;gap:8px">
        <span style="width:44px;height:10px;border-radius:5px;background:#e8ecf1"></span>
        <span style="width:44px;height:10px;border-radius:5px;background:#e8ecf1"></span>
        <span style="width:44px;height:10px;border-radius:5px;background:#d4a44a"></span>
      </div>
    </div>
    <div style="background:linear-gradient(135deg,#0e2444,#1d4e89);border-radius:12px;padding:18px 16px">
      <div style="height:14px;width:70%;border-radius:7px;background:rgba(255,255,255,.9);margin-bottom:9px"></div>
      <div style="height:10px;width:50%;border-radius:5px;background:rgba(255,255,255,.45);margin-bottom:14px"></div>
      <div style="display:inline-block;background:#d4a44a;color:#0a1d36;font-weight:700;font-size:14px;border-radius:8px;padding:7px 14px">Découvrir</div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px">
      <div style="border:1px solid #e4e8ee;border-radius:10px;padding:10px"><div style="font-size:20px">🖼️</div><div style="height:8px;width:80%;border-radius:4px;background:#e8ecf1;margin-top:8px"></div></div>
      <div style="border:1px solid #e4e8ee;border-radius:10px;padding:10px"><div style="font-size:20px">📝</div><div style="height:8px;width:70%;border-radius:4px;background:#e8ecf1;margin-top:8px"></div></div>
    </div>
  </div>
</div>""",
    },
    "shop": {
        "sub": "votre boutique en ligne, pas à pas",
        "steps": ["Installer", "Configurer", "Vendre"],
        "notif": ("", "✓", "Nouvelle commande !", "votre boutique encaisse"),
        "visual": """
<div class="browser">
  <div class="bbar">
    <div class="bdot" style="background:#ff5f57"></div>
    <div class="bdot" style="background:#febc2e"></div>
    <div class="bdot" style="background:#28c840"></div>
    <div class="burl">ma-boutique.fr</div>
  </div>
  <div style="padding:18px 20px 22px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <b style="font-size:20px">Ma Boutique</b>
      <div style="font-size:24px;position:relative">🛒<em style="position:absolute;top:-8px;right:-12px;font-style:normal;background:#e5484d;color:#fff;font-size:13px;font-weight:700;border-radius:50%;width:22px;height:22px;display:grid;place-items:center">3</em></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div style="border:1px solid #e4e8ee;border-radius:12px;overflow:hidden">
        <div style="height:78px;display:grid;place-items:center;font-size:38px;background:linear-gradient(135deg,#ffe9c7,#ffd08a)">👜</div>
        <div style="padding:8px 10px 10px"><div style="font-size:14px;font-weight:600;color:#33404d">Sac artisanal</div><div style="font-size:15px;font-weight:700;color:#7f54b3;margin-top:2px">49,90 €</div></div>
      </div>
      <div style="border:1px solid #e4e8ee;border-radius:12px;overflow:hidden">
        <div style="height:78px;display:grid;place-items:center;font-size:38px;background:linear-gradient(135deg,#d8e7ff,#a9c8ff)">👟</div>
        <div style="padding:8px 10px 10px"><div style="font-size:14px;font-weight:600;color:#33404d">Sneakers</div><div style="font-size:15px;font-weight:700;color:#7f54b3;margin-top:2px">89,00 €</div></div>
      </div>
    </div>
    <div style="margin-top:14px;background:#7f54b3;color:#fff;text-align:center;font-weight:700;font-size:18px;border-radius:10px;padding:12px">Ajouter au panier</div>
  </div>
</div>""",
    },
    "server": {
        "sub": "bien choisir son hébergeur",
        "steps": ["Comparer", "Choisir", "Migrer"],
        "notif": ("", "⚡", "Site rapide !", "chargement quasi instantané"),
        "visual": """
<div class="panel">
  <h3>🖥️ Votre hébergement</h3>
  <div class="row"><span class="ico">⏱️</span><span class="grow">Disponibilité</span><span class="pill green">99,9 %</span></div>
  <div class="row"><span class="ico">⚡</span><span class="grow" style="max-width:150px">Vitesse</span><span class="grow"><span class="progress"><i style="width:88%"></i></span></span></div>
  <div class="row"><span class="ico">💬</span><span class="grow">Support réactif</span><span class="pill gold">Testé</span></div>
</div>""",
    },
    "ranking": {
        "sub": "le classement testé, sans sponsor",
        "steps": ["Vitesse", "Support", "Prix"],
        "notif": ("gold", "🏆", "Notre favori", "le verdict du comparatif"),
        "visual": """
<div class="panel">
  <h3>🏆 Le classement</h3>
  <div class="row"><span class="ico">🥇</span><span class="grow">Choix nº1 <div class="stars">★★★★★</div></span><span class="pill gold">9,4</span></div>
  <div class="row"><span class="ico">🥈</span><span class="grow">Choix nº2 <div class="stars">★★★★☆</div></span><span class="pill green">8,7</span></div>
  <div class="row"><span class="ico">🥉</span><span class="grow">Choix nº3 <div class="stars">★★★★☆</div></span><span class="pill green">8,1</span></div>
</div>""",
    },
    "plugins": {
        "sub": "les indispensables, rien de plus",
        "steps": ["Choisir", "Installer", "Configurer"],
        "notif": ("", "✓", "Extension activée", "votre site reste rapide"),
        "visual": """
<div class="panel">
  <h3>🧩 Extensions installées</h3>
  <div class="row"><span class="ico">🔍</span><span class="grow">SEO</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">⚡</span><span class="grow">Cache</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🛡️</span><span class="grow">Sécurité</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🗑️</span><span class="grow">42 plugins gadgets</span><span class="pill red">Évités</span></div>
</div>""",
    },
    "themes": {
        "sub": "gratuit ou premium, bien choisir",
        "steps": ["Design", "Vitesse", "Prix"],
        "notif": ("", "✓", "Thème installé", "léger et personnalisable"),
        "visual": """
<div class="panel">
  <h3>🎨 Thèmes testés</h3>
  <div class="minis">
    <div class="mini">
      <div class="hero" style="background:linear-gradient(135deg,#0e2444,#1d4e89)">
        <div class="hbar" style="width:75%"></div>
        <div class="hbar" style="width:50%;opacity:.5"></div>
        <div class="hbtn" style="background:#d4a44a"></div>
      </div>
      <div class="cap">Thème A <span class="pill gold">TOP</span></div>
      <div style="padding:0 10px 10px" class="stars">★★★★★</div>
    </div>
    <div class="mini">
      <div class="hero" style="background:linear-gradient(135deg,#5b7c99,#8aa6bd)">
        <div class="hbar" style="width:70%"></div>
        <div class="hbar" style="width:45%;opacity:.5"></div>
        <div class="hbtn" style="background:#fff"></div>
      </div>
      <div class="cap">Thème B</div>
      <div style="padding:0 10px 10px" class="stars">★★★★☆</div>
    </div>
  </div>
</div>""",
    },
    "speed": {
        "sub": "un site qui charge vite",
        "steps": ["Cache", "Images", "CDN"],
        "notif": ("", "⚡", "-2,4 s gagnées", "au chargement de la page"),
        "visual": """
<div class="panel">
  <h3>⚡ PageSpeed Insights</h3>
  <div class="score-wrap">
    <div class="score"><b>96</b></div>
    <div>
      <div class="row" style="margin-bottom:10px"><span class="grow">Chargement</span><span class="pill green">1,2 s</span></div>
      <div class="row"><span class="grow">Mobile</span><span class="pill green">✓</span></div>
    </div>
  </div>
</div>""",
    },
    "budget": {
        "sub": "les vrais chiffres, sans surprise",
        "steps": ["Domaine", "Création", "Entretien"],
        "notif": ("", "✓", "Devis transparent", "zéro coût caché"),
        "visual": """
<div class="panel">
  <h3>💶 Le vrai budget</h3>
  <div class="row"><span class="ico">🌐</span><span class="grow">Domaine + hébergement</span><span class="pill green">~100 €/an</span></div>
  <div class="row"><span class="ico">🎨</span><span class="grow">Création du site</span><span class="pill green">sur devis</span></div>
  <div class="row" style="border-color:#d4a44a;background:#fffaf0"><span class="ico">💡</span><span class="grow"><b>Budget réaliste</b></span><span class="pill gold">détaillé ici</span></div>
</div>""",
    },
    "revamp": {
        "sub": "moderniser sans tout casser",
        "steps": ["Auditer", "Refondre", "Rediriger"],
        "notif": ("", "📈", "Trafic conservé", "positions Google intactes"),
        "visual": """
<div class="panel">
  <h3>✨ Avant / Après</h3>
  <div class="minis">
    <div class="mini" style="opacity:.75">
      <div class="hero" style="background:#c8cdd4">
        <div class="hbar" style="width:80%;background:#a9b0b9"></div>
        <div class="hbar" style="width:60%;background:#a9b0b9"></div>
        <div class="hbtn" style="background:#8f979f"></div>
      </div>
      <div class="cap">Avant <span class="pill red">Daté</span></div>
    </div>
    <div class="mini">
      <div class="hero" style="background:linear-gradient(135deg,#0e2444,#1d4e89)">
        <div class="hbar" style="width:75%"></div>
        <div class="hbar" style="width:50%;opacity:.5"></div>
        <div class="hbtn" style="background:#d4a44a"></div>
      </div>
      <div class="cap">Après <span class="pill green">Moderne</span></div>
    </div>
  </div>
</div>""",
    },
    "backup": {
        "sub": "ne perdez jamais votre site",
        "steps": ["Planifier", "Stocker", "Tester"],
        "notif": ("", "✓", "Site restauré", "en 5 minutes chrono"),
        "visual": """
<div class="panel">
  <h3>☁️ Sauvegardes</h3>
  <div style="margin-bottom:12px">
    <div style="display:flex;justify-content:space-between;font-size:15px;font-weight:600;color:#33404d;margin-bottom:7px"><span>Sauvegarde en cours…</span><span>100 %</span></div>
    <div class="progress"><i style="width:100%"></i></div>
  </div>
  <div class="row"><span class="ico">🕑</span><span class="grow">Dernière copie</span><span class="pill green">il y a 2 h</span></div>
  <div class="row"><span class="ico">☁️</span><span class="grow">Stockage externe</span><span class="pill green">Actif</span></div>
</div>""",
    },
    "shield": {
        "sub": "bloquez les attaques avant l'impact",
        "steps": ["Pare-feu", "2FA", "Sauvegarde"],
        "notif": ("red", "🚫", "Attaque bloquée !", "IP bannie automatiquement"),
        "visual": """
<div class="panel">
  <h3>🛡️ Protection active</h3>
  <div class="row"><span class="ico">🔒</span><span class="grow">Certificat SSL</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🧱</span><span class="grow">Pare-feu applicatif</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🔑</span><span class="grow">Double authentification</span><span class="pill green">Activée</span></div>
</div>""",
    },
    "serp": {
        "sub": "être trouvé sur Google",
        "steps": ["Technique", "Contenu", "Liens"],
        "notif": ("gold", "🏆", "Position nº1", "sur votre mot-clé"),
        "visual": """
<div class="panel">
  <h3>🔍 Résultats Google</h3>
  <div class="serp-search">🔍 <span>votre activité + votre ville</span></div>
  <div class="serp-res win">
    <span class="rank1">Nº1</span>
    <div class="surl">votre-site.fr</div>
    <div class="stitle">Votre site — ici</div>
    <div class="gbar" style="width:85%"></div>
  </div>
  <div class="serp-res">
    <div class="gbar" style="width:60%;margin-top:0"></div>
    <div class="gbar" style="width:90%"></div>
  </div>
</div>""",
    },
    "dashboard": {
        "sub": "un site sain toute l'année",
        "steps": ["Sauvegarde", "Màj", "Contrôle"],
        "notif": ("", "✓", "Site à jour !", "aucune faille connue"),
        "visual": """
<div class="panel">
  <h3>🔧 Tableau de bord</h3>
  <div class="row"><span class="ico">🧩</span><span class="grow">Extensions</span><span class="pill green">À jour</span></div>
  <div class="row"><span class="ico">🎨</span><span class="grow">Thème</span><span class="pill green">À jour</span></div>
  <div class="row"><span class="ico">⚙️</span><span class="grow">WordPress</span><span class="pill gold">Màj dispo</span></div>
</div>""",
    },
    "migrate": {
        "sub": "changer sans rien perdre",
        "steps": ["Copier", "Basculer", "Rediriger"],
        "notif": ("", "📈", "SEO intact", "0 position perdue"),
        "visual": """
<div class="panel">
  <h3>📦 Migration en cours</h3>
  <div class="row"><span class="ico">🗂️</span><span class="grow">Fichiers</span><span class="pill green">Copiés</span></div>
  <div class="row"><span class="ico">🗄️</span><span class="grow">Base de données</span><span class="pill green">Transférée</span></div>
  <div class="row"><span class="ico">🔀</span><span class="grow">Redirections 301</span><span class="pill gold">En place</span></div>
</div>""",
    },
    "vs": {
        "sub": "le comparatif sans langue de bois",
        "steps": ["Forces", "Faiblesses", "Verdict"],
        "notif": ("gold", "🏆", "Il y a un gagnant", "verdict dans l'article"),
        "visual": None,  # construit via make_vs_visual(a, b)
    },
}
