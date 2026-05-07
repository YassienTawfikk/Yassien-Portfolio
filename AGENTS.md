# AGENTS.md — Portfolio Project (V2)

> **Scope:** This file is the authoritative context document for AI-assisted development on this project.
> It describes the architecture, conventions, known issues, and a prioritized improvement backlog.
> Always read this file before making any changes to templates, scripts, CSS, JS, or content files.

---

## 1. Project Identity

| Field | Value |
|---|---|
| Project | Personal portfolio — static site (V2) |
| Live URL | https://ytawfik-portfolio.netlify.app |
| Hosting | Netlify (static) |
| Build system | Python 3 + Jinja2 |
| Deployment trigger | Git push to main |

---

## 2. Repository Structure

```
/
├── content/                  # All site data — edit these to update content
│   ├── about.json
│   ├── contact.json
│   ├── credentials.json
│   ├── education.json
│   ├── home.json
│   ├── projects.json
│   ├── skills.json
│   └── society.json
│
├── scripts/
│   ├── build.py              # Main build orchestrator — runs at deploy time
│   └── server.py             # Local dev server (serves /public on port 8000)
│
├── static/
│   └── sw.js                 # Service Worker template — PRECACHE_URLS injected by build.py
│
├── theme/
│   ├── static/
│   │   ├── css/
│   │   │   ├── base/         # global.css, normalize.css
│   │   │   ├── components/   # modals.css, preloader.css
│   │   │   └── pages/        # one file per page
│   │   └── js/
│   │       ├── core/         # preloader.js, navbar.js, pwa.js
│   │       ├── pages/        # one file per page
│   │       └── utils/        # gallery_callbacks.js, modal_utils.js, navbar_toggle.js
│   └── templates/
│       ├── base.html         # Master layout — all pages extend this
│       ├── components/       # navbar.html, footer_nav.html, project_card.html
│       └── *.html            # One template per page
│
├── netlify.toml              # Build config + HTTP headers
├── vercel.json               # Legacy — not the active deployment target
├── requirements.txt          # Jinja2==3.1.2
└── package.json              # npm aliases only (build, start)
```

---

## 3. Architecture Mental Model

```
BUILD TIME (Netlify CI)
  content/*.json
       │
       ▼
  scripts/build.py  (Jinja2 render + SW precache injection)
       │
       ▼
  /public/          ← static HTML + CSS + JS + SW
       │
       ▼
  Netlify CDN Edge  ← serves to browser
       │
  ┌────┴────────────────────────┐
  │                             │
Service Worker              EmailJS API
(client-side cache)       (contact form only)
```

There is **no backend, no database, no runtime server**. Every page is pre-rendered.
The only outbound network calls from the browser are:
- External CDNs (Bootstrap, FontAwesome, pdf.js, Google Fonts, EmailJS)
- Image hosts (postimg.cc, Cloudinary, GitHub user-content)
- EmailJS API (contact form submissions only)

---

## 4. Build System Details

### How `scripts/build.py` works

1. Loads all `content/*.json` into a `site_data` dict (key = filename without extension)
2. Calls `setup_directories(site_data)` which:
   - Wipes and recreates `/public`
   - Copies `theme/static/css`, `js`, `images`, `documents`
   - Reads `static/sw.js`, injects the auto-generated `PRECACHE_URLS` list, writes to `/public/sw.js`
3. Processes `projects.json` — maps `project.domain.{name,icon}` → flat `project.domain_name` / `project.domain_icon` for template compatibility
4. Splits projects into `featured_projects` (those with `live_demo`) and `categories` dict
5. Renders each page template with the full `site_data` context
6. Outputs `.html` files to `/public`

### Adding a new page

1. Create `content/newpage.json`
2. Create `theme/templates/newpage.html` extending `base.html`
3. Add `('newpage.html', 'newpage.html')` to the `pages` list in `build.py`
4. Add a `<li>` entry in `theme/templates/components/navbar.html`
5. Add a footer nav `{% with %}` block at the bottom of the preceding page template

### Adding a new project

Edit `content/projects.json` only. No template or script changes needed.
Required fields: `title`, `short_description`, `overview_image`, `tech_stack`, `domain` (`name` + `icon`), `category`, `year`.
Optional: `github_link`, `live_demo`, `video_demo`, `highlights`, `long_description`, `order`.

---

## 5. CSS & JS Conventions

### CSS naming rules

- Page-scoped styles live in `theme/static/css/pages/<pagename>.css`
- Component styles live in `theme/static/css/components/`
- Base/global tokens live in `theme/static/css/base/global.css` as CSS custom properties
- Utility classes for typography: `head-font` (Poppins 800), `body-font` (Roboto 100)
- Unified page title: always use `<span class="unified-page-title title-{left|center} underline-{Npx|80percent}">` — never create new title styles
- Button system: always use `std-button` + `std-button-{primary|secondary}` + optionally `std-button-lg` — never create one-off button styles

### JS conventions

- All JS is vanilla ES6+, no build step, no bundler
- One JS file per page in `theme/static/js/pages/`
- Shared utilities go in `theme/static/js/utils/`
- All scripts are deferred via placement at end of `{% block scripts %}` in each template
- The `base.html` always loads: `bootstrap.bundle.min.js`, `preloader.js`, `navbar.js`, `navbar_toggle.js`, `modal_utils.js`

---

## 6. Known Issues & Active Bug Register

### SECURITY — Critical

**SEC-001: EmailJS public key committed to repository**
- File: `content/contact.json` → `form_configuration.public_key`
- Risk: Anyone with repo access (public or leaked) can exhaust your EmailJS monthly quota or send spoofed emails appearing to originate from your service
- Fix: Restrict the key to your domain in the EmailJS dashboard. Migrate to Netlify Forms (see Fix Backlog #1)

**SEC-002: Unsanitized `videoUrl` injected into iframe `srcdoc`**
- File: `theme/static/js/pages/projects.js` lines ~14–26
- The string `${videoUrl}` is interpolated directly into an HTML string used as `iframe.srcdoc`
- If a `video_demo` URL in `projects.json` ever contains `</video><script>`, it executes in page context
- Fix: Validate `videoUrl` is a GitHub `user-attachments` URL before use; use `DOMParser` or explicit attribute setting instead of raw HTML string construction

**SEC-003: No Subresource Integrity (SRI) on external scripts**
- Files: `theme/templates/base.html`, `theme/templates/home.html`
- External scripts (Bootstrap, FontAwesome, pdf.js) are loaded without `integrity` attributes
- A compromised cdnjs serves arbitrary code with full DOM access
- Fix: Add `integrity="sha384-..."` + `crossorigin="anonymous"` to every external `<script>` and `<link rel="stylesheet">`

**SEC-004: Missing security headers**
- File: `netlify.toml`
- No `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, or `Permissions-Policy`
- Fix: Add headers block in `netlify.toml` (see Fix Backlog #4)

---

### PERFORMANCE — High Priority

**PERF-001: `Cache-Control: no-cache` applied to ALL routes including immutable assets**
- File: `netlify.toml`
- The current wildcard header forces revalidation on every request for CSS, JS, and images — completely negating CDN edge caching and SW benefits for static assets
- Fix: Split headers by asset type (HTML = no-cache; CSS/JS/images = immutable with hash-busting via versioned filenames)

**PERF-002: ~8 external CDN roundtrips block first render**
- Files: `theme/templates/base.html`
- Bootstrap CSS, FontAwesome CSS, Google Fonts, Bootstrap JS, pdf.js, EmailJS — all loaded from external origins
- Fix: Self-host Bootstrap and FontAwesome in `theme/static/`. Subset Google Fonts. Load pdf.js and EmailJS only on the pages that need them (already done for EmailJS, not for pdf.js)

**PERF-003: No image optimization**
- All images are raw JPG/PNG hosted on postimg.cc with no WebP conversion, no responsive `srcset`, no intrinsic size attributes (`width`/`height`)
- This is likely the primary LCP bottleneck on all pages
- Fix: At build time, download images and convert to WebP with `Pillow`; generate multiple sizes; emit `<img srcset="...">` from templates. Add `width` and `height` attributes to eliminate layout shift (CLS)

**PERF-004: pdf.js loaded on every page via `home.html`**
- The pdf.js script (~1.5 MB) is loaded unconditionally on the home page even before the Resume modal is opened
- Fix: Lazy-load pdf.js only when the Resume modal `show.bs.modal` event fires (dynamic `import()` or deferred script injection)

---

### CODE QUALITY — Medium Priority

**DRY-001: Gallery logic triplicated**
- Files: `theme/static/js/pages/credentials.js`, `theme/static/js/pages/society.js`, `theme/static/js/utils/gallery_callbacks.js`
- The `navigate()` function, animation logic (`is-switching` → `anim-next`/`anim-prev`), and keyboard handling are copy-pasted verbatim across all three files
- A bug fix must be applied in three places; current `gallery_callbacks.js` is also a Dash leftover that is never called
- Fix: Create `theme/static/js/utils/gallery.js` as a reusable `Gallery` class (see Fix Backlog #8)

**DRY-002: CSS animation keyframes duplicated**
- `slideInRight` and `slideInLeft` keyframes are defined identically in `credentials.css`, `society.css`, and `modals.css`
- Fix: Consolidate into `theme/static/css/components/modals.css` only; remove from page-specific files

**DRY-003: `build.py` is a monolith**
- Single function handles directory setup, asset copying, SW generation, data transformation, and page rendering
- Makes unit testing impossible; breaks separation of concerns
- Fix: Extract into `scripts/sw_builder.py` and `scripts/transform.py` (see Fix Backlog #9)

**DRY-004: `gallery_callbacks.js` is dead code**
- File: `theme/static/js/utils/gallery_callbacks.js`
- This is a leftover from the previous Dash-based architecture. It references `dash_clientside` which does not exist in the current static build
- Fix: Delete the file; ensure no template references it

---

### RELIABILITY — Medium Priority

**REL-001: No image fallback on broken external URLs**
- All `<img>` tags in templates have no `onerror` handler
- postimg.cc and Cloudinary have no SLA — any image 404 silently shows a broken image icon
- Fix: Add `onerror="this.style.opacity='0'"` or a placeholder fallback to all `<img>` tags in Jinja2 templates

**REL-002: SW precache list grows unboundedly**
- `build.py` adds every project image to the SW precache on install
- As the project list grows, the SW install payload increases proportionally, increasing install failure probability on slow connections
- Fix: Limit precache to core UI assets only; cache project images lazily via the fetch handler on first visit

**REL-003: `vercel.json` present but Netlify is the active platform**
- Causes confusion about the deployment target
- Fix: Either remove `vercel.json` or add a comment explaining it is retained for fallback use

---

### OBSERVABILITY — Low Priority

**OBS-001: Zero production error visibility**
- No error tracking, no analytics, no alerting
- A broken deployment is invisible until a user reports it
- Fix: Add Sentry (JS error tracking, free tier) via single script in `base.html`; add Plausible or Netlify Analytics

---

## 7. Fix Backlog (Prioritized)

### Tier 1 — Do Immediately (Security & Correctness)

**Fix #1 — Migrate contact form from EmailJS to Netlify Forms**
- Remove `form_configuration` from `content/contact.json`
- Replace the `<div id="zen-contact-form">` with a real `<form>` element with `netlify` attribute in `contact.html`
- Delete EmailJS SDK `<script>` tag from `contact.html`
- Rewrite `theme/static/js/pages/contact.js` to use `fetch()` POST to Netlify's form endpoint
- No exposed credentials, no monthly limits, spam filtering included

**Fix #2 — Sanitize video URL injection in `projects.js`**
```javascript
// BEFORE (vulnerable)
const videoHtml = `...<video src="${videoUrl}" ...>...`;

// AFTER (safe)
const ALLOWED_VIDEO_ORIGIN = 'https://github.com/user-attachments/assets/';
if (!videoUrl.startsWith(ALLOWED_VIDEO_ORIGIN)) return;
const video = document.createElement('video');
video.src = videoUrl;
video.controls = true;
video.autoplay = true;
video.loop = true;
```

**Fix #3 — Add SRI hashes to all external resources in `base.html`**
- Use https://www.srihash.org/ to generate hashes for Bootstrap CSS/JS and FontAwesome
- Pattern: `<script src="..." integrity="sha384-..." crossorigin="anonymous">`

**Fix #4 — Add security headers in `netlify.toml`**
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://cdn.emailjs.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https: blob:; connect-src 'self' https://api.emailjs.com; frame-src 'none';"
```

---

### Tier 2 — Fix This Sprint (Performance & Cache)

**Fix #5 — Split Cache-Control headers by asset type in `netlify.toml`**
```toml
# HTML pages — always fresh
[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "no-cache, no-store, must-revalidate"

# Versioned static assets — cache forever
[[headers]]
  for = "/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```
- Note: To make this safe, asset filenames must include a content hash (e.g. `global.abc123.css`). Add a simple hash-suffix step to `build.py` when copying static assets, then update template `<link>` hrefs accordingly. Alternatively use Netlify's asset optimization.

**Fix #6 — Self-host Bootstrap and FontAwesome**
- Download Bootstrap 5.3 CSS + JS bundle to `theme/static/css/vendors/` and `theme/static/js/vendors/`
- Download FontAwesome 6.4 webfonts + CSS to same structure
- Remove CDN `<link>` and `<script>` tags from `base.html`, replace with local paths
- Eliminates 4 external roundtrips, enables SRI, removes cdnjs availability dependency

**Fix #7 — Lazy-load pdf.js only on modal open**

In `theme/templates/home.html`, replace the static `<script>` tags with:
```javascript
document.getElementById('resume-modal').addEventListener('show.bs.modal', function handler() {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    script.onload = () => initPdfViewer();
    document.head.appendChild(script);
    this.removeEventListener('show.bs.modal', handler); // load once
});
```

---

### Tier 3 — Refactor (Code Quality & Maintainability)

**Fix #8 — Consolidate gallery logic into `gallery.js`**

Create `theme/static/js/utils/gallery.js`:
```javascript
export class Gallery {
    constructor({ modalElementId, imageElementId, prevBtnId, nextBtnId, triggerSelector, srcAttribute = 'data-src' }) { ... }
    open(index) { ... }
    navigate(direction) { ... }  // -1 or 1
    _animateImage(direction) { ... }
    _bindKeyboard() { ... }
}
```
- Delete `gallery_callbacks.js` entirely (dead Dash code)
- Rewrite `credentials.js` and `society.js` to instantiate `Gallery` with their specific IDs
- Consolidate `slideInRight`/`slideInLeft` keyframes into `modals.css` only, remove from `credentials.css` and `society.css`

**Fix #9 — Decompose `build.py` into focused modules**

```
scripts/
├── build.py           # Orchestrator only — calls the modules below
├── transform.py       # Data normalization (domain mapping, project categorization)
├── sw_builder.py      # SW precache list generation and injection
└── server.py          # Unchanged
```

`build.py` becomes:
```python
from transform import process_site_data
from sw_builder import inject_service_worker

site_data = load_data()
site_data = process_site_data(site_data)
setup_directories()
inject_service_worker(site_data)
render_pages(site_data)
```

**Fix #10 — Add `onerror` fallback to all `<img>` tags in templates**

Add a global handler in `base.html`:
```html
<script>
  document.addEventListener('error', function(e) {
      if (e.target.tagName === 'IMG') e.target.style.opacity = '0';
  }, true);
</script>
```
This handles all images globally without modifying individual templates.

**Fix #11 — Limit SW precache to core UI assets only**

In `build.py` `setup_directories()`, change the precache list construction:
```python
# Only cache core shell assets — images are cached lazily via fetch handler
precache_list = [
    '/',
    '/index.html',
    '/projects.html',
    '/css/base/global.css',
    '/css/base/normalize.css',
    '/js/core/navbar.js',
    '/js/core/preloader.js',
]
# Do NOT add project/credential images to install-time precache
```

Update `static/sw.js` fetch handler to cache images lazily on first request.

---

### Tier 4 — Enhancements (Observability & Adaptability)

**Fix #12 — Add Sentry for JS error tracking**

In `theme/templates/base.html` `<head>` (before all other scripts):
```html
<script
  src="https://browser.sentry-cdn.com/7.x.x/bundle.min.js"
  integrity="sha384-..."
  crossorigin="anonymous"
></script>
<script>
  Sentry.init({ dsn: "YOUR_DSN", environment: "production" });
</script>
```

**Fix #13 — Add Plausible Analytics (privacy-friendly)**
```html
<script defer data-domain="ytawfik-portfolio.netlify.app"
  src="https://plausible.io/js/script.js"></script>
```
Add to `base.html` only when `NETLIFY_ENV == 'production'` — inject via `build.py` using an env var check.

**Fix #14 — Remove or annotate `vercel.json`**

Either delete it, or add a comment block at the top explaining its purpose:
```json
{
  "_comment": "Retained as fallback deployment config. Active platform is Netlify (netlify.toml).",
  "$schema": "...",
  ...
}
```

**Fix #15 — Add GPA correction**

`content/education.json` currently shows `"gpa": "3.4"` but the actual GPA is 3.62.
Update the value to `"3.62"`.

---

## 8. Content Schema Reference

### `projects.json` — single project object

```json
{
  "title": "string — display name",
  "short_description": "string — shown on card",
  "long_description": "string — optional, for future detail page",
  "overview_image": "URL — card thumbnail",
  "github_link": "URL | null",
  "live_demo": "URL | null — presence triggers featured section + LIVE DEMO badge",
  "video_demo": "URL | null — must be github user-attachments URL",
  "tech_stack": ["string", "..."],
  "tags": ["string", "..."],
  "highlights": ["string", "..."],
  "year": "string",
  "domain": {
    "name": "string — displayed in badge",
    "icon": "string — FontAwesome class e.g. fa-solid fa-brain"
  },
  "category": "one of: AI & Data Science | Computer Vision & Image Processing | Biomedical & Signal Processing | Web, Mobile & Software | Embedded Systems & IoT | Game Development",
  "order": "integer | null — lower = appears first within category"
}
```

### `credentials.json` — field experience item

```json
{
  "id": "exp_XXX",
  "role": "string",
  "organization": "string",
  "organizationLink": "URL | null",
  "date": "string",
  "type": "Internship | Clinical Training | Technical Training",
  "description": "string",
  "certificateImage": "URL | null",
  "github_link": "URL | null"
}
```

### `society.json` — involvement item

```json
{
  "role": "string",
  "organization": "string",
  "description": ["string", "..."],
  "image_url": "URL",
  "facebook_url": "URL | empty string",
  "instagram_url": "URL | empty string",
  "youtube_url": "URL | empty string",
  "website_url": "URL | empty string",
  "certficates": ["URL", "..."]
}
```
Note: `certficates` is a deliberate typo preserved for backward compatibility — do not rename without updating `society.html` template and `society.js`.

---

## 9. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Build the site
python3 scripts/build.py
# OR
npm run build

# Serve locally
python3 scripts/server.py
# OR
npm start

# Open http://localhost:8000
```

There is no hot-reload. After any change to templates, CSS, JS, or JSON, you must re-run `build.py` and refresh the browser.

---

## 10. Deployment

Deployment is fully automatic on push to `main` via Netlify CI. The build command is defined in `netlify.toml`:

```
pip install -r requirements.txt && python3 scripts/build.py
```

Output directory: `public/`

**Never commit the `/public` directory.** It is in `.gitignore` and is rebuilt fresh on every deploy.

To test a change in production conditions without affecting the live site, use Netlify's deploy preview feature (automatic on pull requests).

---

## 11. Constraints & Invariants

These rules must be preserved in all future changes:

1. **No backend runtime.** The site must remain fully static. All dynamic behavior must happen in the browser or at build time.
2. **No breaking the Jinja2 build.** `build.py` must exit 0 for deployment to succeed. Always test locally before pushing.
3. **Content changes go in `content/*.json` only.** Templates should never contain hardcoded content that belongs in data files.
4. **`std-button` must be used for all buttons.** Never create one-off button styles.
5. **`unified-page-title` must be used for all page headings.** Never create per-page title classes.
6. **The `domain` object in `projects.json` must always have both `name` and `icon`.** `build.py` maps them to flat keys for template compatibility.
7. **`video_demo` URLs must be GitHub `user-attachments` URLs.** Other video hosts are not supported and may introduce security issues.
