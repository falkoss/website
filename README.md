# falkOSS – website

One static page for **falkOSS – Falcon Lake Open Source Software**: no build step, no framework, no external
resources (no fonts, scripts or embeds from other servers), no cookies, no tracking.

| Path | What |
|---|---|
| `index.html`, `style.css` | the one page (English) |
| `impressum.html`, `datenschutz.html` | legal pages (German) – **drafts with placeholders**, fill in before going public |
| `assets/` | favicon, icons, lockup, mark, social preview, web manifest – **copies** of `web/` from [falkoss/brand](https://github.com/falkoss/brand) |
| `assets/projects/` | project icons (copied from each project's brand) |

Preview locally:

```sh
python3 -m http.server 8000
```

After a design change, regenerate the brand kit in `falkoss/brand` and copy its head assets here:

```sh
python3 ../brand/generate.py && cp -R ../brand/web/. assets/
```

Licence: the site's code is **AGPL-3.0-or-later** (`LICENSE`). The files in `assets/` from falkoss/brand are under
CC BY-ND 4.0 (the project icons under their projects' brand licences); the brand itself (logo, name, marks) is not
covered by any licence – see falkoss/brand.

## Publishing

GitHub Pages, deployed by `.github/workflows/pages.yml` on every push to `main` (only the public files are
copied into the artifact – not `README.md` or the workflow). Free organisations can publish Pages only from
**public** repositories, so the repo goes public together with the site.

One-time setup:

1. Repo → Settings → Pages → Source: **GitHub Actions**; Custom domain: `falkoss.org`; then **Enforce HTTPS**.
2. DNS at IONOS for `falkoss.org` – replace the IONOS defaults:
   - `A @` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA @` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `CNAME www` → `falkoss.github.io`
   - keep MX/SPF (mail) untouched; the Pages domain verification TXT is already in place.
3. `falkoss.com`, `.de`, `.dev`: IONOS redirect **301** to `https://falkoss.org` – these need an SSL certificate at
   IONOS too (`.dev` is HTTPS-only in every browser, HSTS preload).
