/* Cogent Intelligence: shared site script (map, smooth scroll, nav, WhatsApp booking flow, depth cards, article reader). */
(() => {
  'use strict';

  /* ===== Settings: check these before going live ===== */
  const CONFIG = {
    whatsapp: '+447753226214',   // Booking briefs open a WhatsApp chat with this number
    bookingUrl: '',              // Optional Cal.com / Calendly link, shown as "Or choose a time"
    formEndpoint: '',            // Optional: also POST the brief as JSON (Formspree, Make, Zapier...)
    setupPrice: '',              // e.g. '£1,500'. Blank shows "Founding rate"
    setupNote: '',
    monthlyPrice: '',            // e.g. '£450/mo'. Blank shows "Priced on hours saved"
    monthlyNote: '',
    foundingPlacesLeft: 3
  };

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const html = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(pointer: fine)').matches;
  const page = document.body.dataset.page || 'home';
  const WA_DIGITS = CONFIG.whatsapp.replace(/\D/g, '');
  const WA_DISPLAY = '+44 ' + WA_DIGITS.slice(2, 6) + ' ' + WA_DIGITS.slice(6);
  const waLink = (text) => 'https://wa.me/' + WA_DIGITS + (text ? '?text=' + encodeURIComponent(text) : '');

  const Cogent = window.Cogent = {
    CONFIG, $, $$, reduce, fine, page, waLink, WA_DISPLAY,
    lenis: null,
    calcState: null,
    mapT: page === 'home' ? { tilt: 0.08, hole: 0, heat: 0, apex: 0 } : { tilt: 0.55, hole: 0, heat: 0.15, apex: 0 },
    openFunnel: () => {},
    closeMenu: () => {}
  };

  const ICON_ARROW = '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const ICON_WA = '<svg class="ico-wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9.2 8.2c.3-.6.6-.6.9-.6h.6c.2 0 .4.1.5.4l.7 1.7c.1.2 0 .5-.1.6l-.5.6c-.1.1-.2.3 0 .5.5.9 1.3 1.7 2.2 2.2.2.1.4.1.5 0l.6-.6c.2-.2.4-.2.6-.1l1.7.8c.2.1.3.3.3.5v.5c0 .4-.2.8-.6 1-.5.3-1.4.5-2.5.1-1.7-.6-3.6-2.4-4.3-4.2-.4-1.1-.2-2 .1-2.4z" fill="currentColor"/></svg>';
  Cogent.ICON_ARROW = ICON_ARROW;

  const safe = (fn, name) => { try { fn(); } catch (err) { console.warn('[cogent] ' + name, err); } };
  if (!reduce) html.classList.add('motion');

  safe(initMap, 'map');
  safe(initLenis, 'lenis');
  safe(initNav, 'nav');
  safe(initWaLinks, 'wa');
  safe(initFunnel, 'funnel');
  safe(initOffer, 'offer');
  safe(initCovers, 'covers');
  safe(initTilt, 'tilt');
  safe(initParallax, 'parallax');
  safe(initFocusPull, 'focus-pull');
  safe(initArticle, 'article');
  safe(initMagnetic, 'magnetic');

  /* ---------- WebGL contour map ---------- */
  function initMap() {
    const canvas = $('#map');
    if (!canvas) return;
    let gl = null;
    try { gl = canvas.getContext('webgl', { antialias: false, alpha: false, depth: false, stencil: false, powerPreference: 'high-performance' }); } catch (e) { gl = null; }
    if (!gl) { html.classList.add('no-webgl'); return; }
    const deriv = !!gl.getExtension('OES_standard_derivatives');
    const FRAG = `
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
uniform vec2 u_res; uniform float u_time; uniform vec2 u_mouse; uniform float u_scroll;
uniform float u_tilt; uniform float u_hole; uniform float u_heat; uniform float u_apex; uniform vec2 u_apexPos;
vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}
vec2 mod289(vec2 x){return x-floor(x*(1.0/289.0))*289.0;}
vec3 permute(vec3 x){return mod289(((x*34.0)+1.0)*x);}
float snoise(vec2 v){
  const vec4 C=vec4(0.211324865405187,0.366025403784439,-0.577350269189626,0.024390243902439);
  vec2 i=floor(v+dot(v,C.yy)); vec2 x0=v-i+dot(i,C.xx);
  vec2 i1=(x0.x>x0.y)?vec2(1.0,0.0):vec2(0.0,1.0);
  vec4 x12=x0.xyxy+C.xxzz; x12.xy-=i1; i=mod289(i);
  vec3 p=permute(permute(i.y+vec3(0.0,i1.y,1.0))+i.x+vec3(0.0,i1.x,1.0));
  vec3 m=max(0.5-vec3(dot(x0,x0),dot(x12.xy,x12.xy),dot(x12.zw,x12.zw)),0.0); m=m*m; m=m*m;
  vec3 x=2.0*fract(p*C.www)-1.0; vec3 h=abs(x)-0.5; vec3 ox=floor(x+0.5); vec3 a0=x-ox;
  m*=1.79284291400159-0.85373472095314*(a0*a0+h*h);
  vec3 g; g.x=a0.x*x0.x+h.x*x0.y; g.yz=a0.yz*x12.xz+h.yz*x12.yw;
  return 130.0*dot(m,g);
}
float fbm(vec2 p){
  float f=0.0; float a=0.5; mat2 r=mat2(0.8,0.6,-0.6,0.8);
  for(int i=0;i<4;i++){ f+=a*snoise(p); p=r*p*2.03+3.1; a*=0.5; }
  return f;
}
float hash(vec2 p){ return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453); }
void main(){
  vec2 uv=(gl_FragCoord.xy-0.5*u_res)/u_res.y;
  float horizon=mix(3.5,0.82,u_tilt);
  float d=horizon/(horizon-uv.y);
  vec2 p=uv*d;
  vec2 q=p*1.3+vec2(0.2,u_scroll*3.2+u_time*0.012);
  vec2 w=vec2(snoise(q*0.55+vec2(u_time*0.021,0.0)),snoise(q*0.55+vec2(5.2,-u_time*0.017)));
  float h=fbm(q+0.45*w);
  vec2 ap=uv-u_apexPos;
  float ad=dot(ap,ap);
  h+=u_apex*0.85*exp(-ad*5.0);
  float f=h*8.0;
#ifdef HAS_DERIV
  float fw=fwidth(f);
#else
  float fw=0.045*d;
#endif
  fw=max(fw,0.0001);
  float dist=abs(fract(f+0.5)-0.5);
  float line=1.0-smoothstep(0.0,fw*1.3,dist);
  float fm=f/5.0;
  float major=1.0-smoothstep(0.0,fw*0.32,abs(fract(fm+0.5)-0.5));
  line*=1.0-smoothstep(0.35,0.9,fw);
  float hi=smoothstep(-0.35,0.75,h);
  float md=length(uv-u_mouse);
  float glow=exp(-md*md*7.0);
  vec3 bg=vec3(0.043,0.039,0.039);
  vec3 bone=vec3(0.945,0.92,0.89);
  vec3 ember=vec3(1.0,0.478,0.184);
  vec3 lc=mix(bone,ember,clamp(u_heat*0.85+glow*0.85,0.0,1.0));
  float a=line*(0.05+0.13*hi+0.1*major)*(1.0+glow*2.4);
  vec3 col=bg+lc*a+ember*glow*0.03;
  float r=length(uv*vec2(0.85,1.15));
  float hr=u_hole*0.62;
  float inside=1.0-smoothstep(hr-0.02,hr+0.2,r);
  float rr=(r-hr-0.06)/0.075;
  float rim=exp(-rr*rr)*u_hole;
  col=mix(col,bg*0.5,inside*clamp(u_hole*3.0,0.0,1.0));
  col+=lc*line*rim*0.45+ember*rim*0.025;
  float al=sqrt(ad);
  float ph=fract(u_time*0.22);
  float pr=(al-ph*0.75)/0.012;
  col+=ember*u_apex*((1.0-smoothstep(0.0,0.014,al))*0.9+exp(-ad*420.0)*0.22+exp(-pr*pr)*(1.0-ph)*0.28);
  col*=1.0-0.6*smoothstep(0.35,1.3,length(uv*vec2(0.72,1.0)));
  col=mix(col,bg,smoothstep(horizon-0.95,horizon-0.15,uv.y)*u_tilt);
  col+=(hash(gl_FragCoord.xy+fract(u_time)*91.0)-0.5)*0.02;
  gl_FragColor=vec4(col,1.0);
}`;
    const prefix = deriv ? '#extension GL_OES_standard_derivatives : enable\n#define HAS_DERIV 1\n' : '';
    const compile = (type, src) => {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    };
    let prog;
    try {
      prog = gl.createProgram();
      gl.attachShader(prog, compile(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0.0,1.0);}'));
      gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, prefix + FRAG));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    } catch (err) {
      console.warn('[cogent] shader', err);
      html.classList.add('no-webgl');
      return;
    }
    gl.useProgram(prog);
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const aLoc = gl.getAttribLocation(prog, 'a');
    gl.enableVertexAttribArray(aLoc);
    gl.vertexAttribPointer(aLoc, 2, gl.FLOAT, false, 0, 0);
    const U = {};
    ['u_res', 'u_time', 'u_mouse', 'u_scroll', 'u_tilt', 'u_hole', 'u_heat', 'u_apex', 'u_apexPos'].forEach((n) => { U[n] = gl.getUniformLocation(prog, n); });

    const small = window.matchMedia('(max-width: 899px)').matches;
    let W = 0, H = 0, dirty = true;
    const size = () => {
      const w = window.innerWidth, h = window.innerHeight;
      if (W && Math.abs(w - W) < 1 && Math.abs(h - H) < 140) return;
      W = w; H = h;
      const dpr = Math.min(window.devicePixelRatio || 1, small ? 1.25 : 1.5);
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      dirty = true;
    };
    size();
    window.addEventListener('resize', size, { passive: true });

    const m = { x: 0.3, y: -0.05 }, mc = { x: 0.3, y: -0.05 };
    let lastMove = -1e9;
    window.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      m.x = (e.clientX - window.innerWidth / 2) / window.innerHeight;
      m.y = -(e.clientY - window.innerHeight / 2) / window.innerHeight;
      lastMove = performance.now();
    }, { passive: true });

    const mapT = Cogent.mapT;
    const cur = Object.assign({}, mapT);
    const progI = $('.prog i');
    const t0 = performance.now();
    let running = true, lastSc = -1;
    document.addEventListener('visibilitychange', () => {
      running = !document.hidden;
      if (running) requestAnimationFrame(frame);
    });

    function frame() {
      if (!running) return;
      const now = performance.now();
      const t = (now - t0) / 1000;
      for (const k in mapT) cur[k] += (mapT[k] - cur[k]) * (reduce ? 1 : 0.07);
      if (!fine || now - lastMove > 5000) {
        m.x = Math.sin(t * 0.13) * 0.45;
        m.y = Math.cos(t * 0.17) * 0.22 - 0.05;
      }
      mc.x += (m.x - mc.x) * 0.05;
      mc.y += (m.y - mc.y) * 0.05;
      const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      const sc = Math.min(1, Math.max(0, (Cogent.lenis ? Cogent.lenis.scroll : window.scrollY) / max));
      if (progI) progI.style.transform = 'translateY(' + (sc * 102).toFixed(1) + 'px)';
      if (reduce && !dirty && Math.abs(sc - lastSc) < 1e-4) { requestAnimationFrame(frame); return; }
      lastSc = sc; dirty = false;
      const aspect = window.innerWidth / window.innerHeight;
      gl.uniform2f(U.u_res, canvas.width, canvas.height);
      gl.uniform1f(U.u_time, reduce ? 14.0 : t);
      gl.uniform2f(U.u_mouse, mc.x, mc.y);
      gl.uniform1f(U.u_scroll, sc);
      gl.uniform1f(U.u_tilt, cur.tilt);
      gl.uniform1f(U.u_hole, cur.hole);
      gl.uniform1f(U.u_heat, cur.heat);
      gl.uniform1f(U.u_apex, cur.apex);
      gl.uniform2f(U.u_apexPos, aspect < 1 ? Math.max(0.04, aspect / 2 - 0.12) : Math.min(0.5, aspect / 2 - 0.3), aspect < 1 ? 0.24 : 0.14);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* ---------- Smooth scroll ---------- */
  function initLenis() {
    if (!window.Lenis || reduce) return;
    const lenis = Cogent.lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true });
    if (html.classList.contains('is-loading')) lenis.stop();
    const G = window.gsap, ST = window.ScrollTrigger;
    if (G) {
      if (ST) { G.registerPlugin(ST); lenis.on('scroll', ST.update); }
      G.ticker.add((t) => lenis.raf(t * 1000));
      G.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }

  /* ---------- Nav, menu, anchors, sticky CTA ---------- */
  function initNav() {
    const nav = $('#nav'), menu = $('#menu'), btn = $('.nav-menu'), mcta = $('#mcta');
    if (!nav) return;
    const setMenu = (open) => {
      if (!menu) return;
      if (open) {
        menu.hidden = false;
        requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('is-open')));
        html.classList.add('menu-open');
        if (Cogent.lenis) Cogent.lenis.stop();
      } else {
        if (menu.hidden) return;
        menu.classList.remove('is-open');
        html.classList.remove('menu-open');
        if (Cogent.lenis) Cogent.lenis.start();
        setTimeout(() => { if (!menu.classList.contains('is-open')) menu.hidden = true; }, 400);
      }
      if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    Cogent.closeMenu = () => setMenu(false);
    if (btn) btn.addEventListener('click', () => setMenu(menu.hidden));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && menu && !menu.hidden) setMenu(false); });

    Cogent.scrollTo = (target, opts) => {
      if (Cogent.lenis) Cogent.lenis.scrollTo(target, Object.assign({ duration: 1.4 }, opts || {}));
      else target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    };
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const wasOpen = menu && !menu.hidden;
      setMenu(false);
      wasOpen ? setTimeout(() => Cogent.scrollTo(target), 60) : Cogent.scrollTo(target);
    });

    const hideAt = $$('[data-mcta-hide]');
    const onScroll = () => {
      const y = window.scrollY;
      nav.classList.toggle('is-scrolled', y > 30);
      if (!mcta) return;
      const covered = hideAt.some((el) => { const r = el.getBoundingClientRect(); return r.top < window.innerHeight * 0.85 && r.bottom > 0; });
      mcta.classList.toggle('is-on', y > window.innerHeight * 0.7 && !covered);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    const spy = $$('.nav-links a[href^="#"]');
    if (spy.length && 'IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (!en.isIntersecting) return;
          spy.forEach((l) => l.classList.toggle('is-active', l.getAttribute('href') === '#' + en.target.id));
        });
      }, { rootMargin: '-48% 0px -48% 0px' });
      spy.forEach((l) => { const el = document.querySelector(l.getAttribute('href')); if (el) io.observe(el); });
    }
  }

  /* ---------- WhatsApp quick links ---------- */
  function initWaLinks() {
    $$('[data-wa]').forEach((a) => {
      a.href = waLink(a.dataset.wa || 'Hi Cogent, I\'d like to book a free 30-minute discovery call.');
      a.target = '_blank';
      a.rel = 'noopener';
    });
    $$('[data-wa-number]').forEach((n) => { n.textContent = WA_DISPLAY; });
  }

  /* ---------- Booking funnel → WhatsApp ---------- */
  function funnelTemplate() {
    const chip = (type, name, id, value, label) => '<span class="chip"><input type="' + type + '" id="' + id + '" name="' + name + '" value="' + value + '"><label for="' + id + '">' + label + '</label></span>';
    const jobs = ['Replying to enquiries', 'Writing quotes', 'Chasing invoices', 'Inbox admin', 'Booking and reminders', 'Copying data between apps', 'Reporting on my numbers', 'Something else'];
    return '' +
'<div class="funnel" id="funnel" role="dialog" aria-modal="true" aria-labelledby="f-title-1" hidden data-lenis-prevent>' +
' <div class="funnel-inner">' +
'  <div class="funnel-top">' +
'   <span class="brand" aria-hidden="true">' + markSvg() + '</span>' +
'   <div class="funnel-progress" aria-hidden="true"><i id="funnel-bar"></i></div>' +
'   <span class="funnel-count" id="funnel-count">Step 1 of 3</span>' +
'   <button class="funnel-close" type="button" aria-label="Close booking">×</button>' +
'  </div>' +
'  <form class="funnel-form" id="funnel-form" novalidate>' +
'   <fieldset class="fstep" data-step="0">' +
'    <legend class="fstep-title" id="f-title-1">Let\'s start with your business.</legend>' +
'    <p class="fstep-sub">Two minutes now means the call is spent on your business, not on forms.</p>' +
'    <label class="flabel" for="f-business">Business name</label>' +
'    <input class="finput" id="f-business" name="business" type="text" autocomplete="organization" placeholder="e.g. Hartley Kitchens">' +
'    <p class="ferr" id="f-business-err" hidden></p>' +
'    <label class="flabel" for="f-sell">What do you sell, and who to? <em>(optional)</em></label>' +
'    <input class="finput" id="f-sell" name="sell" type="text" placeholder="e.g. Kitchen fitting for homeowners in Leeds">' +
'    <p class="flabel" id="f-team-l">Team size</p>' +
'    <div class="chips" role="radiogroup" aria-labelledby="f-team-l">' +
       chip('radio', 'team', 'f-team-1', 'solo', 'Just me') + chip('radio', 'team', 'f-team-2', '2-5', '2 to 5') + chip('radio', 'team', 'f-team-3', '6-15', '6 to 15') + chip('radio', 'team', 'f-team-4', '16-50', '16 to 50') + chip('radio', 'team', 'f-team-5', '50-plus', '50+') +
'    </div>' +
'   </fieldset>' +
'   <fieldset class="fstep" data-step="1" hidden>' +
'    <legend class="fstep-title" id="f-title-2">Where does your time go?</legend>' +
'    <p class="fstep-sub">Pick anything that eats your week. We\'ll dig into it on the call.</p>' +
'    <div class="chips" role="group" aria-label="Jobs that take your time">' + jobs.map((j, i) => chip('checkbox', 'jobs', 'f-job-' + (i + 1), j, j)).join('') + '</div>' +
'    <p class="ferr" id="f-jobs-err" hidden></p>' +
'    <p class="flabel" id="f-hrs-l">Roughly how many hours a week, all in?</p>' +
'    <div class="chips" role="radiogroup" aria-labelledby="f-hrs-l">' +
       chip('radio', 'hours', 'f-hrs-1', 'under-5', 'Under 5') + chip('radio', 'hours', 'f-hrs-2', '5-10', '5 to 10') + chip('radio', 'hours', 'f-hrs-3', '10-20', '10 to 20') + chip('radio', 'hours', 'f-hrs-4', '20-plus', '20+') +
'    </div>' +
'    <label class="flabel" for="f-handoff">The one job you\'d hand off tomorrow <em>(optional)</em></label>' +
'    <input class="finput" id="f-handoff" name="handoff" type="text" placeholder="e.g. Replying to new enquiries">' +
'   </fieldset>' +
'   <fieldset class="fstep" data-step="2" hidden>' +
'    <legend class="fstep-title" id="f-title-3">Who should we talk to?</legend>' +
'    <p class="fstep-sub">We\'ll reply on WhatsApp to arrange your 30-minute call.</p>' +
'    <label class="flabel" for="f-name">Your name</label>' +
'    <input class="finput" id="f-name" name="name" type="text" autocomplete="name" placeholder="First and last name">' +
'    <p class="ferr" id="f-name-err" hidden></p>' +
'    <label class="flabel" for="f-email">Email for your Top 3 summary <em>(optional)</em></label>' +
'    <input class="finput" id="f-email" name="email" type="email" autocomplete="email" inputmode="email" placeholder="name@yourbusiness.co.uk">' +
'    <p class="ferr" id="f-email-err" hidden></p>' +
'    <p class="fprivacy">Leave it blank and we\'ll send your summary on WhatsApp instead. We only use your details to arrange the call.</p>' +
'    <p class="ferr" id="f-submit-err" hidden></p>' +
'   </fieldset>' +
'   <fieldset class="fstep" data-step="3" hidden>' +
'    <legend class="fstep-title" id="f-title-4">Last step, <span id="d-name">thanks</span>. Send it on WhatsApp.</legend>' +
'    <p class="fstep-sub">Tap the button and WhatsApp opens with your brief already written. Press send and we\'ll reply to book your call.</p>' +
'    <dl class="brief" id="d-brief"></dl>' +
'    <div class="done-actions">' +
'     <a class="btn btn-glow btn-lg" id="d-wa" href="' + waLink('') + '" target="_blank" rel="noopener">' + ICON_WA + ' Send on WhatsApp</a>' +
'     <a class="btn btn-ghost" id="d-book" href="#" target="_blank" rel="noopener" hidden>Or choose a time</a>' +
'     <button class="btn btn-ghost" type="button" id="f-restart">Edit answers</button>' +
'    </div>' +
'    <p class="wa-number">Our WhatsApp <b id="d-number">' + WA_DISPLAY + '</b><button class="copy-btn" type="button" id="d-copy">Copy number</button></p>' +
'    <p class="done-note">Nothing is sent until you press send in WhatsApp.</p>' +
'   </fieldset>' +
'   <div class="funnel-nav">' +
'    <button class="btn btn-ghost" type="button" id="f-back" hidden>Back</button>' +
'    <button class="btn btn-glow btn-lg" type="submit" id="f-next"><span>Continue</span> ' + ICON_ARROW + '</button>' +
'   </div>' +
'  </form>' +
' </div>' +
'</div>';
  }

  function markSvg() {
    return '<svg class="mark" viewBox="0 0 32 32"><path d="M24.5 7.5A12 12 0 1 0 24.5 24.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M20.9 11.1A7 7 0 1 0 20.9 20.9" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" opacity=".6"/><circle cx="16" cy="16" r="2.3" style="fill:var(--ember)"/></svg>';
  }

  function initFunnel() {
    document.body.insertAdjacentHTML('beforeend', funnelTemplate());
    const el = $('#funnel'), form = $('#funnel-form');
    const steps = $$('.fstep', form);
    const bar = $('#funnel-bar'), count = $('#funnel-count'), back = $('#f-back'), next = $('#f-next');
    const nextLabel = $('span', next);
    const F = { i: 0, opener: null, done: false };
    const labelFor = (input) => { const l = form.querySelector('label[for="' + input.id + '"]'); return l ? l.textContent.trim() : input.value; };

    const go = (i) => {
      i = Math.max(0, Math.min(3, i));
      F.i = i;
      steps.forEach((s, k) => { s.hidden = k !== i; });
      const s = steps[i];
      s.classList.remove('is-entering');
      void s.offsetWidth;
      s.classList.add('is-entering');
      el.setAttribute('aria-labelledby', 'f-title-' + (i + 1));
      bar.style.width = ((i + 1) / 4) * 100 + '%';
      count.textContent = i < 3 ? 'Step ' + (i + 1) + ' of 3' : 'Brief ready';
      back.hidden = i === 0 || i === 3;
      next.hidden = i === 3;
      nextLabel.textContent = i === 2 ? 'Write my brief' : 'Continue';
      setTimeout(() => {
        const first = $('input.finput, input[type=radio], input[type=checkbox], #d-wa', s);
        if (first) first.focus({ preventScroll: true });
      }, 80);
    };

    const showErr = (id, msg) => { const e = document.getElementById(id); if (e) { e.textContent = msg; e.hidden = false; } };
    const clearErrs = (scope) => {
      $$('.ferr', scope).forEach((e) => { e.hidden = true; e.textContent = ''; });
      $$('[aria-invalid]', scope).forEach((n) => n.removeAttribute('aria-invalid'));
    };
    const invalid = (input, msg) => { input.setAttribute('aria-invalid', 'true'); showErr(input.id + '-err', msg); return input; };

    const validate = (i) => {
      clearErrs(steps[i]);
      const bad = [];
      if (i === 0) {
        const b = $('#f-business');
        if (b.value.trim().length < 2) bad.push(invalid(b, 'Add your business name so we can prepare.'));
      }
      if (i === 1) {
        const any = $$('input[name="jobs"]:checked', form).length > 0 || $('#f-handoff').value.trim().length > 0;
        if (!any) { showErr('f-jobs-err', 'Pick at least one job, or type one in the last box.'); bad.push($('#f-job-1')); }
      }
      if (i === 2) {
        const n = $('#f-name'), em = $('#f-email');
        if (!n.value.trim()) bad.push(invalid(n, 'Add your name.'));
        const ev = em.value.trim();
        if (ev && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(ev)) bad.push(invalid(em, 'Check the email, or leave it blank.'));
      }
      if (bad.length) { bad[0].focus(); return false; }
      return true;
    };

    const collect = () => {
      const fd = new FormData(form);
      const checkedLabel = (name) => { const c = $('input[name="' + name + '"]:checked', form); return c ? labelFor(c) : ''; };
      return {
        business: (fd.get('business') || '').trim(),
        sells: (fd.get('sell') || '').trim(),
        team: checkedLabel('team'),
        jobs: fd.getAll('jobs'),
        hours: checkedLabel('hours'),
        handoff: (fd.get('handoff') || '').trim(),
        name: (fd.get('name') || '').trim(),
        email: (fd.get('email') || '').trim(),
        calculator: Cogent.calcState,
        page: location.pathname.split('/').pop() || 'index.html',
        submittedAt: new Date().toISOString()
      };
    };

    const waText = (d) => {
      const L = ['Hi Cogent, I\'d like to book a free 30-minute discovery call.', ''];
      L.push('Name: ' + d.name);
      if (d.business) L.push('Business: ' + d.business + (d.sells ? ' (' + d.sells + ')' : ''));
      if (d.team) L.push('Team size: ' + d.team);
      if (d.jobs.length) L.push('Time drains: ' + d.jobs.join(', '));
      if (d.hours) L.push('Hours a week: ' + d.hours);
      if (d.handoff) L.push('Hand off first: ' + d.handoff);
      L.push('Send my Top 3 summary to: ' + (d.email || 'WhatsApp'));
      return L.join('\n');
    };

    const renderBrief = (d) => {
      $('#d-name').textContent = d.name.split(/\s+/)[0] || 'thanks';
      const rows = [
        ['Business', d.business + (d.sells ? ' · ' + d.sells : '')],
        ['Team', d.team || 'Not given'],
        ['Time drains', d.jobs.length ? d.jobs.join(', ') : 'Not given'],
        ['Hours a week', d.hours || 'Not given'],
        ['Hand off first', d.handoff || d.jobs[0] || 'We\'ll find it on the call'],
        ['Summary to', d.email || 'WhatsApp']
      ];
      const dl = $('#d-brief');
      dl.textContent = '';
      rows.forEach(([k, v]) => {
        const wrap = document.createElement('div');
        const dt = document.createElement('dt'); dt.textContent = k;
        const dd = document.createElement('dd'); dd.textContent = v;
        wrap.append(dt, dd);
        dl.appendChild(wrap);
      });
      $('#d-wa').href = waLink(waText(d));
      const book = $('#d-book');
      book.hidden = !CONFIG.bookingUrl;
      if (CONFIG.bookingUrl) book.href = CONFIG.bookingUrl;
    };

    const submit = () => {
      const data = collect();
      if (CONFIG.formEndpoint) {
        fetch(CONFIG.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) }).catch(() => {});
      }
      renderBrief(data);
      F.done = true;
      go(3);
    };

    const prefillFromCalc = () => {
      const cs = Cogent.calcState;
      if (!cs) return;
      const map = [['enquir', 'Replying to enquiries'], ['quote', 'Writing quotes'], ['invoice', 'Chasing invoices'], ['chas', 'Chasing invoices'], ['inbox', 'Inbox admin'], ['email', 'Inbox admin'], ['book', 'Booking and reminders'], ['schedul', 'Booking and reminders'], ['remind', 'Booking and reminders'], ['copy', 'Copying data between apps'], ['data', 'Copying data between apps'], ['report', 'Reporting on my numbers']];
      const boxes = $$('input[name="jobs"]', form);
      cs.rows.filter((r) => r.hrs > 0).forEach((r) => {
        const n = r.name.toLowerCase();
        const hit = map.find(([k]) => n.indexOf(k) > -1);
        const box = boxes.find((c) => c.value === (hit ? hit[1] : 'Something else'));
        if (box) box.checked = true;
      });
      if (cs.peak) $('#f-handoff').value = cs.peak;
      const t = cs.total;
      const band = t < 5 ? 'under-5' : t < 10 ? '5-10' : t < 20 ? '10-20' : '20-plus';
      const hb = $('input[name="hours"][value="' + band + '"]', form);
      if (hb) hb.checked = true;
    };

    const trap = (e) => {
      const f = $$('a[href]:not([hidden]), button:not([disabled]):not([hidden]), input:not([disabled])', el).filter((x) => x.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };

    const close = () => {
      if (el.hidden) return;
      el.classList.remove('is-open');
      html.classList.remove('funnel-open');
      if (Cogent.lenis) Cogent.lenis.start();
      setTimeout(() => { if (!el.classList.contains('is-open')) el.hidden = true; }, 450);
      if (F.opener && F.opener.focus) F.opener.focus({ preventScroll: true });
    };

    Cogent.openFunnel = (opts) => {
      opts = opts || {};
      Cogent.closeMenu();
      F.opener = document.activeElement;
      if (opts.fromCalc && !F.done) prefillFromCalc();
      el.hidden = false;
      html.classList.add('funnel-open');
      if (Cogent.lenis) Cogent.lenis.stop();
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-open')));
      go(F.done ? 3 : F.i);
    };

    document.addEventListener('click', (e) => {
      const t = e.target.closest('[data-funnel]');
      if (!t) return;
      e.preventDefault();
      Cogent.openFunnel();
    });
    $('.funnel-close', el).addEventListener('click', close);
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') trap(e);
    });
    back.addEventListener('click', () => go(F.i - 1));
    $('#f-restart').addEventListener('click', () => { F.done = false; go(0); });
    $('#d-copy').addEventListener('click', () => {
      const b = $('#d-copy');
      const done = (ok) => { b.textContent = ok ? 'Copied' : 'Select and copy'; setTimeout(() => { b.textContent = 'Copy number'; }, 1800); };
      const sel = () => { const r = document.createRange(); r.selectNodeContents($('#d-number')); const s = window.getSelection(); s.removeAllRanges(); s.addRange(r); };
      try {
        navigator.clipboard.writeText(CONFIG.whatsapp).then(() => done(true), () => { sel(); done(false); });
      } catch (err) { sel(); done(false); }
    });
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!validate(F.i)) return;
      if (F.i === 2) submit();
      else go(F.i + 1);
    });
  }

  /* ---------- Offer: prices + founding places ---------- */
  function initOffer() {
    const left = Math.max(0, Math.min(3, CONFIG.foundingPlacesLeft | 0));
    $$('.seats i').forEach((s, k) => s.classList.toggle('open', k < left));
    const lab = $('#seats-label');
    if (lab) lab.textContent = left ? left + ' of 3 places open' : 'All 3 founding places taken';
    $$('.js-places').forEach((n) => { n.textContent = left; });
    if (!left) $$('.js-founding').forEach((n) => { n.textContent = 'Founding places filled · book a free call'; });
    const set = (id, v) => { const n = document.getElementById(id); if (n && v) n.textContent = v; };
    set('price-setup', CONFIG.setupPrice);
    set('price-setup-note', CONFIG.setupNote);
    set('price-monthly', CONFIG.monthlyPrice);
    set('price-monthly-note', CONFIG.monthlyNote);
  }

  /* ---------- Generative contour covers ---------- */
  function initCovers() {
    const covers = $$('canvas.cover');
    if (!covers.length) return;
    const rng = (seed) => () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const draw = (c) => {
      const r = c.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      c.width = Math.round(r.width * dpr);
      c.height = Math.round(r.height * dpr);
      const ctx = c.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const W = r.width, H = r.height;
      const rand = rng(+(c.dataset.seed || 1) * 9973);
      const hot = c.dataset.hot ? c.dataset.hot.split(',').map(Number) : [0.68, 0.38];
      const bg = ctx.createRadialGradient(W * hot[0], H * hot[1], 0, W * hot[0], H * hot[1], Math.max(W, H) * 0.95);
      bg.addColorStop(0, 'rgba(255,122,47,0.26)');
      bg.addColorStop(0.45, 'rgba(26,22,20,1)');
      bg.addColorStop(1, 'rgba(12,11,10,1)');
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, W, H);
      const n = +(c.dataset.peaks || 2);
      const base = Math.max(W, H);
      const peaks = [];
      for (let i = 0; i < n; i++) peaks.push({ x: W * (i === 0 ? hot[0] : 0.15 + rand() * 0.7), y: H * (i === 0 ? hot[1] : 0.2 + rand() * 0.6), s: i === 0 ? 1 : 0.55 + rand() * 0.4, ph: rand() * 6.28, main: i === 0 });
      peaks.forEach((p) => {
        const rings = p.main ? 22 : 14;
        for (let k = 1; k <= rings; k++) {
          const rad = k * base * 0.034 * p.s;
          ctx.beginPath();
          for (let s = 0; s <= 160; s++) {
            const a = (s / 160) * Math.PI * 2;
            const wob = 1 + 0.13 * Math.sin(3 * a + p.ph + k * 0.32) + 0.07 * Math.sin(5 * a - p.ph * 1.7 + k * 0.5) + 0.035 * Math.sin(9 * a + k * 0.9);
            const x = p.x + Math.cos(a) * rad * wob * 1.25;
            const y = p.y + Math.sin(a) * rad * wob * 0.82;
            s ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
          }
          const nearPeak = p.main && k <= 4;
          ctx.strokeStyle = nearPeak ? 'rgba(255,140,70,' + (0.95 - k * 0.15) + ')' : 'rgba(241,235,227,' + (k % 5 === 0 ? 0.26 : 0.12) + ')';
          ctx.lineWidth = nearPeak || k % 5 === 0 ? 1.3 : 1;
          ctx.stroke();
        }
        if (p.main) {
          const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 26);
          g.addColorStop(0, 'rgba(255,122,47,0.9)');
          g.addColorStop(1, 'rgba(255,122,47,0)');
          ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(p.x, p.y, 26, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#FFB27C';
          ctx.beginPath(); ctx.arc(p.x, p.y, 3.2, 0, Math.PI * 2); ctx.fill();
        }
      });
      const v = ctx.createLinearGradient(0, H * 0.55, 0, H);
      v.addColorStop(0, 'rgba(11,10,10,0)');
      v.addColorStop(1, 'rgba(11,10,10,0.55)');
      ctx.fillStyle = v;
      ctx.fillRect(0, 0, W, H);
    };
    covers.forEach(draw);
    let t = null;
    window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => covers.forEach(draw), 200); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => covers.forEach(draw));
  }

  /* ---------- Depth: 3D tilt + parallax layers ---------- */
  function initTilt() {
    if (!fine || reduce) return;
    $$('[data-tilt]').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        el.classList.add('is-tilting');
        el.style.setProperty('--ry', ((px - 0.5) * 9).toFixed(2) + 'deg');
        el.style.setProperty('--rx', ((0.5 - py) * 7).toFixed(2) + 'deg');
        el.style.setProperty('--gx', (px * 100).toFixed(1) + '%');
        el.style.setProperty('--gy', (py * 100).toFixed(1) + '%');
      });
      el.addEventListener('pointerleave', () => {
        el.classList.remove('is-tilting');
        el.style.setProperty('--rx', '0deg');
        el.style.setProperty('--ry', '0deg');
      });
    });
  }

  function initParallax() {
    const scenes = $$('[data-parallax]');
    if (!scenes.length || reduce) return;
    let mx = 0, my = 0, tx = 0, ty = 0;
    if (fine) window.addEventListener('pointermove', (e) => { mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5; }, { passive: true });
    const layers = scenes.map((s) => ({ s, items: $$('[data-depth]', s).map((n) => ({ n, d: +n.dataset.depth })) }));
    const loop = () => {
      tx += (mx - tx) * 0.06; ty += (my - ty) * 0.06;
      layers.forEach(({ s, items }) => {
        const r = s.getBoundingClientRect();
        if (r.bottom < 0 || r.top > window.innerHeight) return;
        const sc = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
        items.forEach(({ n, d }) => {
          n.style.transform = 'translate3d(' + (tx * d * 40).toFixed(2) + 'px,' + (ty * d * 28 + sc * d * -60).toFixed(2) + 'px,0)';
        });
      });
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Focus pull (blur to sharp on entry) ---------- */
  function initFocusPull() {
    const els = $$('.fp');
    if (!els.length) return;
    if (reduce || !('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    els.forEach((e) => io.observe(e));
  }

  /* ---------- Article reader: progress, contents, focus mode ---------- */
  function initArticle() {
    const art = $('.article');
    if (!art) return;
    const bar = $('.read-progress i');
    const prose = $('.prose', art);
    const sections = $$('.prose > section', art);
    const tocLinks = $$('.toc a');
    const blocks = [];
    sections.forEach((s) => Array.from(s.children).forEach((c) => { c.classList.add('fblock'); blocks.push(c); }));
    const toggles = $$('.focus-toggle');
    let focus = true;
    try { if (localStorage.getItem('cogent-focus') === '0') focus = false; } catch (e) {}
    let ticking = false;
    const update = () => {
      ticking = false;
      const r = prose.getBoundingClientRect();
      const total = r.height - window.innerHeight * 0.6;
      const p = Math.min(1, Math.max(0, (window.innerHeight * 0.3 - r.top) / Math.max(1, total)));
      if (bar) bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
      if (focus) {
        const top = window.innerHeight * 0.28, bot = window.innerHeight * 0.72;
        blocks.forEach((b) => { const br = b.getBoundingClientRect(); b.classList.toggle('in-focus', br.bottom > top && br.top < bot); });
      }
      let cur = sections[0];
      sections.forEach((s) => { if (s.getBoundingClientRect().top < window.innerHeight * 0.4) cur = s; });
      if (cur) tocLinks.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + cur.id));
    };
    const setFocus = (on) => {
      focus = on;
      prose.classList.toggle('is-focus', on);
      toggles.forEach((t) => {
        t.setAttribute('aria-pressed', on ? 'true' : 'false');
        const st = $('.ft-state', t);
        if (st) st.textContent = on ? 'on' : 'off';
      });
      try { localStorage.setItem('cogent-focus', on ? '1' : '0'); } catch (e) {}
      update();
    };
    toggles.forEach((t) => t.addEventListener('click', () => setFocus(!focus)));
    window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    setFocus(focus);
  }

  /* ---------- Magnetic CTAs ---------- */
  function initMagnetic() {
    if (!fine || reduce) return;
    $$('[data-magnetic]').forEach((b) => {
      b.addEventListener('pointermove', (e) => {
        const r = b.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
        b.style.translate = (x * 0.16).toFixed(1) + 'px ' + (y * 0.26).toFixed(1) + 'px';
      });
      b.addEventListener('pointerleave', () => { b.style.translate = ''; });
    });
  }
})();
