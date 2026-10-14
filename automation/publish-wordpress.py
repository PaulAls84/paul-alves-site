#!/usr/bin/env python3
"""Publie un article du dossier src/content/blog sur le site WordPress.

Usage :
    python3 automation/publish-wordpress.py <slug>

Variables d'environnement (jamais committées) :
    WP_URL           ex. https://paul-alves.fr (sans slash final)
    WP_USER          identifiant WordPress de l'administrateur
    WP_APP_PASSWORD  mot de passe d'application WordPress
                     (Profil > Mots de passe d'application)

Étapes : rendu Markdoc -> HTML avec maillage interne (render-article.mjs),
conversion en blocs Gutenberg (wp_blocks.py), envoi de la couverture dans la
médiathèque, puis création de l'article (ou mise à jour s'il existe déjà avec
ce slug). Le titre et la description servent aussi de titre et de méta
description Rank Math.

Les articles déjà en ligne ne sont jamais réécrits par ce script, sauf celui
passé en argument : Paul peut les modifier librement dans WordPress.
"""
import base64
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'automation'))
import wp_blocks  # noqa: E402

CATEGORIES = {'WordPress': 'wordpress', 'SEO': 'seo', 'Plugins': 'plugins', 'Maintenance': 'maintenance'}


def env(name):
    value = os.environ.get(name, '').strip()
    if not value:
        sys.exit(f'[wp] Variable d\'environnement manquante : {name}')
    return value


WP_URL = env('WP_URL').rstrip('/')
AUTH = 'Basic ' + base64.b64encode(f"{env('WP_USER')}:{env('WP_APP_PASSWORD')}".encode()).decode()


def api(route, method='GET', data=None, raw=None, headers=None):
    url = f'{WP_URL}/wp-json{route}'
    # X-PA-Authorization : l'hébergeur supprime Authorization, le thème lit celui-ci.
    h = {'Authorization': AUTH, 'X-PA-Authorization': AUTH, 'Accept': 'application/json'}
    body = None
    if raw is not None:
        body = raw
        h.update(headers or {})
    elif data is not None:
        body = json.dumps(data).encode()
        h['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'[wp] {method} {route} -> HTTP {e.code} : {e.read().decode(errors="replace")[:400]}')


def render(slug):
    out = pathlib.Path(tempfile.mkdtemp()) / 'article.json'
    subprocess.run(['node', str(ROOT / 'automation/render-article.mjs'), str(ROOT), str(out), slug], check=True)
    posts = json.loads(out.read_text())
    if not posts:
        sys.exit(f'[wp] Article introuvable : src/content/blog/{slug}/index.mdoc')
    return posts[0]


def upload_cover(slug, title):
    path = ROOT / 'public/images/blog' / f'{slug}.jpg'
    if not path.exists():
        print(f'[wp] Pas de couverture {path.name}, article publié sans image à la une')
        return None
    existing = api('/wp/v2/media?' + urllib.parse.urlencode({'search': slug, 'per_page': 20}))
    for m in existing:
        if m.get('source_url', '').rsplit('/', 1)[-1] == f'{slug}.jpg':
            return m['id']
    media = api('/wp/v2/media', 'POST', raw=path.read_bytes(), headers={
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment; filename="{slug}.jpg"',
    })
    api(f"/wp/v2/media/{media['id']}", 'POST', {'alt_text': title})
    return media['id']


def category_id(name):
    slug = CATEGORIES.get(name)
    if not slug:
        sys.exit(f'[wp] Catégorie inconnue : {name} (attendu : {", ".join(CATEGORIES)})')
    found = api('/wp/v2/categories?' + urllib.parse.urlencode({'slug': slug}))
    if found:
        return found[0]['id']
    return api('/wp/v2/categories', 'POST', {'name': name, 'slug': slug})['id']


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    post = render(slug)
    content = wp_blocks.convert(post['html'])
    payload = {
        'title': post['title'],
        'slug': slug,
        'status': 'publish',
        'content': content,
        'excerpt': post['description'],
        'date': f"{str(post['publishedAt'])[:10]}T09:00:00",
        'categories': [category_id(post['category'])],
        'comment_status': 'closed',
        'ping_status': 'closed',
        'meta': {'rank_math_title': post['title'], 'rank_math_description': post['description']},
    }
    cover = upload_cover(slug, post['title'])
    if cover:
        payload['featured_media'] = cover

    existing = api('/wp/v2/posts?' + urllib.parse.urlencode({'slug': slug, 'status': 'any', 'context': 'edit'}))
    if existing:
        result = api(f"/wp/v2/posts/{existing[0]['id']}", 'POST', payload)
        action = 'mis à jour'
    else:
        result = api('/wp/v2/posts', 'POST', payload)
        action = 'publié'

    # Contrôle : la page publique doit répondre 200.
    link = result['link']
    try:
        with urllib.request.urlopen(link, timeout=60) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    print(f'[wp] OK article {action} : {link} (HTTP {status}, id {result["id"]})')
    if status != 200:
        sys.exit('[wp] La page publique ne répond pas 200 : vérifier dans WordPress.')


if __name__ == '__main__':
    main()
