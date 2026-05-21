import sharp from 'sharp'
import fs from 'node:fs'

const SRC = './Logo-Paul Alves.png'
const OUT = './public/assets/logo-wordmark.webp'
const TARGET_KB = 30

// 1. Charge le PNG, ajoute le canal alpha
// 2. Remplace les pixels (quasi)blancs par de la transparence
// 3. Resize → 600px de large
// 4. Encode en WebP avec compression progressive jusqu'à passer sous 30 KB
async function main() {
  const base = sharp(SRC).ensureAlpha()

  const { data, info } = await base
    .raw()
    .toBuffer({ resolveWithObject: true })

  // Convertir les pixels blancs en transparents
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2]
    // Seuil 245 : capte les blancs + l'anti-aliasing clair
    if (r > 245 && g > 245 && b > 245) {
      data[i + 3] = 0 // alpha à 0 → transparent
    }
  }

  // Recadre au plus près du contenu (supprime les marges transparentes parasites)
  const trimmed = await sharp(data, {
    raw: { width: info.width, height: info.height, channels: 4 },
  })
    .trim({ threshold: 5 })
    .toBuffer({ resolveWithObject: true })

  const transparent = sharp(trimmed.data, {
    raw: { width: trimmed.info.width, height: trimmed.info.height, channels: 4 },
  }).resize({ width: 800, withoutEnlargement: true })

  for (let q = 90; q >= 30; q -= 5) {
    await transparent.clone().webp({ quality: q, effort: 6, alphaQuality: 100 }).toFile(OUT)
    const sizeKB = fs.statSync(OUT).size / 1024
    console.log(`quality=${q} → ${sizeKB.toFixed(1)} KB`)
    if (sizeKB <= TARGET_KB) {
      console.log(`\n✓ Final : ${OUT} (${sizeKB.toFixed(1)} KB, quality ${q}, fond transparent)`)
      return
    }
  }
}
main()
