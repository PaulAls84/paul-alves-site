"""Crée ou met à jour les pages Elementor sur le WordPress de préproduction.

Usage : python3 publish_pages.py [slug ...]   (sans argument : toutes les pages)
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import wp  # noqa: E402
import pages  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATE = pathlib.Path(__file__).parent / 'page_ids.json'


def legal_html(astro_file):
    """Contenu de <div class="legal-content"> d'une page légale Astro."""
    src = (ROOT / 'src/pages' / astro_file).read_text()
    start = src.index('<div class="legal-content">') + len('<div class="legal-content">')
    end = src.index('</div>\n    </div>\n  </section>', start)
    body = src[start:end].strip()
    body = body.replace('data-cookie-prefs', 'class="cky-banner-element"')
    return re.sub(r'\n\s+', '\n', body)


# slug, titre, constructeur, titre SEO, description SEO (repris des <Layout> Astro)
PAGES = [
    ('accueil', 'Accueil', pages.page_accueil,
     'Paul Alves | Développeur Web & Consultant SEO à Soissons',
     "J'aide les entreprises à se développer en ligne grâce à des sites web sur mesure, rapides et optimisés pour le SEO."),
    ('services', 'Services', pages.page_services,
     'Services WordPress & SEO | Paul Alves',
     'Création de site WordPress, refonte, SEO, performances et maintenance. Solutions sur mesure dès 400 €, à Soissons et partout en France.'),
    ('a-propos', 'À propos', pages.page_a_propos,
     'À propos | Paul Alves, développeur WordPress & consultant SEO',
     'De nosamisleschiens.fr et 1 million de visiteurs à consultant WordPress & SEO : découvrez le parcours de Paul Alves, freelance basé à Soissons.'),
    ('realisations', 'Réalisations', pages.page_realisations,
     'Réalisations | Paul Alves, projets WordPress & SEO',
     'Projets WordPress réalisés par Paul Alves : sites vitrines, e-commerce, audits SEO et optimisations de performances pour PME et entrepreneurs.'),
    ('contact', 'Contact', pages.page_contact,
     'Contact | Paul Alves, développeur WordPress & SEO à Soissons',
     'Contactez Paul Alves pour votre projet WordPress ou SEO : appel découverte gratuit de 30 min, réponse sous 24 h. Basé à Soissons.'),
    ('mentions-legales', 'Mentions légales',
     lambda: pages.page_legal('Mentions légales', legal_html('mentions-legales.astro')),
     'Mentions légales | Paul Alves',
     'Mentions légales du site paul-alves.fr : informations légales et éditoriales.'),
    ('politique-confidentialite', 'Politique de confidentialité',
     lambda: pages.page_legal('Politique de confidentialité', legal_html('politique-confidentialite.astro')),
     None, None),
    ('plan-du-site', 'Plan du site', pages.page_plan_du_site,
     'Plan du site | Paul Alves',
     "Vue d'ensemble de toutes les pages du site paul-alves.fr : accueil, services, à propos, réalisations, blog, contact et pages légales."),
]


def politique_meta():
    src = (ROOT / 'src/pages/politique-confidentialite.astro').read_text()
    title = re.search(r'title="([^"]+)"', src).group(1)
    desc = re.search(r'description="([^"]+)"', src).group(1)
    return title, desc


def main(only):
    ids = json.loads(STATE.read_text()) if STATE.exists() else {}
    for slug, title, build, seo_title, seo_desc in PAGES:
        if only and slug not in only:
            continue
        if slug == 'politique-confidentialite':
            seo_title, seo_desc = politique_meta()
        data = build()
        payload = {
            'title': title, 'slug': slug, 'status': 'publish',
            'template': 'elementor_header_footer',
            'comment_status': 'closed', 'ping_status': 'closed',
            'meta': {
                '_elementor_edit_mode': 'builder',
                '_elementor_template_type': 'wp-page',
                '_elementor_version': '4.3.5',
                '_elementor_data': json.dumps(data, ensure_ascii=False),
                '_elementor_page_settings': {},
                'rank_math_title': seo_title,
                'rank_math_description': seo_desc,
            },
        }
        route = f'/wp/v2/pages/{ids[slug]}' if slug in ids else '/wp/v2/pages'
        r = wp.api(route, 'POST', payload)
        if isinstance(r, dict) and r.get('id'):
            ids[slug] = r['id']
            print('ok', r['id'], r['link'])
        else:
            print('ERREUR', slug, str(r)[:400])
        STATE.write_text(json.dumps(ids, indent=1))
    # Page du blog (liste des articles, gérée par le thème)
    if not only or 'blog' in only:
        payload = {'title': 'Blog', 'slug': 'blog', 'status': 'publish', 'content': '',
                   'meta': {'rank_math_title': 'Blog | Paul Alves · Développeur Web & Consultant SEO',
                            'rank_math_description': 'Conseils SEO, développement web et stratégie digitale par Paul Alves.'}}
        route = f"/wp/v2/pages/{ids['blog']}" if 'blog' in ids else '/wp/v2/pages'
        r = wp.api(route, 'POST', payload)
        if isinstance(r, dict) and r.get('id'):
            ids['blog'] = r['id']
            print('ok', r['id'], r['link'])
        STATE.write_text(json.dumps(ids, indent=1))
    return ids


if __name__ == '__main__':
    main(sys.argv[1:])
