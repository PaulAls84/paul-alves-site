// Rend chaque article Markdoc en HTML, avec le même maillage interne que le site Astro.
import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
const P = process.argv[2], OUT = process.argv[3]
const require = createRequire(path.join(P, 'package.json'))
const Markdoc = require('@markdoc/markdoc')
const yaml = require('js-yaml')
const dir = path.join(P, 'src/content/blog')
const posts = fs.readdirSync(dir).map(slug => {
  const raw = fs.readFileSync(path.join(dir, slug, 'index.mdoc'), 'utf8')
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  return { slug, fm: yaml.load(m[1]), body: m[2] }
})
const SKIP = new Set(['a','code','pre','h1','h2','h3','h4','h5','h6'])
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
function inject(tree, current, maxLinks = 3) {
  const cands = []
  for (const p of posts) {
    if (p.slug === current) continue
    for (const a of p.fm.anchors ?? []) {
      const phrase = String(a).trim(); if (phrase.length < 3) continue
      cands.push({ slug: p.slug, phrase, regex: new RegExp(`(?<![\\p{L}\\p{N}])${esc(phrase)}(?![\\p{L}\\p{N}])`, 'iu') })
    }
  }
  cands.sort((x, y) => y.phrase.length - x.phrase.length)
  const st = { remaining: maxLinks, used: new Set() }
  const linkify = text => {
    if (st.remaining <= 0) return [text]
    let best = null
    for (const c of cands) {
      if (st.used.has(c.slug)) continue
      const m = c.regex.exec(text)
      if (m && (!best || m.index < best.index)) best = { index: m.index, len: m[0].length, matched: m[0], slug: c.slug }
    }
    if (!best) return [text]
    st.remaining--; st.used.add(best.slug)
    const out = []
    const before = text.slice(0, best.index), after = text.slice(best.index + best.len)
    if (before) out.push(before)
    out.push(new Markdoc.Tag('a', { href: `/${best.slug}/`, class: 'internal-link' }, [best.matched]))
    out.push(...linkify(after))
    return out
  }
  const walk = (nodes, can) => {
    const out = []
    for (const n of nodes) {
      if (typeof n === 'string') out.push(...(can ? linkify(n) : [n]))
      else if (Markdoc.Tag.isTag(n)) { n.children = walk(n.children ?? [], can && !SKIP.has(n.name)); out.push(n) }
      else out.push(n)
    }
    return out
  }
  walk(Array.isArray(tree) ? tree : [tree], true)
  return tree
}
const out = posts.map(p => {
  const tree = inject(Markdoc.transform(Markdoc.parse(p.body)), p.slug)
  return { slug: p.slug, ...p.fm, html: Markdoc.renderers.html(tree) }
})
fs.writeFileSync(OUT, JSON.stringify(out, null, 1))
console.log(out.length, 'articles rendus')
