/* Cogent Intelligence home page: intro, scroll scenes, ask-your-business demo, 14-day focus timeline, calculator. */
(() => {
  'use strict';
  const C = window.Cogent;
  if (!C) return;
  const { $, $$, reduce } = C;
  const html = document.documentElement;
  const mapT = C.mapT;
  const safe = (fn, name) => { try { fn(); } catch (err) { console.warn('[cogent home] ' + name, err); } };

  safe(splitWords, 'words');
  safe(initIntro, 'intro');
  safe(initScroll, 'scroll');
  safe(initHeroChips, 'chips');
  safe(initSequences, 'sequences');
  safe(initAsk, 'ask');
  safe(initSteps, 'steps');
  safe(initCalc, 'calc');
  safe(initFaq, 'faq');
  safe(initControl, 'control');
  safe(initHashLanding, 'hash');

  /* ---------- Manifesto words ---------- */
  function splitWords() {
    $$('[data-words]').forEach((p) => {
      const out = document.createDocumentFragment();
      Array.from(p.childNodes).forEach((node) => {
        const hl = node.nodeType === 1;
        node.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { out.appendChild(document.createTextNode(' ')); return; }
          const s = document.createElement('span');
          s.className = hl ? 'w hl' : 'w';
          s.textContent = part;
          out.appendChild(s);
        });
      });
      p.textContent = '';
      p.appendChild(out);
    });
  }

  /* ---------- Intro / loader ---------- */
  function initIntro() {
    const loader = $('#loader');
    const go = () => html.classList.add('intro-go');
    if (!html.classList.contains('is-loading') || !loader) {
      requestAnimationFrame(() => requestAnimationFrame(go));
      return;
    }
    const bar = $('.loader-line i', loader), count = $('.loader-count', loader);
    const t0 = performance.now(), D = 950;
    let finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      html.classList.remove('is-loading');
      go();
      try { sessionStorage.setItem('cogent-seen', '1'); } catch (e) {}
      if (C.lenis) C.lenis.start();
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
    };
    const tick = () => {
      const p = Math.min(1, (performance.now() - t0) / D);
      const e = 1 - Math.pow(1 - p, 3);
      bar.style.transform = 'scaleX(' + e + ')';
      count.textContent = String(Math.round(e * 100)).padStart(3, '0');
      if (p < 1) { requestAnimationFrame(tick); return; }
      loader.classList.add('is-out');
      setTimeout(go, 280);
      setTimeout(finish, 950);
    };
    requestAnimationFrame(tick);
    setTimeout(finish, 3200);
  }

  /* ---------- Scroll choreography ---------- */
  function initScroll() {
    const G = window.gsap, ST = window.ScrollTrigger;
    if (!G || !ST) { html.classList.add('no-gsap'); return; }
    ST.config({ ignoreMobileResize: true });
    const mm = G.matchMedia();
    mm.add({ desk: '(min-width: 900px)', mob: '(max-width: 899.98px)', motion: '(prefers-reduced-motion: no-preference)' }, (ctx) => {
      const desk = ctx.conditions.desk;
      if (!ctx.conditions.motion) return;
      sceneHero(G);
      sceneManifesto(G, desk);
      sceneRail(G, desk);
      sceneReveals(G);
      sceneMap(G, desk);
      sceneFinal(G);
      return () => { $('.rail').classList.remove('is-pinned'); };
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => ST.refresh());
    window.addEventListener('load', () => ST.refresh());
  }

  function sceneHero(G) {
    G.to('.hero-core', { yPercent: -12, scale: 0.94, autoAlpha: 0, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    G.to(['.hero-corner', '.scroll-pill', '.hero-chips'], { autoAlpha: 0, y: -30, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: '35% top', scrub: true } });
  }

  function sceneManifesto(G, desk) {
    const sec = $('.manifesto');
    const words = $$('.manifesto-text .w', sec);
    G.set(words, { opacity: 0.13 });
    const tl = G.timeline({
      scrollTrigger: desk
        ? { trigger: sec, start: 'top top', end: '+=150%', pin: true, scrub: 0.6, anticipatePin: 1 }
        : { trigger: sec, start: 'top 80%', end: 'bottom 70%', scrub: 0.6 }
    });
    tl.to(words, { opacity: 1, ease: 'none', stagger: 0.06, duration: 0.4 })
      .from('.manifesto-after', { autoAlpha: 0.15, y: 24, duration: 0.8, ease: 'power2.out' }, '-=0.2');
  }

  function sceneRail(G, desk) {
    if (!desk) return;
    const sec = $('.rail'), track = $('.rail-track'), vp = $('.rail-viewport');
    sec.classList.add('is-pinned');
    vp.scrollLeft = 0;
    const dist = () => Math.max(0, track.scrollWidth - vp.clientWidth);
    const tween = G.to(track, {
      x: () => -dist(), ease: 'none',
      scrollTrigger: { trigger: sec, start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1 }
    });
    G.fromTo('.rail-progress i', { scaleX: 0 }, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: sec, start: 'top top', end: () => '+=' + dist(), scrub: true, invalidateOnRefresh: true } });
    $$('.agent-card', track).forEach((card) => {
      G.fromTo(card, { y: 70, rotate: 3, autoAlpha: 0.35 }, { y: 0, rotate: 0, autoAlpha: 1, ease: 'none', scrollTrigger: { trigger: card, containerAnimation: tween, start: 'left 100%', end: 'left 62%', scrub: true } });
    });
  }

  function sceneReveals(G) {
    $$('[data-reveal]').forEach((el) => G.from(el, { y: 40, autoAlpha: 0.2, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } }));
    $$('[data-stagger]').forEach((g) => G.from(g.children, { y: 48, autoAlpha: 0.2, duration: 1, stagger: 0.09, ease: 'power3.out', scrollTrigger: { trigger: g, start: 'top 85%', once: true } }));
  }

  function sceneMap(G, desk) {
    const st = (trigger, start, end) => ({ trigger, start, end, scrub: true });
    G.fromTo(mapT, { tilt: 0.08 }, { tilt: 0.85, ease: 'none', immediateRender: false, scrollTrigger: st('.hero', 'top top', 'bottom top') });
    G.fromTo(mapT, { hole: 0 }, { hole: 1, ease: 'none', immediateRender: false, scrollTrigger: st('.manifesto', 'top 70%', desk ? 'top -55%' : 'center 50%') });
    G.fromTo(mapT, { hole: 1 }, { hole: 0, ease: 'none', immediateRender: false, scrollTrigger: st('.intel', 'top 90%', 'top 20%') });
    G.fromTo(mapT, { tilt: 0.85 }, { tilt: 0.3, ease: 'none', immediateRender: false, scrollTrigger: st('.process', 'top 80%', 'top top') });
    G.fromTo(mapT, { apex: 0 }, { apex: 1, ease: 'none', immediateRender: false, scrollTrigger: st('.calc', 'top 85%', 'top 25%') });
    G.fromTo(mapT, { tilt: 0.3 }, { tilt: 0.62, ease: 'none', immediateRender: false, scrollTrigger: st('.offer', 'top bottom', 'bottom top') });
    G.fromTo(mapT, { heat: 0 }, { heat: 1, ease: 'none', immediateRender: false, scrollTrigger: st('.final', 'top 85%', 'center 55%') });
  }

  function sceneFinal(G) {
    G.fromTo('.final-title', { scale: 0.8, autoAlpha: 0.25 }, { scale: 1, autoAlpha: 1, ease: 'none', scrollTrigger: { trigger: '.final', start: 'top 90%', end: 'center 60%', scrub: true } });
  }

  /* ---------- Hero activity chips ---------- */
  function initHeroChips() {
    if (reduce) return;
    const pool = [
      { t: 'Monday briefing ready', c: 'violet' }, { t: 'Enquiry answered · 23:47', c: 'ok' },
      { t: 'Priya prefers Thursdays', c: 'violet' }, { t: 'Quote ready for your OK', c: 'ember' },
      { t: 'Paid: INV-2038', c: 'ok' }, { t: 'Enquiries up 12% this week', c: 'violet' },
      { t: 'Booked: Thu 10:30', c: 'ok' }, { t: 'Refund awaiting your OK', c: 'ember' },
      { t: 'Reminder 2 sent · INV-2044', c: 'ok' }, { t: 'Supplier email filed', c: 'ok' }
    ];
    const chips = $$('.hchip'), live = $('.hero-live');
    let i = 0, visible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe($('.hero'));
    setInterval(() => {
      if (!visible || document.hidden) return;
      i++;
      const desk = window.innerWidth >= 1240;
      const chip = desk ? chips[i % chips.length] : live;
      if (!chip) return;
      const showing = (desk ? chips : [live]).map((c) => $('.txt', c).textContent);
      let msg = pool[i % pool.length];
      for (let k = 1; k < pool.length && showing.indexOf(msg.t) > -1; k++) msg = pool[(i + k) % pool.length];
      chip.classList.add('swap');
      setTimeout(() => {
        $('.txt', chip).textContent = msg.t;
        const dot = $('.dot', chip);
        dot.classList.toggle('ember', msg.c === 'ember');
        dot.classList.toggle('violet', msg.c === 'violet');
        chip.classList.remove('swap', 'ping');
        void chip.offsetWidth;
        chip.classList.add('ping');
      }, 300);
    }, 2300);
  }

  /* ---------- Sequenced motion graphics (agent cards, approval demo) ---------- */
  function initSequences() {
    if (reduce || !('IntersectionObserver' in window)) return;
    const seqs = $$('[data-seq]').map((el) => {
      const items = $$('[data-at]', el).map((n) => ({ n, at: +n.dataset.at, until: n.dataset.until != null ? +n.dataset.until : Infinity }));
      const movers = $$('[data-moves]', el).map((n) => ({ n, pts: JSON.parse(n.dataset.moves) }));
      return { el, items, movers, max: Math.max(0, ...items.map((x) => x.at)), hold: +(el.dataset.hold || 5), tick: +(el.dataset.tick || 700), step: 0, last: 0, live: false };
    });
    const apply = (s) => {
      s.items.forEach((x) => x.n.classList.toggle('on', s.step >= x.at && s.step < x.until));
      s.movers.forEach((mv) => {
        const p = mv.pts[Math.min(s.step, mv.pts.length - 1)];
        mv.n.style.left = p[0] + '%';
        mv.n.style.top = p[1] + '%';
      });
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        const s = seqs.find((x) => x.el === en.target);
        if (!s) return;
        s.live = en.isIntersecting;
        if (s.live) {
          s.step = 0; s.last = performance.now();
          apply(s);
          s.el.classList.add('is-live');
        } else {
          s.el.classList.remove('is-live');
          s.items.forEach((x) => x.n.classList.remove('on'));
          s.movers.forEach((mv) => { mv.n.style.left = ''; mv.n.style.top = ''; });
        }
      });
    }, { threshold: 0.3 });
    seqs.forEach((s) => io.observe(s.el));
    const loop = () => {
      const t = performance.now();
      seqs.forEach((s) => {
        if (!s.live || t - s.last < s.tick) return;
        s.last = t;
        s.step = s.step >= s.max + s.hold ? 0 : s.step + 1;
        apply(s);
      });
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Ask your business (demo data) ---------- */
  function initAsk() {
    const root = $('#ask');
    if (!root) return;
    const qEl = $('#ask-q'), textEl = $('#ask-text'), vizEl = $('#ask-viz'), srcEl = $('#ask-src');
    const caps = $$('.cap');
    const QA = [
      { q: 'What did Priya ask for last time?', a: 'A full kitchen refit quote in March. She prefers Thursday surveys and asked about paying in stages.', src: ['Memory', 'CRM'],
        viz: { type: 'memo', title: 'Priya S. · customer memory', items: ['12 Mar · Quote Q-0291, full kitchen refit', 'Prefers Thursday morning surveys', 'Asked about paying in stages'] } },
      { q: 'What do we charge for a bathroom refit in LS6?', a: 'From £5,800 for a standard refit, plus £240 waste removal. LS6 is inside your service area, so there\'s no travel charge.', src: ['Price list', 'Business Map'],
        viz: { type: 'bars', title: 'Bathroom refits · your price list', rows: [['Standard refit', '£5,800', 83], ['Premium refit', '£7,000', 100], ['Waste removal', '£240', 6]] } },
      { q: 'How did enquiries do last week?', a: '41 new enquiries, up 12% on the week before. 38 were answered in under 5 minutes, and most arrived after 6pm.', src: ['Web form', 'Gmail'],
        viz: { type: 'spark', title: 'Enquiries · week of 5 Oct', days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], vals: [4, 6, 5, 7, 6, 8, 5] } },
      { q: 'Chase the quotes that are still waiting.', a: 'Three quotes, £14,260 in total. I\'ve drafted a follow-up for each in your tone. Nothing goes out until you approve it.', src: ['Quote Drafter', 'Approvals on'],
        viz: { type: 'drafts', title: 'Follow-ups drafted', rows: [['Hartley Kitchens', '£7,050 · waiting 9 days'], ['Moss Lane Dental', '£4,410 · waiting 6 days'], ['Bramble Café', '£2,800 · waiting 2 days']] } }
    ];
    const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
    const renderViz = (qa) => {
      const v = qa.viz;
      vizEl.textContent = '';
      vizEl.appendChild(el('p', 'vz-title', v.title));
      if (v.type === 'bars') {
        const box = el('div', 'vz-rows');
        v.rows.forEach(([l, val, pct]) => {
          const row = el('div', 'vz-row');
          row.appendChild(el('span', 'l', l));
          const b = el('span', 'b'); const i = el('i'); i.style.setProperty('--w', pct + '%'); b.appendChild(i);
          row.appendChild(b);
          row.appendChild(el('span', 'v', val));
          box.appendChild(row);
        });
        vizEl.appendChild(box);
      } else if (v.type === 'spark') {
        const box = el('div', 'vz-spark');
        const max = Math.max.apply(null, v.vals);
        v.vals.forEach((n, k) => {
          const col = el('div');
          const i = el('i'); i.style.setProperty('--h', Math.round((n / max) * 100) + '%'); i.title = n + ' enquiries';
          col.appendChild(i); col.appendChild(el('span', '', v.days[k]));
          box.appendChild(col);
        });
        vizEl.appendChild(box);
      } else if (v.type === 'memo') {
        const ul = el('ul', 'vz-memo');
        v.items.forEach((t) => ul.appendChild(el('li', '', t)));
        vizEl.appendChild(ul);
      } else if (v.type === 'drafts') {
        const box = el('div', 'vz-drafts');
        v.rows.forEach(([n, d]) => {
          const r = el('div', 'vz-draft');
          r.appendChild(el('b', '', n)); r.appendChild(el('small', '', d)); r.appendChild(el('span', '', 'Waiting for your OK'));
          box.appendChild(r);
        });
        vizEl.appendChild(box);
      }
    };
    const renderSrc = (qa) => { srcEl.textContent = ''; qa.src.forEach((s) => srcEl.appendChild(el('span', '', s))); };
    const setCap = (i) => caps.forEach((c, k) => c.setAttribute('aria-pressed', k === i ? 'true' : 'false'));
    let idx = 0, token = 0, live = false, pausedUntil = 0;
    const renderStatic = (i) => {
      idx = i;
      const qa = QA[i];
      setCap(i);
      root.classList.remove('is-thinking', 'is-stale');
      qEl.textContent = qa.q;
      textEl.textContent = qa.a;
      renderViz(qa);
      renderSrc(qa);
    };
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const play = async (i, tk) => {
      const qa = QA[i];
      idx = i;
      setCap(i);
      root.classList.add('is-stale');
      qEl.textContent = '';
      for (const ch of qa.q) { if (tk !== token) return; qEl.textContent += ch; await sleep(26); }
      await sleep(350); if (tk !== token) return;
      root.classList.add('is-thinking');
      await sleep(750);
      root.classList.remove('is-thinking', 'is-stale');
      if (tk !== token) return;
      textEl.textContent = ''; srcEl.textContent = '';
      renderViz(qa);
      const words = qa.a.split(' ');
      for (let w = 0; w < words.length; w++) { if (tk !== token) return; textEl.textContent += (w ? ' ' : '') + words[w]; await sleep(34); }
      renderSrc(qa);
    };
    const loop = async () => {
      const tk = ++token;
      while (tk === token) {
        await play(idx, tk);
        if (tk !== token) return;
        await sleep(3800);
        if (tk !== token) return;
        if (performance.now() < pausedUntil) { await sleep(pausedUntil - performance.now()); if (tk !== token) return; }
        idx = (idx + 1) % QA.length;
      }
    };
    caps.forEach((c, k) => c.addEventListener('click', () => {
      pausedUntil = performance.now() + 9000;
      if (reduce || !live) { token++; renderStatic(k); return; }
      idx = k;
      loop();
    }));
    renderStatic(0);
    if (reduce || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(([en]) => {
      if (en.isIntersecting && !live) { live = true; loop(); }
      else if (!en.isIntersecting && live) { live = false; token++; renderStatic(idx); }
    }, { threshold: 0.35 }).observe(root);
  }

  /* ---------- 14 days: steps come into focus, day counter follows ---------- */
  function initSteps() {
    const steps = $$('.step');
    if (!steps.length) return;
    const list = $('.steps');
    const nums = $$('[data-day-num]'), phases = $$('[data-day-phase]'), fills = $$('[data-day-fill]');
    list.classList.add('is-armed');
    let cur = -1, shown = 14, raf = 0;
    const roll = (to) => {
      cancelAnimationFrame(raf);
      const from = shown, s = performance.now();
      const step = () => {
        const p = reduce ? 1 : Math.min(1, (performance.now() - s) / 600);
        const v = Math.round(from + (to - from) * (1 - Math.pow(1 - p, 3)));
        nums.forEach((n) => { n.textContent = String(v).padStart(2, '0'); });
        if (p < 1) raf = requestAnimationFrame(step); else shown = to;
      };
      raf = requestAnimationFrame(step);
    };
    const set = (i) => {
      if (i === cur) return;
      cur = i;
      steps.forEach((s, k) => s.classList.toggle('is-active', k === i));
      const s = steps[i];
      roll(+s.dataset.day);
      phases.forEach((p) => { p.textContent = s.dataset.phase; });
      fills.forEach((f) => { f.style.transform = 'scaleX(' + Math.min(1, +s.dataset.day / 30).toFixed(3) + ')'; });
    };
    let ticking = false;
    const update = () => {
      ticking = false;
      const mid = window.innerHeight * 0.5;
      let best = 0, bestD = Infinity;
      steps.forEach((s, k) => {
        const r = s.getBoundingClientRect();
        const d = Math.abs(r.top + r.height / 2 - mid);
        if (d < bestD) { bestD = d; best = k; }
      });
      set(best);
    };
    window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- Quick Wins calculator ---------- */
  function initCalc() {
    const rowsEl = $('#calc-rows');
    if (!rowsEl) return;
    const addBtn = $('#calc-add'), rate = $('#rate'), rateOut = $('#rate-out');
    const out = { name: $('#peak-name'), meta: $('#peak-meta'), hours: $('#out-hours'), cost: $('#out-cost'), days: $('#out-days') };
    const gbp = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', maximumFractionDigits: 0 });
    const fmt = (v) => (Math.round(v * 10) / 10).toString();
    const MAX = 8;
    const rows = [];
    let uid = 0;
    const roll = (node, to, f) => {
      const from = node._v == null ? to : node._v;
      node._v = to;
      cancelAnimationFrame(node._raf);
      if (reduce || from === to) { node.textContent = f(to); return; }
      const s = performance.now();
      const step = () => {
        const p = Math.min(1, (performance.now() - s) / 500), e = 1 - Math.pow(1 - p, 3);
        node.textContent = f(from + (to - from) * e);
        if (p < 1) node._raf = requestAnimationFrame(step);
      };
      node._raf = requestAnimationFrame(step);
    };
    const update = () => {
      let peak = null, maxScore = 0, total = 0;
      rows.forEach((r) => {
        r.score = r.hrs * r.ease;
        total += r.hrs;
        if (!peak || r.score > peak.score || (r.score === peak.score && r.hrs > peak.hrs)) peak = r;
        maxScore = Math.max(maxScore, r.score);
      });
      rows.forEach((r) => {
        $('.job-score b', r.el).textContent = fmt(r.score);
        $('.bar i', r.el).style.setProperty('--w', (maxScore ? (r.score / maxScore) * 100 : 0) + '%');
        $('output', r.el).textContent = fmt(r.hrs);
        $('input[type=range]', r.el).style.setProperty('--p', (r.hrs / 20) * 100 + '%');
        r.el.classList.toggle('is-peak', r === peak && r.score > 0);
        $('.job-del', r.el).disabled = rows.length <= 1;
      });
      addBtn.disabled = rows.length >= MAX;
      const rv = +rate.value;
      rateOut.textContent = gbp.format(rv);
      rate.style.setProperty('--p', ((rv - +rate.min) / (+rate.max - +rate.min)) * 100 + '%');
      roll(out.hours, total, (v) => fmt(Math.round(v * 2) / 2));
      roll(out.cost, (total * rv * 52) / 12, (v) => gbp.format(v));
      out.days.textContent = fmt((total * 52) / 12 / 8);
      const hasPeak = peak && peak.score > 0;
      out.name.textContent = hasPeak ? (peak.name.trim() || 'Your top job') : 'Add your jobs';
      out.meta.textContent = hasPeak ? fmt(peak.hrs) + ' hrs a week · ease ' + peak.ease + ' · score ' + fmt(peak.score) : 'Set hours and ease to find your peak';
      C.calcState = { rows: rows.map((r) => ({ name: r.name.trim(), hrs: r.hrs, ease: r.ease, score: r.score })), peak: hasPeak ? peak.name.trim() : '', total };
    };
    const addRow = (job, focus) => {
      if (rows.length >= MAX) return;
      const id = ++uid;
      const r = { id, name: job.name, hrs: job.hrs, ease: job.ease, score: 0 };
      const el = document.createElement('div');
      el.className = 'calc-row';
      el.innerHTML =
        '<span class="peak-badge">Build first</span>' +
        '<label class="sr-only" for="job-name-' + id + '">Job</label>' +
        '<input class="job-name" id="job-name-' + id + '" type="text" maxlength="60" placeholder="Name the job" autocomplete="off">' +
        '<div class="job-hrs"><span class="mlabel">Hrs/wk</span><input type="range" id="job-hrs-' + id + '" min="0" max="20" step="0.5" aria-label="Hours a week"><output for="job-hrs-' + id + '"></output></div>' +
        '<div class="job-ease"><span class="mlabel">Ease</span><div class="seg" role="radiogroup" aria-label="How easy to hand off">' +
        [1, 2, 3].map((v) => '<input type="radio" id="job-ease-' + id + '-' + v + '" name="job-ease-' + id + '" value="' + v + '"><label for="job-ease-' + id + '-' + v + '" title="' + ['Hard', 'Medium', 'Easy'][v - 1] + '">' + v + '</label>').join('') +
        '</div></div>' +
        '<div class="job-score"><b>0</b><span class="bar"><i></i></span></div>' +
        '<button type="button" class="job-del" aria-label="Remove this job">×</button>';
      const name = $('.job-name', el), hrs = $('input[type=range]', el);
      name.value = r.name;
      hrs.value = r.hrs;
      $('#job-ease-' + id + '-' + r.ease, el).checked = true;
      name.addEventListener('input', () => { r.name = name.value; update(); });
      hrs.addEventListener('input', () => { r.hrs = +hrs.value; update(); });
      $$('.seg input', el).forEach((inp) => inp.addEventListener('change', () => { r.ease = +inp.value; update(); }));
      $('.job-del', el).addEventListener('click', () => {
        const k = rows.indexOf(r);
        if (k > -1 && rows.length > 1) { rows.splice(k, 1); el.remove(); update(); }
      });
      r.el = el;
      rows.push(r);
      rowsEl.appendChild(el);
      update();
      if (focus) name.focus();
    };
    [
      { name: 'Replying to new enquiries', hrs: 6, ease: 3 },
      { name: 'Writing quotes', hrs: 5, ease: 2 },
      { name: 'Copying data between apps', hrs: 4, ease: 2 },
      { name: 'Chasing unpaid invoices', hrs: 3, ease: 3 },
      { name: 'Weekly numbers report', hrs: 2, ease: 3 }
    ].forEach((j) => addRow(j));
    addBtn.addEventListener('click', () => addRow({ name: '', hrs: 2, ease: 2 }, true));
    rate.addEventListener('input', update);
    $('#calc-cta').addEventListener('click', () => C.openFunnel({ fromCalc: true }));
  }

  /* ---------- FAQ ---------- */
  function initFaq() {
    $$('.qa button').forEach((b) => b.addEventListener('click', () => {
      const qa = b.closest('.qa');
      const open = !qa.classList.contains('is-open');
      qa.classList.toggle('is-open', open);
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    }));
  }

  /* ---------- Approvals toggle + trust track ---------- */
  function initControl() {
    const sec = $('.control');
    if (reduce || !sec || !('IntersectionObserver' in window)) return;
    sec.classList.add('is-armed');
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        setTimeout(() => sec.classList.add('is-on'), 350);
        io.disconnect();
      });
    }, { threshold: 0.35 });
    io.observe(sec);
  }

  /* ---------- Arriving from another page with #section ---------- */
  function initHashLanding() {
    const id = location.hash;
    if (!id || id.length < 2) return;
    let target = null;
    try { target = document.querySelector(id); } catch (e) { return; }
    if (!target) return;
    const jump = () => {
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
      if (C.lenis) C.lenis.scrollTo(target, { immediate: true, force: true });
      else target.scrollIntoView();
    };
    window.addEventListener('load', () => setTimeout(jump, 120));
  }
})();
