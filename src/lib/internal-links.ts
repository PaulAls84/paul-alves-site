import Markdoc from '@markdoc/markdoc'
import type { RenderableTreeNode } from '@markdoc/markdoc'

/** Un article candidat au maillage : son slug + ses ancres (phrases-cibles). */
export type ArticleRef = { slug: string; anchors: string[] }

// On ne pose jamais de lien à l'intérieur de ces balises :
// - a    : ne pas imbriquer un lien dans un lien
// - h1-6 : garder les titres propres (et ils servent d'ancres au sommaire)
// - code/pre : ne pas polluer les extraits de code
const SKIP_TAGS = new Set(['a', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * Regex qui matche la phrase entière (insensible à la casse), en s'assurant
 * qu'elle n'est pas collée à d'autres lettres/chiffres — évite de lier
 * "SEO" à l'intérieur de "SEOptimisation". Les accents sont gérés via \p{L}.
 */
function buildMatcher(phrase: string): RegExp {
  return new RegExp(`(?<![\\p{L}\\p{N}])${escapeRegExp(phrase)}(?![\\p{L}\\p{N}])`, 'iu')
}

type Candidate = { slug: string; phrase: string; regex: RegExp }
type State = {
  remaining: number
  usedTargets: Set<string>
  candidates: Candidate[]
}

/**
 * Découpe une chaîne de texte : remplace la 1re ancre trouvée par un lien,
 * puis continue récursivement sur le reste (pour placer d'autres liens vers
 * d'autres articles si le budget le permet).
 */
function linkifyString(text: string, state: State): RenderableTreeNode[] {
  if (state.remaining <= 0) return [text]

  let best: { index: number; length: number; matched: string; slug: string } | null = null
  for (const c of state.candidates) {
    if (state.usedTargets.has(c.slug)) continue // 1 lien par article cible max
    const m = c.regex.exec(text)
    if (m && (best === null || m.index < best.index)) {
      best = { index: m.index, length: m[0].length, matched: m[0], slug: c.slug }
    }
  }

  if (!best) return [text]

  state.remaining--
  state.usedTargets.add(best.slug)

  const before = text.slice(0, best.index)
  const after = text.slice(best.index + best.length)
  const link = new Markdoc.Tag(
    'a',
    { href: `/${best.slug}/`, class: 'internal-link' },
    [best.matched]
  )

  const out: RenderableTreeNode[] = []
  if (before) out.push(before)
  out.push(link)
  out.push(...linkifyString(after, state))
  return out
}

/** Parcourt récursivement les nœuds, en liant le texte hors balises interdites. */
function walk(nodes: RenderableTreeNode[], canLink: boolean, state: State): RenderableTreeNode[] {
  const out: RenderableTreeNode[] = []
  for (const node of nodes) {
    if (typeof node === 'string') {
      out.push(...(canLink ? linkifyString(node, state) : [node]))
    } else if (Markdoc.Tag.isTag(node)) {
      const allowed = canLink && !SKIP_TAGS.has(node.name)
      node.children = walk((node.children ?? []) as RenderableTreeNode[], allowed, state)
      out.push(node)
    } else {
      out.push(node)
    }
  }
  return out
}

/**
 * Maillage interne automatique.
 * Injecte au maximum `maxLinks` liens contextuels dans l'arbre Markdoc rendu,
 * vers les autres articles dont une ancre apparaît dans le texte.
 *
 * @param tree        arbre renvoyé par Markdoc.transform(...)
 * @param currentSlug slug de l'article courant (pour ne pas s'auto-lier)
 * @param articles    tous les articles avec leurs ancres
 * @param maxLinks    plafond de liens injectés (2–3 recommandé)
 */
export function injectInternalLinks(
  tree: RenderableTreeNode,
  currentSlug: string,
  articles: ArticleRef[],
  maxLinks = 3
): RenderableTreeNode {
  const candidates: Candidate[] = []
  for (const a of articles) {
    if (a.slug === currentSlug) continue
    for (const raw of a.anchors ?? []) {
      const phrase = String(raw).trim()
      if (phrase.length < 3) continue // ancres trop courtes = trop de faux positifs
      candidates.push({ slug: a.slug, phrase, regex: buildMatcher(phrase) })
    }
  }
  if (candidates.length === 0) return tree

  // Ancres les plus longues d'abord : "hébergement WordPress" avant "WordPress".
  candidates.sort((x, y) => y.phrase.length - x.phrase.length)

  const state: State = { remaining: maxLinks, usedTargets: new Set(), candidates }
  const roots = Array.isArray(tree) ? tree : [tree]
  walk(roots as RenderableTreeNode[], true, state)
  return tree
}

/**
 * Lit tous les articles et renvoie leurs ancres, prêt à passer à
 * injectInternalLinks. Lecture résiliente : un article illisible est ignoré.
 */
export async function getArticleRefs(reader: any): Promise<ArticleRef[]> {
  try {
    const slugs: string[] = await reader.collections.blog.list()
    const refs = await Promise.all(
      slugs.map(async (slug: string) => {
        try {
          const e = await reader.collections.blog.read(slug)
          const anchors = ((e?.anchors ?? []) as unknown[])
            .map((a) => String(a).trim())
            .filter(Boolean)
          return { slug, anchors }
        } catch {
          return { slug, anchors: [] as string[] }
        }
      })
    )
    return refs.filter((r) => r.anchors.length > 0)
  } catch {
    return []
  }
}
