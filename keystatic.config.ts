import { config, collection, fields } from '@keystatic/core'

export default config({
  storage: {
    kind: 'github',
    repo: 'PaulAls84/paul-alves-site',
  },
  ui: {
    brand: {
      name: 'Paul Alves — Studio',
    },
  },
  collections: {
    blog: collection({
      label: 'Articles de blog',
      slugField: 'title',
      path: 'src/content/blog/*/',
      entryLayout: 'content',
      format: { contentField: 'content' },
      schema: {
        title: fields.slug({ name: { label: 'Titre' } }),
        description: fields.text({ label: 'Description', multiline: true }),
        publishedAt: fields.date({ label: 'Date de publication' }),
        category: fields.text({ label: 'Catégorie (ex: SEO, Dev Web)' }),
        image: fields.image({
          label: 'Image de couverture',
          directory: 'public/images/blog',
          publicPath: '/images/blog/',
        }),
        content: fields.markdoc({ label: 'Contenu' }),
      },
    }),
  },
})
