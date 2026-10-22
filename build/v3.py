"""v3: scenes in every box, industry-aware booking form, Cal.com, email course sign-up, consent + GA4, legal pages, local SEO, OG images."""
import os as _os
_B = _os.path.dirname(_os.path.abspath(__file__))
_R = _os.path.dirname(_B)
import re, os, json, html as H
from industries_data import I
import scenes

OUT = _os.path.join(_R, 'site')
DOMAIN = 'https://cogentintelligence.co.uk'
EMAIL = 'hello@cogentintelligence.co.uk'
CAL = 'https://cal.com/jamiemac/30min'
GA = 'G-4MVYR1TFDB'
e = lambda s: H.escape(s, quote=False)
ea = lambda s: H.escape(s, quote=True)
CORE = [d for d in I if d['group'] == 'core']
NICHE = [d for d in I if d['group'] == 'niche']
ARROW = '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CAL_ICO = '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><rect x="2" y="3" width="12" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M2 6.5h12M5.5 1.5v3M10.5 1.5v3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'

def files():
    for root, _, fs in os.walk(OUT):
        for f in fs:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                yield p, os.path.relpath(p, OUT)

def pre(rel): return '../' * rel.count('/')

# ------------------------------------------------------------------ index: proper document
def fix_index():
    p = f'{OUT}/index.html'; s = open(p).read()
    if s.startswith('<!doctype html><html><head><meta charset=utf8>'):
        head = s[s.index('<title>'): s.index('<!-- /head -->')]
        body = s[s.index('<!-- /head -->') + len('<!-- /head -->'):]
        s = ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + head + '</head>\n<body data-page="home">' + body)
    open(p, 'w').write(s)

# ------------------------------------------------------------------ scenes everywhere
def scene_img(key, p, extra=''):
    return f'<img class="cover scene" src="{p}assets/scenes/{key}.svg" alt="" loading="lazy" decoding="async"{extra}>'

def apply_scenes(s, rel):
    p = pre(rel)
    def card(m):
        href = m.group(1)
        key = os.path.basename(href).replace('.html', '')
        if key == 'index': key = 'industries'
        return m.group(0)[:m.start(2) - m.start(0)] + scene_img(key, p) + m.group(0)[m.end(2) - m.start(0):]
    s = re.sub(r'<a class="dcard" href="([^"]+)"[^>]*>\s*<div class="dcard-cover">(<canvas class="cover"[^>]*></canvas>)', card, s)
    s = re.sub(r'(<div class="dgrid">\s*<div class="fp"><a class="dcard" href="[^"]*second-brain\.html"[^>]*>\s*<div class="dcard-cover"><img class="cover scene" src="[^"]*?)second-brain\.svg"', r'\1second-brain-tall.svg"', s)
    key = os.path.basename(rel).replace('.html', '')
    if 'class="art-cover"' in s and os.path.exists(f'{OUT}/assets/scenes/{key}.svg'):
        s = re.sub(r'(<div class="art-cover"[^>]*>)\s*<canvas class="cover"[^>]*></canvas>.*?(</div>)',
                   lambda m: m.group(1) + '\n        ' + scene_img(key, p, ' data-depth="0.25"').replace(' loading="lazy"', ' fetchpriority="high"') + '\n      ' + m.group(2), s, count=1, flags=re.S)
    if rel == 'index.html':
        for d in CORE:
            s = s.replace(f'id="sp-{d["slug"]}" aria-labelledby="st-{d["slug"]}"', f'id="sp-{d["slug"]}" aria-labelledby="st-{d["slug"]}" data-scene', 1)
        s = re.sub(r'(<div class="sector-panel[^"]*" role="tabpanel" id="sp-([a-z-]+)"[^>]*>.*?<div class="sp-side">)',
                   lambda m: m.group(1) + f'\n            <div class="sp-scene"><img src="assets/scenes/{m.group(2)}.svg" alt="" loading="lazy" decoding="async"></div>', s, flags=re.S)
    return s

# ------------------------------------------------------------------ labels, footer, head, scripts
def tidy(s, rel):
    p = pre(rel)
    for a, b in [('<p class="ask-note">Demo · dummy data</p>', ''), ('Watch it work · demo data', 'Watch it work'),
                 ('Example questions and answers, demo data', 'Example questions and answers'),
                 ('<figcaption class="fig-cap">Example log entries · dummy data.</figcaption>', ''),
                 ('<p class="fig-cap">Example · dummy data. Score = hours a week × ease.</p>', '<p class="fig-cap">Score = hours a week × ease.</p>'),
                 ('<b>Example · dummy data</b>', '<b>Example</b>'), (', dummy data</caption>', '</caption>'),
                 ('The business and the numbers are made up, but the shape is real.', 'The shape is what matters.')]:
        s = s.replace(a, b)
    legal = (f'<div class="foot-base"><span>© 2026 Cogent Intelligence · Solihull, West Midlands</span>'
             f'<span class="foot-legal"><a href="{p}privacy.html">Privacy</a><a href="{p}terms.html">Terms</a><a href="{p}cookies.html">Cookies</a>'
             f'<button type="button" class="cookie-link" data-cookie-settings>Cookie settings</button></span></div>')
    s = re.sub(r'<div class="foot-base">.*?</div>', legal, s, count=1, flags=re.S)
    s = s.replace(f'<li><a href="{DOMAIN}">cogentintelligence.co.uk</a></li>', f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>')
    s = re.sub(re.escape(DOMAIN) + r'/([A-Za-z0-9/_-]+)\.html', DOMAIN + r'/\1', s)
    s = s.replace('<li><a href="#" data-funnel>Book a free call</a></li>', f'<li><a href="#" data-funnel>Book a free call</a></li><li><a href="{CAL}" target="_blank" rel="noopener" data-cal>Pick a time in the calendar</a></li>', 1)
    s = re.sub(r'(<h4>Explore</h4>\s*<ul>)', lambda m: m.group(1) + f'<li><a href="{p}ai-automation-birmingham.html">Birmingham &amp; West Midlands</a></li>', s, count=1)
    # head: consent defaults before anything else loads, robots
    head_add = ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});</script>\n")
    if 'noindex' not in s:
        head_add = '<meta name="robots" content="index, follow, max-image-preview:large">\n' + head_add
    s = s.replace('viewport-fit=cover">\n', 'viewport-fit=cover">\n' + head_add, 1)
    src = '/assets/site.js' if rel == '404.html' else f'{p}assets/site.js'
    s = s.replace('</body>', f'<script src="{src}" defer></script>\n</body>', 1)
    # mobile menu + final section: direct calendar link
    s = s.replace('<span>Message us on WhatsApp</span></a>\n  </div>\n</div>', f'<span>Message us on WhatsApp</span></a>\n    <a class="wa-link" href="{CAL}" target="_blank" rel="noopener" data-cal>{CAL_ICO}<span>Pick a time in the calendar</span></a>\n  </div>\n</div>', 1)
    return s

# ------------------------------------------------------------------ email course block
COURSE_DAYS = ['Find your peak', 'Write your Business Map', 'Alone, ask first, never', 'Delegate, don\'t do', 'Measure the gain']
def course_block(p, compact=False):
    opts = ''.join(f'<option value="{ea(d["name"])}">{e(d["name"])}</option>' for d in CORE + NICHE) + '<option value="Other">Something else</option>'
    days = ''.join(f'<li><b>Day {i + 1}</b>{e(t)}</li>' for i, t in enumerate(COURSE_DAYS))
    return f'''<section class="course{' course--compact' if compact else ''}" id="course" aria-labelledby="course-h">
    <div class="{'' if compact else 'wrap'}">
      <div class="course-card" data-reveal>
        <div class="course-copy">
          <p class="kicker">Free 5-day email course</p>
          <h2 class="h2" id="course-h">Hand off your admin.</h2>
          <p class="lede">Not ready for a call? One short email a day for five days, with the same method we use with clients. By Friday you'll know which job to hand off first and how to keep control of it.</p>
          <ol class="course-days">{days}</ol>
        </div>
        <form class="course-form" data-signup novalidate>
          <label class="flabel" for="c-name{'-c' if compact else ''}">First name</label>
          <input class="finput" id="c-name{'-c' if compact else ''}" name="first_name" type="text" autocomplete="given-name" placeholder="Your first name">
          <label class="flabel" for="c-email{'-c' if compact else ''}">Work email</label>
          <input class="finput" id="c-email{'-c' if compact else ''}" name="email" type="email" autocomplete="email" inputmode="email" placeholder="name@yourbusiness.co.uk" required>
          <label class="flabel" for="c-ind{'-c' if compact else ''}">Your industry</label>
          <select class="finput" id="c-ind{'-c' if compact else ''}" name="industry"><option value="">Choose one</option>{opts}</select>
          <label class="consent"><input type="checkbox" name="consent" required><span>Send me the course and occasional emails from Cogent Intelligence. Unsubscribe any time.</span></label>
          <button class="btn btn-glow btn-lg" type="submit">Send me day 1 {ARROW}</button>
          <p class="course-status" role="status" aria-live="polite"></p>
          <p class="course-fine">We never share your email. <a href="{p}privacy.html">Privacy notice</a></p>
        </form>
      </div>
    </div>
  </section>'''

def add_course(s, rel):
    p = pre(rel)
    if rel == 'index.html':
        s = s.replace('  <!-- FINAL -->', '  ' + course_block(p) + '\n\n  <!-- FINAL -->', 1)
        s = s.replace('<a class="wa-link" href="#" data-wa>' , '<a class="wa-link" href="#" data-wa>', 1)
        s = s.replace('<span>Or message us on WhatsApp</span></a>\n      </div>\n      <p class="final-note">',
                      f'<span>Or message us on WhatsApp</span></a>\n        <a class="wa-link" href="{CAL}" target="_blank" rel="noopener" data-cal>{CAL_ICO}<span>Or pick a time in the calendar</span></a>\n      </div>\n      <p class="final-note">', 1)
    elif rel.startswith('industries/') or rel.startswith('insights/') or rel == 'ai-automation-birmingham.html':
        if 'class="article wrap"' in s:
            s = s.replace('  </article>', '    ' + course_block(p, True) + '\n  </article>', 1)
        elif '<aside class="art-cta"' in s:
            s = s.replace('    <aside class="art-cta"', '    ' + course_block(p, True) + '\n\n    <aside class="art-cta"', 1)
    return s

# ------------------------------------------------------------------ booking form (cogent.js)
def patch_cogent_js():
    p = f'{OUT}/assets/cogent.js'; s = open(p).read()
    data = {d['slug']: dict(tab=d['tab'], name=d['name'], core=d['group'] == 'core',
                            jobs=[j for j, h, x in sorted(d['score'], key=lambda r: -(r[1] * r[2]))][:5]) for d in I}
    s = 'window.COGENT_INDUSTRIES = ' + json.dumps(data, ensure_ascii=False) + ';\n' + s
    rep = [
        ("bookingUrl: '',", f"bookingUrl: '{CAL}',"),
        ("  const waLink = (text) => 'https://wa.me/' + WA_DIGITS + (text ? '?text=' + encodeURIComponent(text) : '');",
         "  const waLink = (text) => 'https://wa.me/' + WA_DIGITS + (text ? '?text=' + encodeURIComponent(text) : '');\n"
         "  const IND = window.COGENT_INDUSTRIES || {};\n"
         "  const esc = (v) => String(v).replace(/[&<>\"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;' }[c]));\n"
         "  const GENERAL_JOBS = ['Replying to enquiries', 'Writing quotes', 'Chasing invoices', 'Inbox admin', 'Booking and reminders', 'Copying data between apps', 'Reporting on my numbers'];\n"
         "  function jobChips(slug, checked) {\n"
         "    const ind = IND[slug];\n"
         "    const hot = ind ? ind.jobs : [];\n"
         "    const seen = new Set(hot.map((j) => j.toLowerCase()));\n"
         "    const all = hot.map((j) => [j, true]).concat(GENERAL_JOBS.filter((j) => !seen.has(j.toLowerCase())).map((j) => [j, false])).concat([['Something else', false]]);\n"
         "    return all.map(([j, h], i) => '<span class=\"chip' + (h ? ' chip--hot' : '') + '\"><input type=\"checkbox\" id=\"f-job-' + (i + 1) + '\" name=\"jobs\" value=\"' + esc(j) + '\"' + (checked.indexOf(j) > -1 ? ' checked' : '') + '><label for=\"f-job-' + (i + 1) + '\">' + esc(j) + '</label></span>').join('');\n"
         "  }\n"
         "  function industryList() {\n"
         "    const list = Object.keys(IND).filter((k) => IND[k].core).map((k) => [k, IND[k].tab]);\n"
         "    const here = document.body.dataset.industry;\n"
         "    if (here && IND[here] && !IND[here].core) list.unshift([here, IND[here].tab]);\n"
         "    return list.concat([['other', 'Something else']]);\n"
         "  }"),
        ("'   </fieldset>' +\n'   <fieldset class=\"fstep\" data-step=\"1\" hidden>' +",
         "'    <p class=\"flabel\" id=\"f-ind-l\">Your industry</p>' +\n'    <div class=\"chips chips--ind\" role=\"radiogroup\" aria-labelledby=\"f-ind-l\">' + industryList().map((x, i) => chip('radio', 'industry', 'f-ind-' + (i + 1), x[0], x[1])).join('') + '</div>' +\n'   </fieldset>' +\n'   <fieldset class=\"fstep\" data-step=\"1\" hidden>' +"),
        ("'    <div class=\"chips\" role=\"group\" aria-label=\"Jobs that take your time\">' + jobs.map((j, i) => chip('checkbox', 'jobs', 'f-job-' + (i + 1), j, j)).join('') + '</div>' +",
         "'    <p class=\"fhint\" id=\"f-jobs-hint\" hidden></p>' +\n'    <div class=\"chips\" id=\"f-jobs\" role=\"group\" aria-label=\"Jobs that take your time\">' + jobChips('', []) + '</div>' +"),
        ("Pick anything that eats your week. We\\'ll dig into it on the call.", "Pick anything that eats your week. Highlighted jobs are the ones we see most in your industry."),
        ("We\\'ll reply on WhatsApp to arrange your 30-minute call.", "Next, pick a time in our calendar. Your answers come with the booking."),
        ("Last step, <span id=\"d-name\">thanks</span>. Send it on WhatsApp.", "Last step, <span id=\"d-name\">thanks</span>. Pick a time."),
        ("Tap the button and WhatsApp opens with your brief already written. Press send and we\\'ll reply to book your call.",
         "Choose a slot in the calendar and your brief comes with it. Prefer to chat first? Send the brief on WhatsApp instead."),
        ("'     <a class=\"btn btn-glow btn-lg\" id=\"d-wa\" href=\"' + waLink('') + '\" target=\"_blank\" rel=\"noopener\">' + ICON_WA + ' Send on WhatsApp</a>' +\n'     <a class=\"btn btn-ghost\" id=\"d-book\" href=\"#\" target=\"_blank\" rel=\"noopener\" hidden>Or choose a time</a>' +",
         "'     <a class=\"btn btn-glow btn-lg\" id=\"d-book\" href=\"#\" target=\"_blank\" rel=\"noopener\" data-cal hidden>" + CAL_ICO.replace("'", "\\'") + " Pick a time for your call</a>' +\n'     <a class=\"btn btn-ghost\" id=\"d-wa\" href=\"' + waLink('') + '\" target=\"_blank\" rel=\"noopener\">' + ICON_WA + ' Or send on WhatsApp</a>' +"),
        ("Nothing is sent until you press send in WhatsApp.", "Nothing is sent until you confirm a time or press send in WhatsApp."),
        ("input[type=checkbox], #d-wa', s)", "input[type=checkbox], #d-book, #d-wa', s)"),
        ("    const labelFor = (input) => { const l = form.querySelector('label[for=\"' + input.id + '\"]'); return l ? l.textContent.trim() : input.value; };",
         "    const labelFor = (input) => { const l = form.querySelector('label[for=\"' + input.id + '\"]'); return l ? l.textContent.trim() : input.value; };\n"
         "    const jobsBox = $('#f-jobs'), jobsHint = $('#f-jobs-hint');\n"
         "    const setIndustry = (slug) => {\n"
         "      const checked = $$('input[name=\"jobs\"]:checked', form).map((c) => c.value);\n"
         "      jobsBox.innerHTML = jobChips(slug, checked);\n"
         "      const ind = IND[slug];\n"
         "      jobsHint.hidden = !ind;\n"
         "      if (ind) jobsHint.textContent = 'Highlighted: common in ' + ind.name.toLowerCase().replace(':', '');\n"
         "    };\n"
         "    $$('input[name=\"industry\"]', form).forEach((r) => r.addEventListener('change', () => setIndustry(r.value)));\n"
         "    const preselect = () => {\n"
         "      const sl = document.body.dataset.industry;\n"
         "      if (!sl || $('input[name=\"industry\"]:checked', form)) return;\n"
         "      const r = $('input[name=\"industry\"][value=\"' + sl + '\"]', form);\n"
         "      if (r) { r.checked = true; setIndustry(sl); }\n"
         "    };\n"
         "    document.addEventListener('click', (ev) => { if (ev.target.closest && ev.target.closest('[data-funnel]')) setTimeout(preselect, 0); }, true);"),
        ("        team: checkedLabel('team'),", "        team: checkedLabel('team'),\n        industry: checkedLabel('industry'),"),
        ("      if (d.team) L.push('Team size: ' + d.team);", "      if (d.industry) L.push('Industry: ' + d.industry);\n      if (d.team) L.push('Team size: ' + d.team);"),
        ("        ['Team', d.team || 'Not given'],", "        ['Industry', d.industry || 'Not given'],\n        ['Team', d.team || 'Not given'],"),
        ("      if (CONFIG.bookingUrl) book.href = CONFIG.bookingUrl;",
         "      if (CONFIG.bookingUrl) {\n        const q = new URLSearchParams();\n        if (d.name) q.set('name', d.name);\n        if (d.email) q.set('email', d.email);\n        q.set('notes', waText(d).split('\\n').slice(2).join('\\n'));\n        book.href = CONFIG.bookingUrl + '?' + q.toString();\n      }"),
        ("      renderBrief(data);", "      renderBrief(data);\n      if (window.CogentTrack) window.CogentTrack('generate_lead', { industry: data.industry || 'not set' });"),
    ]
    for a, b in rep:
        assert a in s, 'cogent.js anchor missing: ' + a[:70]
        s = s.replace(a, b, 1)
    open(p, 'w').write(s)
    # home tabs tell the form which industry the visitor looked at
    hp = f'{OUT}/assets/home.js'; h = open(hp).read()
    a = "  const select = (i, focus) => {\n"
    assert a in h
    h = h.replace(a, a + "    document.body.dataset.industry = tabs[i].id.slice(3);\n", 1)
    open(hp, 'w').write(h)

SITE_JS = r"""/* Cogent Intelligence: cookie consent + GA4 (loads only after consent), email course sign-up, conversion events. */
(() => {
  'use strict';
  /* ===== Settings ===== */
  const GA_ID = '__GA__';
  // Paste your email tool's form URL here (MailerLite, Kit or Formspree). Blank = sign-ups arrive by email instead.
  const SIGNUP_ACTION = '';
  const EMAIL = '__EMAIL__';
  const KEY = 'cogent-consent';

  const store = {
    get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
    set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  };
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  const prefix = () => {
    const m = document.querySelector('.brand img.mark');
    return m ? m.getAttribute('src').replace(/assets\/brand\/.*$/, '') : '';
  };
  let loaded = false;
  const loadGA = () => {
    if (loaded) return;
    loaded = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GA_ID);
  };
  const clearGA = () => {
    const host = location.hostname.split('.');
    const doms = ['', location.hostname, '.' + host.slice(-3).join('.'), '.' + host.slice(-2).join('.')];
    document.cookie.split(';').map((c) => c.split('=')[0].trim()).filter((n) => /^_ga/.test(n)).forEach((n) => {
      doms.forEach((d) => { document.cookie = n + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : ''); });
    });
  };
  const track = window.CogentTrack = (name, params) => { if (loaded) { try { gtag('event', name, params || {}); } catch (e) {} } };

  /* ---------- Cookie banner ---------- */
  const banner = () => {
    if (document.getElementById('cookie-banner')) return;
    const el = document.createElement('div');
    el.id = 'cookie-banner';
    el.className = 'cookie-banner';
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', 'Cookie choices');
    el.innerHTML = '<p><b>Your choice on cookies.</b> We\'d like to use Google Analytics cookies to see which pages help. They stay off unless you accept. <a href="' + prefix() + 'cookies.html">Cookie policy</a></p>' +
      '<div class="cookie-actions"><button type="button" class="btn btn-ghost" data-c="reject">Reject</button><button type="button" class="btn btn-ghost btn-accept" data-c="accept">Accept analytics</button></div>';
    document.body.appendChild(el);
    requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-on')));
    el.addEventListener('click', (ev) => {
      const b = ev.target.closest('[data-c]');
      if (!b) return;
      const ok = b.dataset.c === 'accept';
      store.set(ok ? 'granted' : 'denied');
      if (ok) loadGA();
      else { gtag('consent', 'update', { analytics_storage: 'denied' }); clearGA(); }
      el.classList.remove('is-on');
      setTimeout(() => el.remove(), 450);
    });
  };
  document.addEventListener('click', (ev) => {
    if (ev.target.closest('[data-cookie-settings]')) { ev.preventDefault(); banner(); }
    const cal = ev.target.closest('[data-cal]');
    if (cal) track('book_call_click', { link_url: cal.href });
    if (ev.target.closest('[data-wa], #d-wa')) track('whatsapp_click');
  });
  const choice = store.get();
  if (choice === 'granted') loadGA();
  else if (!choice) setTimeout(banner, 1200);

  /* ---------- Email course sign-up ---------- */
  document.addEventListener('submit', async (ev) => {
    const f = ev.target.closest('[data-signup]');
    if (!f) return;
    ev.preventDefault();
    const st = f.querySelector('.course-status');
    const btn = f.querySelector('button[type=submit]');
    const em = f.email.value.trim(), nm = f.first_name.value.trim(), ind = f.industry.value;
    st.classList.remove('is-err');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) { st.textContent = 'Check your email address.'; st.classList.add('is-err'); f.email.focus(); return; }
    if (!f.consent.checked) { st.textContent = 'Tick the box so we can send you the course.'; st.classList.add('is-err'); f.consent.focus(); return; }
    btn.disabled = true;
    const done = (msg) => {
      f.classList.add('is-done');
      st.textContent = msg;
      track('sign_up', { method: 'email_course', industry: ind || 'not set' });
    };
    try {
      if (SIGNUP_ACTION) {
        const fd = new FormData();
        if (/mailerlite/.test(SIGNUP_ACTION)) {
          fd.append('fields[email]', em); fd.append('fields[name]', nm); fd.append('fields[industry]', ind); fd.append('ml-submit', '1'); fd.append('anticsrf', 'true');
          await fetch(SIGNUP_ACTION, { method: 'POST', body: fd, mode: 'no-cors' });
        } else if (/kit\.com|convertkit/.test(SIGNUP_ACTION)) {
          fd.append('email_address', em); fd.append('first_name', nm); fd.append('fields[industry]', ind);
          await fetch(SIGNUP_ACTION, { method: 'POST', body: fd, mode: 'no-cors' });
        } else {
          const r = await fetch(SIGNUP_ACTION, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ email: em, first_name: nm, industry: ind, source: '5-day course', page: location.pathname }) });
          if (!r.ok) throw new Error('signup ' + r.status);
        }
        done('You\'re in' + (nm ? ', ' + nm : '') + '. Day 1 is on its way to ' + em + '.');
      } else {
        const body = 'Please send me the free 5-day course, Hand off your admin.\n\nName: ' + nm + '\nEmail: ' + em + '\nIndustry: ' + (ind || 'Not given');
        location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Sign me up: Hand off your admin') + '&body=' + encodeURIComponent(body);
        done('Your email app should open with your sign-up ready. Press send and day 1 follows.');
      }
    } catch (err) {
      btn.disabled = false;
      st.classList.add('is-err');
      st.textContent = 'That didn\'t go through. Try again, or email ' + EMAIL + '.';
    }
  });
})();
"""

CSS = r'''
/* ---------- v3: scenes, booking form, course, cookies ---------- */
img.cover{object-fit:cover}
.art-cover img.cover{position:absolute;inset:-4%;width:108%;height:108%}
.dcard-cover img.cover{position:absolute;inset:0;width:100%;height:100%;transition:transform .9s var(--ease)}
.dcard:hover .dcard-cover img.cover{transform:scale(1.04)}
.chip--hot label{border-color:rgba(255,122,47,.55);background:rgba(255,122,47,.09);color:var(--bone)}
.chip--hot label::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--ember);box-shadow:0 0 10px var(--ember)}
.fhint{margin:0 0 4px;font:500 11px/1.4 var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ember-2)}
.chips--ind .chip label{padding:9px 13px;font-size:14px}
.foot-legal{display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center}
.foot-legal a,.cookie-link{color:var(--mute);text-decoration:none;background:none;border:0;padding:0;font:inherit;cursor:pointer}
.foot-legal a:hover,.cookie-link:hover{color:var(--bone)}
.cookie-banner{position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:95;display:grid;gap:14px;max-width:min(560px,calc(100vw - 32px));padding:18px 20px;border-radius:20px;border:1px solid rgba(255,122,47,.35);background:rgba(20,18,17,.96);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);box-shadow:0 30px 70px -30px rgba(0,0,0,.9);opacity:0;transform:translateY(20px);transition:opacity .45s var(--ease),transform .45s var(--ease)}
.cookie-banner.is-on{opacity:1;transform:none}
.cookie-banner p{margin:0;color:var(--bone-2);font-size:14.5px;line-height:1.55}
.cookie-banner b{color:var(--bone)}
.cookie-banner a{color:var(--ember-2)}
.cookie-actions{display:flex;gap:10px;flex-wrap:wrap}
.cookie-actions .btn{flex:1 1 0;min-width:0;justify-content:center;padding-inline:12px}
@media (max-width:560px){.cookie-banner{padding:14px 16px;gap:10px}.cookie-banner p{font-size:13.5px}.cookie-actions .btn{padding-block:10px}}
.cookie-actions .btn-accept{border-color:rgba(255,122,47,.5)}
.course{padding-block:clamp(70px,10vh,120px)}
.course--compact{padding-block:56px 0}
.course-card{position:relative;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);padding:clamp(24px,4vw,48px);border-radius:28px;border:1px solid var(--rule);background:radial-gradient(90% 120% at 0% 0%,rgba(140,107,255,.14),transparent 55%),radial-gradient(80% 100% at 100% 100%,rgba(255,122,47,.12),transparent 60%),rgba(20,18,17,.9);overflow:hidden}
.course-copy{display:grid;gap:16px;align-content:start}
.course--compact .h2{font-size:clamp(1.7rem,3.2vw,2.6rem)}
.course-days{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:8px}
.course-days li{display:flex;gap:14px;align-items:baseline;padding:10px 14px;border-radius:12px;border:1px solid var(--rule-2);background:rgba(11,10,10,.4);color:var(--bone-2);font-size:15px}
.course-days b{flex:none;width:52px;font:500 11px/1 var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ember-2)}
.course-form{display:grid;gap:8px;align-content:start}
.course-form .flabel{margin-top:6px}
.course-form select.finput{appearance:none;-webkit-appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--mute) 50%),linear-gradient(135deg,var(--mute) 50%,transparent 50%);background-position:calc(100% - 22px) 50%,calc(100% - 16px) 50%;background-size:6px 6px;background-repeat:no-repeat;padding-right:40px}
.course-form select.finput option{background:var(--ink-2);color:var(--bone)}
.consent{display:flex;gap:12px;align-items:flex-start;margin:10px 0 6px;color:var(--mute);font-size:14px;line-height:1.5;cursor:pointer}
.consent input{flex:none;width:18px;height:18px;margin-top:2px;accent-color:var(--ember)}
.course-form .btn{justify-content:center;margin-top:6px}
.course-status{margin:4px 0 0;min-height:1.4em;color:var(--ok);font-size:14.5px}
.course-status.is-err{color:var(--err)}
.course-fine{margin:0;color:var(--dim);font-size:13px}
.course-fine a{color:var(--mute)}
.course-form.is-done .finput,.course-form.is-done .flabel,.course-form.is-done .consent,.course-form.is-done .btn{display:none}
.course-form.is-done .course-status{font-size:17px;color:var(--bone)}
@media (max-width:899px){.course-card{grid-template-columns:1fr}}
.prose .course,.article .course{margin-top:24px}
'''

HOME_CSS = r'''
.sp-scene{position:relative;aspect-ratio:16/7;border-radius:18px;overflow:hidden;border:1px solid var(--rule);background:var(--ink-2)}
.sp-scene img{display:block;width:100%;height:100%;object-fit:cover}
'''

# ------------------------------------------------------------------ legal + local pages
def prose_page(title_h1, dek, crumb, sections):
    toc = ''.join(f'<li><a href="#p{i + 1}">{e(h)}</a></li>' for i, (h, _) in enumerate(sections))
    body = ''.join(f'<section id="p{i + 1}"><h2><span class="num">{i + 1:02d}</span>{e(h)}</h2>{html}</section>\n' for i, (h, html) in enumerate(sections))
    return f'''  <article class="article wrap">
    <header class="art-hero">
      <div class="art-hero-text">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>{e(crumb)}</span></nav>
        <h1 class="art-title">{e(title_h1)}</h1>
        <p class="art-dek">{dek}</p>
      </div>
    </header>
    <div class="art-grid">
      <aside class="toc" aria-label="On this page"><p class="toc-h">On this page</p><ol>{toc}</ol></aside>
      <div class="prose">
{body}      </div>
    </div>
  </article>'''

UPDATED = '12 October 2026'
PRIVACY = [
 ('Who we are', f'<p>This website is run by Cogent Intelligence ("we", "us"), based in Solihull, West Midlands. We decide how the personal data described here is used, which makes us the data controller. Contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or on WhatsApp at +44 7753 226214.</p>'),
 ('What we collect', '<ul><li><strong>Booking form:</strong> your business name, industry, team size, the jobs taking your time, roughly how many hours they take, your name and, if you choose, your email address.</li><li><strong>Calendar bookings:</strong> when you book through Cal.com, your name, email, chosen time and any notes you add.</li><li><strong>Email course:</strong> your first name, email address and industry.</li><li><strong>Messages:</strong> anything you send us by WhatsApp or email, including your phone number.</li><li><strong>Analytics (only if you accept):</strong> pages visited, rough location (city level), device and browser type, and which buttons were used, collected by Google Analytics.</li><li><strong>Technical data:</strong> our hosting provider processes your IP address and basic browser details to deliver the site and protect it from abuse.</li></ul><p>The booking form doesn\'t store your answers on our servers. They travel with your calendar booking or your WhatsApp message, and only when you choose to send them.</p>'),
 ('Why we use it', '<ul><li>To arrange and prepare for your discovery call and send your one-page summary. Lawful basis: steps you\'ve asked us to take before a contract, and our legitimate interest in replying to business enquiries.</li><li>To send the email course and occasional emails. Lawful basis: your consent, which you can withdraw at any time with the unsubscribe link.</li><li>To understand how the site is used and improve it. Lawful basis: your consent through the cookie banner.</li></ul><p>We don\'t sell your data or use it for advertising.</p>'),
 ('Who we share it with', '<ul><li><strong>Cloudflare</strong> hosts this website and routes our email.</li><li><strong>Cal.com</strong> runs our booking calendar.</li><li><strong>Google</strong> provides Google Analytics (only with your consent) and serves the site\'s fonts.</li><li><strong>WhatsApp (Meta)</strong> carries any messages you send us there.</li><li><strong>Our email provider</strong> sends the email course.</li></ul><p>Some of these providers process data outside the UK. Where they do, they rely on recognised safeguards such as the UK International Data Transfer Addendum, the UK-US data bridge or adequacy regulations.</p>'),
 ('How long we keep it', '<p>If you don\'t become a client, we delete your enquiry details within 12 months of our last contact. Course subscribers stay on our list until they unsubscribe. Analytics data is kept for 14 months. If you become a client, we keep records for as long as the contract runs and for six years afterwards for legal and accounting reasons.</p>'),
 ('Cookies', '<p>Analytics cookies are only set if you accept them. You can change your choice at any time with the "Cookie settings" link at the foot of every page. The <a href="cookies.html">cookie policy</a> lists every cookie we use.</p>'),
 ('Your rights', f'<p>You can ask for a copy of your data, ask us to correct or delete it, object to how we use it, ask us to restrict it, or withdraw consent. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we\'ll reply within one month. If you\'re unhappy with how we\'ve handled your data, you can complain to the Information Commissioner\'s Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk</a>.</p>'),
 ('Client data', '<p>When we build agents for a client, we process their customers\' data on the client\'s instructions as a data processor. That\'s covered by a separate data processing agreement, signed before any agent goes live.</p>'),
]
TERMS = [
 ('About these terms', f'<p>These terms cover your use of cogentintelligence.co.uk and set out the main terms on which Cogent Intelligence ("we", "us") provides its services. Your written proposal and our client agreement give the full detail for any paid work, and they take priority if anything differs. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'),
 ('Using this website', '<p>You may use this site to learn about our services and to contact us. Don\'t misuse it: no attempts to break its security, scrape it in bulk, or send us harmful material. We may change or withdraw any part of the site without notice.</p>'),
 ('Information on the site', '<p>Content on this site is general information, not advice for your business. Demos, briefings and figures show how our agents work. They are examples, not results we promise for your business. Your discovery call and written proposal set out what we expect for you.</p>'),
 ('Prices and quotes', '<p>Prices on the site are starting prices and exclude VAT where applicable. You\'ll get a fixed written quote after your discovery call. A quote is valid for 30 days unless it says otherwise.</p>'),
 ('Payment', '<ul><li><strong>Setup:</strong> 50% when you accept the proposal, and 50% when your first agent goes live.</li><li><strong>Monthly plans:</strong> billed monthly in advance from the go-live date, by Direct Debit or card.</li><li>Invoices are due within 14 days. We may pause agents if an invoice is more than 30 days overdue, after giving you notice.</li></ul>'),
 ('The 14-day promise', '<p>For Standard setup, your first agent will be live within 14 days of the end of your mapping session. If it isn\'t, you won\'t pay the second 50% of setup until it is. The promise depends on you giving us the access, information and approvals we ask for within two working days of each request. Days lost waiting on those don\'t count. Custom AI agents follow the timeline agreed in your proposal.</p>'),
 ('Approvals and your responsibilities', '<p>Agents work from the Business Map and approval rules agreed with you. You\'re responsible for checking and approving anything that goes to a customer or involves money while approvals are on, for the accuracy of the information you give us, and for any regulated advice or decisions in your business. You can tighten or loosen approvals at any time.</p>'),
 ('Monthly plans and cancelling', '<p>Monthly plans roll month to month. Either side can cancel with 30 days\' written notice. Task allowances are set out in your plan. If you regularly go over yours, we\'ll talk to you before anything changes, and we won\'t add charges without your agreement. When you leave, we hand back your Business Map and export your data, then delete it from our systems within 30 days.</p>'),
 ('Data protection', '<p>Where we process personal data for you, we do so as your data processor under a data processing agreement signed before any agent goes live. Our <a href="privacy.html">privacy notice</a> explains how we handle data about you.</p>'),
 ('Intellectual property', '<p>You own your data, your Business Map and the content your agents produce for you. We keep ownership of our templates, methods and software, and give you a licence to use them for as long as you\'re a client. The content and design of this site belong to us.</p>'),
 ('Liability', '<p>Nothing in these terms limits liability for death or personal injury caused by negligence, for fraud, or for anything else that can\'t be limited by law. Otherwise, our total liability under any client agreement is limited to the fees you paid us in the 12 months before the claim. We\'re not liable for indirect losses, or for loss of profit, revenue or data that could have been avoided by following the agreed approval rules.</p>'),
 ('Law', '<p>These terms are governed by the law of England and Wales, and the courts of England and Wales have jurisdiction.</p>'),
]
COOKIES = [
 ('In short', '<p>We use one optional set of cookies, from Google Analytics, and only if you accept them. Everything else the site stores is there to make it work, and it never leaves your device.</p>'),
 ('Cookies and storage we use', '''<div class="table-wrap"><table><thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">What it does</th><th scope="col">How long</th></tr></thead><tbody>
<tr><td>_ga</td><td>Analytics (optional)</td><td>Google Analytics: tells visits apart</td><td>2 years</td></tr>
<tr><td>_ga_4MVYR1TFDB</td><td>Analytics (optional)</td><td>Google Analytics: keeps track of your current visit</td><td>2 years</td></tr>
<tr><td>cogent-consent</td><td>Necessary (local storage)</td><td>Remembers your cookie choice</td><td>Until you clear it</td></tr>
<tr><td>cogent-seen</td><td>Necessary (session storage)</td><td>Skips the intro animation after your first page</td><td>Until you close the tab</td></tr>
<tr><td>cogent-focus</td><td>Preference (local storage)</td><td>Remembers your reading-mode setting on articles</td><td>Until you clear it</td></tr>
</tbody></table></div>'''),
 ('Changing your mind', '<p>Use the "Cookie settings" link at the foot of any page to accept or reject analytics. If you reject them after accepting, we delete the Google Analytics cookies straight away. You can also clear cookies in your browser settings.</p>'),
 ('Third-party sites', '<p>Our booking calendar (Cal.com) and WhatsApp open on their own sites when you click through, and they set their own cookies under their own policies. Fonts are served by Google Fonts, which doesn\'t set cookies.</p>'),
]
TOWNS = ['Birmingham', 'Solihull', 'Coventry', 'Wolverhampton', 'Sutton Coldfield', 'Walsall', 'Dudley', 'West Bromwich', 'Redditch', 'Warwick and Leamington Spa']
def birmingham_body():
    links = ''.join(f'<li><a href="industries/{d["slug"]}.html">{e(d["name"])}</a></li>' for d in CORE)
    faqs = [('Do you come to our office?', 'Yes. Across the West Midlands we can run the half-day mapping session at your premises, which is often the fastest way to see how work really flows. Outside the region we run it by video.'),
            ('Do you only work with West Midlands businesses?', 'No. We work with service businesses across the UK. Being local just means we can meet you in person.'),
            ('How much does AI automation cost for a small business in Birmingham?', 'The discovery call is free. Standard setup starts at £1,997 and a custom AI agent at £4,997. Monthly plans start at £297 for one agent.'),
            ('How quickly can we have an agent working?', 'Your first agent from Standard setup goes live within 14 days of the mapping session, or you don\'t pay the second half of setup until it does.')]
    fq = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in faqs)
    secs = [
        ('Local, and in the room', f'<p>Cogent Intelligence is based in Solihull. We build AI agents and a business second brain for owner-led service businesses across Birmingham and the West Midlands, including {", ".join(TOWNS[1:-1])} and {TOWNS[-1]}.</p><p>Most AI automation agencies work remotely. We can sit with your team for the mapping session, see how enquiries, quotes, chasing and reporting really happen, and come back 14 days later with your first agent working.</p><div class="keyidea"><p class="kicker">Key idea</p><p>The fastest way to map a business is to watch it work for an afternoon.</p></div>'),
        ('Industries we work with', f'<p>Each sector has its own playbook of agents, approvals and the tools it already uses:</p><ul>{links}</ul><p>We also work with <a href="industries/index.html">specialist niches</a> such as EPC assessors, fire and H&amp;S consultants, renewables installers, brokers, training providers, venues and garages.</p>'),
        ('How it works', '<ol><li><strong>Free discovery call (30 minutes).</strong> We find your top 3 time-wasters and send a one-page summary within 24 hours.</li><li><strong>Mapping session (half a day).</strong> On site or by video, we map your people, tools, prices and rules into your Business Map.</li><li><strong>Build (days 4 to 12).</strong> Your first agent is built from tested templates, with approvals set.</li><li><strong>Go live (day 14).</strong> It starts work around the clock, and anything customer-facing or money-related waits for your tap.</li></ol>'),
        ('Pricing', '<p>Standard setup from £1,997 and a custom AI agent from £4,997, both one-off. Monthly plans from £297 for one agent, £597 for up to three and £897 for up to six, with tasks included. Rolling monthly, no long contracts. <a href="index.html#offer">See full pricing</a>.</p>'),
        ('Questions', fq),
    ]
    return prose_page('AI automation for Birmingham and West Midlands businesses',
                      'AI agents and a business second brain for service businesses in Birmingham, Solihull, Coventry and across the West Midlands. Mapped in person, live in 14 days.', 'Birmingham & West Midlands', secs).replace('<header class="art-hero">\n      <div class="art-hero-text">', '<header class="art-hero">\n      <div class="art-hero-text">', 1), faqs

def legal_pages(page_shell):
    pages = [
        ('privacy.html', 'Privacy notice · Cogent Intelligence', 'How Cogent Intelligence collects, uses and protects personal data when you use this website, book a call or join the email course.', prose_page('Privacy notice', f'What we collect when you use this website, book a call or join the email course, why, and your rights. Last updated {UPDATED}.', 'Privacy', PRIVACY), None),
        ('terms.html', 'Terms and conditions · Cogent Intelligence', 'Website terms of use and the main terms on which Cogent Intelligence provides AI agent setup and monthly plans.', prose_page('Terms and conditions', f'The terms for using this website and the main terms for our services, including payment, the 14-day promise and cancelling. Last updated {UPDATED}.', 'Terms', TERMS), None),
        ('cookies.html', 'Cookie policy · Cogent Intelligence', 'The cookies and browser storage cogentintelligence.co.uk uses, and how to change your choice.', prose_page('Cookie policy', f'Which cookies we use, why, and how to change your mind. Last updated {UPDATED}.', 'Cookies', COOKIES), None),
    ]
    bbody, bfaq = birmingham_body()
    pages.append(('ai-automation-birmingham.html', 'AI Automation Birmingham & West Midlands | AI Agents for Local Businesses · Cogent Intelligence',
                  'AI automation for Birmingham, Solihull and West Midlands service businesses. AI agents that answer, chase and report, mapped in person and live in 14 days. Free 30-minute call.', bbody, bfaq))
    for rel, title, desc, body, faq in pages:
        url = DOMAIN + '/' + rel.replace('.html', '')
        graph = [{"@type": "WebPage", "name": title, "url": url, "dateModified": "2026-10-12"},
                 {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": title.split(' · ')[0].split(' | ')[0], "item": url}]}]
        if faq:
            graph.append({"@type": "ProfessionalService", "name": "Cogent Intelligence", "url": DOMAIN + "/", "image": DOMAIN + "/assets/og/birmingham.jpg",
                          "address": {"@type": "PostalAddress", "addressLocality": "Solihull", "addressRegion": "West Midlands", "addressCountry": "GB"},
                          "areaServed": [{"@type": "City", "name": t} for t in TOWNS], "telephone": "+44 7753 226214", "email": EMAIL, "priceRange": "££"})
            graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        s = page_shell('', rel, title, desc, body, False, {"@context": "https://schema.org", "@graph": graph}, page='article')
        s = s.replace(' class="is-active" aria-current="page"', '')
        if rel == 'ai-automation-birmingham.html':
            s = s.replace('<header class="art-hero">\n      <div class="art-hero-text">', '<header class="art-hero">\n      <div class="art-hero-text">', 1)
            s = s.replace('</p>\n      </div>\n    </header>', '</p>\n      </div>\n      <div class="art-cover" data-parallax aria-hidden="true">\n        ' + scene_img('birmingham', '', ' data-depth="0.25"').replace(' loading="lazy"', ' fetchpriority="high"') + '\n      </div>\n    </header>', 1)
        open(f'{OUT}/{rel}', 'w').write(s)

# ------------------------------------------------------------------ SEO extras
def seo(s, rel):
    key = os.path.basename(rel).replace('.html', '')
    if rel == 'index.html': key = 'home'
    elif rel == 'industries/index.html': key = 'industries'
    elif rel == 'insights/index.html': key = 'second-brain'
    elif rel == 'ai-automation-birmingham.html': key = 'birmingham'
    elif not os.path.exists(f'{OUT}/assets/scenes/{key}.svg'): key = 'home'
    s = s.replace(f'content="{DOMAIN}/assets/brand/og-image.jpg"', f'content="{DOMAIN}/assets/og/{key}.jpg"')
    if rel.startswith('industries/') and rel != 'industries/index.html':
        s = s.replace('<body class="page-article" data-page="article">', f'<body class="page-article" data-page="article" data-industry="{key}">', 1)
    if rel == 'index.html':
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S)
        g = json.loads(m.group(1))
        for n in g['@graph']:
            if n.get('@type') == 'ProfessionalService':
                n.update({"address": {"@type": "PostalAddress", "addressLocality": "Solihull", "addressRegion": "West Midlands", "addressCountry": "GB"},
                          "email": EMAIL, "priceRange": "££", "image": DOMAIN + "/assets/og/home.jpg",
                          "areaServed": [{"@type": "Country", "name": "United Kingdom"}, {"@type": "AdministrativeArea", "name": "West Midlands"}]})
        s = s[:m.start(1)] + json.dumps(g, ensure_ascii=False) + s[m.end(1):]
    return s, key

def sitemap_llms():
    sm = open(f'{OUT}/sitemap.xml').read()
    add = ''.join(f'  <url><loc>{DOMAIN}/{u}</loc><lastmod>2026-10-12</lastmod></url>\n' for u in ['terms', 'cookies', 'ai-automation-birmingham'] if f'/{u}<' not in sm)
    sm = sm.replace('</urlset>', add + '</urlset>').replace('2026-10-09', '2026-10-12').replace('2026-10-11', '2026-10-12')
    open(f'{OUT}/sitemap.xml', 'w').write(sm)
    lines = ['# Cogent Intelligence', '', '> AI agents and a business second brain for UK service businesses. Based in Solihull, West Midlands. Free 30-minute discovery call; standard setup from £1,997, custom AI agent from £4,997, monthly plans from £297 per month. First agent live in 14 days, with human approval on anything customer-facing or involving money. Owners can delegate jobs by WhatsApp, Slack, Telegram, email or voice note.', '',
             '## Key pages', f'- [Home]({DOMAIN}/): what Cogent does, pricing and FAQs', f'- [Industries]({DOMAIN}/industries/): playbooks by sector', f'- [Birmingham and West Midlands]({DOMAIN}/ai-automation-birmingham)', f'- [Book a call]({CAL})', '', '## Industry playbooks']
    lines += [f'- [{d["name"]}]({DOMAIN}/industries/{d["slug"]}): {d["meta"]}' for d in I]
    lines += ['', '## Insights', f'- [Your business needs a second brain]({DOMAIN}/insights/second-brain)', f'- [Find your peak]({DOMAIN}/insights/find-your-peak)', f'- [Approvals first]({DOMAIN}/insights/approvals-first)', '', '## Legal', f'- [Privacy]({DOMAIN}/privacy)', f'- [Terms]({DOMAIN}/terms)', f'- [Cookies]({DOMAIN}/cookies)']
    open(f'{OUT}/llms.txt', 'w').write('\n'.join(lines) + '\n')

OG_TITLES = {}

def run(page_shell):
    scenes.build()
    fix_index()
    patch_cogent_js()
    legal_pages(page_shell)
    for p, rel in files():
        s = open(p).read()
        s = apply_scenes(s, rel)
        s = tidy(s, rel)
        s = add_course(s, rel)
        s, key = seo(s, rel)
        t = re.search(r'<title>(.*?)</title>', s)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, flags=re.S)
        OG_TITLES[key] = OG_TITLES.get(key) or re.sub('<[^>]+>', ' ', h1.group(1)).strip() if h1 else (t.group(1) if t else '')
        if rel == '404.html':
            s = re.sub(r'(href|src)="(?!https?:|#|/|mailto:)([^"]+)"', r'\1="/\2"', s)
        open(p, 'w').write(s)
    open(f'{OUT}/assets/site.js', 'w').write(SITE_JS.replace('__GA__', GA).replace('__EMAIL__', EMAIL))
    open(f'{OUT}/assets/cogent.css', 'a').write(CSS)
    open(f'{OUT}/assets/home.css', 'a').write(HOME_CSS)
    sitemap_llms()
    OG_TITLES['home'] = 'AI agents and a second brain for UK service businesses'
    OG_TITLES['industries'] = 'AI agents built for your industry'
    json.dump(OG_TITLES, open(_os.path.join(_B, 'og_titles.json'), 'w'), ensure_ascii=False, indent=1)
