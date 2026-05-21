import sharp from 'sharp'
import fs from 'node:fs'

const SRC = './Logo-Paul Alves.png'
const OUT = './public/assets/logo-wordmark.webp'
const TARGET_KB = 30

// Itère sur quality jusqu'à descendre sous 30 KB
async function compress() {
  for (let q = 90; q >= 30; q -= 5) {
    await sharp(SRC)
      .resize({ width: 600, withoutEnlargement: true })
      .webp({ quality: q, effort: 6 })
      .toFile(OUT)
    const sizeKB = fs.statSync(OUT).size / 1024
    console.log(`quality=${q} → ${sizeKB.toFixed(1)} KB`)
    if (sizeKB <= TARGET_KB) {
      console.log(`\n✓ Final : ${OUT} (${sizeKB.toFixed(1)} KB, quality ${q})`)
      return
    }
  }
}
compress()
