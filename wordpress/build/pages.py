"""Pages du site reconstruites en Elementor (contenu repris des pages Astro)."""
from elementor import (box, section, heading, text, html, shortcode, image, button,
                       cal_button, phone_button, accordion, eyebrow, section_head,
                       media_url, PHONE, PHONE_DISPLAY)

# ── Icônes SVG (identiques au site Astro) ─────────────────────────────────
def svg(paths, size=24, sw='1.8', fill='none'):
    stroke = '' if fill != 'none' else f' stroke="currentColor" stroke-width="{sw}"'
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}"{stroke}>{paths}</svg>'

CHECK_CIRCLE = '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>'
CHECK = '<polyline points="20 6 9 17 4 12"/>'
PHONE_P = '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/>'
MAIL_P = '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>'
PIN_P = '<path d="M20 10c0 7-8 12-8 12s-8-5-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'
BOLT = '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>'
SEARCH = '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'
USERS = '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>'
SHIELD = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
CHART = '<path d="M3 20h18M5 17V9M9 17V5M13 17v-7M17 17V7m-13-4 5-6 4 4 8-8"/>'
USER_P = '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/>'
CHEVRONS = '<path d="M7 13l5 5 5-5M7 6l5 5 5-5"/>'
TREND = '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>'
INFO = '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>'
CLOCK = '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'


def cta_band():
    return box('pa-shortcode-section', shortcode('[pa_cta_band]'))


def hero_simple(cls, eyebrow_label, title, lede, ctas=None):
    """Hero centré des pages intérieures (services, réalisations, contact)."""
    return section(cls, box('wrap',
        eyebrow(eyebrow_label, 'eyebrow'),
        heading(title, 'h1'),
        text(f'<p class="lede">{lede}</p>'),
        box('hero-ctas', *ctas) if ctas else None,
    ))


# ══════════════════════════════════════════════════════════════════════════
# ACCUEIL
# ══════════════════════════════════════════════════════════════════════════
def page_accueil():
    trust = ('<div class="trust-row">'
             f'<span class="item">{svg(CHECK_CIRCLE, 20, "2")} Sites rapides &amp; sécurisés</span>'
             f'<span class="item">{svg(CHART, 20, "2")} SEO technique &amp; contenu</span>'
             f'<span class="item">{svg(USER_P, 20, "2")} Accompagnement personnalisé</span>'
             '</div>')
    hero = section('hero', box('wrap', box('hero-grid',
        box('',
            eyebrow('Développeur Web &amp; Consultant SEO', 'eyebrow'),
            heading('Des sites performants.<br />Un meilleur référencement.<br />Plus de <span class="accent">résultats.</span>', 'h1'),
            text('<p class="lede">J\'aide les entreprises à se développer en ligne grâce à des sites web sur mesure, rapides et optimisés pour le SEO.</p>'),
            box('cta-row', cal_button('Réserver un appel gratuit →'), phone_button()),
            html(trust),
        ),
        image('hero-visual.webp', 'hero-visual', 'Paul Alves, développeur web et consultant SEO'),
    )), id='accueil')

    services_items = [
        ('<path d="m8 6-6 6 6 6"/><path d="m16 6 6 6-6 6"/>', 'Développement Web',
         'Sites vitrines, landing pages ou sites sur mesure. Modernes, rapides et adaptés à tous les appareils. Code propre, performances optimales.'),
        (SEARCH, 'Consultant SEO',
         'Audit SEO, optimisation technique, stratégie de contenu et netlinking pour améliorer votre visibilité sur Google et générer du trafic qualifié.'),
        ('<rect x="3" y="13" width="4" height="8"/><rect x="10" y="8" width="4" height="13"/><rect x="17" y="3" width="4" height="18"/>',
         'Performance &amp; SEO Local',
         'Suivi des performances, Core Web Vitals, optimisation de la fiche Google My Business et stratégie digitale locale sur mesure.'),
    ]
    services = section('', box('wrap',
        *section_head('Mes services', 'Des solutions digitales complètes pour votre <span class="accent">réussite</span> en ligne.'),
        box('services-grid', *[
            box('service',
                html(f'<div class="service-icon">{svg(icon, 22)}</div>'),
                heading(title, 'h3'),
                text(f'<p>{desc}</p>'))
            for icon, title, desc in services_items
        ]),
    ), id='services')

    about_list = '<ul class="about-list">' + ''.join(
        f'<li>{svg(CHECK_CIRCLE, 18, "2")} {t}</li>'
        for t in ('Sur le web depuis 2012', 'Des solutions sur mesure', 'Un seul objectif : vos résultats')
    ) + '</ul>'
    about = section('', box('wrap', box('about-grid',
        # Portrait à remettre quand une vraie photo sera disponible (cf. About.astro)
        html('<div class="about-photo about-photo--placeholder" aria-hidden="true">'
             f'<img src="{media_url("logo-mark.png")}" alt="" width="360" height="432" loading="lazy" decoding="async" /></div>'),
        box('about-body',
            eyebrow('À propos', 'eyebrow'),
            heading('Qui suis-je ?', 'h2'),
            text('<p>Je suis Paul Alves, développeur web et consultant SEO passionné par le digital et les résultats. Basé à Soissons, j\'accompagne des entreprises partout en France.</p>'
                 '<p>J\'aide les entreprises et entrepreneurs dans la création de sites web efficaces et dans l\'optimisation de leur référencement pour générer plus de trafic et de conversions.</p>'),
            html(about_list),
            button('Me contacter', '/#contact', 'btn btn-navy'),
        ),
    )), id='apropos')

    stats_items = [
        ('<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>',
         '2012', 'Premier site lancé'),
        ('<path d="M3 20h18m-16-6 5-6 4 4 8-8M17 4h4v4"/>', '+1M', 'Visiteurs organiques générés'),
        ('<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
         '0 €', 'De budget publicitaire'),
        ('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>', '14 ans', 'De WordPress et de SEO'),
    ]
    stats = section('stats', box('wrap', box('stats-grid', *[
        box('stat',
            html(f'<div class="stat-icon">{svg(icon, 32, "1.6")}</div>'),
            text(f'<div class="stat-num">{num}</div><div class="stat-label">{label}</div>'))
        for icon, num, label in stats_items
    ])))

    projects = section('projects', box('wrap',
        *section_head('Réalisation', 'Un site construit de zéro, jusqu\'au million de visiteurs'),
        box('case-grid',
            html('<a href="/a-propos/" class="case-img" aria-label="Voir le parcours de Paul Alves">'
                 f'<img src="{media_url("nosamisleschiens-card.webp")}" alt="Page d\'accueil de nosamisleschiens.fr, le blog canin créé par Paul Alves" width="600" height="380" loading="lazy" decoding="async" /></a>'),
            box('case-body',
                text('<span class="case-category">Blog éditorial, SEO, monétisation</span>'),
                heading('nosamisleschiens.fr', 'h3'),
                text('<p>Lancé en 2012 sans budget ni formation, ce site canin a dépassé le million de visiteurs organiques par an. Tout ce que je propose aujourd\'hui aux entreprises, je l\'ai d\'abord appliqué et mesuré ici : recherche de mots-clés, maillage interne, vitesse de chargement, acquisition de liens.</p>'
                     '<ul class="case-facts"><li><strong>+1M</strong> visiteurs organiques par an</li><li><strong>100 %</strong> de trafic SEO, sans publicité</li><li><strong>2012</strong> année de lancement</li></ul>'
                     '<a href="/a-propos/" class="project-link">Lire le parcours complet &nbsp;→</a>'),
            ),
        ),
    ), id='realisations')

    blog = section('blog-preview', box('wrap',
        *section_head('Blog', 'Derniers <span class="accent">articles</span>'),
        shortcode('[pa_derniers_articles nombre="3"]'),
    ), id='blog')

    return [hero, services, about, stats, projects, blog,
            box('pa-shortcode-section', shortcode('[pa_newsletter]')), cta_band()]


# ══════════════════════════════════════════════════════════════════════════
# SERVICES
# ══════════════════════════════════════════════════════════════════════════
SERVICES = [
    ('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>', 'Création de site WordPress', 'À partir de 1 500€', '2 – 4 semaines',
     ['Design personnalisé et responsive', 'Intégration de fonctionnalités avancées', 'Formation à l\'administration', 'Optimisation SEO de base', 'Conformité RGPD', 'Support post-lancement 30 jours']),
    ('<path d="M21 12a9 9 0 1 1-6.22-8.56"/><polyline points="21 3 21 9 15 9"/>', 'Refonte de site existant', 'À partir de 1 200€', '2 – 3 semaines',
     ['Audit complet de l\'existant', 'Nouveau design moderne', 'Migration de contenu sécurisée', 'Amélioration de l\'UX/UI', 'Optimisation des performances', 'Redirections 301 configurées']),
    (SEARCH, 'Optimisation SEO', 'À partir de 800€', '1 – 2 semaines',
     ['Audit SEO technique complet', 'Recherche de mots-clés stratégiques', 'Optimisation on-page', 'Amélioration de la vitesse', 'Configuration Search Console', 'Rapport mensuel de suivi']),
    (BOLT, 'Optimisation des performances', 'À partir de 600€', '3 – 5 jours',
     ['Audit de performance détaillé', 'Optimisation des images (WebP)', 'Mise en cache avancée', 'Minification CSS / JS', 'CDN et lazy loading', 'Score PageSpeed 90+']),
    (SHIELD, 'Sécurisation WordPress', 'À partir de 400€', '1 – 2 jours',
     ['Audit de sécurité complet', 'Installation firewall avancé', 'Sauvegardes automatiques', 'Certificat SSL', 'Monitoring 24/7', 'Rapport de sécurité détaillé']),
    ('<path d="M3 12a9 9 0 1 0 18 0 9 9 0 0 0-18 0"/><path d="M12 8v4l3 3"/>', 'Maintenance mensuelle', '150€ / mois', 'Abonnement',
     ['Mises à jour WordPress & plugins', 'Sauvegardes hebdomadaires', 'Monitoring de disponibilité', 'Corrections de bugs', 'Support technique prioritaire', 'Rapport mensuel détaillé']),
]
STEPS = [
    ('01', 'Découverte', 'Un appel gratuit de 30 minutes pour comprendre votre projet, vos objectifs et votre cible.'),
    ('02', 'Proposition', 'Un devis détaillé et transparent sous 24h, avec planning et livrables clairement définis.'),
    ('03', 'Réalisation', 'Développement itératif avec des points d\'avancement réguliers pour valider ensemble chaque étape.'),
    ('04', 'Livraison', 'Mise en ligne, formation à l\'administration et support post-lancement inclus.'),
]
FAQS = [
    ('Combien coûte la création d\'un site WordPress ?', 'La création d\'un site WordPress sur mesure démarre à 1 500€ pour un site vitrine. Le tarif varie selon la complexité, le nombre de pages et les fonctionnalités souhaitées (e-commerce, formulaires avancés, animations…). Je fournis un devis détaillé et transparent sous 24h après notre premier échange.'),
    ('Combien de temps faut-il pour créer un site web ?', 'La durée moyenne est de 2 à 4 semaines pour un site vitrine, et de 2 à 3 semaines pour une refonte. Le planning précis est défini dès la proposition commerciale avec des jalons clairs pour valider chaque étape ensemble. Une optimisation SEO ou de performances peut être réalisée en 3 à 5 jours.'),
    ('Travaillez-vous avec des clients en dehors de Soissons ?', 'Absolument. J\'interviens partout en France. Le travail s\'effectue majoritairement à distance via des outils collaboratifs (visioconférence, partage d\'écran, espaces de travail partagés). Je me déplace ponctuellement si le projet le justifie.'),
    ('Proposez-vous une maintenance après la création du site ?', 'Oui. Je propose une formule de maintenance mensuelle à 150€/mois qui inclut les mises à jour WordPress et plugins, les sauvegardes hebdomadaires, le monitoring de disponibilité 24h/24, les corrections de bugs et un support technique prioritaire avec rapport mensuel.'),
    ('Mon site existant peut-il être repris et amélioré ?', 'Oui, je propose une prestation de refonte de site existant à partir de 1 200€. Elle inclut un audit complet de l\'existant, un nouveau design, la migration sécurisée du contenu, l\'amélioration de l\'UX et la configuration des redirections 301 pour préserver votre référencement.'),
    ('Quel est votre délai de réponse ?', 'Je m\'engage à répondre à toutes les demandes dans les 24h en semaine. Vous pouvez également réserver directement un appel de découverte gratuit via mon calendrier en ligne pour convenir d\'un créneau qui vous convient.'),
]


def page_services():
    hero = hero_simple('services-hero', 'Mes services',
        'Des solutions digitales pour votre <span class="accent">réussite</span> en ligne',
        'Création, refonte, SEO, performances ou maintenance : j\'interviens sur toutes les dimensions de votre présence web WordPress pour générer des résultats concrets et durables.',
        [cal_button('Réserver un appel gratuit'), phone_button()])

    stats = section('stats', box('wrap', box('stats-grid', *[
        box('stat', text(f'<div class="stat-num">{n}</div><div class="stat-label">{l}</div>'))
        for n, l in [('14 ans', 'De WordPress et de SEO'), ('+1M', 'Visiteurs organiques générés'),
                     ('0 €', 'De budget publicitaire'), ('24h', 'Pour recevoir un devis')]
    ])))

    cards = []
    for icon, title, price, duration, features in SERVICES:
        feats = '<ul class="srv-features">' + ''.join(
            f'<li>{svg(CHECK, 14, "2.5")} {f}</li>' for f in features) + '</ul>'
        cards.append(box('srv-card',
            box('srv-header',
                html(f'<div class="srv-icon">{svg(icon)}</div>'),
                text(f'<div class="srv-meta"><span class="srv-price">{price}</span><span class="srv-duration">{duration}</span></div>')),
            heading(title, 'h3'),
            html(feats, 'pa-grow'),
            cal_button('Demander un devis', 'btn btn-outline srv-cta'),
        ))
    grid = section('services-section', box('wrap',
        *section_head('Ce que je propose', 'Choisissez la <span class="accent">prestation</span> adaptée à vos besoins'),
        box('srv-grid', *cards)), id='services-grid')

    process = section('process-section', box('wrap',
        *section_head('Comment ça marche', 'Un processus simple et <span class="accent">transparent</span>'),
        box('process-grid', *[
            box('process-step', text(f'<div class="step-num">{n}</div>'), heading(t, 'h3'), text(f'<p>{d}</p>'))
            for n, t, d in STEPS
        ])))

    faq = section('faq-section', box('wrap',
        *section_head('FAQ', 'Questions <span class="accent">fréquentes</span>'),
        box('faq-list', accordion(FAQS))), id='faq')

    return [hero, stats, grid, process, faq, cta_band()]


# ══════════════════════════════════════════════════════════════════════════
# À PROPOS
# ══════════════════════════════════════════════════════════════════════════
def page_a_propos():
    mockup = (
        '<div class="about-hero-photo">'
        '<div class="browser-mockup">'
        '<div class="browser-bar"><span class="browser-dot"></span><span class="browser-dot"></span><span class="browser-dot"></span>'
        '<span class="browser-url">nosamisleschiens.fr</span></div>'
        '<div class="browser-scroll" tabindex="0" aria-label="Aperçu du site nosamisleschiens.fr (faites défiler pour explorer)">'
        f'<img src="{media_url("nosamisleschiens-screenshot.webp")}" alt="Capture d\'écran du blog nosamisleschiens.fr, site canin lancé par Paul en 2012" width="800" height="7731" loading="lazy" decoding="async" />'
        '</div>'
        f'<div class="browser-hint" aria-hidden="true">{svg(CHEVRONS, 14, "2")} Faites défiler pour explorer</div>'
        '</div>'
        '<div class="photo-badge"><span class="badge-num">+1M</span><span class="badge-label">visiteurs<br/>organiques</span></div>'
        '</div>'
    )
    hero = section('about-hero', box('wrap', box('about-hero-grid',
        box('about-hero-text',
            eyebrow('À propos', 'eyebrow'),
            heading('De blogueur à <span class="accent">1 million de visiteurs</span>, puis consultant pour les entreprises', 'h1'),
            text('<p class="lede">Je ne suis pas devenu expert en WordPress et en SEO dans une école. Je l\'ai appris en construisant un site qui a attiré plus d\'un million de visiteurs et en faisant du référencement ma principale source de revenus.</p>'),
            box('hero-ctas', cal_button('Réserver un appel gratuit →'), phone_button()),
        ),
        html(mockup),
    )))

    timeline_items = [
        ('2012', SHIELD, False, 'Le premier pas dans le web',
         '<p>Passionné par les chiens, je lance <strong>nosamisleschiens.fr</strong>, un blog dédié au monde canin. Zéro budget, zéro formation : juste de la curiosité, une connexion internet et une envie de créer. Ce projet est mon premier terrain d\'apprentissage du web, du contenu et du référencement.</p>', ''),
        ('2012–<br/>2019', SEARCH, False, 'L\'école du SEO grandeur nature',
         '<p>Pendant sept ans, je teste, j\'analyse, j\'échoue et je recommence. J\'apprends le SEO <em>par la pratique</em> : recherche de mots-clés, optimisation on-page, maillage interne, acquisition de backlinks, vitesse de chargement… Chaque article publié est une expérience. Chaque hausse dans Google, une validation.</p>', ''),
        ('2019–<br/>2020', '<path d="M3 20h18M5 17V9M9 17V5M13 17v-7M17 17V7"/>', True, '+1 000 000 de visiteurs : la preuve par les chiffres',
         '<p>nosamisleschiens.fr franchit le cap du <strong>million de visiteurs organiques</strong>. Le site devient ma principale source de revenus grâce à la monétisation publicitaire et aux partenariats. Ce n\'est plus un hobby, c\'est une vraie activité digitale, entièrement construite sur du trafic SEO sans budget publicitaire.</p>',
         '<div class="tl-stat-row">'
         '<div class="tl-stat"><span class="tl-stat-num">+1M</span><span class="tl-stat-label">visiteurs/an</span></div>'
         '<div class="tl-stat"><span class="tl-stat-num">100%</span><span class="tl-stat-label">trafic organique</span></div>'
         '<div class="tl-stat"><span class="tl-stat-num">0€</span><span class="tl-stat-label">budget pub</span></div>'
         '</div>'),
        ('2025', '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>', False, 'Formation développeur WordPress chez OpenClassrooms',
         '<p>Fort de mon expérience terrain, je structure mes compétences techniques avec une formation certifiante de <strong>développeur WordPress sur OpenClassrooms</strong>. Je maîtrise désormais l\'ensemble de la chaîne : architecture, développement sur mesure, performances et intégration SEO. La théorie rejoint la pratique.</p>', ''),
        ('Aujourd\'hui', USERS, False, 'Consultant WordPress &amp; SEO pour les entreprises',
         '<p>J\'accompagne désormais les <strong>PME et les entrepreneurs solo</strong> qui veulent une présence web qui génère de vrais résultats : plus de trafic, plus de leads, plus de clients. Ce que j\'ai appris en construisant mon propre trafic, je le mets maintenant au service de vos objectifs, avec la rigueur d\'un développeur et l\'instinct d\'un référenceur.</p>', ''),
    ]
    timeline = section('timeline-section', box('wrap',
        *section_head('Mon parcours', 'Une histoire vraie, bâtie sur les <span class="accent">résultats</span>'),
        box('timeline', *[
            box('timeline-item' + (' tl-highlight' if hl else ''),
                text(f'<div class="tl-marker"><span class="tl-year">{year}</span></div>'),
                box('tl-card',
                    html(f'<div class="tl-icon{" tl-icon--gold" if hl else ""}">{svg(icon, 22)}</div>'),
                    heading(title, 'h3'),
                    text(body),
                    text(extra) if extra else None))
            for year, icon, hl, title, body, extra in timeline_items
        ])))

    values = [
        (BOLT, 'Performance avant tout', 'Un site lent, c\'est du chiffre d\'affaires perdu. J\'optimise chaque projet pour qu\'il soit rapide, fluide et bien positionné.'),
        (SEARCH, 'SEO ancré dans l\'expérience', 'J\'ai appris le référencement à la dure, en gérant un vrai site avec un vrai trafic. Pas de la théorie, du concret qui fonctionne.'),
        (USERS, 'Partenaire, pas prestataire', 'Je m\'implique dans votre réussite comme si c\'était mon propre business. Réactivité, transparence et résultats mesurables.'),
    ]
    values_sec = section('values-section', box('wrap',
        *section_head('Ma philosophie', 'Ce qui guide <span class="accent">chaque projet</span>'),
        box('values-grid', *[
            box('value-card', html(f'<div class="value-icon">{svg(icon)}</div>'), heading(t, 'h3'), text(f'<p>{d}</p>'))
            for icon, t, d in values
        ])))

    stack = ['WordPress', 'WooCommerce', 'Elementor', 'Kadence', 'Gutenberg', 'Rank Math', 'Yoast SEO', 'WP Rocket',
             'Imagify', 'Google Search Console', 'Google Analytics', 'PageSpeed Insights', 'Ahrefs', 'Semrush',
             'HTML / CSS', 'JavaScript', 'PHP', 'Git', 'Astro']
    stack_sec = section('stack-section', box('wrap',
        *section_head('Mes outils', 'Stack &amp; <span class="accent">compétences</span>'),
        text('<div class="stack-tags">' + ''.join(f'<span class="stack-tag">{s}</span>' for s in stack) + '</div>')))

    return [hero, timeline, values_sec, stack_sec, cta_band()]


# ══════════════════════════════════════════════════════════════════════════
# RÉALISATIONS
# ══════════════════════════════════════════════════════════════════════════
PROJECTS = [
    ('nosamisleschiens-card.webp', 'SEO', 'seo', 'nosamisleschiens.fr, blog canin à plus d\'un million de visiteurs',
     'Mon propre site, lancé en 2012 sans budget. Recherche de mots-clés, architecture, maillage interne, vitesse et acquisition de liens : tout a été construit et mesuré ici avant d\'être proposé aux entreprises.',
     ['WordPress', 'Stratégie éditoriale', 'Maillage interne', 'Monétisation'], '+1M de visiteurs organiques par an, 0 € de publicité', '/a-propos/'),
    ('photo-1460925895917-afdab827c52f.webp', 'Site vitrine', 'site-vitrine', 'Site vitrine WordPress pour TPE et indépendants',
     'Mission type : conception sur mesure, pages services optimisées pour le SEO local, formulaire de contact fiable, formation à la prise en main. Livré prêt à être trouvé sur Google.',
     ['WordPress', 'Kadence', 'Rank Math', 'WP Rocket'], None, None),
    ('photo-1556742049-0cfed4f6a45d.webp', 'E-commerce', 'e-commerce', 'Boutique en ligne WooCommerce',
     'Mission type : catalogue et fiches produits, paiement Stripe ou PayPal, livraison, tunnel d\'achat épuré, suivi des ventes dans Google Analytics.',
     ['WooCommerce', 'Stripe', 'Imagify', 'GA4'], None, None),
    ('photo-1551288049-bebda4e38f71.webp', 'Audit SEO', 'audit-seo', 'Audit SEO et plan d\'action',
     'Mission type : audit technique, on-page et contenu, priorisé par impact. Vous repartez avec une liste d\'actions claire, que vous pouvez appliquer vous-même ou me confier.',
     ['Search Console', 'Screaming Frog', 'Schema.org', 'Core Web Vitals'], None, None),
    ('photo-1531973576160-7125cd663d86.webp', 'Refonte', 'refonte', 'Refonte de site existant sans perdre le référencement',
     'Mission type : nouveau design, migration du contenu, redirections 301, contrôle des positions avant et après la mise en ligne.',
     ['WordPress', 'Redirections 301', 'SEO', 'Performance'], None, None),
    ('photo-1504868584819-f8e8b4b6d7e3.webp', 'Performance', 'performance', 'Optimisation de la vitesse de chargement',
     'Mission type : diagnostic PageSpeed, images, cache, polices, scripts tiers, choix d\'hébergement. Objectif : des Core Web Vitals au vert sur mobile.',
     ['WP Rocket', 'Imagify', 'Cloudflare', 'LiteSpeed'], None, None),
    ('photo-1563986768609-322da13575f3.webp', 'Maintenance', 'maintenance', 'Maintenance et sécurité mensuelles',
     'Mission type : mises à jour testées, sauvegardes externalisées, surveillance de disponibilité, correctifs et rapport mensuel.',
     ['Wordfence', 'UpdraftPlus', 'Monitoring', 'SSL'], None, None),
]
FILTERS = [('Tous', 'tous'), ('Site vitrine', 'site-vitrine'), ('E-commerce', 'e-commerce'), ('Audit SEO', 'audit-seo'),
           ('Refonte', 'refonte'), ('Performance', 'performance'), ('Maintenance', 'maintenance')]


def page_realisations():
    hero = hero_simple('real-hero', 'Réalisations',
        'Des projets concrets,<br />des <span class="accent">résultats mesurables</span>',
        'Un projet documenté de bout en bout, le mien, et le détail de ce que comprend chaque type de mission. Les projets clients seront ajoutés avec leur accord.')

    filters = '<div class="filters" id="filters">' + ''.join(
        f'<button class="filter-btn{" active" if i == 0 else ""}" data-filter="{slug}">{label}</button>'
        for i, (label, slug) in enumerate(FILTERS)) + '</div>'

    cards = []
    for img, cat, slug, title, desc, tags, result, href in PROJECTS:
        alt = title if href else ''
        role = '' if href else ' role="presentation"'
        img_html = (f'<img src="{media_url(img)}" alt="{alt}"{role} width="600" height="380" loading="lazy" />'
                    f'<span class="real-card-category">{cat}</span>')
        img_block = (f'<a href="{href}" class="real-card-img-wrap">{img_html}</a>' if href
                     else f'<div class="real-card-img-wrap">{img_html}</div>')
        result_html = (f'<div class="real-card-result">{svg(TREND, 15, "2.5")} {result}</div>'
                       if result else '')
        cards.append(box(f'real-card real-cat-{slug}' + (' is-real' if href else ''),
            html(img_block),
            box('real-card-body',
                heading(title, 'h3', link=href),
                text(f'<p>{desc}</p>', 'pa-grow'),
                text('<div class="real-card-tags">' + ''.join(f'<span class="real-tag">{t}</span>' for t in tags) + '</div>'),
                html(result_html) if result_html else None),
            tag='article'))

    note = html('<div class="placeholder-note">'
                f'{svg(INFO, 18, "2")}'
                'Les cartes « mission type » décrivent le contenu d\'une prestation, pas un client. Seul nosamisleschiens.fr est un projet réel et chiffré.</div>')

    grid = section('projects-section', box('wrap', html(filters), box('real-grid', *cards, id='projectsGrid'), note))

    stats = section('real-stats', box('wrap', box('real-stats-grid', *[
        box('real-stat', text(f'<span class="real-stat-num">{n}</span><span class="real-stat-label">{l}</span>'))
        for n, l in [('2012', 'Premier site lancé'), ('+1M', 'Visiteurs organiques par an'),
                     ('0 €', 'De budget publicitaire'), ('24h', 'Pour recevoir un devis')]
    ])))
    return [hero, grid, stats, cta_band()]


# ══════════════════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════════════════
def page_contact():
    hero = hero_simple('contact-hero', 'Contact', 'Parlons de votre <span class="accent">projet</span>',
        'Un nouveau site, une refonte ou du SEO ? Décrivez votre besoin, je reviens vers vous sous 24h avec une première analyse.')

    info = ('<ul class="contact-info-list">'
            f'<li><div class="ci-icon">{svg(MAIL_P, 18, "2")}</div><a href="mailto:contact@paul-alves.fr">contact@paul-alves.fr</a></li>'
            f'<li><div class="ci-icon">{svg(PHONE_P, 18, "2")}</div><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></li>'
            f'<li><div class="ci-icon">{svg(PIN_P, 18, "2")}</div><span>Soissons, remote toute la France</span></li>'
            '</ul>')
    guarantees = '<ul class="cal-guarantees">' + ''.join(
        f'<li>{svg(CHECK, 14, "2.5")} {t}</li>'
        for t in ('Réponse de confirmation sous 24h', 'Annulation possible à tout moment', 'Aucune vente forcée')) + '</ul>'
    response = ('<div class="response-time">'
                f'{svg(CLOCK, 22)}'
                '<div><strong>Réponse sous 24h</strong><span>Du lundi au vendredi</span></div></div>')

    aside = box('contact-aside',
        box('aside-card', heading('Coordonnées', 'h3'), html(info)),
        box('aside-card aside-card--navy',
            text('<div class="cal-badge">Gratuit · Sans engagement</div>'),
            heading('Préférez un appel ?', 'h3'),
            text('<p>Réservez un créneau de <strong>30 minutes</strong> directement dans mon calendrier. On discute de votre projet, je vous donne une première analyse, sans engagement.</p>'),
            cal_button('Réserver un appel gratuit', 'btn btn-gold cal-btn', icon='far fa-calendar'),
            html(guarantees)),
        box('aside-card aside-card--light', html(response)),
        tag='aside')

    body = section('contact-section', box('wrap', box('contact-grid', shortcode('[pa_contact_form]'), aside)))
    return [hero, body]


# ══════════════════════════════════════════════════════════════════════════
# PAGES LÉGALES ET PLAN DU SITE
# ══════════════════════════════════════════════════════════════════════════
def page_legal(title, content_html):
    return [section('legal-section', box('wrap wrap--narrow',
        eyebrow('Légal', 'eyebrow'),
        heading(title, 'h1', 'legal-h1', inherit=False),
        text(f'<div class="legal-content">{content_html}</div>')))]


def page_plan_du_site():
    hero = section('sitemap-hero', box('wrap',
        eyebrow('Navigation', 'eyebrow'),
        heading('Plan du site', 'h1'),
        text('<p class="lede">Toutes les pages du site, organisées par thématique. Pour le sitemap XML utilisé par les moteurs de recherche, voir <a href="/sitemap_index.xml">sitemap_index.xml</a>.</p>')))
    body = section('sitemap-body', box('wrap', shortcode('[pa_plan_du_site]')))
    return [hero, body]
