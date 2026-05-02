# Webcam Saint-Malo

A minimal static site that displays **4 YouTube webcams in a 2×2 grid**, optimized for TVs, large screens, and mobile devices.

🔗 **[Live site](https://hrialan.github.io/webcam-saint-malo/)**

---

## Features

- 4 live YouTube webcams in a responsive 2×2 grid
- Zero JavaScript at runtime — pure static HTML + CSS
- Fullscreen layout, dark theme, no UI clutter
- Mobile-friendly stacked layout
- Webcam IDs are configurable via **GitHub Actions Variables** — no code changes required to swap a webcam
- Automatic build & deploy to GitHub Pages on every push to `main`

---

## Tech stack

- [Astro 5](https://astro.build) — static site generator
- Plain CSS (no framework)
- GitHub Actions → GitHub Pages

---

## Configuration: changing the webcams

The 4 webcam IDs are read at **build time** from environment variables. Each variable holds only the YouTube video ID — the part after `watch?v=` in the URL.

| Variable | Position |
| --- | --- |
| `YOUTUBE_VIDEO_TOP_LEFT_ID` | top-left |
| `YOUTUBE_VIDEO_TOP_RIGHT_ID` | top-right |
| `YOUTUBE_VIDEO_BOTTOM_LEFT_ID` | bottom-left |
| `YOUTUBE_VIDEO_BOTTOM_RIGHT_ID` | bottom-right |

### In production (GitHub Pages)

1. Open the repository on GitHub → **Settings → Secrets and variables → Actions → Variables**.
2. Create the 4 variables above with the corresponding YouTube IDs.
3. Trigger a rebuild:
   - push any commit to `main`, **or**
   - go to **Actions → Build & Deploy → Run workflow** (manual trigger).

The site rebuilds and redeploys automatically; no code changes are needed to swap a webcam.

### In local development

Copy `.env.example` to `.env.local` and fill in IDs:

```bash
cp .env.example .env.local
```

```dotenv
YOUTUBE_VIDEO_TOP_LEFT_ID=VNOV8KgGR0c
YOUTUBE_VIDEO_TOP_RIGHT_ID=p6nAlz4_bdI
YOUTUBE_VIDEO_BOTTOM_LEFT_ID=OzYp4NRZlwQ
YOUTUBE_VIDEO_BOTTOM_RIGHT_ID=jfKfPfyJRdk
```

`.env.local` is git-ignored.

---

## Local development

```bash
npm install
npm run dev          # http://localhost:4321/webcam-saint-malo/
npm run build        # build to dist/
npm run preview      # preview the production build
```

---

## Project structure

```
.
├── .github/workflows/
│   └── deploy.yml             # CI/CD: build & deploy to GitHub Pages
├── public/
│   └── favicon/               # Favicons + web manifest (served as-is)
├── src/
│   ├── components/
│   │   ├── WebcamFrame.astro  # Single iframe wrapper
│   │   └── WebcamGrid.astro   # 2×2 grid layout
│   ├── layouts/
│   │   └── Layout.astro       # HTML head, meta, GA
│   ├── pages/
│   │   └── index.astro        # Reads env vars, renders the grid
│   └── styles/
│       └── global.css
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

---

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which:

1. Installs dependencies (`npm ci`)
2. Builds the site, injecting the 4 `YOUTUBE_VIDEO_*_ID` GitHub Actions Variables
3. Uploads `dist/` as a Pages artifact
4. Deploys to GitHub Pages

The workflow can also be triggered manually from the **Actions** tab.

> **First-time setup:** in the repository **Settings → Pages**, set **Source = GitHub Actions** (instead of "Deploy from a branch").

---

© Hugo R.
