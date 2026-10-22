# Cogent Intelligence website

The static site for [cogentintelligence.co.uk](https://cogentintelligence.co.uk), hosted on Cloudflare Pages.

## Layout

| Folder | What it is |
|---|---|
| `site/` | **The live website.** Everything Cloudflare publishes. Plain HTML, CSS and JS, no build step needed. |
| `build/` | The Python scripts that generate `site/` (industry pages, pictures, SEO, legal pages). Only needed when regenerating pages in bulk. |
| `build/source/` | The original hand-built pages the scripts start from. |

## Cloudflare Pages settings

Connect this repository to a Cloudflare Pages project with:

- **Production branch:** `main`
- **Framework preset:** None
- **Build command:** *(leave empty)*
- **Build output directory:** `site`

Every push to `main` then deploys automatically.

## Regenerating the site (optional)

```bash
cd build
npm install @tabler/icons            # icons used by the scene pictures
python3 build.py                     # rebuilds site/
npm install playwright @fontsource-variable/archivo @fontsource/jetbrains-mono @fontsource/instrument-sans
node og.js                           # re-renders the link-preview images in site/assets/og
```

Small text edits can be made directly in `site/`, but note that a full rebuild overwrites `site/` from the scripts.

## Still to connect

- `site/assets/site.js`: set `SIGNUP_ACTION` to your email tool's form URL (e.g. MailerLite) so course sign-ups go straight to the list.
