"""Petit DSL pour générer le JSON Elementor (_elementor_data) des pages.

Les conteneurs reprennent la structure HTML et les classes du site Astro,
pour que la feuille de style du thème enfant s'applique telle quelle.
"""
import json
import pathlib
import secrets

MEDIA = json.loads((pathlib.Path(__file__).parent / 'media.json').read_text())
UPLOADS = 'https://navajowhite-turkey-402641.hostingersite.com/wp-content/uploads/2026/10/'

CAL_ATTRS = 'data-cal-link|paul-alves/audit-offert,data-cal-namespace|audit-offert,data-cal-config|{"layout":"month_view"}'
PHONE = '+33656666684'
PHONE_DISPLAY = '06 56 66 66 84'


def _id():
    return secrets.token_hex(4)[:7]


def media(name):
    """URL et id d'une image de la médiathèque."""
    m = MEDIA[name]
    return {'url': m['url'], 'id': m['id']}


def media_url(name):
    if name == 'nosamisleschiens-screenshot.webp':  # l'original, pas la version réduite
        return UPLOADS + name
    return MEDIA[name]['url']


def box(cls='', *children, tag='div', id=None, link=None):
    """Conteneur (pleine largeur, sans style propre) portant les classes du site."""
    s = {'content_width': 'full', 'html_tag': tag}
    if cls:
        s['css_classes'] = cls
    if id:
        s['_element_id'] = id
    if link:
        s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    return {'id': _id(), 'elType': 'container', 'isInner': False, 'settings': s,
            'elements': [c for c in children if c]}


def section(cls='', *children, id=None):
    return box(cls, *children, tag='section', id=id)


def _widget(kind, settings, cls=''):
    if cls:
        settings['_css_classes'] = cls
    return {'id': _id(), 'elType': 'widget', 'widgetType': kind, 'settings': settings, 'elements': []}


def heading(title, tag='h2', cls='', link=None, inherit=True):
    """Titre. Si cls est fourni, il est posé sur le wrapper et le titre en hérite."""
    s = {'title': title, 'header_size': tag}
    if link:
        s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    return _widget('heading', s, (cls + (' pa-h-inherit' if inherit else '')).strip() if cls else '')


def text(html, cls=''):
    """Éditeur de texte (le HTML garde les classes du site : <p class="lede">…)."""
    return _widget('text-editor', {'editor': html}, cls)


def html(code, cls=''):
    """Bloc HTML brut (icônes SVG, éléments décoratifs)."""
    return _widget('html', {'html': code}, cls)


def shortcode(code, cls=''):
    return _widget('shortcode', {'shortcode': code}, cls)


def image(name, cls='', alt=''):
    s = {'image': {**media(name), 'alt': alt}, 'image_size': 'full'}
    return _widget('image', s, cls)


def button(label, url='#', classes='btn btn-gold', cal=False, icon=None, cls=''):
    attrs = f'class|{classes}' + (',' + CAL_ATTRS if cal else '')
    s = {'text': label, 'link': {'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': attrs}}
    if icon:
        s['selected_icon'] = {'value': icon, 'library': 'fa-solid' if icon.startswith('fas') else 'fa-regular'}
        s['icon_align'] = 'left'
    return _widget('button', s, cls)


def cal_button(label, classes='btn btn-gold', icon=None, cls=''):
    return button(label, '#', classes, cal=True, icon=icon, cls=cls)


def phone_button(classes='btn btn-ghost-light hero-tel'):
    return button(PHONE_DISPLAY, 'tel:' + PHONE, classes, icon='fas fa-phone-alt')


def accordion(items, cls=''):
    tabs = [{'_id': _id(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in items]
    s = {
        'tabs': tabs,
        'faq_schema': 'yes',
        'selected_icon': {'value': 'fas fa-chevron-down', 'library': 'fa-solid'},
        'selected_active_icon': {'value': 'fas fa-chevron-up', 'library': 'fa-solid'},
        'icon_align': 'right',
        'title_html_tag': 'div',
    }
    # Widget « Bascule » : toutes les questions fermées au chargement (comme les <details> Astro)
    return _widget('toggle', s, cls)


def eyebrow(label, cls='section-eyebrow'):
    return text(f'<p class="{cls}">{label}</p>')


def section_head(eyebrow_label, title_html):
    return [eyebrow(eyebrow_label), heading(title_html, 'h2', 'section-title')]
