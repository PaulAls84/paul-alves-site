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
        featured: fields.checkbox({
          label: 'Mettre en avant sur la page d’accueil',
          defaultValue: false,
        }),
        category: fields.select({
          label: 'Catégorie',
          options: [
            { label: 'WordPress', value: 'WordPress' },
            { label: 'SEO', value: 'SEO' },
            { label: 'Plugins', value: 'Plugins' },
            { label: 'Maintenance', value: 'Maintenance' },
          ],
          defaultValue: 'WordPress',
        }),
        image: fields.image({
          label: 'Image de couverture',
          directory: 'public/images/blog',
          publicPath: '/images/blog/',
        }),
        anchors: fields.array(fields.text({ label: 'Ancre / mot-clé' }), {
          label: 'Ancres pour le maillage interne',
          description:
            'Mots-clés qui, lorsqu’ils apparaissent dans un AUTRE article, ' +
            'deviennent automatiquement un lien vers celui-ci. ' +
            'Ex : « SEO WordPress », « référencement ». 2 à 4 ancres suffisent.',
          itemLabel: (props) => props.value || 'Ancre vide',
        }),
        content: fields.markdoc({ label: 'Contenu' }),
      },
    }),
  },
})
