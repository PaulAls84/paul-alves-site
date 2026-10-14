# Backlog éditorial : routine de rédaction automatique

La routine (tous les 3 jours, 8h) prend le **premier sujet `status: todo`** de la
liste ci-dessous, rédige l'article, le publie, puis passe son `status` à `done`
avec la date de publication.

Quand il ne reste plus de sujet `todo`, la routine ne publie rien et signale que
le backlog est vide → il faut alors le réalimenter (relancer une analyse de
mots-clés Cuik / Search Console et ajouter de nouvelles entrées).

Données de volume : Google Ads Keyword Planner (France, FR), relevé 2026-06-30.

---

## File d'attente

Volumes : estimations à valider au Keyword Planner (France, FR) au prochain relevé.

Réalimentée le 2026-10-14 (Keyword Planner France via Cuik + Search Console 07-10/2026).
Sujets choisis parmi les clusters non couverts par les 35 articles déjà publiés.

### 31. Consultant SEO freelance : comment le choisir et ce qu'il doit livrer
- **status:** todo
- **slug:** consultant-seo-freelance
- **mot-clé principal:** consultant seo (2 900/mois) + consultant seo freelance (880/mois) + consultant seo wordpress (390/mois) + consultant seo local (390/mois), concurrence faible
- **catégorie:** SEO
- **angle:** page à intention commerciale, pendant SEO de developpeur-wordpress-freelance : ce que fait (et ne fait pas) un consultant SEO, freelance contre agence, les livrables à exiger (audit priorisé, plan d'action, suivi Search Console), les promesses qui doivent alerter (positions garanties, packs de liens), les questions à poser avant de signer. Conflit d'intérêts annoncé en intro (Paul est consultant SEO). Tarifs : uniquement ceux de la page Services (optimisation SEO dès 800 €), aucune moyenne de marché inventée. Ne citer aucun consultant concurrent par son nom.
- **maillage interne suggéré:** developpeur-wordpress-freelance, audit-seo-wordpress, seo-wordpress, referencement-local, page Services

### 32. Google Search Console : le guide pour bien démarrer
- **status:** todo
- **slug:** google-search-console
- **mot-clé principal:** search console google (2 900/mois) + google search console seo (90/mois) + google search console gratuit (50/mois), concurrence faible (le terme « google search console » seul est surtout navigationnel)
- **catégorie:** SEO
- **angle:** guide pratique pour un propriétaire de site : ajouter et valider son site (propriété domaine ou préfixe d'URL), envoyer le sitemap, lire le rapport Performances (requêtes, pages, CTR, position), repérer les pages non indexées et leurs motifs, inspecter une URL, les erreurs fréquentes. Captures décrites en texte, pas d'images inventées.
- **maillage interne suggéré:** audit-seo-wordpress, recherche-mots-cles, seo-wordpress, sitemap-wordpress

### 33. Maillage interne : la méthode pour relier vos pages et mieux ranker
- **status:** todo
- **slug:** maillage-interne
- **mot-clé principal:** maillage interne (590/mois) + maillage interne seo (320/mois) + seo maillage interne (110/mois), concurrence faible
- **catégorie:** SEO
- **angle:** à quoi sert le maillage (exploration, transmission de popularité, parcours lecteur), structure en silos ou pages piliers, choix des ancres, nombre de liens raisonnable, pages orphelines, outils pour l'auditer (Search Console liens internes, crawler gratuit), et comment faire sur WordPress (liens manuels, blocs « articles liés », limites des plugins de maillage automatique).
- **maillage interne suggéré:** seo-wordpress, recherche-mots-cles, audit-seo-wordpress, backlinks

### 34. Balise title et meta description : les écrire pour gagner des clics
- **status:** todo
- **slug:** balise-title-meta-description
- **mot-clé principal:** meta description (720/mois) + balise title (260/mois) + méta description (170/mois) + metadescription wordpress (90/mois) + meta title et meta description (50/mois), concurrence faible
- **catégorie:** SEO
- **angle:** rôle de chacune (la title compte pour le classement, la meta description pour le clic), longueurs utiles en pixels et caractères, pourquoi Google réécrit parfois, formules qui fonctionnent par type de page (accueil, service, article, fiche produit), erreurs fréquentes (doublons, bourrage de mots-clés), et où les renseigner sur WordPress (Rank Math, Yoast). Exemples réécrits avant/après présentés comme des situations types.
- **maillage interne suggéré:** rank-math-ou-yoast, seo-wordpress, audit-seo-wordpress, recherche-mots-cles

### 35. SEO e-commerce : référencer sa boutique WooCommerce
- **status:** todo
- **slug:** seo-e-commerce
- **mot-clé principal:** seo e commerce (590/mois) + seo site e commerce (50/mois) + optimisation site e commerce (40/mois), concurrence moyenne
- **catégorie:** SEO
- **angle:** les spécificités d'une boutique : architecture catégories/produits, fiches produits uniques (pas de description fournisseur copiée), pages catégories rédigées, filtres et pagination (duplication, indexation), produits en rupture, données structurées Product, vitesse. Focus WooCommerce, PrestaShop et Shopify cités pour comparaison sans les dénigrer.
- **maillage interne suggéré:** creer-boutique-woocommerce, hebergement-woocommerce, wordpress-ou-shopify, seo-wordpress, core-web-vitals

### 36. Données structurées : le guide SEO pour WordPress
- **status:** todo
- **slug:** donnees-structurees
- **mot-clé principal:** données structurées (590/mois) + donnees structurees (210/mois) + données structurées seo (140/mois), concurrence faible (attention : une partie des recherches vient de l'enseignement SNT, cibler l'intention SEO)
- **catégorie:** SEO
- **angle:** ce que sont les données structurées (schema.org, JSON-LD), ce qu'elles apportent réellement (résultats enrichis possibles, jamais garantis), les types utiles pour une PME (Organization, LocalBusiness, Article, FAQ, Product, Breadcrumb), comment les ajouter sur WordPress (Rank Math, Yoast, manuellement), et comment les tester (outil de test des résultats enrichis, rapports Search Console).
- **maillage interne suggéré:** seo-wordpress, rank-math-ou-yoast, referencement-local, seo-e-commerce

### 37. Sitemap XML WordPress : le créer, l'envoyer, le corriger
- **status:** todo
- **slug:** sitemap-wordpress
- **mot-clé principal:** sitemap wordpress (480/mois) + sitemap xml wordpress (480/mois) + sitemap yoast seo (30/mois), concurrence faible
- **catégorie:** SEO
- **angle:** ce qu'est un sitemap et ce qu'il ne fait pas (il n'oblige pas Google à indexer), le sitemap natif de WordPress (wp-sitemap.xml) contre celui de Rank Math ou Yoast (ne jamais en garder deux), quoi exclure (pages de remerciement, archives inutiles), l'envoi dans la Search Console et la lecture des erreurs « URL envoyée non indexée ».
- **maillage interne suggéré:** google-search-console, rank-math-ou-yoast, seo-wordpress, audit-seo-wordpress

### 38. Nom de domaine : choisir et acheter le bon pour un site pro
- **status:** todo
- **slug:** nom-de-domaine
- **mot-clé principal:** trouver un nom de domaine (320/mois) + extension du nom de domaine (170/mois) + choisir un nom de domaine (110/mois) + nom de domaine pour site internet (110/mois), concurrence élevée sur les annonces mais intention informationnelle
- **catégorie:** WordPress
- **monétisation:** affiliation
- **angle:** les critères d'un bon nom (court, prononçable, sans tiret si possible, marque plutôt que mot-clé), .fr ou .com et les autres extensions, vérifier la disponibilité et les droits de marque, où l'acheter (bureau d'enregistrement ou hébergeur), prix réels publics, renouvellement, et le piège classique : le domaine enregistré au nom du prestataire. Hébergeurs et registraires cités selon le tableau d'affiliation (sans lien tant que `<À REMPLIR>`).
- **maillage interne suggéré:** creer-un-site-wordpress, hebergement-wordpress, meilleur-hebergeur-wordpress, migrer-site-wordpress

### 39. Rédaction web SEO : écrire des pages qui se positionnent
- **status:** todo
- **slug:** redaction-web-seo
- **mot-clé principal:** rédaction seo (480/mois) + rédaction web seo freelance (480/mois) + rédaction web seo (320/mois) + rédacteur seo (260/mois), concurrence faible
- **catégorie:** SEO
- **angle:** méthode pour écrire une page utile et bien positionnée : intention de recherche d'abord, plan à partir des questions réelles, titres, paragraphes courts, champ lexical sans bourrage, éléments qui font la différence (exemples, tableaux, réponse directe en tête), mise à jour des contenus. Position honnête sur les textes générés par IA : utiles comme brouillon, jamais publiés sans relecture et apport réel.
- **maillage interne suggéré:** recherche-mots-cles, balise-title-meta-description, maillage-interne, seo-wordpress

### 40. Google Analytics 4 sur WordPress : l'installer proprement (et légalement)
- **status:** todo
- **slug:** google-analytics-wordpress
- **mot-clé principal:** google analytics wordpress (140/mois) + google analytics wp (140/mois) + monsterinsight (140/mois), concurrence faible
- **catégorie:** Plugins
- **angle:** les trois façons d'installer GA4 (Site Kit de Google, MonsterInsights, balise manuelle), le consentement obligatoire (bandeau cookies, Consent Mode v2), les événements utiles pour une PME (formulaire envoyé, clic téléphone, prise de rendez-vous), et les alternatives sans cookie (Matomo, Plausible) à citer sans lien.
- **maillage interne suggéré:** rgpd-wordpress, meilleur-plugin-wordpress, google-search-console

### 41. Landing page WordPress : créer une page qui convertit
- **status:** todo
- **slug:** landing-page-wordpress
- **mot-clé principal:** landing page wordpress (140/mois) + landing page wp (140/mois), concurrence moyenne
- **catégorie:** WordPress
- **angle:** ce qui distingue une landing page d'une page classique (un seul objectif, une seule action), la structure qui convertit (promesse, preuves, objections, appel à l'action), avec quoi la construire sur WordPress (éditeur de blocs, Elementor, thème léger), la vitesse et le suivi des conversions. Aucune preuve sociale inventée dans les exemples.
- **maillage interne suggéré:** elementor-ou-gutenberg, meilleur-theme-wordpress, optimiser-vitesse-site-wordpress, google-analytics-wordpress

### 42. Paiement WooCommerce : Stripe, PayPal ou les deux ?
- **status:** todo
- **slug:** paiement-woocommerce
- **mot-clé principal:** woocommerce stripe (140/mois) + plugin stripe woocommerce + paiement en plusieurs fois stripe (longue traîne), concurrence moyenne
- **catégorie:** WordPress
- **angle:** comparatif des passerelles pour une boutique française : WooCommerce Stripe, PayPal Payments, solutions bancaires françaises, frais publics à citer uniquement depuis les grilles officielles (vérifier, ne jamais inventer), 3D Secure, paiement en plusieurs fois, et les erreurs de configuration fréquentes (mode test oublié, webhooks).
- **maillage interne suggéré:** creer-boutique-woocommerce, hebergement-woocommerce, seo-e-commerce, securiser-site-wordpress

---

## Affiliation (monétisation)

Pour les articles tagués `monétisation: affiliation`, la routine insère les liens
affiliés du tableau ci-dessous (attribut `rel="sponsored nofollow"`) et ajoute une
**mention de transparence** en début d'article.

**Tant qu'un lien vaut `<À REMPLIR>`, la routine cite le service SANS lien** (elle
n'invente jamais de lien affilié). Paul doit s'inscrire lui-même aux programmes et
coller ses liens ici.

Légende : ⭐ = correspond à un article déjà publié ou au backlog (monétise tout de suite) · 🔁 = commission récurrente.

**Hébergement** (commission one-shot, gros panier)
| Service | Lien affilié | Note |
|---|---|---|
| Hostinger ⭐ | `<À REMPLIR>` | déjà client, bon programme FR |
| o2switch ⭐ | `<À REMPLIR>` | hébergeur FR très apprécié |
| OVHcloud ⭐ | `<À REMPLIR>` | leader FR |
| Infomaniak ⭐ | `<À REMPLIR>` | FR/Suisse, éco-responsable |
| PlanetHoster | `<À REMPLIR>` | FR/Canada |
| Kinsta 🔁 | `<À REMPLIR>` | managed premium, grosse commission |
| Cloudways 🔁 | `<À REMPLIR>` | cloud infogéré, récurrent |

**Builders & thèmes** (correspond au comparatif thèmes + création)
| Service | Lien affilié | Note |
|---|---|---|
| Elementor Pro ⭐🔁 | `<À REMPLIR>` | builder n°1, récurrent |
| Divi / Elegant Themes ⭐ | `<À REMPLIR>` | très populaire |
| Astra ⭐🔁 | `<À REMPLIR>` | thème léger, récurrent |
| GeneratePress | `<À REMPLIR>` | thème dev, performant |

**Performance** (correspond à ton article « optimiser la vitesse »)
| Service | Lien affilié | Note |
|---|---|---|
| WP Rocket ⭐🔁 | `<À REMPLIR>` | cache n°1, FR, **top priorité** |
| Imagify ⭐🔁 | `<À REMPLIR>` | optim images, FR (même éditeur que WP Rocket) |

**SEO** (ton cœur de métier + articles SEO)
| Service | Lien affilié | Note |
|---|---|---|
| Rank Math Pro ⭐🔁 | `<À REMPLIR>` | plugin SEO, récurrent |
| SEOPress ⭐🔁 | `<À REMPLIR>` | plugin SEO **français** |
| Semrush 🔁 | `<À REMPLIR>` | outil SEO, bonne commission |

**Sauvegarde & sécurité** (correspond aux articles maintenance/sauvegarde)
| Service | Lien affilié | Note |
|---|---|---|
| UpdraftPlus ⭐🔁 | `<À REMPLIR>` | sauvegarde n°1 |
| Solid Security (ex-iThemes) 🔁 | `<À REMPLIR>` | sécurité |

**Email / marketing**
| Service | Lien affilié | Note |
|---|---|---|
| Systeme.io ⭐🔁 | `<À REMPLIR>` | **déjà utilisé sur le site**, 40 % récurrent |
| Brevo (ex-Sendinblue) 🔁 | `<À REMPLIR>` | emailing FR |

**Mention de transparence à insérer**, UNIQUEMENT si l'article contient au
moins un vrai lien affilié (≠ `<À REMPLIR>`). Un article qui cite des services
sans lien affilié ne porte PAS de mention :
> *Cet article contient des liens affiliés. Si vous souscrivez via l'un d'eux, je peux percevoir une commission, sans surcoût pour vous.*

---

## Publiés

### Développeur WordPress freelance : comment le choisir
- **status:** done : 2026-10-01
- **slug:** developpeur-wordpress-freelance
- **mot-clé principal:** développeur wordpress freelance (140/mois) + developpeur freelance wordpress (140/mois), concurrence moyenne. Page à intention commerciale : comparatif freelance / agence / plateforme (Malt citée sans dénigrement, commission mentionnée sans chiffre inventé), forfait contre TJM, les sept questions à poser avant de signer, six signaux d'alerte. Conflit d'intérêts annoncé en intro (Paul est lui-même freelance) et deuxième cas type où l'agence est le bon choix, pour rester honnête. Tarifs cités : uniquement les tarifs publics de la page Services (création dès 1 500 €, refonte dès 1 200 €, SEO dès 800 €, performances dès 600 €, sécurisation dès 400 €, maintenance 150 €/mois), aucune moyenne de marché inventée. Aucun service lié en affiliation, donc pas de mention de transparence. Maillage vers prix-site-wordpress, maintenance-wordpress, creer-un-site-wordpress, et les pages services et contact. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Backlinks : obtenir des liens de qualité sans pénalité
- **status:** done : 2026-09-30
- **slug:** backlinks
- **mot-clé principal:** backlinks (2 400/mois) + backlinks de qualité (70/mois) + backlink toxique (50/mois), concurrence moyenne. Ce qu'est un bon lien (pertinence, trafic réel de la page liante, ancre, contexte), les six techniques réalistes pour une PME (annuaires locaux et professionnels, partenaires et fournisseurs, presse locale, contenu de référence, liens cassés, mentions non liées) avec un tableau effort/délai/risque, les pratiques à fuir (packs de liens, PBN, échanges systématiques, sur-optimisation des ancres) et l'audit du profil de liens via la Search Console, avec la réserve de Google sur l'outil de désaveu. Aucun service lié en affiliation (aucun outil SEO cité avec lien), donc pas de mention de transparence. Maillage vers referencement-local, recherche-mots-cles, audit-seo-wordpress, seo-wordpress et la page contact. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Recherche de mots-clés : trouver ceux qui rapportent
- **status:** done : 2026-09-28
- **slug:** recherche-mots-cles
- **mot-clé principal:** recherche de mots clés (320/mois) + mots clés seo (480/mois) + trouver des mots clés (260/mois), concurrence moyenne. Méthode pour une PME : les quatre intentions de recherche, la Search Console et les suggestions Google avant tout outil payant, le Keyword Planner et ses limites, la longue traîne (tableau comparatif), puis la transformation de la liste en plan de pages en quatre étapes. Aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence : Semrush, Ahrefs et Ubersuggest sont cités SANS lien. Maillage vers audit-seo-wordpress, seo-wordpress, referencement-local. Cas présentés comme des situations types (artisan local, boutique de niche) : `cas-clients.md` est toujours vide.

### Formulaire de contact WordPress : quel plugin choisir
- **status:** done : 2026-09-25
- **slug:** formulaire-contact-wordpress
- **mot-clé principal:** formulaire de contact wordpress (110/mois) + formulaire wordpress (70/mois) + plugin formulaire wordpress (20/mois), concurrence moyenne. Comparatif Contact Form 7 / WPForms Lite / Fluent Forms / Gravity Forms, plus les formulaires natifs d'Elementor et Divi, arbitré par le profil de celui qui gérera le site. Tableau de synthèse, installation pas à pas, envoi SMTP authentifié (SPF/DKIM/DMARC), anti-spam (honeypot, Turnstile, Akismet) et RGPD. Aucun des services cités ne figure au tableau d'affiliation : cités SANS lien, donc pas de mention de transparence. Maillage vers rgpd-wordpress, creer-un-site-wordpress, meilleur-plugin-wordpress, sauvegarde-wordpress. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Fiche d'établissement Google : créer, optimiser, réactiver
- **status:** done : 2026-09-21
- **slug:** fiche-etablissement-google
- **mot-clé principal:** créer une fiche google my business (590/mois) + fiche google suspendue (210/mois) + fiche établissement google (2 900/mois), concurrence faible. Guide opérationnel TPE/artisans : création, validation (dont la vidéo), champs qui comptent, avis et posts, puis la procédure complète de réactivation d'une fiche suspendue (tableau des motifs). Renvoi explicite vers referencement-local pour la stratégie d'ensemble, sans doublonner sa section fiche. Aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence. Maillage vers referencement-local et seo-wordpress. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Site WordPress multilingue : WPML, Polylang ou Weglot
- **status:** done : 2026-09-18
- **slug:** wordpress-multilingue
- **mot-clé principal:** site multilingue wordpress (110/mois) + wordpress multilingue (70/mois) + wpml (90/mois) + weglot wordpress (50/mois), concurrence moyenne. Comparatif WPML / Polylang / Weglot arbitré par le modèle (traduction stockée en base contre service externe), plus TranslatePress et multisite cités en alternatives. Weglot et WPML ne figurent pas dans le tableau d'affiliation : cités SANS lien, donc pas de mention de transparence, à reprendre si les liens sont renseignés. Maillage vers seo-wordpress, creer-boutique-woocommerce, meilleur-plugin-wordpress, maintenance-wordpress, sauvegarde-wordpress, optimiser-vitesse-site-wordpress, rgpd-wordpress. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Plugin de cache WordPress : lequel choisir en 2026
- **status:** done : 2026-09-14
- **slug:** plugin-cache-wordpress
- **mot-clé principal:** cache wordpress (110/mois) + plugin cache wordpress (70/mois) + wp super cache (110/mois) + wp fastest cache (110/mois), concurrence faible. Comparatif LiteSpeed Cache / WP Rocket / WP Super Cache / W3 Total Cache, arbitré par le type de serveur. WP Rocket cité SANS lien affilié (lien non renseigné), donc pas de mention de transparence : à reprendre quand le lien sera rempli. Maillage vers wp-rocket-avis, optimiser-vitesse-site-wordpress, hebergement-wordpress, hebergement-woocommerce, core-web-vitals, sauvegarde-wordpress. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Core Web Vitals : comprendre et corriger sur WordPress
- **status:** done : 2026-09-11
- **slug:** core-web-vitals
- **mot-clé principal:** core web vitals (1 000/mois), concurrence faible. Aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence. Maillage vers optimiser-vitesse-site-wordpress, wp-rocket-avis, hebergement-wordpress, audit-seo-wordpress. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Audit SEO WordPress : la checklist complète en 6 blocs
- **status:** done : 2026-09-08
- **slug:** audit-seo-wordpress
- **mot-clé principal:** audit seo wordpress (390/mois) + audit technique seo (590/mois) + audit seo site (320/mois), concurrence faible. Aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence. CTA discret vers l'audit offert (page contact). Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Erreur WordPress : 500, erreur critique, page blanche
- **status:** done : 2026-09-04
- **slug:** erreur-wordpress
- **mot-clé principal:** erreur 500 wordpress (110/mois) + erreur critique wordpress (40/mois) + erreur 404 wordpress (90/mois), concurrence faible à moyenne. Aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence. Cas présentés comme des situations types : `cas-clients.md` est toujours vide.

### Référencement local : faire apparaître son entreprise sur Google [2026]
- **status:** done : 2026-08-28
- **slug:** referencement-local
- **mot-clé principal:** référencement local / google my business (volume à valider, concurrence moyenne), aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence. Cas présentés comme des situations types : `cas-clients.md` est vide.

### RGPD et WordPress : mettre son site en conformité [2026]
- **status:** done : 2026-08-25
- **slug:** rgpd-wordpress
- **mot-clé principal:** rgpd wordpress / bandeau cookies wordpress (volume à valider, concurrence faible), aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence

### Mettre à jour WordPress sans rien casser : la procédure [2026]
- **status:** done : 2026-08-21
- **slug:** mise-a-jour-wordpress
- **mot-clé principal:** mise à jour wordpress (volume à valider, concurrence faible), aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence

### WordPress ou Shopify : que choisir pour vendre en ligne en [2026] ?
- **status:** done 2026-08-18
- **slug:** wordpress-ou-shopify
- **mot-clé principal:** shopify ou wordpress / woocommerce ou shopify (volume à valider, concurrence moyenne), aucun service lié en affiliation (liens non renseignés), donc pas de mention de transparence

### WP Rocket : mon avis et le guide de configuration [2026]
- **status:** done 2026-08-15
- **slug:** wp-rocket-avis
- **mot-clé principal:** wp rocket avis / wp rocket (volume à valider, concurrence moyenne), WP Rocket et Imagify cités SANS lien (affiliation non renseignée), donc pas de mention de transparence. À reprendre quand le lien affilié WP Rocket sera rempli.

### Rank Math ou Yoast : quel plugin SEO pour WordPress [2026]
- **status:** done 2026-08-12
- **slug:** rank-math-ou-yoast
- **mot-clé principal:** yoast ou rank math / plugin seo wordpress (volume à valider, concurrence moyenne), Rank Math Pro et SEOPress cités sans lien (affiliation non renseignée), donc pas de mention de transparence

### Elementor ou Gutenberg : quel éditeur choisir [2026]
- **status:** done 2026-08-09
- **slug:** elementor-ou-gutenberg
- **mot-clé principal:** elementor ou gutenberg / elementor avis (volume à valider, concurrence moyenne), Elementor Pro cité sans lien (affiliation non renseignée), donc pas de mention de transparence

### Site WordPress piraté : que faire (et comment l'éviter) [2026]
- **status:** done 2026-08-06
- **slug:** site-wordpress-pirate
- **mot-clé principal:** site wordpress piraté / wordpress hacké (volume à valider, concurrence faible), services de sécurité cités sans lien (affiliation non renseignée)

### Migrer son site WordPress sans perdre son SEO : le guide complet [2026]
- **status:** done 2026-08-03
- **slug:** migrer-site-wordpress
- **mot-clé principal:** migrer site wordpress / migration site wordpress (90/mois, concurrence moyenne), affiliation hébergeur

### Créer une boutique en ligne avec WooCommerce : le guide pas à pas [2026]
- **status:** done 2026-07-30
- **slug:** creer-boutique-woocommerce
- **mot-clé principal:** boutique en ligne wordpress (140/mois) + woocommerce boutique (90/mois)

### Meilleur thème WordPress : le comparatif [2026]
- **status:** done 2026-07-27
- **slug:** meilleur-theme-wordpress
- **mot-clé principal:** meilleur thème wordpress (170/mois) + thème wordpress gratuit (880/mois), affiliation thème

### Hébergement WooCommerce : quel hébergeur pour sa boutique
- **status:** done 2026-07-24
- **slug:** hebergement-woocommerce
- **mot-clé principal:** hébergement woocommerce (390/mois, concurrence faible), affiliation hébergeur

### Meilleur hébergeur WordPress : le comparatif [2026]
- **status:** done 2026-07-21
- **slug:** meilleur-hebergeur-wordpress
- **mot-clé principal:** meilleur hébergeur wordpress / meilleur hébergement wordpress (720/mois, concurrence faible), article phare de monétisation (affiliation hébergeur)

### Hébergement WordPress : comment bien choisir
- **status:** done 2026-07-18
- **slug:** hebergement-wordpress
- **mot-clé principal:** hébergement wordpress / hébergeur wordpress (8100/mois, concurrence faible), TRÈS gros volume

### Sécuriser son site WordPress
- **status:** done 2026-07-15
- **slug:** securiser-site-wordpress
- **mot-clé principal:** sécuriser site wordpress / sécuriser wordpress (~180/mois cumulé, concurrence faible)

### Refonte de site WordPress
- **status:** done 2026-07-12
- **slug:** refonte-site-wordpress
- **mot-clé principal:** refonte wordpress / refonte site wordpress (140 + 110/mois, concurrence faible)

### Sauvegarde WordPress
- **status:** done 2026-07-09
- **slug:** sauvegarde-wordpress
- **mot-clé principal:** sauvegarde wordpress / sauvegarde site wordpress (170/mois, concurrence faible)

### WordPress ou Wix : que choisir
- **status:** done 2026-07-06
- **slug:** wordpress-ou-wix
- **mot-clé principal:** wix ou wordpress / wordpress ou wix (210 + 90/mois, concurrence faible)

### Prix d'un site WordPress
- **status:** done 2026-07-03
- **slug:** prix-site-wordpress
- **mot-clé principal:** wordpress prix / prix site wordpress (390 + 110/mois, concurrence moyenne)

### Créer un site WordPress
- **status:** done 2026-06-30
- **slug:** creer-un-site-wordpress
- **mot-clé principal:** créer un site wordpress (1000/mois, concurrence faible)

### Maintenance WordPress
- **status:** done 2026-06-30
- **slug:** maintenance-wordpress
- **mot-clé principal:** maintenance wordpress (720/mois, concurrence faible)
