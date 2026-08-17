// Notifie IndexNow (Bing, et par ricochet DuckDuckGo/Ecosia/Qwant) des URL
// modifiées au dernier commit. Lancé après le build Vercel (voir package.json).
//
// - Ne tourne qu'en production Vercel (VERCEL_ENV=production) : les builds
//   locaux et les previews ne pingent pas.
// - Ne fait jamais échouer le build : toute erreur est loggée puis avalée.
//
// La clé est publiée dans public/<clé>.txt, comme l'exige le protocole :
// https://www.indexnow.org/documentation

import { execSync } from 'node:child_process'

const SITE = 'https://paul-alves.fr'
const KEY = 'b2024858fc5ecd1436fc7f724277f225'

// Fichier modifié → URL publique correspondante, ou null si non publiable.
function urlForFile(file) {
  // Article : src/content/blog/<slug>/... → /<slug>/ (servi à la racine)
  const article = file.match(/^src\/content\/blog\/([^/]+)\//)
  if (article) return `${SITE}/${article[1]}/`

  // Page : src/pages/<route>.astro → /<route>/ (hors 404, API, routes dynamiques)
  const page = file.match(/^src\/pages\/([^[]+)\.astro$/)
  if (page && !['404', 'qrcode'].includes(page[1]) && !page[1].startsWith('api/')) {
    return page[1] === 'index' ? `${SITE}/` : `${SITE}/${page[1]}/`
  }

  return null
}

async function main() {
  if (process.env.VERCEL_ENV !== 'production') {
    console.log('[indexnow] pas en production Vercel, ping ignoré')
    return
  }

  let changed
  try {
    changed = execSync('git diff --name-only HEAD~1 HEAD', { encoding: 'utf8' })
      .split('\n')
      .filter(Boolean)
  } catch {
    // Clone trop shallow ou premier commit : on ne peut pas diff, tant pis.
    console.log('[indexnow] git diff indisponible, ping ignoré')
    return
  }

  const urls = [...new Set(changed.map(urlForFile).filter(Boolean))]
  if (urls.length === 0) {
    console.log('[indexnow] aucune URL publiable modifiée')
    return
  }

  const res = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({
      host: 'paul-alves.fr',
      key: KEY,
      keyLocation: `${SITE}/${KEY}.txt`,
      urlList: urls,
    }),
  })
  console.log(`[indexnow] ${urls.length} URL soumise(s), statut ${res.status}`)
  urls.forEach((u) => console.log(`[indexnow]   ${u}`))
}

main().catch((err) => {
  console.error('[indexnow] erreur ignorée :', err.message)
})
