# Routine de rédaction automatique d'articles

Cette routine publie **un article de blog par semaine** (lundi 8h) de façon
autonome, à partir d'un backlog de sujets validés SEO.

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
     (date du jour), `category`, `image: /images/blog/<slug>.jpg`.
   - **RÈGLE YAML CRITIQUE** : toute valeur contenant `:`, `"`, `[`, `]` ou
     commençant par un caractère spécial **doit être entre guillemets doubles**.
     Une frontmatter invalide casse la lecture de l'article. (La lecture du site
     est désormais résiliente — un article fautif s'auto-exclut — mais l'article
     concerné ne s'affichera pas. Donc valider le YAML.)
   - Corps : intro accroche (problème → promesse), sections `##`/`###`, gras,
     listes, au moins un tableau si pertinent, citations `>`, `## Conclusion`,
     `## FAQ` (3-4 questions en gras). Cible : 1200-1800 mots, ton pro et direct,
     français. S'inspirer du style des articles déjà publiés.
   - **Maillage interne** : insérer 1-2 liens vers les articles suggérés dans
     l'entrée du backlog. Les articles sont servis à la **racine** (style
     WordPress) : `https://paul-alves.fr/<slug>/` (et NON `/blog/<slug>/`).
     La page `/blog/` reste la liste des articles.

4. **Générer la couverture** :
   ```
   python3 automation/generate-cover.py "<titre>" "<catégorie>" "public/images/blog/<slug>.jpg"
   ```
   Si `OPENAI_API_KEY` est défini dans l'environnement, l'image de fond est
   générée par IA puis habillée à la charte ; sinon une couverture charte est
   produite localement. Dans les deux cas un fichier valide est créé.

5. **Mettre à jour le backlog** : passer l'entrée de `status: todo` à
   `status: done — <date>` et la déplacer dans la section « Publiés ».

6. **Vérifier puis publier** :
   - Idéalement, lancer `npm run build` pour confirmer que le site compile.
   - **N'ajouter QUE les fichiers de l'article** (jamais `git add -A`/`git add .` :
     un autre travail en cours dans le dossier serait embarqué par erreur) :
     ```
     git add src/content/blog/<slug>/ public/images/blog/<slug>.jpg automation/content-plan.md
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
