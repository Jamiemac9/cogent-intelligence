"""v4: why-it's-different (vs ChatGPT/Claude), the map, chapter indicators, cleaner offer, lighter copy, comparison article."""
import os as _os
_B = _os.path.dirname(_os.path.abspath(__file__))
_R = _os.path.dirname(_B)
import re, os, json, html as H

OUT = _os.path.join(_R, 'site')
DOMAIN = 'https://cogentintelligence.co.uk'
e = lambda s: H.escape(s, quote=False)
CHECK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ART = 'insights/ai-agents-vs-chatgpt.html'

def ico(paths):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'
I_MEM = ico('<path d="M12 4.5a3.5 3.5 0 0 0-6.6 1.7A3.5 3.5 0 0 0 4 12.5a3.5 3.5 0 0 0 3 5.3 3 3 0 0 0 5 1.2m0-14.5a3.5 3.5 0 0 1 6.6 1.7A3.5 3.5 0 0 1 20 12.5a3.5 3.5 0 0 1-3 5.3 3 3 0 0 1-5 1.2m0-14.5V19" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
I_TASK = ico('<path d="M13 2.5 4.5 14H11l-1 7.5L18.5 10H12l1-7.5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>')
I_AUTO = ico('<circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 7.5V12l3 2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>')
I_TOOLS = ico('<rect x="3.5" y="4.5" width="17" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 9.5h17M8 4.5v5" fill="none" stroke="currentColor" stroke-width="1.6"/>')
I_AGENTS = ico('<rect x="5" y="8" width="14" height="11" rx="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 8V4.5M9.5 13h.01M14.5 13h.01" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')
I_YOU = ico('<rect x="7" y="2.5" width="10" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M9.5 12.5l1.8 1.8 3.4-3.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')

# ------------------------------------------------------------------ 01 why it's different
PILLARS = [
    ('mem', I_MEM, 'Memory', 'Remembers your business, not just your chats',
     'Notes about you, in your own account', 'Every customer, job, price and rule, shared by every agent',
     '''<div class="pv-rows" data-seq data-tick="800" data-hold="5" aria-hidden="true">
          <p data-at="1"><i class="violet"></i><b>Priya S.</b><span>prefers Thursday mornings</span></p>
          <p data-at="2"><i></i><b>LS6</b><span>call-out £85, 2-hour slots</span></p>
          <p data-at="3"><i class="ember"></i><b>Rule</b><span>never quote boilers by email</span></p>
          <span class="vchip ok" data-at="4">Shared with every agent</span>
        </div>'''),
    ('task', I_TASK, 'Tasks', 'Does the job, not just the draft',
     'Hands you text to copy, paste and send', 'Works inside your inbox, calendar, accounts and CRM',
     '''<div class="pv-rows" data-seq data-tick="800" data-hold="5" aria-hidden="true">
          <p data-at="1"><i></i><b>Enquiry answered</b><span class="st ok">Done</span></p>
          <p data-at="2"><i></i><b>Invoice #2214 chased</b><span class="st ok">Done</span></p>
          <p data-at="3"><i></i><b>Survey in the diary</b><span class="st ok">Done</span></p>
          <p data-at="4"><i class="ember"></i><b>Quote Q-0318</b><span class="st ask">Your OK</span></p>
        </div>'''),
    ('auto', I_AUTO, 'Autonomy', 'Starts on its own, day and night',
     'Waits until you open it and type', 'Starts when an email lands, a bill goes overdue or it&rsquo;s Monday 7am',
     '''<div class="pv-rows pv-rows--time" data-seq data-tick="800" data-hold="5" aria-hidden="true">
          <p data-at="1"><time>23:47</time><b>New enquiry</b><span>reply drafted</span></p>
          <p data-at="2"><time>Mon 07:00</time><b>Briefing</b><span>sent to you</span></p>
          <p data-at="3"><time>Fri 16:00</time><b>Timesheets</b><span>chased</span></p>
          <span class="vchip ok" data-at="4">Nobody typed a thing</span>
        </div>'''),
]
ROWS = [
    ('Who uses it', 'One person, one chat window', 'Your whole team, by WhatsApp, Slack, Telegram or email'),
    ('Control', 'You check every answer yourself', 'Clear rules: what it does alone, what waits for your tap. Every action logged'),
    ('Learning', 'You re-explain how you like things done', 'Your corrections are saved, so it does it your way next time'),
    ('Setup and upkeep', 'You write the prompts and fix what breaks', 'We map, build, monitor and fix it for you'),
]

def different_section():
    cards = ''.join(f'''
      <article class="pillar pillar--{k}">
        <div class="pv">{vis}</div>
        <div class="pb">
          <p class="pk"><span class="pi">{icon}</span>{label}</p>
          <h3>{h}</h3>
          <dl class="vs"><div class="them"><dt>Chat app</dt><dd>{them}</dd></div><div class="us"><dt>Cogent</dt><dd>{us}</dd></div></dl>
        </div>
      </article>''' for k, icon, label, h, them, us, vis in PILLARS)
    rows = ''.join(f'<div class="dt-row" role="row"><span role="rowheader">{a}</span><span role="cell" class="them">{b}</span><span role="cell" class="us">{c}</span></div>' for a, b, c in ROWS)
    return f'''<section class="diff" id="different" aria-labelledby="diff-h">
    <div class="wrap">
      <div class="diff-head" data-reveal>
        <div>
          <p class="kicker"><span class="kn">01</span>Why not just ChatGPT?</p>
          <h2 class="h2" id="diff-h">A chat app answers.<br>Cogent gets it done.</h2>
        </div>
        <p class="lede">ChatGPT and Claude are brilliant at helping whoever is typing. Cogent is built around your business, so it remembers, acts and keeps going when nobody is.</p>
      </div>
      <div class="pillars" data-stagger>{cards}
      </div>
      <div class="dtable" role="table" aria-label="Chat app compared with Cogent" data-reveal>
        <div class="dt-row dt-head" role="row"><span role="columnheader">And around it</span><span role="columnheader" class="them">Chat app</span><span role="columnheader" class="us">Cogent</span></div>
        {rows}
      </div>
      <p class="diff-fine">Cogent runs on leading AI models, the same kind behind ChatGPT and Claude. The difference is everything built around them. <a class="link-arrow" href="{ART}">Read the full comparison {ARROW}</a></p>
    </div>
  </section>

  '''

# ------------------------------------------------------------------ 02 the map
NODES = [
    ('tools', I_TOOLS, 'Your tools', 'Connected, not replaced', ['Inbox', 'Calendar', 'Xero or QuickBooks', 'CRM', 'WhatsApp']),
    ('brain', I_MEM, 'Second brain', 'Your Business Map and memory', ['Customers', 'Prices', 'Rules', 'Tone', 'History']),
    ('agents', I_AGENTS, 'AI agents', 'Do the work, around the clock', ['Enquiry Responder', 'Quote Drafter', 'Invoice Chaser', 'Monday Briefing']),
    ('you', I_YOU, 'You', 'Stay in charge from your phone', ['Approve with a tap', 'Ask anything', 'Delegate by voice note']),
]

def map_section():
    nodes = ''.join(f'''
        <li class="mnode mnode--{k}">
          <span class="mnum">{i + 1}</span>
          <span class="mico">{icon}</span>
          <h3>{t}</h3>
          <p>{sub}</p>
          <ul class="mchips">{''.join(f'<li>{c}</li>' for c in chips)}</ul>
        </li>''' for i, (k, icon, t, sub, chips) in enumerate(NODES))
    return f'''<section class="bmap" id="fits" aria-labelledby="map-h">
    <div class="wrap">
      <div class="bmap-head" data-reveal>
        <p class="kicker"><span class="kn">02</span>How it fits together</p>
        <h2 class="h2" id="map-h">One map. Every agent works from it.</h2>
        <p class="lede">Your tools feed one memory. Agents work from it. You approve what matters.</p>
      </div>
      <ol class="mflow" data-stagger>{nodes}
      </ol>
      <p class="mloop" data-reveal><span class="mloop-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 0 1 13.7-5.6L20 8.5M20 4v4.5h-4.5M20 12a8 8 0 0 1-13.7 5.6L4 15.5M4 20v-4.5h4.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Every correction you make goes back into memory, so the whole system gets better each week.</p>
    </div>
  </section>

  '''

# ------------------------------------------------------------------ offer
SETUP = [
    dict(name='Standard setup', price='£1,997', note='One-off · first agent live in 14 days', badge='Most businesses start here', feature=True,
         items=['Your Business Map: people, tools, prices and rules', 'Inbox, calendar, accounts and CRM connected', 'One agent from tested templates, approvals set', 'Live in 14 days, or the rest of setup waits']),
    dict(name='Custom AI agent', price='£4,997', note='One-off · timeline agreed in writing', feature=False,
         items=['Everything in Standard setup', 'An agent built around your own process and documents', 'Delegation by WhatsApp, Slack, Telegram or email', 'Works old systems that have no integration']),
]
TIERS = [
    dict(name='Starter', price='£297', who='1 agent · 1,000 tasks a month', items=['Monitored and fixed by us', 'Monday briefing on your numbers', 'Ask your second brain anything']),
    dict(name='Growth', price='£597', who='Up to 3 agents · 3,000 tasks', badge='Most popular', feature=True, items=['Everything in Starter', 'Delegate by message or voice note', 'Scheduled jobs and a monthly review']),
    dict(name='Scale', price='£897', who='Up to 6 agents · 7,500 tasks', items=['Everything in Growth', 'Same-working-day fixes', 'Per-team briefings, quarterly Map refresh']),
]

def offer_section():
    def lis(items): return ''.join(f'<li>{CHECK}{e(i)}</li>' for i in items)
    setup = ''.join(f'''<article class="plan{' plan--feature' if p.get('feature') else ''}">
          {f'<span class="plan-badge">{p["badge"]}</span>' if p.get('badge') else ''}<h3>{p['name']}</h3>
          <div class="plan-price"><small class="plan-from">from</small><b>{p['price']}</b><span>{p['note']}</span></div>
          <ul>{lis(p['items'])}</ul>
          <button class="btn {'btn-glow' if p.get('feature') else 'btn-ghost'}" type="button" data-funnel>Start with the free call</button>
        </article>''' for p in SETUP)
    tiers = ''.join(f'''<article class="plan plan--tier{' plan--feature' if t.get('feature') else ''}">
          {f'<span class="plan-badge">{t["badge"]}</span>' if t.get('badge') else ''}<h3>{t['name']}</h3>
          <div class="plan-price"><b>{t['price']}<em>/mo</em></b><span>{t['who']}</span></div>
          <ul>{lis(t['items'])}</ul>
        </article>''' for t in TIERS)
    return f'''<section class="offer" id="offer" aria-label="Pricing">
    <div class="wrap">
      <div class="offer-head" data-reveal>
        <p class="kicker"><span class="kn">08</span>Pricing</p>
        <h2 class="h2">Two prices. No surprises.</h2>
        <p class="lede">A one-off setup, then a monthly plan. It all starts with a free call.</p>
      </div>
      <ol class="pladder" data-stagger>
        <li><span class="ln">1</span><span class="lt">Free call</span><b>£0</b><small>Your top 3 time-wasters, on one page</small></li>
        <li><span class="ln">2</span><span class="lt">Setup</span><b>from £1,997</b><small>One-off. First agent live in 14 days</small></li>
        <li><span class="ln">3</span><span class="lt">Monthly</span><b>from £297<em>/mo</em></b><small>Agents running, watched and improved</small></li>
      </ol>
      <p class="offer-label"><span>Step 2</span>One-off setup</p>
      <div class="offer-grid offer-grid--two" data-stagger>
        {setup}
      </div>
      <p class="offer-label"><span>Step 3</span>Monthly plan · priced per agent, tasks included</p>
      <div class="offer-grid offer-grid--tiers" data-stagger>
        {tiers}
      </div>
      <p class="offer-fine">A task is one job done, like an enquiry answered or an invoice chased. Extra agents £147/mo. Rolling monthly with 30 days' notice. Setup is paid 50% to start and 50% at go-live. Prices exclude VAT where applicable.</p>
      <div class="promise-bar" data-reveal>
        <p><b>The 14-day promise.</b> If your first agent isn't live 14 days after mapping, the second half of setup waits until it is.</p>
        <button class="btn btn-glow" type="button" data-funnel data-magnetic>Book the free call {ARROW}</button>
      </div>
    </div>
  </section>'''

# ------------------------------------------------------------------ FAQ + chapters
NEW_Q = "Isn't this just ChatGPT with extra steps?"
NEW_A = ("No. ChatGPT and Claude help whoever is typing. Cogent is set up around your business: it remembers every customer, price and rule, "
         "works inside your inbox, calendar, accounts and CRM, starts jobs on its own when something happens, and asks before anything reaches a customer "
         "or touches money. We build it, watch it and fix it, so there's nothing for you to prompt or maintain.")
CHAPTERS = [('different', '01', 'Why Cogent'), ("fits", "02", "How it fits"), ('intelligence', '03', 'Memory'), ('agents', '04', 'Tasks'),
            ('delegate', '05', 'Autonomy'), ('industries', '06', 'Your industry'), ('how', '07', '14 days'), ('offer', '08', 'Pricing'), ('faq', '09', 'Questions')]
KICKERS = {'intelligence': ('Your second brain', 'Memory'), 'agents': ('The AI team', 'Tasks'), 'delegate': ("Delegate, don't do", 'Autonomy'),
           'industries': ('Built for your industry', 'Your industry'), 'how': ('How it works', '14 days to live'), 'faq': ('Questions', 'Questions')}

def sub_once(pat, rep, s, flags=re.S):
    s2, n = re.subn(pat, rep, s, count=1, flags=flags)
    assert n == 1, pat[:60]
    return s2

def rep_once(old, new, s):
    assert old in s, old[:70]
    return s.replace(old, new, 1)

def section(s, sid):
    m = re.search(r'<section[^>]*id="%s".*?</section>' % sid, s, re.S)
    assert m, sid
    return m

def edit_section(s, sid, fn):
    m = section(s, sid)
    return s[:m.start()] + fn(m.group(0)) + s[m.end():]

def home():
    p = f'{OUT}/index.html'; s = open(p).read()
    # hero
    s = sub_once(r'<p class="hero-sub([^"]*)"([^>]*)>.*?</p>',
                 r'<p class="hero-sub\1"\2>Not another chatbot. An AI team that <b>remembers</b> your business, <b>does the work</b> and <b>runs on its own</b>, with you approving anything that matters.</p>', s)
    s = rep_once('<a class="btn btn-ghost btn-lg" href="#intelligence">See it think</a>', '<a class="btn btn-ghost btn-lg" href="#different">Why not ChatGPT?</a>', s)
    s = rep_once('<a class="scroll-pill" href="#problem">Scroll to see what it knows', '<a class="scroll-pill" href="#problem">Scroll to see the difference', s)
    # manifesto becomes the one-line difference
    s = sub_once(r'<p class="kicker">Sound familiar\?</p>\s*<p class="manifesto-text" data-words>.*?</p>',
                 '<p class="kicker">The difference</p>\n      <p class="manifesto-text" data-words>A chat app <em>waits for you to ask.</em> Cogent <em>knows your business,</em> <em>starts the work itself</em> and <em>finishes the job.</em> You just <em>approve what matters.</em></p>', s)
    s = sub_once(r'(<div class="manifesto-after">\s*)<p>.*?</p>\s*<a class="link-arrow" href="#intelligence">See it think',
                 r'\1<p>Same kind of AI underneath. Everything around it is built for your business.</p>\n        <a class="link-arrow" href="#different">See the difference', s)
    # new sections after the manifesto
    m = section(s, 'problem')
    s = s[:m.end()] + '\n\n  ' + different_section() + map_section().rstrip() + s[m.end():]
    # numbered kickers
    for sid, (old, new) in KICKERS.items():
        num = next(n for c, n, _ in CHAPTERS if c == sid)
        s = edit_section(s, sid, lambda t, old=old, new=new, num=num: rep_once(f'<p class="kicker">{old}</p>', f'<p class="kicker"><span class="kn">{num}</span>{new}</p>', t))
    # lighter copy
    s = edit_section(s, 'intelligence', lambda t: sub_once(r'<p class="lede">.*?</p>', '<p class="lede">Your inbox, calendar, accounts and CRM in one memory. Ask in plain English and get the answer with the numbers behind it.</p>', t))
    def deleg(t):
        t = sub_once(r'<p class="lede">.*?</p>', '<p class="lede">Send a message or voice note on WhatsApp, Slack, Telegram or email. Your operator splits it into jobs, hands them to the right agents and reports back.</p>', t)
        return re.sub(r'(<li><b>[^<]*</b>)[^<]*(</li>)', r'\1\2', t)
    s = edit_section(s, 'delegate', deleg)
    def sectors(t):
        t = sub_once(r'<p class="lede">.*?</p>', '<p class="lede">An Enquiry Responder for a plumber isn\'t the same as one for a solicitor. Every setup starts from a playbook for your sector.</p>', t)
        return re.sub(r'(<li><b>[^<]*</b>)[^<]*(</li>)', r'\1\2', t)
    s = edit_section(s, 'industries', sectors)
    s = edit_section(s, 'demo', lambda t: sub_once(r'<p class="lede">.*?</p>', '<p class="lede">It reads the enquiry, checks your Map and drafts a reply in seconds. It\'s going to a customer, so it waits for your tap at breakfast.</p>', t))
    s = edit_section(s, 'control', lambda t: sub_once(r'<p class="lede">.*?</p>', '<p class="lede">Anything that reaches a customer or touches money waits for your yes. Approvals loosen only after a clean track record.</p>', t))
    s = edit_section(s, 'course', lambda t: sub_once(r'<p class="lede">.*?</p>', '<p class="lede">Not ready for a call? Five short emails, one a day. By Friday you\'ll know which job to hand off first.</p>', t))
    # offer
    m = section(s, 'offer'); s = s[:m.start()] + offer_section() + s[m.end():]
    # FAQ: new first question, show 6 then "all"
    def faq(t):
        t = t.replace('<div class="qa is-open">', '<div class="qa">', 1).replace('aria-expanded="true" aria-controls="qa-1"', 'aria-expanded="false" aria-controls="qa-1"', 1)
        new = f'''<div class="qa is-open"><h3><button type="button" aria-expanded="true" aria-controls="qa-0" id="qa-0-b">{e(NEW_Q)}<span class="x" aria-hidden="true"></span></button></h3>
          <div class="qa-panel" id="qa-0" role="region" aria-labelledby="qa-0-b"><div><p>{e(NEW_A)}</p></div></div></div>
        '''
        t = rep_once('<div class="faq-list">', '<div class="faq-list">\n        ' + new, t)
        k = [0]
        def tag(mm):
            k[0] += 1
            return '<div class="qa qa--more">' if k[0] > 6 else mm.group(0)
        t = re.sub(r'<div class="qa(?: is-open)?">', lambda mm: mm.group(0) if 'is-open' in mm.group(0) else tag(mm), t)
        n = t.count('class="qa')
        t = rep_once('\n      </div>\n    </div>\n  </section>', f'\n        <button class="btn btn-ghost faq-more" type="button" aria-expanded="false">Show all {n} questions</button>\n      </div>\n    </div>\n  </section>', t)
        return t
    s = edit_section(s, 'faq', faq)
    # FAQ schema
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S)
    g = json.loads(m.group(1))
    for n in g['@graph']:
        if n.get('@type') == 'FAQPage':
            n['mainEntity'].insert(0, {"@type": "Question", "name": NEW_Q, "acceptedAnswer": {"@type": "Answer", "text": NEW_A}})
        if n.get('@type') == 'ProfessionalService':
            n['description'] = ('AI agents and a business second brain for UK service businesses. Unlike a chat app, Cogent remembers every customer, price and rule, '
                                'works inside your own tools, starts jobs on its own and asks your approval on anything customer-facing or involving money.')
    s = s[:m.start(1)] + json.dumps(g, ensure_ascii=False) + s[m.end(1):]
    # chapter indicator
    chap = '<nav class="chapters" aria-label="On this page">' + ''.join(f'<a href="#{c}"><span class="cn">{n}</span><span class="cl">{l}</span></a>' for c, n, l in CHAPTERS) + '</nav>\n'
    s = rep_once('<main', chap + '<main', s) if '<main' in s else rep_once('<section class="hero"', chap + '<section class="hero"', s)
    open(p, 'w').write(s)

def nav_all():
    for root, _, fs in os.walk(OUT):
        for f in fs:
            if not f.endswith('.html'): continue
            p = os.path.join(root, f); s = open(p).read(); o = s
            s = re.sub(r'\n\s*<a href="([^"]*)#how">How it works</a>', '', s)
            s = re.sub(r'<a href="([^"]*)#intelligence">Second brain</a>', r'<a href="\1#different">Why Cogent</a>', s)
            s = re.sub(r'<a href="([^"]*)#agents">Agents</a>', r'<a href="\1#fits">How it works</a>', s)
            if s != o: open(p, 'w').write(s)

# ------------------------------------------------------------------ article
ART_SECTIONS = [
    ('The short answer', '<p>ChatGPT and Claude are general assistants. They are excellent at helping whoever is typing: writing, summarising, thinking things through. An AI agent system like Cogent is set up around one business. It knows your customers, prices and rules, works inside the tools you already use, and starts jobs without being asked.</p><div class="keyidea"><p class="kicker">Key idea</p><p>A chat app is a very clever colleague you have to brief every time. A second brain is one that already knows the business and gets on with it.</p></div>'),
    ('Memory: you, or your business?', '<p>Chat apps can remember things about <em>you</em>: your name, your writing style, a project you mentioned. That memory lives in one person\'s account.</p><p>Cogent remembers the <em>business</em>. Every customer, conversation, price list, service area, rule and correction sits in one place, written into your Business Map. Every agent works from it, and anyone on your team can ask it a question. When Priya rings back in six months, it knows she prefers Thursday mornings.</p>'),
    ('Tasks: a draft, or a finished job?', '<p>Ask a chat app to chase an invoice and you get a well-written email. You still have to find the invoice, copy the text, paste it into your inbox, send it and remember to check for a reply.</p><p>A Cogent agent does the whole job inside your own tools. It spots the overdue invoice in Xero, sends the reminder on your schedule, logs the reply and updates the record. Anything that goes to a customer or touches money waits for your approval first.</p>'),
    ('Autonomy: waits, or starts?', '<p>A chat app does nothing until someone opens it and types. Most of the time-wasting work in a service business happens when nobody is at a keyboard: the enquiry at 11:47pm, the timesheet that didn\'t arrive, the Monday numbers nobody has pulled together.</p><p>Cogent agents start on their own when something happens (an email lands, a bill goes overdue, it\'s Monday at 7am). You can also delegate by message or voice note, and say "every Friday at 4pm" once for it to happen every week.</p>'),
    ('Control and upkeep', '<p>With a chat app you are the quality check, and you maintain the prompts. With Cogent the rules are agreed up front: what each agent does alone, what waits for your tap, and what it never does. Every action is logged. We monitor the agents, fix them when something changes and review the log with you every month.</p>'),
    ('When a chat app is enough', '<p>If you mainly want help writing, researching or thinking, a personal ChatGPT or Claude subscription is great value, and we\'d tell you that on the call. Cogent is worth it when the same jobs repeat every week across your inbox, diary and accounts, and someone is losing hours to them.</p>'),
    ('Side by side', '''<div class="table-wrap"><table><thead><tr><th scope="col"></th><th scope="col">Chat app (ChatGPT, Claude)</th><th scope="col">Cogent</th></tr></thead><tbody>
<tr><th scope="row">Built around</th><td>The person typing</td><td>Your business</td></tr>
<tr><th scope="row">Memory</th><td>Notes about you, in your account</td><td>Every customer, price and rule, shared by every agent</td></tr>
<tr><th scope="row">Tasks</th><td>Drafts to copy and paste</td><td>Finished jobs inside your inbox, calendar, accounts and CRM</td></tr>
<tr><th scope="row">Starts work</th><td>When you open it and type</td><td>On its own: new email, overdue bill, a set time</td></tr>
<tr><th scope="row">Team access</th><td>One person per account</td><td>Whole team, by WhatsApp, Slack, Telegram or email</td></tr>
<tr><th scope="row">Control</th><td>You check every answer</td><td>Agreed approval rules, every action logged</td></tr>
<tr><th scope="row">Upkeep</th><td>You</td><td>Us, with a monthly review</td></tr>
</tbody></table></div>'''),
]
ART_FAQ = [
    ('Does Cogent use ChatGPT?', 'Cogent runs on leading AI models from established providers, chosen for each job. Customer data only goes to models approved for personal data. The difference is the memory, connections, rules and monitoring built around the model.'),
    ('Can I build this myself with ChatGPT?', 'You can get part of the way with a lot of time, integrations and prompt upkeep. Most owners we speak to would rather spend that time on paying work, which is why we map, build and maintain it for you.'),
    ('Is an AI agent the same as a chatbot?', 'No. A chatbot answers questions in a chat window. An AI agent takes actions in your systems, such as replying to an enquiry, chasing an invoice or updating a record, within rules you set.'),
]

def article_body():
    toc = ''.join(f'<li><a href="#p{i + 1}">{e(h)}</a></li>' for i, (h, _) in enumerate(ART_SECTIONS + [('Questions', '')]))
    fq = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in ART_FAQ)
    secs = ART_SECTIONS + [('Questions', fq + '<p><a href="../index.html#offer">See pricing</a> or <a href="https://cal.com/jamiemac/30min">book a free 30-minute call</a>.</p>')]
    body = ''.join(f'<section id="p{i + 1}"><h2><span class="num">{i + 1:02d}</span>{e(h)}</h2>{html}</section>\n' for i, (h, html) in enumerate(secs))
    return f'''  <article class="article wrap">
    <header class="art-hero">
      <div class="art-hero-text">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="index.html">Insights</a><span aria-hidden="true">/</span><span>AI agents vs ChatGPT</span></nav>
        <p class="art-meta">5 min read · 12 October 2026</p>
        <h1 class="art-title">AI agents vs ChatGPT: what's the difference for a small business?</h1>
        <p class="art-dek">ChatGPT and Claude help whoever is typing. A second brain remembers your business, does the work and starts on its own. Here's the difference in plain English, and when a chat app is all you need.</p>
      </div>
      <div class="art-cover" data-parallax aria-hidden="true">
        <img class="scene" src="../assets/scenes/ai-agents-vs-chatgpt.svg" alt="" data-depth="0.25" fetchpriority="high" decoding="async">
      </div>
    </header>
    <div class="art-grid">
      <aside class="toc" aria-label="On this page"><p class="toc-h">On this page</p><ol>{toc}</ol></aside>
      <div class="prose">
{body}      </div>
    </div>
  </article>'''

def pre(page_shell):
    """Create the article before v3 runs so it gets the shared footer, consent, course and SEO passes."""
    os.makedirs(f'{OUT}/assets/scenes', exist_ok=True)
    url = f'{DOMAIN}/insights/ai-agents-vs-chatgpt'
    title = "AI Agents vs ChatGPT for Small Business: What's the Difference? · Cogent Intelligence"
    desc = 'ChatGPT and Claude help whoever is typing. AI agents remember your business, do the work in your own tools and start on their own. A plain-English comparison for UK service businesses.'
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": "AI agents vs ChatGPT: what's the difference for a small business?", "description": desc, "url": url,
         "datePublished": "2026-10-12", "dateModified": "2026-10-12", "image": f"{DOMAIN}/assets/og/ai-agents-vs-chatgpt.jpg",
         "author": {"@type": "Organization", "name": "Cogent Intelligence", "url": DOMAIN + "/"}, "publisher": {"@id": DOMAIN + "/#org"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                                                       {"@type": "ListItem", "position": 2, "name": "Insights", "item": DOMAIN + "/insights/"},
                                                       {"@type": "ListItem", "position": 3, "name": "AI agents vs ChatGPT", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in ART_FAQ]}]}
    s = page_shell('../', ART, title, desc, article_body(), False, schema, page='article')
    s = s.replace(' class="is-active" aria-current="page"', '')
    open(f'{OUT}/{ART}', 'w').write(s)
    # insights hub card
    hp = f'{OUT}/insights/index.html'; h = open(hp).read()
    if 'ai-agents-vs-chatgpt' not in h:
        card = f'''<div class="fp"><a class="dcard" href="ai-agents-vs-chatgpt.html" data-tilt>
          <div class="dcard-cover"><img class="cover scene" src="../assets/scenes/ai-agents-vs-chatgpt.svg" alt="" loading="lazy" decoding="async"><span class="dcard-tag">Compare</span></div>
          <div class="dcard-body"><p class="dcard-meta">5 min read · 12 October 2026</p><h3>AI agents vs ChatGPT: what's the difference for a small business?</h3><p>Memory, tasks and autonomy, in plain English.</p><span class="dcard-go">Read the article {ARROW}</span></div>
        </a></div>
      </div>
    </section>'''
        h = rep_once('</a></div>\n      </div>\n    </section>', '</a></div>\n        ' + card, h)
        open(hp, 'w').write(h)

# ------------------------------------------------------------------ CSS / JS
HOME_CSS = r'''
/* ---- v4: numbered chapters ---- */
.kicker .kn{display:inline-block;margin-right:10px;padding:3px 6px;border-radius:6px;background:var(--ember-soft);color:var(--ember);letter-spacing:.06em}
.hero-sub b{color:var(--bone);font-weight:600}
.chapters{position:fixed;right:18px;top:50%;z-index:40;display:grid;gap:4px;transform:translate(16px,-50%);opacity:0;pointer-events:none;transition:opacity .4s var(--ease),transform .5s var(--ease)}
.chapters.is-on{opacity:1;transform:translate(0,-50%);pointer-events:auto}
.chapters a{position:relative;display:flex;align-items:center;justify-content:flex-end;gap:10px;padding:5px 4px;color:var(--dim);text-decoration:none;font:500 11px/1 var(--f-mono);letter-spacing:.08em}
.chapters .cn{display:grid;place-items:center;width:26px;height:26px;border-radius:50%;border:1px solid var(--rule);background:rgba(11,10,10,.7);transition:all .3s var(--ease)}
.chapters .cl{position:absolute;right:38px;padding:6px 9px;border-radius:8px;background:var(--glass);border:1px solid var(--rule);color:var(--bone);white-space:nowrap;opacity:0;transform:translateX(6px);transition:all .3s var(--ease);pointer-events:none;text-transform:uppercase}
.chapters a:hover .cl,.chapters a:focus-visible .cl{opacity:1;transform:none}
.chapters a.is-active .cn{background:var(--ember);border-color:var(--ember);color:var(--ink)}
.chapters a.is-done .cn{border-color:rgba(255,122,47,.45);color:var(--ember-2)}
@media (max-width:1359px){.chapters{display:none}}

/* ---- v4: why it's different ---- */
.diff{position:relative;padding:clamp(80px,11vw,150px) 0 clamp(60px,8vw,110px)}
.diff-head,.bmap-head{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(20px,4vw,60px);align-items:end;margin-bottom:clamp(30px,4vw,52px)}
.bmap-head{grid-template-columns:1fr;row-gap:16px;max-width:760px;margin-inline:auto;text-align:center;justify-items:center}
.diff-head .kicker,.bmap-head .kicker{margin-bottom:16px}
.pillars{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pillar{display:flex;flex-direction:column;border-radius:24px;border:1px solid var(--rule);background:var(--glass);overflow:hidden}
.pv{position:relative;height:244px;padding:22px;display:flex;align-items:flex-start;border-bottom:1px solid var(--rule);background:radial-gradient(90% 90% at 20% 0%,rgba(255,122,47,.13),transparent 60%),var(--ink-2)}
.pillar--task .pv{background:radial-gradient(90% 90% at 80% 0%,rgba(159,227,180,.1),transparent 60%),var(--ink-2)}
.pillar--auto .pv{background:radial-gradient(90% 90% at 50% 0%,rgba(140,107,255,.14),transparent 60%),var(--ink-2)}
.pv-rows{display:grid;gap:8px;width:100%}
.pv-rows p{margin:0;display:grid;grid-template-columns:8px auto minmax(0,1fr);align-items:center;gap:10px;padding:10px 12px;border-radius:12px;border:1px solid var(--rule);background:rgba(241,235,227,.035);font-size:13.5px;line-height:1.25}
.pv-rows p i{width:7px;height:7px;border-radius:50%;background:var(--ok)}
.pv-rows p i.violet{background:var(--violet)}.pv-rows p i.ember{background:var(--ember)}
.pv-rows p b{font-weight:600;white-space:nowrap}
.pv-rows p span{color:var(--mute);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pv-rows .st{justify-self:end;font:500 10.5px/1 var(--f-mono);letter-spacing:.06em;text-transform:uppercase;padding:5px 7px;border-radius:999px}
.pv-rows .st.ok{color:var(--ok);background:var(--ok-soft)}.pv-rows .st.ask{color:var(--ember-2);background:var(--ember-soft)}
.pv-rows--time p{grid-template-columns:auto auto minmax(0,1fr)}
.pv-rows--time time{font:500 11px/1 var(--f-mono);color:var(--violet);min-width:64px}
.pv-rows .vchip{margin-top:4px}
.pb{display:grid;gap:14px;padding:22px 22px 24px}
.pk{margin:0;display:flex;align-items:center;gap:10px;font:500 12px/1 var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ember-2)}
.pi{display:grid;place-items:center;width:30px;height:30px;border-radius:9px;background:var(--ember-soft);color:var(--ember)}
.pi svg{width:17px;height:17px}
.pillar h3{margin:0;font-family:var(--f-display);font-weight:700;font-stretch:108%;font-size:clamp(1.25rem,1.8vw,1.5rem);line-height:1.1}
.vs{margin:0;display:grid;gap:8px}
.vs div{display:grid;grid-template-columns:76px minmax(0,1fr);gap:10px;align-items:baseline;padding:10px 12px;border-radius:12px;font-size:14.5px;line-height:1.4}
.vs dt{font:500 10.5px/1.4 var(--f-mono);letter-spacing:.1em;text-transform:uppercase}
.vs dd{margin:0}
.vs .them{color:var(--dim);background:rgba(241,235,227,.025)}
.vs .them dd{text-decoration:line-through;text-decoration-color:rgba(166,158,148,.35)}
.vs .us{background:var(--ember-soft);border:1px solid rgba(255,122,47,.28)}
.vs .us dt{color:var(--ember)}
.dtable{margin-top:16px;border-radius:24px;border:1px solid var(--rule);background:var(--glass);overflow:hidden}
.dt-row{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr) minmax(0,1.3fr);gap:20px;padding:16px 24px;border-top:1px solid var(--rule-2);font-size:15px;line-height:1.4;align-items:center}
.dt-row:first-child{border-top:0}
.dt-row>span:first-child{font-weight:600}
.dt-row .them{color:var(--dim)}
.dt-row .us{color:var(--bone)}
.dt-row:not(.dt-head) .us::before{content:"";display:inline-block;width:7px;height:7px;margin-right:10px;border-radius:50%;background:var(--ember);vertical-align:middle}
.dt-head{font:500 11px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;background:rgba(241,235,227,.03)}
.dt-head>span:first-child{font-weight:500;color:var(--dim)}
.dt-head .us{color:var(--ember)}
.diff-fine{margin:22px 0 0;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;justify-content:space-between;color:var(--mute);font-size:14.5px}
@media (max-width:1023px){.diff-head{grid-template-columns:1fr}.pillars{grid-template-columns:1fr}.pv{height:auto;min-height:228px}}
@media (max-width:719px){.dt-row{grid-template-columns:1fr 1fr;gap:6px 14px;padding:14px 16px}.dt-row>span:first-child{grid-column:1/-1}.dt-head>span:first-child{display:none}.vs div{grid-template-columns:64px minmax(0,1fr)}}

/* ---- v4: the map ---- */
.bmap{position:relative;padding:clamp(60px,8vw,110px) 0 clamp(80px,10vw,140px)}
.mflow{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(28px,3.4vw,48px);counter-reset:n}
.mnode{position:relative;display:grid;align-content:start;justify-items:start;gap:10px;padding:24px 22px;border-radius:24px;border:1px solid var(--rule);background:var(--glass)}
.mnode--brain{border-color:transparent;background:radial-gradient(120% 80% at 50% 0%,rgba(255,122,47,.2),transparent 62%),rgba(24,21,19,.96);box-shadow:0 30px 80px -40px var(--ember-glow)}
.mnode--brain::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;background:var(--iris);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:.75;pointer-events:none}
.mnode:not(:last-child)::after{content:"";position:absolute;top:50%;right:calc(-1 * clamp(28px,3.4vw,48px));width:clamp(28px,3.4vw,48px);height:2px;background:linear-gradient(90deg,rgba(255,122,47,.15),rgba(255,122,47,.7));transform:translateY(-1px)}
.mnode:not(:last-child)>.mnum::after{content:"";position:absolute;top:calc(50% - 4px);right:calc(-1 * clamp(28px,3.4vw,48px) - 2px);width:8px;height:8px;border-radius:50%;background:var(--ember);box-shadow:0 0 12px var(--ember-glow);animation:mpulse 2.4s var(--ease-io) infinite}
@keyframes mpulse{0%{transform:translateX(calc(-1 * clamp(28px,3.4vw,48px)));opacity:0}20%,80%{opacity:1}100%{transform:translateX(0);opacity:0}}
.mnum{position:static;font:500 11px/1 var(--f-mono);letter-spacing:.14em;color:var(--dim)}
.mnum::before{content:"Step "}
.mico{display:grid;place-items:center;width:44px;height:44px;border-radius:13px;background:var(--ember-soft);color:var(--ember);margin-top:2px}
.mico svg{width:22px;height:22px}
.mnode h3{margin:4px 0 0;font-family:var(--f-display);font-weight:700;font-stretch:108%;font-size:clamp(1.3rem,1.8vw,1.55rem);line-height:1.05}
.mnode>p{margin:0;color:var(--mute);font-size:14.5px;line-height:1.4}
.mchips{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.mchips li{padding:6px 9px;border-radius:999px;border:1px solid var(--rule);background:rgba(241,235,227,.04);font:500 11px/1 var(--f-mono);letter-spacing:.02em;color:var(--bone-2)}
.mnode--brain .mchips li{border-color:rgba(255,122,47,.3);color:var(--ember-2)}
.mloop{margin:26px auto 0;max-width:640px;display:flex;align-items:center;justify-content:center;gap:12px;text-align:left;color:var(--mute);font-size:15px}
.mloop-ico{flex:none;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;border:1px dashed rgba(255,122,47,.5);color:var(--ember)}
.mloop-ico svg{width:18px;height:18px}
@media (max-width:1023px){.mflow{grid-template-columns:1fr 1fr}.mnode:nth-child(2)::after,.mnode:nth-child(2)>.mnum::after{display:none}}
@media (max-width:719px){.mflow{grid-template-columns:1fr;gap:34px}
  .mnode:not(:last-child)::after{top:auto;bottom:-34px;right:auto;left:42px;width:2px;height:34px;background:linear-gradient(180deg,rgba(255,122,47,.15),rgba(255,122,47,.7))}
  .mnode:nth-child(2)::after{display:block}
  .mnode:not(:last-child)>.mnum::after{display:none}}
@media (prefers-reduced-motion:reduce){.mnode>.mnum::after{animation:none!important;display:none}}

/* ---- v4: industries lighter on home ---- */
.sectors .sp-does{display:none}
.sectors .sp-pains li{font-size:15px}

/* ---- v4: offer ---- */
.pladder{list-style:none;margin:clamp(30px,4vw,46px) 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-radius:24px;border:1px solid var(--rule);background:var(--glass);overflow:hidden}
.pladder li{position:relative;display:grid;gap:6px;padding:22px 26px 22px 26px;border-left:1px solid var(--rule)}
.pladder li:first-child{border-left:0}
.pladder li:not(:last-child)::after{content:"";position:absolute;right:-9px;top:50%;width:16px;height:16px;border-top:1px solid var(--rule);border-right:1px solid var(--rule);background:var(--ink-2);transform:translateY(-50%) rotate(45deg);z-index:1}
.pladder .ln{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;background:var(--ember);color:var(--ink);font:600 11px/1 var(--f-mono)}
.pladder .lt{font:500 11px/1 var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-top:4px}
.pladder b{font-family:var(--f-display);font-weight:700;font-stretch:112%;font-size:clamp(1.5rem,2.4vw,2rem);line-height:1}
.pladder b em{font-style:normal;font-size:.5em;color:var(--mute);margin-left:3px;font-weight:500}
.pladder small{color:var(--mute);font-size:14px}
.offer-label{margin:clamp(36px,4.5vw,54px) 0 0;display:flex;align-items:center;gap:12px;font:500 12px/1 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--bone-2)}
.offer-label span{padding:5px 8px;border-radius:6px;background:var(--ember-soft);color:var(--ember)}
.offer .offer-label+.offer-grid{margin-top:18px}
.offer-grid--two{grid-template-columns:repeat(2,minmax(0,1fr))}
.plan--tier .plan-price{padding-bottom:16px}
.promise-bar{margin-top:18px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 24px;padding:20px 24px;border-radius:20px;border:1px solid rgba(255,122,47,.38);background:linear-gradient(115deg,rgba(255,122,47,.16),rgba(20,18,17,.92) 60%)}
.promise-bar p{margin:0;max-width:62ch;color:var(--bone-2)}
.promise-bar b{color:var(--bone)}
@media (max-width:1023px){.offer-grid--two{grid-template-columns:1fr}}
@media (max-width:719px){.pladder{grid-template-columns:1fr}.pladder li{border-left:0;border-top:1px solid var(--rule);grid-template-columns:24px auto 1fr;align-items:center;column-gap:12px;padding:16px 18px}.pladder li:first-child{border-top:0}.pladder li::after{display:none}.pladder .lt{margin:0}.pladder b{font-size:1.25rem;justify-self:end}.pladder small{grid-column:2/-1}}

/* ---- v4: FAQ show more ---- */
.faq-list:not(.is-all) .qa--more{display:none}
.faq-more{margin-top:18px}
.faq-list.is-all .faq-more{display:none}
'''

HOME_JS = r'''
/* v4: chapter indicator + FAQ show-all */
(function () {
  const nav = document.querySelector('.chapters');
  if (nav && 'IntersectionObserver' in window) {
    const links = Array.from(nav.querySelectorAll('a'));
    const ids = links.map((a) => a.getAttribute('href').slice(1));
    const secs = ids.map((id) => document.getElementById(id)).filter(Boolean);
    const hero = document.querySelector('.hero'), fin = document.querySelector('.final');
    const update = () => {
      const y = window.innerHeight * 0.45;
      let cur = -1;
      secs.forEach((s, i) => { if (s.getBoundingClientRect().top < y) cur = i; });
      links.forEach((a, i) => { a.classList.toggle('is-active', i === cur); a.classList.toggle('is-done', i < cur); });
      const hb = hero ? hero.getBoundingClientRect().bottom : 0;
      const ft = fin ? fin.getBoundingClientRect().top : Infinity;
      nav.classList.toggle('is-on', hb < window.innerHeight * 0.5 && ft > window.innerHeight * 0.6);
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }
  const more = document.querySelector('.faq-more');
  if (more) more.addEventListener('click', () => {
    const list = more.closest('.faq-list');
    list.classList.add('is-all');
    more.setAttribute('aria-expanded', 'true');
    const first = list.querySelector('.qa--more button');
    if (first) first.focus();
  });
})();
'''

CSS = r'''
.dgrid>.fp:nth-child(4){grid-column:1/-1}
@media (min-width:900px){.dgrid>.fp:nth-child(4) .dcard{flex-direction:row;align-items:center}.dgrid>.fp:nth-child(4) .dcard-cover{flex:0 0 52%;margin:10px;aspect-ratio:21/9}.dgrid>.fp:nth-child(4) .dcard-body{flex:1}}
'''

def run():
    home()
    open(f'{OUT}/assets/cogent.css', 'a').write(CSS)
    nav_all()
    open(f'{OUT}/assets/home.css', 'a').write(HOME_CSS)
    open(f'{OUT}/assets/home.js', 'a').write(HOME_JS)
    # sitemap + llms
    sm = open(f'{OUT}/sitemap.xml').read()
    if 'ai-agents-vs-chatgpt' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{DOMAIN}/insights/ai-agents-vs-chatgpt</loc><lastmod>2026-10-12</lastmod></url>\n</urlset>')
        open(f'{OUT}/sitemap.xml', 'w').write(sm)
    ll = open(f'{OUT}/llms.txt').read()
    if 'ai-agents-vs-chatgpt' not in ll:
        ll = ll.replace('## Insights\n', f'## Insights\n- [AI agents vs ChatGPT for small business]({DOMAIN}/insights/ai-agents-vs-chatgpt): how a business second brain differs from a chat app on memory, tasks and autonomy\n')
        ll = ll.replace('Owners can delegate jobs', 'Unlike a chat app such as ChatGPT or Claude, it remembers the whole business, works inside the client\'s own tools and starts jobs on its own. Owners can delegate jobs')
        open(f'{OUT}/llms.txt', 'w').write(ll)
    t = json.load(open(_os.path.join(_B, 'og_titles.json')))
    t['ai-agents-vs-chatgpt'] = "AI agents vs ChatGPT: what's the difference?"
    json.dump(t, open(_os.path.join(_B, 'og_titles.json'), 'w'), ensure_ascii=False, indent=1)
