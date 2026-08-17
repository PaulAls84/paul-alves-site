# Routine de rédaction automatique d'articles

Cette routine publie **une dizaine d'articles par mois** de façon autonome, à
partir d'un backlog de sujets validés SEO.

**Cadence volontairement irrégulière** (depuis le 2026-08-17) : les jours de
publication sont espacés de 2 à 4 jours au lieu d'un métronome à 3 jours. Le
volume est inchangé ; c'est la **régularité mécanique** qui constituait un signal
de contenu produit en masse, pas la quantité. Ne pas « re-régulariser » ce cron
en le trouvant bizarre : l'irrégularité est le but.

**Où elle tourne :** dans le **cloud** (routine Claude Code, cron
`9 6 1,4,8,11,14,18,21,25,28,30 * *` UTC ≈ 8h09 Paris), depuis le 2026-08-12.
Elle ne dépend donc plus du Mac allumé.
Gestion des routines : <https://claude.ai/code/routines>.

Ce que l'environnement cloud a (constaté le 2026-08-17, Ubuntu 24.04, root) :
- **Pas de Chrome** et impossible d'en installer par `apt` (le paquet
  `chromium` n'est qu'un stub snap, et snap ne tourne pas en conteneur). C'est
  ce qui a fait tomber le run du 15/08 sur la couverture charte.
  `cover_template.find_chrome()` télécharge donc lui-même un
  `chrome-headless-shell` via `npx @puppeteer/browsers` (~15 s, une fois par
  run). Aucune action à faire ; poser `COVER_NO_DOWNLOAD=1` pour l'interdire.
- **Polices déjà présentes** (DejaVu, Liberation, Noto Color Emoji) : accents,
  graisses et emojis des vignettes sortent correctement.
- **Pas de Pillow** au départ → la routine l'installe
  (`pip install --break-system-packages pillow`, ~3 s).
- **Pas de connecteurs MCP** (Search Console / Cuik) : si le backlog `todo` est
  vide, la routine s'arrête et le signale au lieu de chercher des mots-clés.
- Une `OPENAI_API_KEY` **est** présente, mais l'appel images renvoie `429`.
  Sans importance : le fond IA ne concerne que le repli charte, pas la vignette.

## Procédure exécutée à chaque run

1. **Lire le backlog** : ouvrir [`automation/content-plan.md`](./content-plan.md)
   et prendre la **première entrée `status: todo`** de la file d'attente.
   - Si aucune entrée `todo` → **ne rien publier**, signaler que le backlog est
     vide et s'arrêter.

2. **Garde-fou anti-doublon** : vérifier qu'aucun dossier
   `src/content/blog/<slug>/` n'existe déjà pour ce slug. Si collision, marquer
   l'entrée `done` (déjà couverte) et passer à la suivante.

3. **Rédiger l'article** dans `src/content/blog/<slug>/index.mdoc`, au format
   exact des articles existants :
   - Frontmatter YAML : `title` (avec `[2026]`), `description`, `publishedAt`
     (date du jour), `featured: false`, `category`, `image: /images/blog/<slug>.jpg`,
     `anchors` (voir « Maillage interne » ci-dessous).
   - **`category` doit être l'une des valeurs de la liste fixe** (champ select
     Keystatic) : `WordPress`, `SEO`, `Plugins` ou `Maintenance`. Toute autre
     valeur serait invalide. Utiliser la catégorie indiquée dans le backlog.
   - **`featured: false`** par défaut : la mise en avant sur la page d'accueil est
     un choix éditorial manuel de Paul (il coche la case dans Keystatic).
   - **RÈGLE YAML CRITIQUE** : toute valeur contenant `:`, `"`, `[`, `]` ou
     commençant par un caractère spécial **doit être entre guillemets doubles**.
     Une frontmatter invalide casse la lecture de l'article. (La lecture du site
     est désormais résiliente — un article fautif s'auto-exclut — mais l'article
     concerné ne s'affichera pas. Donc valider le YAML.)
   - **Encart « En bref » — tout premier élément du corps**, avant l'intro. C'est
     un simple blockquote Markdown dont la première ligne est `**En bref**`, suivi
     de 3 à 5 puces qui **répondent directement** à la question du titre. Le
     lecteur pressé doit avoir sa réponse sans défiler ; c'est aussi la zone que
     Google peut reprendre en extrait enrichi. Ne pas y mettre de teasing (« nous
     allons voir que… ») : donner le verdict.
     ```
     > **En bref**
     >
     > - **Ce qu'il est vraiment** : …
     > - **Mon verdict** : oui si …, non si …
     > - **Le piège classique** : …
     ```
     Le style « carte » est automatique : le CSS cible le premier blockquote de
     l'article (`.article-content > article > blockquote:first-child` dans
     `src/styles/global.css`). Donc **un seul** blockquote en tête, et les
     citations éventuelles vont plus bas dans le corps.
   - **Voix : la première personne.** Les articles sont signés Paul Alves,
     artisan WordPress à Soissons : écrire « je », « mon avis », « ce que
     j'applique ». Pas de « nous » d'entreprise, pas de ton neutre d'encyclopédie.
   - **Exemples de cas concrets obligatoires.** Chaque article doit descendre dans
     le concret au moins deux fois : un cas de figure précis plutôt qu'un conseil
     abstrait (« un site vitrine sur mutualisé avec quarante extensions actives »,
     « une boutique de 800 références qui migre »), avec ce qu'on fait et ce qu'on
     obtient. Les conseils génériques sans illustration sont ce qui rend un article
     interchangeable — donc invisible.
   - ⚠️ **Mais jamais de vécu inventé.** Lire `automation/cas-clients.md` avant de
     rédiger : c'est la seule source autorisée pour une expérience vécue (chiffres
     relevés, cas client, statistiques du type « un site sur trois »). Si le
     fichier n'a rien sur le sujet, les cas concrets doivent être présentés comme
     des **situations types**, pas comme des souvenirs. La voix est celle de Paul ;
     les faits doivent rester vrais.
   - Puis : intro accroche (problème → promesse), sections `##`/`###`, gras,
     listes, au moins un tableau si pertinent, `## Conclusion`, `## FAQ` (3-4
     questions en gras). Cible : 1200-1800 mots, ton pro et direct, français.
     S'inspirer du style des articles déjà publiés.
   - **Maillage interne** : le maillage est désormais **automatique au build**
     (`src/lib/internal-links.ts`) — il transforme les mots-clés d'un article
     apparaissant dans les autres en liens (max 3/article). Pour que le nouvel
     article **reçoive** des liens entrants, remplir son champ `anchors` dans la
     frontmatter YAML : 2 à 4 mots-clés/phrases distinctifs, en privilégiant
     1-2 phrases longues (« vitesse de votre site WordPress ») + 1-2 mots-clés
     forts et non génériques (ex. `SEO`, `plugins`, `sauvegarde` selon le sujet).
     Éviter le mot seul « WordPress » (trop fréquent → sur-maillage).
     Exemple YAML :
     ```
     anchors:
       - hébergement WordPress
       - hébergeur
     ```
     Des liens éditoriaux manuels dans le corps restent possibles en plus (ils
     ne seront pas doublés par l'auto). Les articles sont servis à la **racine**
     (style WordPress) : `https://paul-alves.fr/<slug>/` (et NON `/blog/<slug>/`).
     La page `/blog/` reste la liste des articles.
   - **Affiliation (monétisation)** : si l'entrée du backlog porte
     `monétisation: affiliation`, consulter la section « Affiliation » de
     `content-plan.md`. Pour chaque service cité dont le lien affilié est
     renseigné (≠ `<À REMPLIR>`), le lier avec `rel="sponsored nofollow"`.
     La **mention de transparence** ne s'ajoute que si l'article contient au
     moins un vrai lien affilié — jamais « préventivement ».
     Si un lien vaut `<À REMPLIR>`, citer le service **sans lien** (ne JAMAIS
     inventer ni deviner un lien affilié).
     **Quand Paul remplit ses liens affiliés** : repasser sur les articles déjà
     publiés qui portent la mention « peut contenir des liens affiliés »,
     insérer les liens et remettre la mention affirmative « contient ». Rester honnête et factuel dans les
     comparatifs (vrais points forts/faibles, pas de survente).

4. **Générer la couverture** :
   ```
   python3 automation/generate-cover.py "<titre>" "<catégorie>" "public/images/blog/<slug>.jpg"
   ```
   Le pipeline principal produit une **vignette « YouTube-style »** (badge,
   titre 3 lignes, sous-titre, étapes, visuel thématique) : la config est
   déduite automatiquement du titre/catégorie et rendue via Chrome headless
   (cf. `automation/cover_template.py`). Pour affiner une vignette (choix du
   visuel, lignes du titre…), passer un `config.json` en 4ᵉ argument — clés
   possibles : `preset` (site, shop, server, ranking, plugins, themes, speed,
   budget, revamp, backup, shield, serp, dashboard, migrate, vs), `badge`,
   `lines`, `sub`, `steps`, `notif`, `visual`.
   **Chrome** : s'il n'y en a pas sur la machine (cas du cloud), le script en
   télécharge un automatiquement (~15 s). **Repli garanti** : si même ça échoue
   (pas de réseau, pas de `npx`), une couverture charte sobre est produite avec
   Pillow. Dans tous les cas un fichier valide est créé — et Paul peut
   régénérer la vignette stylée en local avec les mêmes arguments.
   Après génération, **vérifier l'image produite** : la sortie doit dire
   `OK vignette` et non `OK charte`.
   Le script génère **deux fichiers** : `<slug>.jpg` (og:image / réseaux sociaux)
   **et** `<slug>.webp` (version légère affichée sur le site). La frontmatter
   garde `image: /images/blog/<slug>.jpg` ; l'affichage bascule automatiquement
   sur le `.webp` via le helper `webpCover`. **Committer les deux fichiers.**

5. **Mettre à jour le backlog** : passer l'entrée de `status: todo` à
   `status: done — <date>` et la déplacer dans la section « Publiés ».

6. **Vérifier puis publier** :
   - Idéalement, lancer `npm run build` pour confirmer que le site compile.
   - **N'ajouter QUE les fichiers de l'article** (jamais `git add -A`/`git add .` :
     un autre travail en cours dans le dossier serait embarqué par erreur) :
     ```
     git add src/content/blog/<slug>/ public/images/blog/<slug>.jpg public/images/blog/<slug>.webp automation/content-plan.md
     ```
   - Committer et **pousser sur `main`**. Vercel rebuild et met l'article en ligne
     automatiquement (le repo doit rester PUBLIC, cf. plan Vercel Hobby).
   - Message de commit : `Blog : <titre> (routine auto)`.

## Réalimenter le backlog

Quand la file `todo` est vide, relancer une analyse de mots-clés (Cuik
`get_keyword_ideas` / Search Console `gsc_query_keywords` sur
`sc-domain:paul-alves.fr`), repérer des clusters **non encore couverts** par les
articles existants, et ajouter de nouvelles entrées dans `content-plan.md`.

## Image IA (optionnel)

Pour activer les vraies images IA, définir la clé dans l'environnement où tourne
la routine (ne jamais la committer) :
```
export OPENAI_API_KEY="sk-..."
```
Sans clé, la couverture charte sert de repli — la routine reste fonctionnelle.
