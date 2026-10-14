"""Convertit le HTML rendu par Markdoc en blocs Gutenberg."""
import json
from html.parser import HTMLParser
from html import escape

VOID = {'br', 'hr', 'img'}

class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs or []), [], parent

class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root'); self.cur = self.root
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur); self.cur.children.append(n)
        if tag not in VOID: self.cur = n
    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag: n = n.parent
        if n is not self.root: self.cur = n.parent
    def handle_data(self, data):
        self.cur.children.append(data)

def inner(n):
    return ''.join(outer(c) for c in n.children)

def outer(n, extra_attrs=None):
    if isinstance(n, str): return escape(n, quote=False)
    attrs = dict(n.attrs); attrs.update(extra_attrs or {})
    a = ''.join(f' {k}="{escape(v or "", quote=True)}"' for k, v in attrs.items())
    if n.tag in VOID: return f'<{n.tag}{a}/>'
    return f'<{n.tag}{a}>{inner(n)}</{n.tag}>'

def cmt(name, attrs=None):
    return f'<!-- wp:{name}{" " + json.dumps(attrs, ensure_ascii=False, separators=(",", ":")) if attrs else ""} -->'

def block(n, first_quote):
    if isinstance(n, str):
        return '' if not n.strip() else cmt('paragraph') + f'\n<p>{escape(n.strip(), quote=False)}</p>\n<!-- /wp:paragraph -->'
    t = n.tag
    if t == 'p':
        return cmt('paragraph') + f'\n<p>{inner(n)}</p>\n<!-- /wp:paragraph -->'
    if t in ('h2', 'h3', 'h4'):
        lvl = int(t[1]); at = None if lvl == 2 else {'level': lvl}
        return cmt('heading', at) + f'\n<{t} class="wp-block-heading">{inner(n)}</{t}>\n<!-- /wp:heading -->'
    if t in ('ul', 'ol'):
        return list_block(n)
    if t == 'blockquote':
        cls = 'en-bref' if first_quote[0] else None
        first_quote[0] = False
        at = {'className': cls} if cls else None
        body = '\n'.join(filter(None, (block(c, [False]) for c in n.children)))
        klass = 'wp-block-quote' + (f' {cls}' if cls else '')
        return cmt('quote', at) + f'\n<blockquote class="{klass}">{body}</blockquote>\n<!-- /wp:quote -->'
    if t == 'table':
        return cmt('table') + f'\n<figure class="wp-block-table"><table class="has-fixed-layout">{inner(n)}</table></figure>\n<!-- /wp:table -->'
    if t == 'pre':
        code = n.children[0] if n.children and not isinstance(n.children[0], str) and n.children[0].tag == 'code' else n
        return cmt('code') + f'\n<pre class="wp-block-code"><code>{inner(code)}</code></pre>\n<!-- /wp:code -->'
    if t == 'hr':
        return cmt('separator') + '\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->'
    if t == 'article':
        return '\n\n'.join(filter(None, (block(c, first_quote) for c in n.children)))
    # repli : bloc HTML brut
    return cmt('html') + '\n' + outer(n) + '\n<!-- /wp:html -->'

def list_block(n):
    ordered = n.tag == 'ol'
    items = []
    for li in n.children:
        if isinstance(li, str) or li.tag != 'li': continue
        parts, nested = [], []
        for c in li.children:
            if not isinstance(c, str) and c.tag in ('ul', 'ol'): nested.append(list_block(c))
            elif not isinstance(c, str) and c.tag == 'p': parts.append(inner(c))
            else: parts.append(outer(c))
        body = ''.join(parts) + ''.join(nested)
        items.append(cmt('list-item') + f'\n<li>{body}</li>\n<!-- /wp:list-item -->')
    tag = 'ol' if ordered else 'ul'
    return cmt('list', {'ordered': True} if ordered else None) + f'\n<{tag} class="wp-block-list">' + ''.join(items) + f'</{tag}>\n<!-- /wp:list -->'

def convert(html):
    b = Builder(); b.feed(html)
    first_quote = [True]
    return '\n\n'.join(filter(None, (block(c, first_quote) for c in b.root.children)))
