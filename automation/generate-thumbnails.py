#!/usr/bin/env python3
"""Régénère les vignettes "YouTube-style" des articles existants du blog.

Configs manuelles (badge, titre 3 lignes, sous-titre, étapes, visuel) posées
sur le template commun de cover_template.py. Pour la couverture des NOUVEAUX
articles de la routine auto, voir generate-cover.py (config auto-déduite).

Usage :
    python3 automation/generate-thumbnails.py            # toutes les vignettes
    python3 automation/generate-thumbnails.py <slug>...  # une sélection
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cover_template import lines, render_cover, steps  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "public", "images", "blog")


ARTICLES = [
    {
        "slug": "creer-boutique-woocommerce",
        "badge": "GUIDE PAS À PAS · 2026",
        "title": lines(("CRÉER SA", "cream", 72), ("BOUTIQUE", "gold", 102), ("EN LIGNE", "cream", 88)),
        "sub": 'avec <b class="purple">WooCommerce</b>, sans commission',
        "steps": steps("Installer", "Configurer", "Vendre"),
        "notif": ("", "✓", "Nouvelle commande !", "Sac artisanal — 49,90 €"),
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
    {
        "slug": "creer-un-site-wordpress",
        "badge": "GUIDE ÉTAPE PAR ÉTAPE · 2026",
        "title": lines(("CRÉER UN", "cream", 66), ("SITE", "gold", 124), ("WORDPRESS", "cream", 80)),
        "sub": 'de zéro à la mise en ligne, <b class="gold">sans coder</b>',
        "steps": steps("Domaine", "Installer", "Publier"),
        "notif": ("", "✓", "Site en ligne !", "mon-site.fr est publié"),
        "visual": """
<div class="browser">
  <div class="bbar">
    <div class="bdot" style="background:#ff5f57"></div>
    <div class="bdot" style="background:#febc2e"></div>
    <div class="bdot" style="background:#28c840"></div>
    <div class="burl">mon-site.fr</div>
  </div>
  <div style="padding:18px 20px 22px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <b style="font-size:19px">Mon Site</b>
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
    {
        "slug": "hebergement-woocommerce",
        "badge": "GUIDE · 2026",
        "title": lines(("HÉBERGER SA", "cream", 60), ("BOUTIQUE", "gold", 102), ("EN LIGNE", "cream", 84)),
        "sub": 'quel hébergeur pour <b class="purple">WooCommerce</b> ?',
        "steps": steps("Performance", "Sécurité", "Prix"),
        "notif": ("", "✓", "Pic de trafic absorbé", "0 ralentissement en caisse"),
        "visual": """
<div class="panel">
  <h3>🖥️ Serveur e-commerce</h3>
  <div class="row"><span class="ico">⚡</span><span class="grow">Temps de réponse</span><span class="pill green">180 ms</span></div>
  <div class="row"><span class="ico">🔒</span><span class="grow">SSL &amp; paiement chiffré</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🛒</span><span class="grow">500 commandes / jour</span><span class="pill gold">Sans lag</span></div>
</div>""",
    },
    {
        "slug": "hebergement-wordpress",
        "badge": "BIEN CHOISIR · 2026",
        "title": lines(("CHOISIR SON", "cream", 60), ("HÉBERGEMENT", "gold", 74), ("WORDPRESS", "cream", 84)),
        "sub": "mutualisé, VPS ou infogéré ?",
        "steps": steps("Comparer", "Choisir", "Migrer"),
        "notif": ("", "✓", "Site migré !", "sans interruption"),
        "visual": """
<div class="panel">
  <h3>🖥️ Votre hébergement</h3>
  <div class="row"><span class="ico">⏱️</span><span class="grow">Disponibilité</span><span class="pill green">99,9 %</span></div>
  <div class="row"><span class="ico">⚡</span><span class="grow" style="max-width:150px">Vitesse</span><span class="grow"><span class="progress"><i style="width:88%"></i></span></span></div>
  <div class="row"><span class="ico">💬</span><span class="grow">Support réactif</span><span class="pill gold">Testé</span></div>
</div>""",
    },
    {
        "slug": "maintenance-wordpress",
        "badge": "GUIDE COMPLET · 2026",
        "title": lines(("LA", "cream", 64), ("MAINTENANCE", "gold", 74), ("WORDPRESS", "cream", 84)),
        "sub": "mises à jour, sauvegardes, sécurité",
        "steps": steps("Sauvegarde", "Màj", "Contrôle"),
        "notif": ("", "✓", "Site à jour !", "aucune faille connue"),
        "visual": """
<div class="panel">
  <h3>🔧 Tableau de bord</h3>
  <div class="row"><span class="ico">🧩</span><span class="grow">Extensions</span><span class="pill green">À jour</span></div>
  <div class="row"><span class="ico">🎨</span><span class="grow">Thème</span><span class="pill green">À jour</span></div>
  <div class="row"><span class="ico">⚙️</span><span class="grow">WordPress 6.9</span><span class="pill gold">Màj dispo</span></div>
</div>""",
    },
    {
        "slug": "meilleur-hebergeur-wordpress",
        "badge": "COMPARATIF · 2026",
        "title": lines(("LE MEILLEUR", "cream", 62), ("HÉBERGEUR", "gold", 84), ("WORDPRESS", "cream", 84)),
        "sub": "le classement testé, sans sponsor",
        "steps": steps("Vitesse", "Support", "Prix"),
        "notif": ("gold", "🏆", "Notre favori", "élu meilleur rapport qualité/prix"),
        "visual": """
<div class="panel">
  <h3>🏆 Classement 2026</h3>
  <div class="row"><span class="ico">🥇</span><span class="grow">Hébergeur nº1 <div class="stars">★★★★★</div></span><span class="pill gold">9,4</span></div>
  <div class="row"><span class="ico">🥈</span><span class="grow">Hébergeur nº2 <div class="stars">★★★★☆</div></span><span class="pill green">8,7</span></div>
  <div class="row"><span class="ico">🥉</span><span class="grow">Hébergeur nº3 <div class="stars">★★★★☆</div></span><span class="pill green">8,1</span></div>
</div>""",
    },
    {
        "slug": "meilleur-plugin-wordpress",
        "badge": "SÉLECTION · 2025",
        "title": lines(("LES MEILLEURS", "cream", 56), ("PLUGINS", "gold", 108), ("WORDPRESS", "cream", 80)),
        "sub": "les indispensables, rien de plus",
        "steps": steps("SEO", "Cache", "Sécurité"),
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
    {
        "slug": "meilleur-theme-wordpress",
        "badge": "COMPARATIF · 2026",
        "title": lines(("LE MEILLEUR", "cream", 62), ("THÈME", "gold", 116), ("WORDPRESS", "cream", 80)),
        "sub": "gratuit ou premium, bien choisir",
        "steps": steps("Design", "Vitesse", "Prix"),
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
    {
        "slug": "optimiser-vitesse-site-wordpress",
        "badge": "PERFORMANCE · 2025",
        "title": lines(("ACCÉLÉRER", "cream", 68), ("SON SITE", "gold", 100), ("WORDPRESS", "cream", 80)),
        "sub": 'objectif <b class="green">90+</b> sur PageSpeed ⚡',
        "steps": steps("Cache", "Images", "CDN"),
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
    {
        "slug": "pourquoi-choisir-wordpress",
        "badge": "LE GUIDE · 2025",
        "title": lines(("POURQUOI", "cream", 74), ("WORDPRESS", "gold", 88), ("EN 2025 ?", "cream", 78)),
        "sub": '<b class="gold">43 %</b> du web tourne dessus',
        "steps": steps("Libre", "Évolutif", "Rentable"),
        "notif": ("gold", "🏆", "CMS nº1 mondial", "et de très loin"),
        "visual": """
<div class="panel">
  <h3>📊 Parts du web</h3>
  <div class="score-wrap">
    <div class="donut"><b>43 %</b></div>
    <div class="legend">
      <div><span class="swatch" style="background:#d4a44a"></span> WordPress</div>
      <div><span class="swatch" style="background:#1d4e89"></span> Autres CMS</div>
      <div><span class="swatch" style="background:#e8ecf1"></span> Sur-mesure</div>
    </div>
  </div>
</div>""",
    },
    {
        "slug": "prix-site-wordpress",
        "badge": "BUDGET · 2026",
        "title": lines(("COMBIEN COÛTE", "cream", 54), ("UN SITE", "gold", 104), ("WORDPRESS ?", "cream", 72)),
        "sub": "les vrais chiffres, poste par poste",
        "steps": steps("Domaine", "Création", "Entretien"),
        "notif": ("", "✓", "Devis transparent", "zéro coût caché"),
        "visual": """
<div class="panel">
  <h3>💶 Le vrai budget</h3>
  <div class="row"><span class="ico">🌐</span><span class="grow">Domaine + hébergement</span><span class="pill green">~100 €/an</span></div>
  <div class="row"><span class="ico">🎨</span><span class="grow">Création du site</span><span class="pill green">sur devis</span></div>
  <div class="row" style="border-color:#d4a44a;background:#fffaf0"><span class="ico">💡</span><span class="grow"><b>Budget réaliste</b></span><span class="pill gold">détaillé ici</span></div>
</div>""",
    },
    {
        "slug": "refonte-site-wordpress",
        "badge": "MÉTHODE · 2026",
        "title": lines(("RÉUSSIR SA", "cream", 64), ("REFONTE", "gold", 106), ("WORDPRESS", "cream", 80)),
        "sub": 'moderniser <b class="gold">sans perdre son SEO</b>',
        "steps": steps("Auditer", "Refondre", "Rediriger"),
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
      <div class="cap">2015 <span class="pill red">Daté</span></div>
    </div>
    <div class="mini">
      <div class="hero" style="background:linear-gradient(135deg,#0e2444,#1d4e89)">
        <div class="hbar" style="width:75%"></div>
        <div class="hbar" style="width:50%;opacity:.5"></div>
        <div class="hbtn" style="background:#d4a44a"></div>
      </div>
      <div class="cap">2026 <span class="pill green">Moderne</span></div>
    </div>
  </div>
</div>""",
    },
    {
        "slug": "sauvegarde-wordpress",
        "badge": "GUIDE COMPLET · 2026",
        "title": lines(("NE PERDEZ", "cream", 66), ("JAMAIS", "gold", 112), ("VOTRE SITE", "cream", 72)),
        "sub": "la stratégie de sauvegarde complète",
        "steps": steps("Planifier", "Stocker", "Tester"),
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
    {
        "slug": "securiser-site-wordpress",
        "badge": "SÉCURITÉ · 2026",
        "title": lines(("SÉCURISER", "cream", 74), ("SON SITE", "gold", 100), ("WORDPRESS", "cream", 80)),
        "sub": "bloquez les attaques avant l'impact",
        "steps": steps("Pare-feu", "2FA", "Sauvegarde"),
        "notif": ("red", "🚫", "Attaque bloquée !", "IP bannie automatiquement"),
        "visual": """
<div class="panel">
  <h3>🛡️ Protection active</h3>
  <div class="row"><span class="ico">🔒</span><span class="grow">Certificat SSL</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🧱</span><span class="grow">Pare-feu applicatif</span><span class="pill green">Actif</span></div>
  <div class="row"><span class="ico">🔑</span><span class="grow">Double authentification</span><span class="pill green">Activée</span></div>
</div>""",
    },
    {
        "slug": "seo-wordpress",
        "badge": "SEO · 2026",
        "title": lines(("RÉFÉRENCER", "cream", 64), ("SON SITE", "gold", 100), ("SUR GOOGLE", "cream", 72)),
        "sub": "le guide complet, avis d'expert",
        "steps": steps("Technique", "Contenu", "Liens"),
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
    {
        "slug": "wordpress-ou-wix",
        "badge": "LE MATCH · 2026",
        "title": lines(("WORDPRESS", "cream", 76), ("VS WIX", "gold", 116), ("QUE CHOISIR ?", "cream", 58)),
        "sub": "liberté, prix, SEO : le verdict",
        "steps": steps("Liberté", "Prix", "SEO"),
        "notif": ("gold", "🏆", "Il y a un gagnant", "verdict dans l'article"),
        "visual": """
<div class="panel">
  <h3>⚔️ Le face-à-face</h3>
  <div class="vs-grid">
    <div class="vs-col">
      <div class="head" style="background:#0e2444">WordPress</div>
      <ul><li>✓ 100 % libre</li><li>✓ SEO complet</li><li>✓ Évolutif</li></ul>
    </div>
    <div class="vs-col">
      <div class="head" style="background:#0f9bd7">Wix</div>
      <ul><li>✓ Simple</li><li>✗ Fermé</li><li>✗ Abonnement</li></ul>
    </div>
    <div class="vs-badge">VS</div>
  </div>
</div>""",
    },
]


def main() -> None:
    wanted = set(sys.argv[1:])
    unknown = wanted - {a["slug"] for a in ARTICLES}
    if unknown:
        sys.exit(f"Slugs inconnus : {', '.join(sorted(unknown))}")
    for a in ARTICLES:
        if wanted and a["slug"] not in wanted:
            continue
        out = os.path.join(OUT_DIR, f"{a['slug']}.jpg")
        if not render_cover(a, out):
            sys.exit(f"Échec rendu {a['slug']} (Chrome introuvable ?)")
        print(f"OK {a['slug']}")


if __name__ == "__main__":
    main()
