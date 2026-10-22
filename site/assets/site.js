/* Cogent Intelligence: cookie consent + GA4 (loads only after consent), email course sign-up, conversion events. */
(() => {
  'use strict';
  /* ===== Settings ===== */
  const GA_ID = 'G-4MVYR1TFDB';
  // Paste your email tool's form URL here (MailerLite, Kit or Formspree). Blank = sign-ups arrive by email instead.
  const SIGNUP_ACTION = '';
  const EMAIL = 'hello@cogentintelligence.co.uk';
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
