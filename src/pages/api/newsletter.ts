export const prerender = false

import type { APIRoute } from 'astro'

export const POST: APIRoute = async ({ request }) => {
  const headers = { 'Content-Type': 'application/json' }

  let email: string | null = null

  const contentType = request.headers.get('content-type') ?? ''
  if (contentType.includes('application/json')) {
    const body = await request.json()
    email = body?.email ?? null
  } else {
    const data = await request.formData()
    email = data.get('email') as string | null
  }

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response(JSON.stringify({ error: 'Adresse email invalide.' }), { status: 400, headers })
  }

  const apiKey = import.meta.env.SYSTEME_IO_API_KEY
  if (!apiKey) {
    return new Response(JSON.stringify({ error: 'Configuration manquante.' }), { status: 500, headers })
  }

  try {
    const res = await fetch('https://api.systeme.io/api/contacts', {
      method: 'POST',
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify({
        email,
        tags: [{ name: 'newsletter' }],
      }),
    })

    // 201 = créé, 200 = déjà existant (selon Systeme.io)
    if (res.status === 201 || res.status === 200) {
      return new Response(JSON.stringify({ success: true }), { status: 200, headers })
    }

    const err = await res.text()
    console.error('Systeme.io error:', res.status, err)
    return new Response(JSON.stringify({ error: 'Erreur lors de l\'inscription.' }), { status: 502, headers })
  } catch (e) {
    console.error('Newsletter fetch error:', e)
    return new Response(JSON.stringify({ error: 'Erreur serveur.' }), { status: 500, headers })
  }
}
