# Routine de rédaction automatique d'articles

Cette routine publie **un article de blog tous les 3 jours** (8h) de façon
autonome, à partir d'un backlog de sujets validés SEO.

**Où elle tourne :** dans le **cloud** (routine Claude Code, cron `9 6 */3 * *` UTC),
depuis le 2026-08-12. Elle ne dépend donc plus du Mac allumé. L'environnement
cloud n'a **ni `OPENAI_API_KEY` ni connecteurs MCP** (Search Console / Cuik) :
les couvertures sont celles de la charte, et si le backlog `todo` est vide la
routine s'arrête en le signalant au lieu de chercher de nouveaux mots-clés.
Gestion des routines : <https://claude.ai/code/routines>.

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
   - Corps : intro accroche (problème → promesse), sections `##`/`###`, gras,
     listes, au moins un tableau si pertinent, citations `>`, `## Conclusion`,
     `## FAQ` (3-4 questions en gras). Cible : 1200-1800 mots, ton pro et direct,
     français. S'inspirer du style des articles déjà publiés.
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
   **Repli garanti** : si Chrome/Chromium est introuvable (environnement cloud
   minimal), une couverture charte sobre est produite avec Pillow (fond IA en
   plus si `OPENAI_API_KEY` est défini). Dans tous les cas un fichier valide
   est créé — Paul peut ensuite régénérer la vignette stylée en local :
   `python3 automation/generate-cover.py` (mêmes arguments) sur son Mac.
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
