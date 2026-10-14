"""Publie les articles (posts.json produit par render-posts.mjs) sur WordPress.
Usage : node render-posts.mjs <racine du projet> posts.json && python3 push_posts.py [slug ...]"""
import sys, json, pathlib
S = str(pathlib.Path(__file__).parent)
sys.path.insert(0, S)
import wp, blocks
d = json.load(open(f'{S}/posts.json')); media = json.load(open(f'{S}/media.json')); cats = json.load(open(f'{S}/cats.json'))
only = sys.argv[1:]  # slugs optionnels
done = {}
try: done = json.load(open(f'{S}/post_ids.json'))
except Exception: pass
for p in d:
    p['blocks'] = blocks.convert(p['html'])
    if only and p['slug'] not in only: continue
    img = (p.get('image') or '').rsplit('/', 1)[-1]
    payload = {
        'title': p['title'], 'slug': p['slug'], 'status': 'publish',
        'content': p['blocks'], 'excerpt': p['description'],
        'date': f"{p['publishedAt']}T09:00:00",
        'categories': [cats[p['category']]],
        'comment_status': 'closed', 'ping_status': 'closed',
        'sticky': bool(p.get('featured')),
        'meta': {'rank_math_title': p['title'], 'rank_math_description': p['description']},
    }
    if img in media: payload['featured_media'] = media[img]['id']
    route = f"/wp/v2/posts/{done[p['slug']]}" if p['slug'] in done else '/wp/v2/posts'
    r = wp.api(route, 'POST', payload)
    if isinstance(r, dict) and r.get('id'):
        done[p['slug']] = r['id']; print('ok', r['id'], r['link'])
    else:
        print('ERREUR', p['slug'], str(r)[:300])
    json.dump(done, open(f'{S}/post_ids.json', 'w'), indent=1)
