export const prerender = false

import type { APIRoute } from 'astro'
import { Resend } from 'resend'

export const POST: APIRoute = async ({ request }) => {
  try {
    // ── Parse du body ────────────────────────────────
    let data: Record<string, string> = {}
    const ct = request.headers.get('content-type') ?? ''
    if (ct.includes('application/json')) {
      data = await request.json()
    } else {
      const form = await request.formData()
      for (const [k, v] of form.entries()) data[k] = v.toString()
    }

    const { nom, email, sujet, message, telephone } = data

    // ── Validation ───────────────────────────────────
    if (!nom || !email || !sujet || !message) {
      return new Response(JSON.stringify({ error: 'Champs obligatoires manquants.' }), {
        status: 400, headers: { 'Content-Type': 'application/json' },
      })
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(JSON.stringify({ error: 'Adresse email invalide.' }), {
        status: 400, headers: { 'Content-Type': 'application/json' },
      })
    }

    // ── Resend ───────────────────────────────────────
    const apiKey = import.meta.env.RESEND_API_KEY
    const toEmail   = import.meta.env.CONTACT_TO_EMAIL   ?? 'hello@paul-alves.fr'
    const fromEmail = import.meta.env.CONTACT_FROM_EMAIL ?? 'hello@paul-alves.fr'

    if (!apiKey) {
      console.error('[contact] RESEND_API_KEY manquante')
      return new Response(JSON.stringify({ error: 'Configuration serveur incomplète.' }), {
        status: 500, headers: { 'Content-Type': 'application/json' },
      })
    }

    const resend = new Resend(apiKey)

    // ── Échappement HTML simple ──────────────────────
    const esc = (s: string) => s
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;')

    const html = `
      <div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:560px;margin:0 auto;padding:32px;color:#0a1d36;line-height:1.6;">
        <div style="border-bottom:3px solid #d4a44a;padding-bottom:16px;margin-bottom:24px;">
          <h1 style="font-size:20px;margin:0;color:#0a1d36;">📩 Nouveau message du formulaire</h1>
          <p style="margin:6px 0 0;font-size:13px;color:#6b7a8d;">paul-alves.fr / contact</p>
        </div>

        <table style="width:100%;border-collapse:collapse;font-size:14px;">
          <tr><td style="padding:8px 0;color:#6b7a8d;width:120px;">De</td><td style="padding:8px 0;font-weight:600;">${esc(nom)}</td></tr>
          <tr><td style="padding:8px 0;color:#6b7a8d;">Email</td><td style="padding:8px 0;"><a href="mailto:${esc(email)}" style="color:#d4a44a;">${esc(email)}</a></td></tr>
          ${telephone ? `<tr><td style="padding:8px 0;color:#6b7a8d;">Téléphone</td><td style="padding:8px 0;"><a href="tel:${esc(telephone)}" style="color:#d4a44a;">${esc(telephone)}</a></td></tr>` : ''}
          <tr><td style="padding:8px 0;color:#6b7a8d;">Sujet</td><td style="padding:8px 0;font-weight:600;">${esc(sujet)}</td></tr>
        </table>

        <div style="margin-top:24px;padding:20px;background:#faf7f2;border-radius:10px;border-left:3px solid #d4a44a;">
          <p style="margin:0 0 8px;font-size:12px;font-weight:700;color:#6b7a8d;text-transform:uppercase;letter-spacing:.08em;">Message</p>
          <p style="margin:0;white-space:pre-wrap;color:#243a55;">${esc(message)}</p>
        </div>

        <p style="margin-top:32px;font-size:12px;color:#6b7a8d;border-top:1px solid #e6e0d4;padding-top:16px;">
          Pour répondre, clique simplement sur "Répondre" — la réponse partira directement à ${esc(email)}.
        </p>
      </div>
    `

    const text = [
      `Nouveau message du formulaire de contact — paul-alves.fr`,
      ``,
      `De      : ${nom}`,
      `Email   : ${email}`,
      telephone ? `Tél.    : ${telephone}` : null,
      `Sujet   : ${sujet}`,
      ``,
      `Message :`,
      message,
    ].filter(Boolean).join('\n')

    // ── Envoi email (Resend) + enregistrement Systeme.io en parallèle ──
    const systemeKey = import.meta.env.SYSTEME_IO_API_KEY

    const [emailResult] = await Promise.all([
      resend.emails.send({
        from: `Paul Alves — Contact <${fromEmail}>`,
        to: [toEmail],
        replyTo: email,
        subject: `[Contact] ${sujet} — ${nom}`,
        html,
        text,
      }),
      // Ajout dans Systeme.io sans tag — non bloquant
      systemeKey
        ? fetch('https://api.systeme.io/api/contacts', {
            method: 'POST',
            headers: {
              'X-API-Key': systemeKey,
              'Content-Type': 'application/json',
              'accept': 'application/json',
            },
            body: JSON.stringify({
              email,
              fields: [
                { slug: 'first_name', value: nom.split(' ')[0] ?? nom },
                ...(nom.split(' ').length > 1
                  ? [{ slug: 'surname', value: nom.split(' ').slice(1).join(' ') }]
                  : []),
                ...(telephone ? [{ slug: 'phone_number', value: telephone }] : []),
              ],
            }),
          }).catch((e) => console.error('[contact] Systeme.io error (non bloquant):', e))
        : Promise.resolve(),
    ])

    const { error } = emailResult
    if (error) {
      console.error('[contact] Resend error', error)
      return new Response(JSON.stringify({ error: 'Erreur d\'envoi. Réessayez ou écris-moi directement à hello@paul-alves.fr.' }), {
        status: 502, headers: { 'Content-Type': 'application/json' },
      })
    }

    return new Response(JSON.stringify({ success: true }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    })
  } catch (err) {
    console.error('[contact] Exception', err)
    return new Response(JSON.stringify({ error: 'Une erreur est survenue. Réessayez.' }), {
      status: 500, headers: { 'Content-Type': 'application/json' },
    })
  }
}
