"""Launch pass: pricing (replaces founding rate), Delegate section, privacy + 404, clean URLs, Cloudflare Pages files."""
import os as _os
_B = _os.path.dirname(_os.path.abspath(__file__))
_R = _os.path.dirname(_B)
import re, os, json, html as H

OUT = _os.path.join(_R, 'site')
DOMAIN = 'https://cogentintelligence.co.uk'
EMAIL = 'hello@cogentintelligence.co.uk'
e = lambda s: H.escape(s, quote=False)
TICK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ---------------------------------------------------------------- pricing data (single source of truth)
SETUP = [
    dict(step='Step 01', name='Free Discovery Call', price='Free', note='30 minutes, by video or phone', cta='Book the free call', glow=True,
         items=['We find your top 3 time-wasters', 'One-page Top 3 summary within 24 hours', 'We tell you what not to automate, too', 'Yours to keep, whether you go ahead or not']),
    dict(step='Step 02 · Option A', name='Standard setup', price='£1,997', pre='from', note='One-off · first agent live in 14 days', cta='Starts with the free call', badge='Most businesses start here',
         items=['Your Business Map: a half-day session mapping people, tools, prices and rules', 'Inbox, calendar, accounts and CRM connected', 'One agent built from tested templates, such as Enquiry Responder, Invoice Chaser or Inbox Sorter', 'Approvals set from day one', 'Covered by our 14-day promise']),
    dict(step='Step 02 · Option B', name='Custom AI agent', price='£4,997', pre='from', note='One-off · timeline agreed in writing', cta='Starts with the free call',
         items=['Everything in Standard setup', 'An agent designed around your process: multi-step, multi-system, with your own documents and rules', 'Portal Operator for old systems with no integration', 'Delegation set up in WhatsApp, Slack, Telegram or email', 'Custom reports and scheduled jobs']),
]
MONTHLY = [
    dict(name='Starter', price='£297', agents='1 agent', tasks='Up to 1,000 tasks a month',
         items=['Agent monitored and fixed by us', 'Monday briefing on your numbers', 'Ask your second brain anything, any time', 'Weekly log and monthly ROI report']),
    dict(name='Growth', price='£597', agents='Up to 3 agents', tasks='Up to 3,000 tasks a month', feature=True,
         items=['Everything in Starter', 'Delegate by message or voice note: it hands jobs to the right agent', 'Scheduled jobs, such as "every Friday at 4pm, chase timesheets"', 'Monthly review call, with approvals loosened as trust is earned']),
    dict(name='Scale', price='£897', agents='Up to 6 agents', tasks='Up to 7,500 tasks a month',
         items=['Everything in Growth', 'Same-working-day fixes', 'Quarterly Business Map refresh', 'Briefings and delegation for each team or site']),
]
EXTRA_AGENT = '£147'

def plan_card(p, cls='plan'):
    feat = p.get('feature') or p.get('badge')
    badge = f'<span class="plan-badge">{e(p.get("badge", "Best value"))}</span>' if feat else ''
    items = ''.join(f'<li>{TICK}{e(i)}</li>' for i in p['items'])
    pre = f'<small class="plan-from">{p["pre"]}</small>' if p.get('pre') else ''
    btn = 'btn-glow' if p.get('glow') or feat else 'btn-ghost'
    return f'''<article class="{cls}{' plan--feature' if feat else ''}">
          {badge}<p class="plan-step">{e(p['step'])}</p>
          <h3>{e(p['name'])}</h3>
          <div class="plan-price">{pre}<b>{e(p['price'])}</b><span>{e(p['note'])}</span></div>
          <ul>{items}</ul>
          <button class="btn {btn}" type="button" data-funnel>{e(p['cta'])}</button>
        </article>'''

def monthly_card(p):
    feat = p.get('feature')
    items = ''.join(f'<li>{TICK}{e(i)}</li>' for i in p['items'])
    return f'''<article class="plan plan--tier{' plan--feature' if feat else ''}">
          {'<span class="plan-badge">Most popular</span>' if feat else ''}<p class="plan-step">Monthly · {e(p['agents'])}</p>
          <h3>{e(p['name'])}</h3>
          <div class="plan-price"><b>{e(p['price'])}<em>/mo</em></b><span>{e(p['tasks'])}</span></div>
          <ul>{items}</ul>
          <button class="btn {'btn-glow' if feat else 'btn-ghost'}" type="button" data-funnel>Find my tier on the call</button>
        </article>'''

def offer_section():
    return f'''<!-- OFFER -->
  <section class="offer" id="offer" aria-label="Pricing">
    <div class="wrap">
      <div class="offer-head" data-reveal>
        <p class="kicker">Pricing</p>
        <h2 class="h2">Clear prices. Start with the free call.</h2>
        <p class="lede">Most agencies say "enquire". We'd rather you knew before you book. Setup is a one-off fee, and the monthly fee covers the agents, the second brain and us looking after both.</p>
      </div>
      <div class="offer-grid" data-stagger>
        {''.join(plan_card(p) for p in SETUP)}
      </div>
      <div class="offer-sub" data-reveal>
        <div>
          <p class="kicker">Then, every month</p>
          <h3>Priced per agent, with tasks included.</h3>
        </div>
        <p>A task is one job done, like an enquiry answered, an invoice chased or a record entered. Most businesses use well under their allowance. If you regularly go over, we talk before anything changes. You'll never get a surprise bill.</p>
      </div>
      <div class="offer-grid" data-stagger>
        {''.join(monthly_card(p) for p in MONTHLY)}
      </div>
      <p class="offer-fine">Extra agents {EXTRA_AGENT}/mo each. AI and hosting costs are included within your task allowance. Rolling monthly with 30 days' notice, no long contracts. Setup is paid 50% to start and 50% on go-live. Prices exclude VAT where applicable.</p>
      <div class="founding promise" data-reveal>
        <div class="founding-l">
          <p class="kicker">The 14-day promise</p>
          <h3>Live in 14 days, or the rest waits.</h3>
          <p>If your first agent from Standard setup isn't live 14 days after your mapping session, you don't pay the second half of setup until it is. And if the call shows a smaller fix will do the job, we'll tell you and the price comes down with it.</p>
        </div>
        <div class="founding-r">
          <ul class="promise-list"><li>{TICK}Approvals on from day one</li><li>{TICK}Every action logged</li><li>{TICK}No long contracts</li></ul>
          <button class="btn btn-glow btn-lg" type="button" data-funnel data-magnetic>Book the free call</button>
          <p class="pilot-note">Industry pilots: we're taking a small number of pilot clients in each sector in exchange for a case study. Ask about it on the call.</p>
        </div>
      </div>
    </div>
  </section>

  '''

def delegate_section():
    mic = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="5.5" y="1.5" width="5" height="8.5" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M3 7.5a5 5 0 0 0 10 0M8 12.5V15" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'
    return f'''
  <!-- DELEGATE -->
  <section class="delegate" id="delegate" aria-label="Delegate to your second brain">
    <div class="wrap delegate-grid">
      <div class="delegate-copy" data-reveal>
        <p class="kicker">Delegate, don't do</p>
        <h2 class="h2">Message it like you'd message a colleague.</h2>
        <p class="lede">Above every agent sits an operator. Send it a message or a voice note from WhatsApp, Slack, Telegram or email. It works out which agents should do the job, hands it over and reports back when it's done. Most automation waits for a trigger. This takes instructions.</p>
        <ul class="dl-points">
          <li><b>One message, several jobs.</b>"Chase the quotes, book Priya in, send me Friday's numbers" becomes three jobs for three agents.</li>
          <li><b>Voice notes from the van are fine.</b>It transcribes them and gets on with it while you're on the next job.</li>
          <li><b>Say it once, it happens every week.</b>"Every Friday at 4pm, chase missing timesheets" becomes a scheduled job.</li>
          <li><b>It learns how you work.</b>When you correct it, it saves the fix as a skill and does it your way next time.</li>
        </ul>
        <p class="dl-note">Anything that reaches a customer or touches money still waits for your tap.</p>
      </div>
      <div class="delegate-stage" aria-hidden="true">
        <div class="chat" data-seq data-tick="900" data-hold="6">
          <div class="chat-bar"><span class="chat-av"></span><span><b>Cogent</b><small>your operator · online</small></span></div>
          <div class="chat-body">
            <div class="msg me" data-at="1"><span class="vn">{mic}<i></i><em>0:14</em></span><span class="tr">"Chase last week's quotes, book Priya's survey for Thursday and send me Friday's numbers."</span></div>
            <span class="dots op-typing transient" data-at="2" data-until="3"><b></b><b></b><b></b></span>
            <div class="msg op" data-at="3">On it. That's three jobs:</div>
            <div class="job" data-at="4"><span class="job-a">Quote Chaser</span><span class="job-t">3 follow-ups drafted</span><span class="job-s ask">Needs your OK</span></div>
            <div class="job" data-at="5"><span class="job-a">Booking Assistant</span><span class="job-t">Thu 10:30 offered to Priya</span><span class="job-s">Waiting on Priya</span></div>
            <div class="job" data-at="6"><span class="job-a">Monday Briefing</span><span class="job-t">Friday numbers at 4pm</span><span class="job-s ok">Scheduled</span></div>
            <div class="msg op" data-at="8">Priya's confirmed Thursday 10:30. It's in your calendar and I've remembered she prefers mornings.</div>
          </div>
          <span class="vchip ok" data-at="9">1 voice note · 3 jobs done</span>
        </div>
        <p class="ask-note">Demo · dummy data</p>
      </div>
    </div>
  </section>
'''

NEW_FAQ_COST = "The discovery call is free. Standard setup starts at £1,997 and a custom AI agent at £4,997, both one-off. Monthly plans start at £297 for one agent, £597 for up to three and £897 for up to six, with tasks included. Rolling monthly, no long contracts."
MORE_FAQ = [
    ("Is this an AI receptionist or chatbot?", "No. An AI receptionist answers calls. Cogent builds a second brain that remembers how your business runs, plus agents that do the admin behind the calls: quotes, chasing, data entry, bookings and reports. You can delegate to it by message, like a colleague."),
    ("Can I give it jobs by WhatsApp or voice note?", "Yes. On Growth and Scale plans you can message your second brain on WhatsApp, Slack, Telegram or email, or send a voice note. It splits the request into jobs, hands each one to the right agent and reports back. Customer-facing and money jobs still wait for your approval."),
    ("Where is my data hosted?", "Your second brain and its memory are hosted on UK servers. Personal data is only sent to AI models approved for it, and every action is logged."),
]

CSS = '''
/* ---------- Pricing v2 (added) ---------- */
.plan-from{font:500 11px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.plan-price b em{font-style:normal;font-size:.5em;color:var(--mute);margin-left:4px;font-weight:500}
.offer-sub{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:16px 48px;align-items:end;margin:80px 0 0}
.offer-sub h3{margin:12px 0 0;font-family:var(--f-display);font-weight:650;font-stretch:108%;font-size:clamp(1.6rem,3vw,2.5rem);line-height:1.04;letter-spacing:-.02em}
.offer-sub p:not(.kicker){margin:0;color:var(--mute);max-width:58ch}
.offer-sub+.offer-grid{margin-top:34px}
.offer-fine{margin:22px 0 0;color:var(--dim);font-size:13.5px;max-width:90ch}
.promise{margin-top:56px}
.promise-list{list-style:none;margin:0;padding:0;display:grid;gap:8px;color:var(--bone-2);font-size:15px}
.promise-list li{display:flex;gap:10px;align-items:center}
.promise-list svg{width:16px;height:16px;color:var(--ok);flex:none}
.pilot-note{margin:0;color:var(--dim);font-size:13px;max-width:42ch}
@media (max-width:899px){.offer-sub{grid-template-columns:1fr;margin-top:60px}}

/* ---------- Delegate (added) ---------- */
.delegate{padding-block:clamp(90px,13vh,150px)}
.delegate-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.95fr);gap:clamp(32px,6vw,90px);align-items:center}
.delegate-copy{display:grid;gap:20px}
.dl-points{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:16px}
.dl-points li{display:grid;gap:4px;padding-left:22px;position:relative;color:var(--mute);font-size:15.5px;line-height:1.55}
.dl-points li::before{content:"";position:absolute;left:0;top:.55em;width:9px;height:9px;border-radius:50%;background:var(--violet);box-shadow:0 0 12px var(--violet)}
.dl-points b{color:var(--bone);font-weight:600}
.dl-note{margin:0;font:500 11.5px/1.6 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ember-2)}
.delegate-stage{display:grid;gap:10px}
.chat{position:relative;border-radius:28px;border:1px solid var(--rule);background:linear-gradient(170deg,rgba(30,27,25,.95),rgba(12,11,10,.97));box-shadow:0 40px 90px -50px rgba(0,0,0,.9),0 0 70px -30px var(--violet-soft);overflow:hidden;min-height:470px}
.chat-bar{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--rule);background:rgba(11,10,10,.6)}
.chat-av{width:34px;height:34px;border-radius:50%;background:url(brand/cogent-mark.webp) center/62% no-repeat,radial-gradient(circle,rgba(255,122,47,.22),var(--ink-2));border:1px solid rgba(255,122,47,.4)}
.chat-bar b{display:block;font-family:var(--f-display);font-size:15px}
.chat-bar small{font:500 10.5px/1 var(--f-mono);letter-spacing:.08em;color:var(--ok)}
.chat-body{display:grid;gap:10px;padding:18px}
.msg{max-width:86%;padding:11px 14px;border-radius:16px;font-size:14px;line-height:1.5}
.msg.me{justify-self:end;background:rgba(255,122,47,.16);border:1px solid rgba(255,122,47,.32);border-bottom-right-radius:4px;color:var(--bone)}
.msg.op{justify-self:start;background:rgba(241,235,227,.06);border:1px solid var(--rule);border-bottom-left-radius:4px;color:var(--bone-2)}
.vn{display:flex;align-items:center;gap:9px;margin-bottom:7px;color:var(--ember-2)}
.vn svg{width:15px;height:15px}
.vn i{flex:1;height:14px;min-width:90px;border-radius:2px;background:repeating-linear-gradient(90deg,currentColor 0 2px,transparent 2px 5px);opacity:.55}
.vn em{font:500 11px/1 var(--f-mono);font-style:normal}
.tr{display:block;font-size:13px;color:var(--bone-2);font-style:italic}
.op-typing{justify-self:start;padding:12px 14px;border-radius:16px;background:rgba(241,235,227,.06);border:1px solid var(--rule)}
.job{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 12px;border-radius:12px;border:1px solid var(--rule);background:rgba(11,10,10,.55);font-size:13px}
.job-a{padding:4px 8px;border-radius:999px;background:var(--violet-soft);color:var(--violet);font:500 10px/1 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.job-t{color:var(--bone-2);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.job-s{font:500 10px/1 var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--dim);white-space:nowrap}
.job-s.ask{color:var(--ember-2)} .job-s.ok{color:var(--ok)}
.chat>.vchip{position:absolute;right:18px;bottom:16px}
@media (max-width:899px){.delegate-grid{grid-template-columns:1fr}.chat{min-height:0;padding-bottom:56px}}
@media (max-width:480px){.job{grid-template-columns:1fr auto}.job-a{grid-column:1/-1;justify-self:start}}
'''

def patch_home():
    p = f'{OUT}/index.html'
    s = open(p).read()
    s = re.sub(r'<!-- OFFER -->.*?(?=<!-- FAQ -->)', lambda m: offer_section(), s, count=1, flags=re.S)
    s = s.replace('  <!-- INDUSTRIES -->', delegate_section() + '\n  <!-- INDUSTRIES -->', 1)
    # hero pill + final note: price-led instead of scarcity
    s = s.replace('<span class="js-founding">Founding rate · <b class="js-places">3</b> places open</span>', '<span>From <b>£1,997</b> · live in 14 days</span>')
    s = s.replace('<p class="final-note js-founding">Founding rate · <span class="js-places">3</span> places open</p>', '<p class="final-note">Setup from £1,997 · monthly from £297 · no long contracts</p>')
    # cost FAQ (visible + JSON-LD)
    old_cost = 'The call is free. Setup is a one-off fee and the second brain is monthly, priced against the staff hours it saves you, never against our time. Our first three clients get a reduced founding rate.'
    assert old_cost in s, 'cost faq'
    s = s.replace(old_cost, NEW_FAQ_COST)
    s = s.replace("The discovery call is free. Setup is a one-off fee quoted after the call, and the monthly fee is set against the staff hours we save you, so it should always be less than the time it gives back.", NEW_FAQ_COST)
    # extra FAQs
    n = len(re.findall(r'<div class="qa[ "]', s))
    extra = ''
    for k, (q, a) in enumerate(MORE_FAQ, start=n + 1):
        extra += f'''        <div class="qa"><h3><button type="button" aria-expanded="false" aria-controls="qa-{k}" id="qa-{k}-b">{e(q)}<span class="x" aria-hidden="true"></span></button></h3>
          <div class="qa-panel" id="qa-{k}" role="region" aria-labelledby="qa-{k}-b"><div><p>{e(a)}</p></div></div></div>\n'''
    s = s.replace('      </div>\n    </div>\n  </section>\n\n  <!-- FINAL -->', extra + '      </div>\n    </div>\n  </section>\n\n  <!-- FINAL -->', 1)
    # JSON-LD: priced offers + new FAQs
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S)
    g = json.loads(m.group(1))
    for node in g['@graph']:
        if node.get('@type') == 'Service':
            node['hasOfferCatalog']['itemListElement'] = (
                [{"@type": "Offer", "name": "Free Discovery Call", "price": "0", "priceCurrency": "GBP"},
                 {"@type": "Offer", "name": "Standard setup", "price": "1997", "priceCurrency": "GBP", "description": "Business Map and first agent live in 14 days. Price from."},
                 {"@type": "Offer", "name": "Custom AI agent", "price": "4997", "priceCurrency": "GBP", "description": "Custom-built agent. Price from."}] +
                [{"@type": "Offer", "name": f"{t['name']} monthly plan", "price": t['price'].strip('£').replace(',', ''), "priceCurrency": "GBP",
                  "priceSpecification": {"@type": "UnitPriceSpecification", "price": t['price'].strip('£'), "priceCurrency": "GBP", "unitCode": "MON"}, "description": f"{t['agents']}, {t['tasks'].lower()}"} for t in MONTHLY])
        if node.get('@type') == 'FAQPage':
            node['mainEntity'] += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in MORE_FAQ]
    s = s[:m.start(1)] + json.dumps(g, ensure_ascii=False) + s[m.end(1):]
    s = s.replace('the busywork around the clock, with you approving anything important.', 'the busywork around the clock. Delegate by message or voice note, and approve anything important.', 1)
    assert 'founding' not in s.lower().replace('class="founding', '').replace('founding-l', '').replace('founding-r', ''), 'founding text left'
    open(p, 'w').write(s)
    open(f'{OUT}/assets/home.css', 'a').write(CSS)

def patch_js():
    p = f'{OUT}/assets/cogent.js'
    s = open(p).read()
    s = s.replace("foundingPlacesLeft: 3", "foundingPlacesLeft: 0         // Founding offer retired; kept so old markup can't break")
    s = s.replace("We only use your details to arrange the call.</p>'", "We only use your details to arrange the call. <a href=\"' + sitePrefix() + 'privacy.html\">Privacy</a></p>'")
    s = s.replace("  function markSvg() {", "  function sitePrefix() {\n    const m = document.querySelector('.brand img.mark');\n    return m ? m.getAttribute('src').replace(/assets\\/brand\\/.*$/, '') : '';\n  }\n\n  function markSvg() {", 1)
    s = s.replace("if (!left) $$('.js-founding').forEach((n) => { n.textContent = 'Founding places filled · book a free call'; });", '')
    open(p, 'w').write(s)

def prefix_for(rel):
    return '../' * rel.count('/')

def global_pass():
    for root, _, files in os.walk(OUT):
        for f in files:
            if not f.endswith('.html'): continue
            path = os.path.join(root, f); rel = os.path.relpath(path, OUT); p = prefix_for(rel)
            s = open(path).read()
            # clean URLs for Cloudflare Pages (it serves /page for /page.html)
            s = re.sub(re.escape(DOMAIN) + r'/([A-Za-z0-9/_-]+)\.html', DOMAIN + r'/\1', s)
            # email + privacy in footer
            s = s.replace(f'<li><a href="{DOMAIN}">cogentintelligence.co.uk</a></li>', f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>')
            s = s.replace('<span>© 2026 Cogent Intelligence</span>', f'<span>© 2026 Cogent Intelligence · <a href="{p}privacy.html">Privacy</a></span>')
            open(path, 'w').write(s)
    sm = open(f'{OUT}/sitemap.xml').read()
    sm = re.sub(re.escape(DOMAIN) + r'/([A-Za-z0-9/_-]+)\.html', DOMAIN + r'/\1', sm)
    sm = sm.replace('</urlset>', f'  <url><loc>{DOMAIN}/privacy</loc><lastmod>2026-10-11</lastmod></url>\n</urlset>')
    open(f'{OUT}/sitemap.xml', 'w').write(sm)

PRIVACY = f'''  <article class="article wrap">
    <header class="art-hero">
      <div class="art-hero-text">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Privacy</span></nav>
        <h1 class="art-title">Privacy notice</h1>
        <p class="art-dek">What we collect when you use this website or book a call, why we collect it, and your rights. Last updated 11 October 2026.</p>
      </div>
    </header>
    <div class="art-grid">
      <aside class="toc" aria-label="On this page">
        <p class="toc-h">On this page</p>
        <ol><li><a href="#p1">Who we are</a></li><li><a href="#p2">What we collect</a></li><li><a href="#p3">Why we use it</a></li><li><a href="#p4">Who we share it with</a></li><li><a href="#p5">How long we keep it</a></li><li><a href="#p6">Cookies and storage</a></li><li><a href="#p7">Your rights</a></li><li><a href="#p8">Client data</a></li></ol>
      </aside>
      <div class="prose">
        <section id="p1"><h2><span class="num">01</span>Who we are</h2>
          <p>This website is run by Cogent Intelligence ("we", "us"). We decide how the personal data described here is used, which makes us the data controller. Contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or on WhatsApp at +44 7753 226214.</p></section>
        <section id="p2"><h2><span class="num">02</span>What we collect</h2>
          <ul><li><strong>Booking form:</strong> your name, business name, what you sell, the jobs taking your time, roughly how many hours they take and, if you choose, your email address.</li>
          <li><strong>Messages:</strong> anything you send us by WhatsApp or email, including your phone number.</li>
          <li><strong>Technical data:</strong> our hosting provider processes your IP address and basic browser details to deliver the site and protect it from abuse.</li></ul>
          <p>The booking form doesn't store your answers on our servers. It writes a brief that opens in WhatsApp, and nothing is sent until you press send.</p></section>
        <section id="p3"><h2><span class="num">03</span>Why we use it</h2>
          <p>We use your details to arrange and prepare for your discovery call, send your one-page summary and reply to your messages. Our lawful basis is taking steps at your request before entering into a contract, and our legitimate interest in replying to business enquiries. We don't sell your data, and we don't add you to a mailing list without asking.</p></section>
        <section id="p4"><h2><span class="num">04</span>Who we share it with</h2>
          <ul><li><strong>Cloudflare</strong> hosts this website and handles our email routing.</li><li><strong>WhatsApp (Meta)</strong> carries any messages you send us there.</li><li><strong>Google Fonts</strong> serves the site's fonts, which means your browser requests them from Google.</li></ul>
          <p>Some of these providers may process data outside the UK. Where they do, they rely on recognised safeguards such as the UK International Data Transfer Addendum or adequacy regulations.</p></section>
        <section id="p5"><h2><span class="num">05</span>How long we keep it</h2>
          <p>If you don't become a client, we delete your enquiry details within 12 months of our last contact. If you become a client, we keep records for as long as the contract runs and for six years afterwards for legal and accounting reasons.</p></section>
        <section id="p6"><h2><span class="num">06</span>Cookies and storage</h2>
          <p>We don't use advertising or analytics cookies. The site stores a couple of small settings in your browser, such as whether you've already seen the intro animation and your reading-mode preference. These never leave your device and aren't used to track you.</p></section>
        <section id="p7"><h2><span class="num">07</span>Your rights</h2>
          <p>You can ask for a copy of your data, ask us to correct or delete it, object to how we use it or ask us to restrict it. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll reply within one month. If you're unhappy with how we've handled your data, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk</a>.</p></section>
        <section id="p8"><h2><span class="num">08</span>Client data</h2>
          <p>When we build agents for a client, we process their customers' data on the client's instructions as a data processor. That's covered by a separate data processing agreement, signed before any agent goes live.</p></section>
      </div>
    </div>
  </article>'''

NOTFOUND = '''  <div class="wrap">
    <header class="hub-hero">
      <p class="kicker">404</p>
      <h1 class="hub-title"><span>Lost</span><span>the thread</span></h1>
      <p class="lede">That page doesn't exist, or it's moved. Try the home page, our industry playbooks, or book a free call and we'll point you in the right direction.</p>
      <div class="art-cta-actions" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:10px"><a class="btn btn-glow btn-lg" href="/">Back to home</a><a class="btn btn-ghost btn-lg" href="/industries/">See industries</a></div>
    </header>
  </div>'''

HEADERS = '''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/assets/*
  Cache-Control: public, max-age=604800

/assets/brand/*
  Cache-Control: public, max-age=31536000, immutable
'''

def pages(page_shell):
    for rel, title, desc, body, kind in [
        ('privacy.html', 'Privacy notice · Cogent Intelligence', 'How Cogent Intelligence collects, uses and protects your personal data when you use this website or book a call.', PRIVACY, 'article'),
        ('404.html', 'Page not found · Cogent Intelligence', 'This page could not be found.', NOTFOUND, 'hub')]:
        schema = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": DOMAIN + '/' + rel.replace('.html', '')}
        s = page_shell('', rel, title, desc, body, False, schema, page=kind)
        s = s.replace(' class="is-active" aria-current="page"', '').replace('{p}', '')
        s = s.replace('href="industries/index.html"', 'href="industries/index.html"')
        if rel == '404.html':
            # 404 is served from any path, so use root-absolute URLs
            s = re.sub(r'(href|src)="(?!https?:|#|/|mailto:)([^"]+)"', r'\1="/\2"', s)
            s = s.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')
        open(f'{OUT}/{rel}', 'w').write(s)
    open(f'{OUT}/_headers', 'w').write(HEADERS)

def run(page_shell):
    patch_home(); patch_js(); pages(page_shell); global_pass()
