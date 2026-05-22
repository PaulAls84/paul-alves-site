import sharp from 'sharp'
import fs from 'node:fs'

const SRC = './Projet Nos amis les chiens.png'
const OUT = './public/assets/nosamisleschiens-screenshot.webp'
const TARGET_KB = 100

async function compress() {
  for (let q = 80; q >= 20; q -= 5) {
    await sharp(SRC)
      .resize({ width: 800, withoutEnlargement: true })
      .webp({ quality: q, effort: 6, smartSubsample: true })
      .toFile(OUT)
    const sizeKB = fs.statSync(OUT).size / 1024
    console.log(`quality=${q} → ${sizeKB.toFixed(1)} KB`)
    if (sizeKB <= TARGET_KB) {
      console.log(`\n✓ Final : ${OUT} (${sizeKB.toFixed(1)} KB, quality ${q})`)
      return
    }
  }
  console.log('\n⚠ Impossible de descendre sous 100 KB, gardons la dernière version')
}
compress()
