import { defineConfig } from 'astro/config'
import react from '@astrojs/react'
import keystatic from '@keystatic/astro'
import sitemap from '@astrojs/sitemap'
import vercel from '@astrojs/vercel'

export default defineConfig({
  site: 'https://paul-alves.fr',
  integrations: [react(), keystatic(), sitemap()],

  // Les articles sont servis à la racine (/<slug>/), comme l'ancien WordPress.
  // On redirige (301) les anciennes URL /blog/<slug> vers la racine.
  redirects: {
    '/blog/[slug]': '/[slug]',
  },

  // Mode "hybride" : toutes les pages sont statiques par défaut.
  // Les fichiers avec `export const prerender = false`
  // (src/pages/api/contact.ts et src/pages/api/newsletter.ts)
  // deviennent automatiquement des fonctions serverless sur Vercel.
  output: 'static',

  adapter: vercel({
    webAnalytics: { enabled: false }, // GA4 suffit
  }),
})
