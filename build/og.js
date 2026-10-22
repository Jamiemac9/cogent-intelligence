const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const R = path.resolve(__dirname, '..');
const F = path.join(__dirname, 'node_modules') + '/';
const titles = JSON.parse(fs.readFileSync(path.join(__dirname, 'og_titles.json'), 'utf8'));
const esc = (s) => s.replace(/&amp;/g,'&').replace(/[&<>]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROME_PATH || undefined});
  const p = await b.newPage({viewport:{width:1200,height:630}});
  for (const [key, title] of Object.entries(titles)) {
    const scene = R + '/site/assets/scenes/' + key + '.svg';
    if (!fs.existsSync(scene)) continue;
    const html = `<!doctype html><html><head><style>
@font-face{font-family:Archivo;src:url(file://${F}@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2) format('woff2');font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:Mono;src:url(file://${F}@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2)}
@font-face{font-family:Inst;src:url(file://${F}@fontsource/instrument-sans/files/instrument-sans-latin-500-normal.woff2)}
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#0B0A0A;position:relative;overflow:hidden;font-family:Inst}
.sc{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9}
.fade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,10,10,.97) 0%,rgba(11,10,10,.88) 42%,rgba(11,10,10,.2) 75%,rgba(11,10,10,0))}
.t{position:absolute;left:64px;top:60px;bottom:60px;width:640px;display:flex;flex-direction:column;justify-content:space-between}
.brand{display:flex;align-items:center;gap:14px;font-family:Archivo;font-weight:800;font-stretch:125%;font-size:26px;letter-spacing:.02em;color:#F1EBE3}
.brand img{height:46px}.brand small{font:500 12px Mono;letter-spacing:.2em;color:#7A7268;padding-left:12px;border-left:1px solid #333}
h1{font-family:Archivo;font-weight:650;font-stretch:106%;font-size:${title.length>60?50:58}px;line-height:1.03;letter-spacing:-.02em;color:#F1EBE3}
.k{font:500 15px Mono;letter-spacing:.18em;text-transform:uppercase;color:#FFB27C;margin-bottom:18px}
.u{font:500 17px Mono;color:#A69E94;letter-spacing:.04em}.u b{color:#FF7A2F;font-weight:500}
</style></head><body><img class="sc" src="file://${scene}"><div class="fade"></div>
<div class="t"><div class="brand"><img src="file://${R}/site/assets/brand/cogent-mark.png">COGENT<small>INTELLIGENCE</small></div>
<div><p class="k">AI agents · Second brain</p><h1>${esc(title)}</h1></div>
<p class="u">cogentintelligence.co.uk <b>·</b> Free 30-min call</p></div></body></html>`;
    fs.writeFileSync(__dirname + '/og.html', html);
    await p.goto('file://' + __dirname + '/og.html'); await p.waitForTimeout(250);
    await p.screenshot({ path: R + '/site/assets/og/' + key + '.jpg', type: 'jpeg', quality: 86 });
  }
  await b.close();
})();
