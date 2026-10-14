"""Assemble le CSS du thème enfant à partir des styles Astro d'origine.

global.css est repris tel quel ; les <style> scopés des pages Astro sont
préfixés par la classe de body de la page WordPress correspondante.
Le CSS d'adaptation (Elementor, blocs Gutenberg) est ajouté à la fin.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / 'src'
THEME = ROOT / 'wordpress' / 'hello-elementor-child'

def style_blocks(path):
    txt = path.read_text()
    return '\n'.join(re.findall(r'<style>(.*?)</style>', txt, re.S))

def split_rules(css):
    """Découpe du CSS en blocs de premier niveau (sélecteur, corps)."""
    out, i, n = [], 0, len(css)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    n = len(css)
    while i < n:
        j = css.find('{', i)
        if j == -1: break
        sel = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        out.append((sel, css[j + 1:k - 1]))
        i = k
    return out

def scope(css, prefix):
    res = []
    for sel, body in split_rules(css):
        if sel.startswith('@keyframes') or sel.startswith('@font-face'):
            res.append(f'{sel}{{{body}}}')
        elif sel.startswith('@'):
            res.append(f'{sel}{{\n{scope(body, prefix)}\n}}')
        else:
            parts = []
            for s in sel.split(','):
                s = s.strip()
                if s.startswith((':root', 'html', 'body')):
                    parts.append(s)
                else:
                    parts.append(f'{prefix} {s}')
            res.append(',\n'.join(parts) + ' {' + body + '}')
    return '\n'.join(res)

PAGES = [
    ('pages/services.astro', '.pa-services'),
    ('pages/a-propos.astro', '.pa-a-propos'),
    ('pages/realisations.astro', '.pa-realisations'),
    ('pages/contact.astro', '.pa-contact'),
    ('pages/404.astro', '.error404'),
    ('pages/politique-confidentialite.astro', '.pa-legal'),
    ('pages/plan-du-site.astro', '.pa-plan-du-site'),
    ('pages/[slug].astro', '.single-post'),
]
COMPONENTS = ['About', 'Projects', 'CategoryNav', 'MobileBar']

parts = ['/* Fichier généré par wordpress/build/build_css.py : modifier les sources, pas ce fichier. */',
         (THEME / 'assets/css/reset.css').read_text(),
         '/* ==== global.css (site Astro) ==== */', (SRC / 'styles/global.css').read_text()]
for c in COMPONENTS:
    parts += [f'/* ==== composant {c} ==== */', style_blocks(SRC / f'components/{c}.astro')]
for page, prefix in PAGES:
    parts += [f'/* ==== page {page} -> {prefix} ==== */', scope(style_blocks(SRC / page), prefix)]
parts += ['/* ==== adaptation WordPress / Elementor ==== */', (THEME / 'assets/css/adapter.css').read_text(),
          (THEME / 'assets/css/fixes.css').read_text()]
(THEME / 'assets/css/site.css').write_text('\n'.join(parts))
print('site.css :', len('\n'.join(parts)), 'octets')
