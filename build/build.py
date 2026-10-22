import os as _os
_B = _os.path.dirname(_os.path.abspath(__file__))
_R = _os.path.dirname(_B)
#!/usr/bin/env python3
"""Build Cogent site: brand swap, industry section + pages, SEO. Reads build/source, writes site/."""
import re, json, shutil, os, html as H, sys
sys.path.insert(0, os.path.dirname(__file__))
from industries_data import I

ORIG, OUT = _os.path.join(_B, 'source'), _os.path.join(_R, 'site')
DOMAIN = 'https://cogentintelligence.co.uk'
DATE = '9 October 2026'
WA = '+44 7753 226214'
e = lambda s: H.escape(s, quote=False)
ea = lambda s: H.escape(s, quote=True)
CORE = [d for d in I if d['group'] == 'core']
NICHE = [d for d in I if d['group'] == 'niche']
BYSLUG = {d['slug']: d for d in I}

ARROW = '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
WA_ICO = '<svg class="ico-wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9.2 8.2c.3-.6.6-.6.9-.6h.6c.2 0 .4.1.5.4l.7 1.7c.1.2 0 .5-.1.6l-.5.6c-.1.1-.2.3 0 .5.5.9 1.3 1.7 2.2 2.2.2.1.4.1.5 0l.6-.6c.2-.2.4-.2.6-.1l1.7.8c.2.1.3.3.3.5v.5c0 .4-.2.8-.6 1-.5.3-1.4.5-2.5.1-1.7-.6-3.6-2.4-4.3-4.2-.4-1.1-.2-2 .1-2.4z" fill="currentColor"/></svg>'

def mark(p): return f'<img class="mark" src="{p}assets/brand/cogent-mark.webp" alt="" width="97" height="112">'
def footlogo(href, p): return f'<a href="{href}" class="foot-logo" aria-label="Cogent Intelligence home"><img src="{p}assets/brand/cogent-logo.webp" alt="Cogent Intelligence, cogentintelligence.co.uk" width="480" height="383" loading="lazy"></a>'

def head_extra(p, path, title, desc, img='assets/brand/og-image.jpg'):
    url = DOMAIN + '/' + path
    return (f'<link rel="canonical" href="{url}">\n'
            f'<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/brand/icon-32.png">\n'
            f'<link rel="apple-touch-icon" href="{p}assets/brand/icon-180.png">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Cogent Intelligence">\n'
            f'<meta property="og:title" content="{ea(title)}">\n<meta property="og:description" content="{ea(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{DOMAIN}/{img}">\n'
            f'<meta property="og:locale" content="en_GB">\n<meta name="twitter:card" content="summary_large_image">\n')

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'

ORG = {"@type": "ProfessionalService", "@id": DOMAIN + "/#org", "name": "Cogent Intelligence", "url": DOMAIN + "/",
       "logo": DOMAIN + "/assets/brand/icon-512.png", "image": DOMAIN + "/assets/brand/og-image.jpg",
       "description": "AI agents and a business second brain for UK service businesses. Free discovery call, first agent live in 14 days.",
       "telephone": WA, "areaServed": {"@type": "Country", "name": "United Kingdom"},
       "knowsAbout": ["AI agents", "business process automation", "AI automation for small businesses", "workflow automation", "AI receptionist", "business intelligence"]}

def brandify(s, p, home_href):
    """Swap placeholder SVG marks for the real logo; footer gets the full lockup."""
    s = re.sub(r'<svg class="mark".*?</svg>', mark(p), s, flags=re.S)
    s = re.sub(r'(<span class="loader-mark">)<svg.*?</svg>', r'\1' + mark(p), s, flags=re.S)
    s = re.sub(r'(<div class="foot-brand">\s*)<a [^>]*class="brand".*?</a>', lambda m: m.group(1) + footlogo(home_href, p), s, flags=re.S)
    return s

def add_nav(s, link, active=False):
    cls = ' class="is-active" aria-current="page"' if active else ''
    s = re.sub(r'(<nav class="nav-links" aria-label="Main">.*?Agents</a>)', lambda m: m.group(1) + f'\n    <a href="{link}"{cls}>Industries</a>', s, count=1, flags=re.S)
    s = re.sub(r'(<nav aria-label="Mobile">.*?Agents</a>)', lambda m: m.group(1) + f'\n    <a href="{link}">Industries</a>', s, count=1, flags=re.S)
    return s

def add_foot(s, hub):
    s = re.sub(r'(<h4>Explore</h4>\s*<ul>.*?Second brain</a></li>)', lambda m: m.group(1) + f'<li><a href="{hub}">Industries</a></li>', s, count=1, flags=re.S)
    return s

def foot_industries(p):
    links = ''.join(f'<li><a href="{p}industries/{d["slug"]}.html">{e(d["name"])}</a></li>' for d in CORE[:6])
    return ('<div>\n        <h4>Industries</h4>\n        <ul>' + links + f'<li><a href="{p}industries/index.html">All industries</a></li></ul>\n      </div>\n      ')

def insert_foot_col(s, p):
    return s.replace('<div>\n        <h4>Talk to us</h4>', foot_industries(p) + '<div>\n        <h4>Talk to us</h4>', 1)

# ------------------------------------------------------------------ HOME
def home_section():
    tabs, panels = [], []
    for i, d in enumerate(CORE):
        on = i == 0
        tabs.append(f'<button class="sector-tab" type="button" role="tab" id="st-{d["slug"]}" aria-controls="sp-{d["slug"]}" aria-selected="{"true" if on else "false"}" tabindex="{0 if on else -1}">{e(d["tab"])}</button>')
        ag = ''.join(f'<li class="sp-agent"><span class="sp-cat">{e(a[0])}</span><b>{e(a[1])}</b><span class="sp-does">{e(a[3])}</span></li>' for a in d['agents'])
        pains = ''.join(f'<li><b>{e(t)}.</b> {e(x)}</li>' for t, x in d['pains'][:3])
        q, a = d['asks'][0]
        panels.append(f'''<div class="sector-panel{' is-on' if on else ''}" role="tabpanel" id="sp-{d["slug"]}" aria-labelledby="st-{d["slug"]}"{'' if on else ' hidden'}>
          <div class="sp-copy">
            <p class="sp-name">{e(d["name"])}</p>
            <h3 class="sp-line">{e(d["tagline"])}</h3>
            <ul class="sp-pains">{pains}</ul>
            <a class="link-arrow" href="industries/{d["slug"]}.html">See the {e(d["tab"].lower())} playbook {ARROW}</a>
          </div>
          <div class="sp-side">
            <div class="sp-ask"><p class="sp-q"><span>Ask Cogent</span>{e(q)}</p><p class="sp-a"><i></i>{e(a)}</p></div>
            <ul class="sp-agents">{ag}</ul>
          </div>
        </div>''')
    niche = ''.join(f'<a class="niche-chip" href="industries/{d["slug"]}.html"><i></i>{e(d["name"])}</a>' for d in NICHE)
    return f'''
  <!-- INDUSTRIES -->
  <section class="sectors" id="industries" aria-label="Industries we work with">
    <div class="wrap">
      <div class="sectors-head" data-reveal>
        <div>
          <p class="kicker">Built for your industry</p>
          <h2 class="h2">Same brain.<br>Your playbook.</h2>
        </div>
        <p class="lede">An Enquiry Responder for a plumber isn't the same as one for a solicitor. Every Cogent setup starts from a playbook for your sector: the jobs that eat your week, the agents that take them on, and where approvals have to sit for your rules and regulators.</p>
      </div>
      <div class="sector-tabs" role="tablist" aria-label="Choose your industry" data-lenis-prevent>
        {''.join(tabs)}
      </div>
      <div class="sector-stage">
        {''.join(panels)}
      </div>
      <div class="niches" data-reveal>
        <div class="niches-head">
          <p class="kicker">Specialist niches</p>
          <p>Smaller sectors with the same pattern: lots of repeat enquiries, deadlines and paperwork. They often see the biggest gains.</p>
        </div>
        <div class="niche-list">{niche}<a class="niche-chip niche-chip--all" href="industries/index.html">All industries {ARROW}</a></div>
        <p class="niche-note">Don't see yours? If your week is full of repeatable admin, it'll fit. <button class="btn-text" type="button" data-funnel>Bring it to the free call →</button></p>
      </div>
    </div>
  </section>
'''

EXTRA_FAQ = [
    ("What is an AI agent for a small business?", "An AI agent is software that handles a specific job from start to finish, like replying to enquiries, chasing invoices or entering data, by following your rules and your Business Map. Unlike a chatbot, it takes actions in your tools, and anything that matters waits for your approval."),
    ("Which industries do you work with?", "Service businesses with repeatable admin: trades, estate and letting agents, property managers, supported housing and care providers, accountants, solicitors, architects, clinics, gyms, recruiters, cleaning companies, admin teams and specialist niches such as EPC assessors, compliance consultants, renewables installers, brokers, training providers, venues and garages."),
    ("How much does AI automation cost for a UK small business?", "The discovery call is free. Setup is a one-off fee quoted after the call, and the monthly fee is set against the staff hours we save you, so it should always be less than the time it gives back."),
    ("Will AI agents replace my staff?", "They take the repetitive part of the week off your team, such as copying data, chasing and first replies. Most businesses use the time for work they've been putting off, or to grow without hiring as quickly."),
    ("Is it GDPR compliant?", "Personal data is only processed by AI models approved for it, every action is logged, and your Business Map records which tools hold personal data. We'll walk through it on the call."),
]

def build_home():
    s = open(f'{ORIG}/index.html').read()
    title = 'AI Agents for UK Service Businesses | Cogent Intelligence'
    desc = 'Cogent Intelligence builds AI agents and a business second brain for UK service businesses: trades, estate agents, accountants, solicitors, architects, clinics and more. Enquiries answered 24/7, admin automated, approvals built in. Free 30-minute call.'
    s = s.replace('<title>Cogent Intelligence</title>', f'<title>{e(title)}</title>')
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{ea(desc)}">', s)
    faq_all = [(q, re.sub('<[^>]+>', '', a)) for q, a in re.findall(r'id="qa-\d+-b">(.*?)<span class="x".*?<div><p>(.*?)</p>', s, flags=re.S)] + EXTRA_FAQ
    graph = {"@context": "https://schema.org", "@graph": [ORG,
             {"@type": "WebSite", "url": DOMAIN + "/", "name": "Cogent Intelligence", "publisher": {"@id": DOMAIN + "/#org"}},
             {"@type": "Service", "serviceType": "AI agents and business automation", "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "GB",
              "audience": {"@type": "BusinessAudience", "audienceType": "UK service businesses and SMEs"},
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Cogent Intelligence", "itemListElement": [
                  {"@type": "Offer", "name": "Free Discovery Call", "price": "0", "priceCurrency": "GBP"},
                  {"@type": "Offer", "name": "Setup: Business Map and first agent live in 14 days"},
                  {"@type": "Offer", "name": "Monthly Second Brain"}]}},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_all]}]}
    s = s.replace('<meta name="theme-color" content="#0B0A0A">', '<meta name="theme-color" content="#0B0A0A">\n' + head_extra('', '', title, desc) + ld(graph), 1)
    s = brandify(s, '', '#top')
    s = add_nav(s, '#industries')
    s = add_foot(s, '#industries')
    s = insert_foot_col(s, '')
    s = s.replace('  <!-- 14 DAYS -->', home_section() + '\n  <!-- 14 DAYS -->', 1)
    # hero: name the audience for search without changing the layout
    s = s.replace('Cogent maps how your business runs into one intelligent memory.', 'Cogent maps how your service business runs into one intelligent memory.', 1)
    s = s.replace('<span class="txt">Priya prefers Thursdays</span></span>\n    </div>', '<span class="txt">Priya prefers Thursdays</span></span>\n    </div>\n    <p class="hero-for hero-reveal" style="--d:.9s">AI agents for trades, estate agents, accountants, solicitors, architects, clinics, admin teams and specialist UK service businesses.</p>', 1)
    # extra FAQ items
    n0 = len(re.findall(r'class="qa[ "]', s))
    extra = ''
    for k, (q, a) in enumerate(EXTRA_FAQ, start=n0 + 1):
        extra += f'''        <div class="qa"><h3><button type="button" aria-expanded="false" aria-controls="qa-{k}" id="qa-{k}-b">{e(q)}<span class="x" aria-hidden="true"></span></button></h3>
          <div class="qa-panel" id="qa-{k}" role="region" aria-labelledby="qa-{k}-b"><div><p>{e(a)}</p></div></div></div>\n'''
    s = re.sub(r'(<div class="qa"><h3><button[^>]*id="qa-8-b">.*?</div></div></div>\n)', lambda m: m.group(1) + extra, s, count=1, flags=re.S)
    # insights + industries cards
    s = s.replace('<p>Business intelligence as a second brain, for owner-led businesses that would rather run the business than the admin.</p>',
                  '<p>AI agents and a business second brain for UK service businesses that would rather run the business than the admin.</p>')
    open(f'{OUT}/index.html', 'w').write(s)

# ------------------------------------------------------------------ PAGES
def page_shell(p, path, title, desc, body, active_hub, schema, page='article'):
    nav_insights = f'{p}insights/index.html'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{ea(desc)}">
<meta name="theme-color" content="#0B0A0A">
{head_extra(p, path, title, desc)}{ld(schema)}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Instrument+Sans:wght@400..700&family=JetBrains+Mono:wght@400..600&display=swap">
<link rel="stylesheet" href="{p}assets/cogent.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body class="page-article" data-page="{page}">
<canvas id="map" aria-hidden="true"></canvas>
{'<div class="read-progress" aria-hidden="true"><i></i></div>' if page == 'article' else ''}

<header class="nav" id="nav">
  <a href="{p}index.html" class="brand" aria-label="Cogent Intelligence home">
    {mark(p)}
    <b>Cogent</b><small>Intelligence</small>
  </a>
  <nav class="nav-links" aria-label="Main">
    <a href="{p}index.html#intelligence">Second brain</a>
    <a href="{p}index.html#agents">Agents</a>
    <a href="{p}industries/index.html" class="is-active" aria-current="page">Industries</a>
    <a href="{p}index.html#how">How it works</a>
    <a href="{p}index.html#offer">Pricing</a>
    <a href="{nav_insights}">Insights</a>
  </nav>
  <button class="nav-menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
  <button class="btn btn-glow nav-cta" type="button" data-funnel data-magnetic><span class="long">Book free call</span><span class="short">Book call</span></button>
</header>

<div class="menu" id="menu" hidden data-lenis-prevent>
  <nav aria-label="Mobile">
    <a href="{p}index.html#intelligence">Second brain</a>
    <a href="{p}index.html#agents">Agents</a>
    <a href="{p}industries/index.html">Industries</a>
    <a href="{p}index.html#how">How it works</a>
    <a href="{p}index.html#offer">Pricing</a>
    <a href="{nav_insights}">Insights</a>
  </nav>
  <div class="menu-actions">
    <button class="btn btn-glow btn-lg" type="button" data-funnel>Book your free 30-min call</button>
    <a class="wa-link" href="#" data-wa><span>Message us on WhatsApp</span></a>
  </div>
</div>

<main>
{body}
</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        {footlogo(p + 'index.html', p)}
        <p>AI agents and a business second brain for UK service businesses that would rather run the business than the admin.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul><li><a href="{p}index.html#intelligence">Second brain</a></li><li><a href="{p}industries/index.html">Industries</a></li><li><a href="{p}index.html#how">How it works</a></li><li><a href="{p}index.html#offer">Pricing</a></li><li><a href="{nav_insights}">Insights</a></li></ul>
      </div>
      {foot_industries(p)}<div>
        <h4>Talk to us</h4>
        <ul><li><a href="#" data-funnel>Book a free call</a></li><li><a href="#" data-wa>WhatsApp <span data-wa-number>{WA}</span></a></li><li><a href="{DOMAIN}">cogentintelligence.co.uk</a></li></ul>
      </div>
    </div>
    <div class="foot-base"><span>© 2026 Cogent Intelligence</span><span>Examples on this site use dummy data.</span></div>
  </div>
</footer>

<div class="mcta" id="mcta">
  <span><b>Free 30-min call</b><small>Top 3 summary, yours either way</small></span>
  <a class="mcta-wa" href="#" data-wa aria-label="Message us on WhatsApp">{WA_ICO}</a>
  <button class="btn btn-glow" type="button" data-funnel>Book</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="{p}assets/cogent.js"></script>
</body>
</html>
'''

def card(d, href, meta, desc=True):
    return f'''<div class="fp"><a class="dcard" href="{href}" data-tilt>
          <div class="dcard-cover"><canvas class="cover" data-seed="{d["seed"]}" data-peaks="{d["peaks"]}" data-hot="{d["hot"]}" aria-hidden="true"></canvas><span class="dcard-tag">{e(d["tab"])}</span></div>
          <div class="dcard-body"><p class="dcard-meta">{meta}</p><h3>{e(d["name"])}</h3>{f'<p>{e(d["tagline"])}</p>' if desc else ''}<span class="dcard-go">See the playbook {ARROW}</span></div>
        </a></div>'''

def related(d):
    pool = CORE + NICHE
    i = pool.index(d)
    return [pool[(i + 1) % len(pool)], pool[(i + 2) % len(pool)]]

def industry_page(d):
    p = '../'
    chips_pos = ['left:8%;top:16%', 'right:9%;top:26%', 'left:38%;bottom:16%']
    chips = ''.join(f'<span class="depth-chip{" hot" if k == 0 else ""}" data-depth="{[1.2,0.9,0.7][k]}" style="{chips_pos[k]}"><b>{e(b)}</b>{e(t)}</span>' for k, (b, t) in enumerate(d['chips']))
    pains = ''.join(f'<li><strong>{e(t)}.</strong> {e(x)}</li>' for t, x in d['pains'])
    agents = ''.join(f'''<div class="example agent-x">
            <div class="example-h"><span>{e(a[0])} agent</span><b>{e(a[1])}</b></div>
            <div class="example-b"><dl class="xspec"><div><dt>Trigger</dt><dd>{e(a[2])}</dd></div><div><dt>Does</dt><dd>{e(a[3])}</dd></div><div><dt>Asks you</dt><dd>{e(a[4])}</dd></div></dl></div>
          </div>''' for a in d['agents'])
    asks = ''.join(f'<div class="qa-x"><p class="qx"><span>You</span>{e(q)}</p><p class="ax"><span>Cogent</span>{e(a)}</p></div>' for q, a in d['asks'])
    brief = ''.join(f'<div class="briefing-row"><i{f" class={chr(34)}{c}{chr(34)}" if c else ""}></i><span><strong>{e(b)}</strong> {e(r)}</span></div>' for c, b, r in d['brief'])
    rows = sorted(d['score'], key=lambda r: -(r[1] * r[2]))
    trs = ''.join(f'<tr{" class=" + chr(34) + "peak" + chr(34) if k == 0 else ""}><td>{e(j)}</td><td>{h}</td><td>{x}</td><td>{h*x}</td></tr>' for k, (j, h, x) in enumerate(rows))
    peak = rows[0]
    li = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
    faqs = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in d['faqs'])
    rel = related(d)
    body = f'''  <article class="article wrap">
    <header class="art-hero">
      <div class="art-hero-text">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Industries</a><span aria-hidden="true">/</span><span>{e(d["tab"])}</span></nav>
        <h1 class="art-title">{e(d["h1"])}</h1>
        <p class="art-dek">{e(d["dek"])}</p>
        <div class="art-meta"><span>{'Industry playbook' if d['group']=='core' else 'Specialist niche'}</span><span>For {e(d["who"].split(",")[0])} and more</span><span>{DATE}</span><button class="focus-toggle" type="button" aria-pressed="true"><i></i>Focus mode <span class="ft-state">on</span></button></div>
      </div>
      <div class="art-cover" data-parallax aria-hidden="true">
        <canvas class="cover" data-seed="{d["seed"]}" data-peaks="{d["peaks"]}" data-hot="{d["hot"]}" data-depth="0.25"></canvas>
        {chips}
      </div>
    </header>

    <div class="art-grid">
      <aside class="toc" aria-label="On this page">
        <p class="toc-h">On this page</p>
        <ol>
          <li><a href="#s1">Where the week goes</a></li>
          <li><a href="#s2">Agents built for you</a></li>
          <li><a href="#s3">Ask your business</a></li>
          <li><a href="#s4">Your Monday briefing</a></li>
          <li><a href="#s5">Find your peak</a></li>
          <li><a href="#s6">Where approvals sit</a></li>
          <li><a href="#s7">Works with your tools</a></li>
          <li><a href="#s8">Questions</a></li>
        </ol>
        <button class="focus-toggle" type="button" aria-pressed="true"><i></i>Focus mode <span class="ft-state">on</span></button>
      </aside>

      <div class="prose">
        <section id="s1">
          <h2><span class="num">01</span>Where the week goes</h2>
          <p>We work with {e(d["who"])}. The details differ from firm to firm, but the same few jobs come up on almost every discovery call:</p>
          <ul>{pains}</ul>
          <p>None of these need your expertise. They need doing quickly, the same way every time, and that's exactly the kind of work AI agents do well, with your Business Map telling them how your business runs.</p>
          <div class="keyidea"><p class="kicker">Key idea</p><p>{e(d["keyidea"])}</p></div>
        </section>

        <section id="s2">
          <h2><span class="num">02</span>Agents built for {e(d["name"].lower().replace("&", "and"))}</h2>
          <p>These are the agents we most often switch on first in this sector. Each one reads your second brain, works around the clock and asks you before anything that matters.</p>
          {agents}
          <p>Your first agent is the one with the highest score on your discovery call, not the one on the top of this list. Most firms add a second and third over the following months.</p>
        </section>

        <section id="s3">
          <h2><span class="num">03</span>Ask your business anything</h2>
          <p>Because every agent writes to the same memory, you can ask questions in plain English that used to mean an afternoon in spreadsheets and inboxes.</p>
          <div class="example">
            <div class="example-h"><span>Ask Cogent</span><b>Example · dummy data</b></div>
            <div class="example-b">{asks}</div>
          </div>
        </section>

        <section id="s4">
          <h2><span class="num">04</span>Your Monday briefing</h2>
          <p>At 7am every Monday you get a short briefing built from your own tools: what came in, what's stuck and what changed.</p>
          <div class="example">
            <div class="example-h"><span>Monday briefing</span><b>Example · dummy data</b></div>
            <div class="example-b briefing">{brief}</div>
          </div>
        </section>

        <section id="s5">
          <h2><span class="num">05</span>Find your peak</h2>
          <p>On the call we score every repeating job by hours a week × how easy it is to hand off (1 hard, 2 medium, 3 easy). The highest score gets built first. Here's how a typical list might look.</p>
          <div class="table-wrap">
            <table>
              <caption class="sr-only">Example scores for {e(d["name"])}, dummy data</caption>
              <thead><tr><th scope="col">Job</th><th scope="col">Hours a week</th><th scope="col">Ease</th><th scope="col">Score</th></tr></thead>
              <tbody>{trs}</tbody>
            </table>
          </div>
          <p class="fig-cap">Example · dummy data. Score = hours a week × ease.</p>
          <p>In this example, <strong>{e(peak[0].lower())}</strong> is the peak. Run your own numbers with the <a href="../index.html#calc">calculator on our home page</a>, or bring them to the call.</p>
        </section>

        <section id="s6">
          <h2><span class="num">06</span>Where approvals sit</h2>
          <p>Every agent starts on a short lead. Here's a typical starting point for this sector. Yours is written into your Business Map.</p>
          <div class="cols3">
            <div class="c-ok"><h4>Does alone</h4><ul>{li(d["alone"])}</ul></div>
            <div class="c-ask"><h4>Asks first</h4><ul>{li(d["ask"])}</ul></div>
            <div class="c-never"><h4>Never</h4><ul>{li(d["never"])}</ul></div>
          </div>
          <p>{e(d["reg"])}</p>
        </section>

        <section id="s7">
          <h2><span class="num">07</span>Works with the tools you already use</h2>
          <p>We connect to what you have rather than asking you to move. Common tools in this sector include {e(d["tools"].rstrip("."))}. If a system has no integration, a Portal Operator agent can work it the way a person would.</p>
        </section>

        <section id="s8">
          <h2><span class="num">08</span>Questions</h2>
          {faqs}
        </section>
      </div>
    </div>

    <aside class="art-cta" data-mcta-hide>
      <div>
        <h2>Find your top 3.</h2>
        <p>A free 30-minute call. We'll find the three jobs costing your {e(d["tab"].lower())} business the most time and send you a one-page summary within 24 hours, whether you work with us or not.</p>
      </div>
      <div class="art-cta-actions">
        <button class="btn btn-glow btn-lg" type="button" data-funnel data-magnetic>Book your free call</button>
        <a class="wa-link" href="#" data-wa><span>Or message us on WhatsApp</span></a>
      </div>
    </aside>

    <nav class="more" aria-label="Other industries">
      <div class="more-head"><h2>Other industries</h2><a class="link-arrow" href="index.html">All industries</a></div>
      <div class="dgrid dgrid--pair">
        {card(rel[0], rel[0]["slug"] + ".html", "Industry playbook" if rel[0]["group"]=="core" else "Specialist niche")}
        {card(rel[1], rel[1]["slug"] + ".html", "Industry playbook" if rel[1]["group"]=="core" else "Specialist niche")}
      </div>
    </nav>
  </article>'''
    path = f'industries/{d["slug"]}.html'
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": d["h1"], "serviceType": "AI agents and business automation", "description": d["meta"],
         "provider": {"@type": "ProfessionalService", "name": "Cogent Intelligence", "url": DOMAIN + "/"}, "areaServed": "GB",
         "audience": {"@type": "BusinessAudience", "audienceType": d["name"]}, "url": DOMAIN + "/" + path},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Industries", "item": DOMAIN + "/industries/"},
            {"@type": "ListItem", "position": 3, "name": d["name"], "item": DOMAIN + "/" + path}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]}]}
    open(f'{OUT}/{path}', 'w').write(page_shell(p, path, d['seo_title'], d['meta'], body, True, schema))

def industries_hub():
    p = '../'
    core = ''.join(card(d, d['slug'] + '.html', 'Industry playbook') for d in CORE)
    niche = ''.join(card(d, d['slug'] + '.html', 'Specialist niche') for d in NICHE)
    body = f'''  <div class="wrap">
    <header class="hub-hero">
      <p class="kicker">Industries</p>
      <h1 class="hub-title"><span>Your</span><span>industry</span></h1>
      <p class="lede">AI agents for UK service businesses, set up around the way your sector works. Each playbook shows where the week goes, the agents we switch on first, the questions you can ask your second brain and where approvals sit for your rules and regulators.</p>
    </header>

    <section class="hub-list" aria-label="Industry playbooks">
      <div class="dgrid dgrid--tri">
        {core}
      </div>
    </section>

    <section class="hub-list hub-list--niche" aria-labelledby="niche-h">
      <div class="more-head"><h2 id="niche-h">Specialist niches</h2></div>
      <p class="lede hub-sub">Smaller sectors with the same pattern of repeat enquiries, deadlines and paperwork. They often see the biggest gains, because one agent covers most of the admin.</p>
      <div class="dgrid dgrid--tri">
        {niche}
      </div>
    </section>

    <aside class="art-cta" data-mcta-hide>
      <div>
        <h2>Don't see your industry?</h2>
        <p>If your week is full of repeatable admin, Cogent will fit. Book a free 30-minute call and we'll find your top three time-wasters, whatever you do.</p>
      </div>
      <div class="art-cta-actions">
        <button class="btn btn-glow btn-lg" type="button" data-funnel data-magnetic>Book your free call</button>
        <a class="wa-link" href="#" data-wa><span>Or message us on WhatsApp</span></a>
      </div>
    </aside>
  </div>'''
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Industries · Cogent Intelligence",
              "url": DOMAIN + "/industries/", "hasPart": [{"@type": "WebPage", "name": d["h1"], "url": f'{DOMAIN}/industries/{d["slug"]}.html'} for d in I]}
    open(f'{OUT}/industries/index.html', 'w').write(page_shell(p, 'industries/', 'AI Agents by Industry | UK Service Businesses · Cogent Intelligence',
         'AI agents and automation playbooks for UK trades, estate agents, property managers, supported housing, accountants, solicitors, architects, clinics, gyms, recruiters, cleaning firms, admin teams and specialist niches.', body, True, schema, page='hub'))

def insights():
    for f in ['index.html', 'second-brain.html', 'find-your-peak.html', 'approvals-first.html']:
        s = open(f'{ORIG}/insights/{f}').read()
        t = re.search(r'<title>(.*?)</title>', s).group(1); dsc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
        path = 'insights/' + ('' if f == 'index.html' else f)
        art = {"@context": "https://schema.org", "@type": "Article" if f != 'index.html' else "CollectionPage", "headline": H.unescape(t.split(' · ')[0]),
               "description": H.unescape(dsc), "datePublished": "2026-10-09", "author": {"@type": "Organization", "name": "Cogent Intelligence"},
               "publisher": {"@type": "Organization", "name": "Cogent Intelligence", "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/brand/icon-512.png"}}, "url": DOMAIN + "/" + path}
        s = s.replace('<meta name="theme-color" content="#0B0A0A">', '<meta name="theme-color" content="#0B0A0A">\n' + head_extra('../', path, H.unescape(t), H.unescape(dsc)) + ld(art), 1)
        s = brandify(s, '../', '../index.html')
        s = add_nav(s, '../industries/index.html')
        s = add_foot(s, '../industries/index.html')
        s = insert_foot_col(s, '../')
        s = s.replace('<p>Business intelligence as a second brain, for owner-led businesses that would rather run the business than the admin.</p>',
                      '<p>AI agents and a business second brain for UK service businesses that would rather run the business than the admin.</p>')
        open(f'{OUT}/insights/{f}', 'w').write(s)

def sitemap():
    urls = ['', 'industries/'] + [f'industries/{d["slug"]}.html' for d in I] + ['insights/', 'insights/second-brain.html', 'insights/find-your-peak.html', 'insights/approvals-first.html']
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u}</loc><lastmod>2026-10-09</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(f'{OUT}/sitemap.xml', 'w').write(xml)
    open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')

if __name__ == '__main__':
    os.makedirs(f'{OUT}/industries', exist_ok=True)
    build_home(); insights(); industries_hub()
    for d in I: industry_page(d)
    sitemap()
    print('built', len(I), 'industry pages')

def assets():
    A = f'{OUT}/assets'
    X = os.path.join(os.path.dirname(__file__), 'extra')
    open(f'{A}/cogent.css', 'w').write(open(f'{ORIG}/assets/cogent.css').read() + open(f'{X}/cogent-extra.css').read())
    open(f'{A}/home.css', 'w').write(open(f'{ORIG}/assets/home.css').read() + open(f'{X}/home-extra.css').read())
    open(f'{A}/home.js', 'w').write(open(f'{ORIG}/assets/home.js').read() + open(f'{X}/home-extra.js').read())
    js = open(f'{ORIG}/assets/cogent.js').read()
    js2 = re.sub(r"function markSvg\(\) \{\n\s*return '<svg class=\"mark\".*?';\n\s*\}",
                 "function markSvg() {\n    const m = document.querySelector('.brand img.mark');\n    return m ? '<img class=\"mark\" src=\"' + m.getAttribute('src') + '\" alt=\"\" width=\"97\" height=\"112\">' : '';\n  }", js, flags=re.S)
    assert js2 != js, 'markSvg not patched'
    open(f'{A}/cogent.js', 'w').write(js2)

assets()

import launch
launch.run(page_shell)

import v4
v4.pre(page_shell)

import v3
v3.run(page_shell)

v4.run()
