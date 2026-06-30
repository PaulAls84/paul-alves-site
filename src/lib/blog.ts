import { createReader } from '@keystatic/core/reader'
import keystaticConfig from '../../keystatic.config'

export type Post = {
  slug: string
  title: string
  description: string
  publishedAt: string
  category: string
  image: string
  featured: boolean
}

/** Slug d'URL d'une catégorie (ex. "WordPress" -> "wordpress"). */
export function categorySlug(name: string): string {
  return (name ?? '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
}

/**
 * Liste tous les articles, triés du plus récent au plus ancien.
 * Lecture résiliente : un article corrompu est ignoré, pas tout le blog.
 */
export async function listPosts(): Promise<Post[]> {
  try {
    const reader = createReader(process.cwd(), keystaticConfig)
    const slugs = await reader.collections.blog.list()
    const entries = await Promise.all(
      slugs.map(async (slug) => {
        try {
          const e = await reader.collections.blog.read(slug)
          return e ? { slug, ...e } : null
        } catch {
          return null
        }
      })
    )
    return (entries.filter(Boolean) as any[])
      .map((p) => ({
        slug: p.slug,
        title: typeof p.title === 'object' ? p.title.value ?? '' : p.title ?? '',
        description: p.description ?? '',
        publishedAt: p.publishedAt ?? '',
        category: p.category ?? '',
        image: p.image ?? '',
        featured: p.featured ?? false,
      }))
      .sort(
        (a, b) =>
          new Date(b.publishedAt || 0).getTime() - new Date(a.publishedAt || 0).getTime()
      )
  } catch {
    return []
  }
}

/** Catégories distinctes présentes dans le blog (ordre d'apparition). */
export function distinctCategories(posts: Post[]): string[] {
  return [...new Set(posts.map((p) => p.category).filter(Boolean))]
}
