"""Generate per-page scene illustrations (SVG) in the Cogent copper style: contour field, network motif, glyph tile, live UI cards."""
import os as _os
_B = _os.path.dirname(_os.path.abspath(__file__))
_R = _os.path.dirname(_B)
import math, os, re, random, html as H
from industries_data import I

ICONS = _os.path.join(_B, 'node_modules', '@tabler', 'icons', 'icons', 'outline')
OUT = _os.path.join(_R, 'site', 'assets', 'scenes')
e = lambda s: H.escape(str(s), quote=False)

ICON = {'trades': 'tools', 'estate-agents': 'home-search', 'property-management': 'building-community', 'supported-housing': 'home-heart',
        'accountants': 'calculator', 'solicitors': 'scale', 'architects': 'ruler-measure', 'clinics': 'dental', 'fitness': 'barbell',
        'recruitment': 'users-group', 'cleaning': 'spray', 'admin': 'inbox', 'surveyors': 'home-bolt', 'compliance-consultants': 'fire-extinguisher',
        'renewables': 'solar-panel', 'brokers': 'shield-check', 'training-providers': 'school', 'venues': 'glass-champagne',
        'garages': 'car-garage', 'agencies': 'speakerphone', 'second-brain': 'brain', 'find-your-peak': 'chart-bar', 'approvals-first': 'circle-check',
        'birmingham': 'map-pin', 'ai-agents-vs-chatgpt': 'message-chatbot', 'home': 'brain', 'industries': 'building-community'}
STATUS = [('Done', '#9FE3B4'), ('Needs your OK', '#FFB27C'), ('Logged', '#C4B5FF')]
ACCENTS = ['#C4B5FF', '#8FE6DE', '#FFB27C']

def icon_body(name):
    s = open(f'{ICONS}/{name}.svg').read()
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    return re.sub(r'<path stroke="none" d="M0 0h24v24H0z" fill="none"\s*/>', '', inner)

def contour(cx, cy, rng, n=10):
    out = []
    ph = [rng.uniform(0, 6.28) for _ in range(4)]
    for k in range(n):
        r0 = 70 + k * 58
        pts = []
        for t in range(0, 361, 6):
            a = math.radians(t)
            r = r0 * (1 + .12 * math.sin(3 * a + ph[0] + k * .3) + .07 * math.sin(5 * a + ph[1]) + .05 * math.cos(2 * a + ph[2] + k * .2))
            pts.append((cx + r * math.cos(a) * 1.35, cy + r * math.sin(a)))
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'
        op = max(.08, .62 - k * .055)
        col = '#FF7A2F' if k < 4 else '#B8A99A'
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="{1.6 if k < 3 else 1.1}"/>')
    return ''.join(out)

def flow_lines(rng, n=14):
    out = []
    for i in range(n):
        y0 = rng.uniform(-60, 960); amp = rng.uniform(30, 120); f = rng.uniform(.002, .005); p = rng.uniform(0, 6.28); tilt = rng.uniform(-.25, .25)
        pts = [(x, y0 + tilt * x + amp * math.sin(f * x + p) + 25 * math.sin(.011 * x + p * 2)) for x in range(-40, 1661, 40)]
        d = 'M' + ' L'.join(f'{x:.0f} {y:.1f}' for x, y in pts)
        out.append(f'<path d="{d}" fill="none" stroke="#DCD5CC" stroke-opacity="{rng.uniform(.05, .13):.2f}" stroke-width="1"/>')
    return ''.join(out)

def network(cx, cy, rng):
    nodes = []
    for k in range(11):
        a = rng.uniform(0, 6.28); r = rng.uniform(170, 330)
        nodes.append((cx + r * math.cos(a) * 1.25, cy + r * math.sin(a) * .9))
    lines, dots = [], []
    for i, (x, y) in enumerate(nodes):
        near = sorted(range(len(nodes)), key=lambda j: (nodes[j][0] - x) ** 2 + (nodes[j][1] - y) ** 2)[1:3]
        for j in near:
            if j > i:
                lines.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{nodes[j][0]:.0f}" y2="{nodes[j][1]:.0f}"/>')
        if i % 3 == 0:
            lines.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{cx:.0f}" y2="{cy:.0f}" stroke-dasharray="3 7"/>')
        dots.append(f'<circle class="tw" style="animation-delay:-{i * .7:.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{rng.choice([3, 3.5, 4.5])}"/>')
    return f'<g stroke="#FF9A5C" stroke-opacity=".32" stroke-width="1.2">{"".join(lines)}</g><g fill="#FFB27C">{"".join(dots)}</g>'

def card(x, y, label, value, desc, status, accent, delay, w=430):
    st, sc = status
    sw = 18 + len(st) * 9.2
    return f'''<g class="fl" style="animation-delay:{delay}s"><g transform="translate({x} {y})">
<rect width="{w}" height="104" rx="22" fill="#141211" fill-opacity=".86" stroke="#F1EBE3" stroke-opacity=".14"/>
<rect x="1" y="1" width="{w - 2}" height="102" rx="21" fill="url(#cardsheen)"/>
<circle cx="30" cy="34" r="6" fill="{accent}"/><circle cx="30" cy="34" r="12" fill="{accent}" fill-opacity=".18"/>
<text x="50" y="40" font-family="JetBrains Mono, ui-monospace, Menlo, monospace" font-size="15" letter-spacing="2.4" fill="#A69E94">{e(label.upper())}</text>
<text x="26" y="80"><tspan font-family="Archivo, Instrument Sans, Helvetica Neue, Arial, sans-serif" font-weight="700" font-size="30" fill="#F1EBE3">{e(value)}</tspan><tspan dx="14" font-family="Instrument Sans, Helvetica Neue, Arial, sans-serif" font-size="19" fill="#DCD5CC">{e(desc)}</tspan></text>
<rect x="{w - sw - 20}" y="20" width="{sw}" height="28" rx="14" fill="{sc}" fill-opacity=".14" stroke="{sc}" stroke-opacity=".5"/>
<text x="{w - sw / 2 - 20}" y="39" text-anchor="middle" font-family="JetBrains Mono, ui-monospace, Menlo, monospace" font-size="13" fill="{sc}">{e(st)}</text>
</g></g>'''

LAYOUTS = [
    # glyph at (x,y); cards [(x,y)]
    dict(g=(470, 450), hot=(470, 450), cards=[(830, 214), (900, 398), (800, 582)]),
    dict(g=(800, 430), hot=(800, 430), cards=[(150, 210), (1030, 300), (330, 600)]),
    dict(g=(1130, 450), hot=(1130, 450), cards=[(170, 230), (240, 414), (130, 598)]),
]

TALL = dict(g=(500, 330), hot=(500, 330), cards=[(285, 570), (285, 700)])

def scene(key, cards, seed, layout, W=1600, Hh=900):
    rng = random.Random(seed)
    L = TALL if layout == 'tall' else LAYOUTS[layout % 3]
    gx, gy = L['g']; hx, hy = L['hot']
    acc = ACCENTS[seed % 3]
    H_ = Hh
    cards_svg = ''.join(card(x, y, *cards[k], STATUS[k], [acc, '#FF7A2F', '#9FE3B4'][k], -k * 1.7) for k, (x, y) in enumerate(L['cards']) if k < len(cards))
    body = icon_body(ICON[key])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_}" preserveAspectRatio="xMidYMid slice" role="img">
<style>
.fl{{animation:fl 7s ease-in-out infinite}} @keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
.tw{{animation:tw 4.2s ease-in-out infinite}} @keyframes tw{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.pulse{{animation:pu 5s ease-in-out infinite;transform-origin:{gx}px {gy}px}} @keyframes pu{{0%,100%{{opacity:.55;transform:scale(1)}}50%{{opacity:.9;transform:scale(1.06)}}}}
@media (prefers-reduced-motion:reduce){{.fl,.tw,.pulse{{animation:none}}}}
</style>
<defs>
<radialGradient id="hot" cx="{hx / W * 100:.1f}%" cy="{hy / H_ * 100:.1f}%" r="55%"><stop offset="0" stop-color="#FF7A2F" stop-opacity=".62"/><stop offset=".45" stop-color="#7A3510" stop-opacity=".35"/><stop offset="1" stop-color="#0B0A0A" stop-opacity="0"/></radialGradient>
<radialGradient id="cool" cx="{(W - hx) / W * 100:.1f}%" cy="85%" r="45%"><stop offset="0" stop-color="{acc}" stop-opacity=".16"/><stop offset="1" stop-color="#0B0A0A" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#FF7A2F" stop-opacity=".55"/><stop offset="1" stop-color="#FF7A2F" stop-opacity="0"/></radialGradient>
<linearGradient id="cardsheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F1EBE3" stop-opacity=".06"/><stop offset=".5" stop-color="#F1EBE3" stop-opacity="0"/></linearGradient>
<linearGradient id="tile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A211C"/><stop offset="1" stop-color="#120F0E"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFB27C"/><stop offset=".5" stop-color="#FF7A2F" stop-opacity=".4"/><stop offset="1" stop-color="#8C6BFF" stop-opacity=".5"/></linearGradient>
</defs>
<rect width="{W}" height="{H_}" fill="#0E0C0B"/>
<rect width="{W}" height="{H_}" fill="url(#hot)"/><rect width="{W}" height="{H_}" fill="url(#cool)"/>
{flow_lines(rng)}
{contour(hx, hy, rng)}
{network(gx, gy, rng)}
<circle class="pulse" cx="{gx}" cy="{gy}" r="230" fill="url(#halo)"/>
<g transform="translate({gx - 120} {gy - 120})">
<rect width="240" height="240" rx="52" fill="url(#tile)" stroke="url(#rim)" stroke-width="2.5"/>
<rect x="10" y="10" width="220" height="110" rx="44" fill="#F1EBE3" fill-opacity=".04"/>
<g transform="translate(48 48) scale(6)" fill="none" stroke="#FFB27C" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round">{body}</g>
</g>
<circle cx="{gx}" cy="{gy}" r="4" fill="#FF7A2F"/>
{cards_svg}
</svg>'''

EXTRA = {
    'second-brain': dict(seed=7, cards=[('Remembers', 'Priya', 'prefers Thursday surveys'), ('Knows', 'v4', 'price list and service area'), ('Briefs', '07:00', 'Monday briefing ready')]),
    'find-your-peak': dict(seed=21, cards=[('Peak', '18', 'Replying to enquiries'), ('Next', '10', 'Writing quotes'), ('Then', '9', 'Chasing invoices')]),
    'approvals-first': dict(seed=43, cards=[('Approvals', 'ON', 'customer and money jobs'), ('Owner', '07:12', 'approved with one tap'), ('Learning', '3', 'corrections remembered')]),
    'home': dict(seed=3, cards=[('Delegated', '3 jobs', 'from one voice note'), ('Briefing', '07:00', 'Monday numbers ready'), ('Memory', 'Priya', 'prefers Thursdays')]),
    'industries': dict(seed=13, cards=[('Trades', '23:47', 'Enquiry answered'), ('Lettings', '14 days', 'EICR booked'), ('Accounts', '27', 'clients chased')]),
    'ai-agents-vs-chatgpt': dict(seed=91, cards=[('Memory', 'Every customer', 'shared by every agent'), ('Tasks', 'End to end', 'inside your own tools'), ('Autonomy', '24/7', 'starts without being asked')]),
    'birmingham': dict(seed=58, cards=[('Mapping', 'Solihull', 'half-day session on site'), ('Live', '14 days', 'first agent working'), ('Covering', 'West Mids', 'Birmingham to Coventry')]),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    for i, d in enumerate(I):
        cards = [(d['agents'][k][0], b, t) for k, (b, t) in enumerate(d['chips'])]
        open(f'{OUT}/{d["slug"]}.svg', 'w').write(scene(d['slug'], cards, d['seed'], i))
    for k, (key, v) in enumerate(EXTRA.items()):
        open(f'{OUT}/{key}.svg', 'w').write(scene(key, v['cards'], v['seed'], k + 1))
    v = EXTRA['second-brain']
    open(f'{OUT}/second-brain-tall.svg', 'w').write(scene('second-brain', v['cards'], v['seed'], 'tall', 1000, 1100))
    return len(I) + len(EXTRA)

if __name__ == '__main__':
    print(build())
