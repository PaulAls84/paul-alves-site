/**
 * Scripts du site paul-alves.fr (repris des composants Astro).
 * Chaque bloc ne s'exécute que si les éléments concernés sont présents.
 */
(() => {
  const w = window
  const $ = (s, root = document) => root.querySelector(s)
  const $$ = (s, root = document) => [...root.querySelectorAll(s)]
  const api = (path) => (w.PA && w.PA.rest ? w.PA.rest : '/wp-json/pa/v1/') + path

  /* ── Suivi GA4 (Tracking.astro) ───────────────────────────── */
  w.track = (name, params = {}) => {
    if (typeof w.gtag === 'function') w.gtag('event', name, params)
  }
  const locate = (el) => {
    if (el.closest('#mobile-bar')) return 'mobile_bar'
    if (el.closest('nav, header')) return 'nav'
    if (el.closest('footer')) return 'footer'
    const section = el.closest('section[id], section[class], aside')
    return (section && (section.id || section.classList[0])) || 'page'
  }
  document.addEventListener('click', (e) => {
    const el = e.target && e.target.closest ? e.target.closest('a, button') : null
    if (!el) return
    const href = el.getAttribute('href') || ''
    const params = {
      link_location: locate(el),
      link_text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60),
    }
    if (href.startsWith('tel:')) w.track('phone_click', params)
    else if (href.startsWith('mailto:')) w.track('email_click', params)
    else if (el.hasAttribute('data-cal-link')) w.track('booking_cta_click', params)
  }, { capture: true })

  /* ── Navigation (Nav.astro) ───────────────────────────────── */
  const nav = $('#nav')
  const toggle = $('#mobileToggle')
  const navLinks = $('#navLinks')
  if (nav && navLinks) {
    window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 8), { passive: true })
    toggle && toggle.addEventListener('click', () => navLinks.classList.toggle('open'))
    $$('a', navLinks).forEach((a) => a.addEventListener('click', () => navLinks.classList.remove('open')))

    // Sur l'accueil : lien actif selon la section visible
    if (document.body.classList.contains('home')) {
      const sections = ['accueil', 'services', 'apropos', 'realisations', 'contact']
      const linkMap = {}
      $$('a', navLinks).forEach((a) => {
        const id = (a.getAttribute('href') || '').split('#')[1]
        if (id && sections.includes(id)) linkMap[id] = a
      })
      window.addEventListener('scroll', () => {
        let current = 'accueil'
        sections.forEach((id) => {
          const el = document.getElementById(id)
          if (el && el.getBoundingClientRect().top <= 120) current = id
        })
        Object.entries(linkMap).forEach(([id, a]) => a.classList.toggle('active', id === current))
      }, { passive: true })
    }
  }

  /* ── Barre d'actions mobile (MobileBar.astro) ─────────────── */
  const bar = $('#mobile-bar')
  if (bar) {
    const hero = $('#accueil, .services-hero, .article-hero')
    const footer = $('footer.site-footer')
    const update = () => {
      const y = window.scrollY
      const threshold = hero ? hero.offsetTop + hero.offsetHeight - 60 : 350
      const footerTop = footer ? footer.getBoundingClientRect().top + y - window.innerHeight : Infinity
      const show = y > threshold && y < footerTop
      bar.classList.toggle('mobile-bar--visible', show)
      bar.setAttribute('aria-hidden', show ? 'false' : 'true')
    }
    window.addEventListener('scroll', update, { passive: true })
    update()
  }

  /* ── Cal.com, chargé à la première interaction (CalLoader.astro) ── */
  const ns = (w.PA && w.PA.calNs) || 'audit-offert'
  let calLoaded = false
  const initCal = () => {
    if (calLoaded) return
    calLoaded = true
    ;(function (C, A, L) {
      const p = (a, ar) => a.q.push(ar)
      const d = C.document
      C.Cal = C.Cal || function () {
        const cal = C.Cal
        const ar = arguments
        if (!cal.loaded) {
          cal.ns = {}; cal.q = cal.q || []
          d.head.appendChild(d.createElement('script')).src = A
          cal.loaded = true
        }
        if (ar[0] === L) {
          const apiFn = function () { p(apiFn, arguments) }
          const namespace = ar[1]
          apiFn.q = apiFn.q || []
          typeof namespace === 'string' ? (cal.ns[namespace] = apiFn) && p(apiFn, ar) : p(cal, ar)
          return
        }
        p(cal, ar)
      }
    })(w, 'https://app.cal.eu/embed/embed.js', 'init')
    w.Cal('init', ns, { origin: 'https://cal.eu' })
    w.Cal.ns[ns]('on', {
      action: 'bookingSuccessfulV2',
      callback: () => w.track('book_appointment', { method: 'cal_com', event_type: ns }),
    })
  }
  const calEvents = ['pointerdown', 'touchstart', 'keydown', 'scroll', 'mousemove']
  const onFirst = () => { initCal(); calEvents.forEach((e) => window.removeEventListener(e, onFirst)) }
  calEvents.forEach((e) => window.addEventListener(e, onFirst, { once: true, passive: true }))
  setTimeout(initCal, 5000)
  // Les liens Cal ne doivent jamais faire remonter la page.
  document.addEventListener('click', (e) => {
    const a = e.target && e.target.closest ? e.target.closest('a[data-cal-link]') : null
    if (a && a.getAttribute('href') === '#') e.preventDefault()
  })

  /* ── Newsletter (Newsletter.astro) ────────────────────────── */
  $$('form[data-pa-newsletter]').forEach((form) => {
    const msg = form.parentElement.querySelector('.newsletter-notice')
    const label = $('.btn-label', form)
    const loading = $('.btn-loading', form)
    const button = $('button', form)
    form.addEventListener('submit', async (e) => {
      e.preventDefault()
      const email = form.elements.email.value.trim()
      if (!email) return
      label.style.display = 'none'; loading.style.display = 'inline'; button.disabled = true
      try {
        const res = await fetch(api('newsletter'), {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email }),
        })
        const data = await res.json()
        msg.style.display = 'block'
        if (res.ok) {
          msg.style.color = '#2d7a3a'
          msg.textContent = '✓ Merci ! Vous êtes bien inscrit à la newsletter.'
          form.reset()
          w.track('sign_up', { method: 'newsletter' })
        } else {
          msg.style.color = '#c0392b'
          msg.textContent = data.error || 'Une erreur est survenue. Réessayez.'
        }
      } catch {
        msg.style.display = 'block'; msg.style.color = '#c0392b'
        msg.textContent = 'Erreur réseau. Vérifiez votre connexion.'
      } finally {
        label.style.display = 'inline'; loading.style.display = 'none'; button.disabled = false
      }
    })
  })

  /* ── Formulaire de contact (contact.astro) ────────────────── */
  const cform = $('#contactForm')
  if (cform) {
    const btn = $('#submitBtn')
    const msgBox = $('#formMsg')
    const btnHTML = btn.innerHTML
    const setMsg = (text, type) => { msgBox.textContent = text; msgBox.className = `form-msg form-msg--${type}` }
    cform.addEventListener('submit', async (e) => {
      e.preventDefault()
      if (!cform.checkValidity()) {
        setMsg('Merci de remplir les champs obligatoires avec une adresse email valide.', 'error')
        return
      }
      btn.disabled = true; btn.textContent = 'Envoi en cours…'
      msgBox.className = 'form-msg'; msgBox.textContent = ''
      try {
        const payload = Object.fromEntries(new FormData(cform))
        const res = await fetch(api('contact'), {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
        })
        const json = await res.json()
        if (res.ok && json.success) {
          setMsg('✓ Message envoyé ! Je vous réponds sous 24h.', 'success')
          w.track('generate_lead', { form_name: 'contact', form_subject: payload.sujet })
          cform.reset()
        } else {
          setMsg(json.error || 'Une erreur est survenue. Réessayez.', 'error')
        }
      } catch {
        setMsg('Problème réseau. Vérifiez votre connexion et réessayez.', 'error')
      } finally {
        btn.disabled = false; btn.innerHTML = btnHTML
      }
    })
  }

  /* ── Sommaire automatique des articles ([slug].astro) ─────── */
  const content = $('.article-content')
  const tocList = $('#tocList')
  const toc = $('#articleToc')
  if (content && tocList && toc) {
    const headings = $$('h2, h3', content)
    if (headings.length < 2) {
      toc.classList.add('toc-hidden')
      const layout = $('.article-layout')
      layout && layout.classList.add('no-toc')
    } else {
      const slugify = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
        .replace(/[^\w\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-')
      const used = {}
      headings.forEach((h, i) => {
        const text = (h.textContent || '').trim()
        let id = slugify(text) || `section-${i}`
        if (used[id] !== undefined) { used[id]++; id += `-${used[id]}` } else { used[id] = 0 }
        h.id = id
        const li = document.createElement('li')
        li.className = `toc-item toc-${h.tagName.toLowerCase()}`
        const a = document.createElement('a')
        a.href = `#${id}`; a.textContent = text; a.className = 'toc-link'
        a.addEventListener('click', (e) => {
          e.preventDefault()
          const target = document.getElementById(id)
          if (target) window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 90, behavior: 'smooth' })
        })
        li.appendChild(a); tocList.appendChild(li)
      })
      const links = $$('.toc-link', tocList)
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            links.forEach((l) => l.classList.remove('toc-active'))
            const active = tocList.querySelector(`a[href="#${entry.target.id}"]`)
            active && active.classList.add('toc-active')
          }
        })
      }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 })
      headings.forEach((h) => observer.observe(h))
    }
  }

  /* ── Bouton « Copier le lien » ────────────────────────────── */
  const copyBtn = $('#copyBtn')
  const copyLabel = $('#copyLabel')
  if (copyBtn && copyLabel) {
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(window.location.href)
        copyLabel.textContent = 'Lien copié !'
        copyBtn.classList.add('copied')
        setTimeout(() => { copyLabel.textContent = 'Copier le lien'; copyBtn.classList.remove('copied') }, 2000)
      } catch { /* silencieux */ }
    })
  }

  /* ── Filtres des réalisations (realisations.astro) ────────────
     Chaque carte (conteneur Elementor) porte la classe real-cat-<filtre>. */
  const filterBtns = $$('.filter-btn')
  if (filterBtns.length) {
    const cards = $$('.real-card')
    filterBtns.forEach((btn) => btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.remove('active'))
      btn.classList.add('active')
      const filter = btn.dataset.filter
      cards.forEach((card) => {
        card.style.display = filter === 'tous' || card.classList.contains(`real-cat-${filter}`) ? '' : 'none'
      })
    }))
  }
})()
