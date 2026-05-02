# Migration Plan - Webcam Saint-Malo

## Global Objective
Refactor the project to simplify the codebase, improve performance, and automate deployment via GitHub Actions with webcam URL management through environment variables.

---

## 1. Architecture & Tech Stack

### Framework Choice
- **Astro** (or lightweight alternative if preferred)
  - Reason: Modern static site generator, zero JS at runtime by default, perfect for GitHub Pages
  - Alternatives: Hugo (very lightweight, performant) or Eleventy (flexible, simple)

### Project Structure
```
webcam-saint-malo/
├── src/
│   ├── layouts/
│   │   └── Layout.astro          # Main layout
│   ├── pages/
│   │   └── index.astro           # Home page (2x2 grid)
│   ├── components/
│   │   ├── WebcamGrid.astro      # Grid component
│   │   └── WebcamFrame.astro     # Video frame component
│   └── styles/
│       └── global.css            # Global styles
├── astro.config.mjs              # Astro configuration
├── package.json
├── .github/workflows/
│   └── deploy.yml                # GitHub Actions workflow
├── public/                        # Static assets (favicons, etc)
└── README.md
```

---

## 2. Cleanup of Existing Code

### To Remove
- ❌ Delete `v2/` folder (Vite codebase)
- ❌ Remove Meteoblue dependency
- ❌ Remove obsolete built assets (`assets/`, `dist/`)
- ✅ Keep `CLAUDE.md`, `README.md`
- ✅ Delete `MIGRATION.md` (replaced by this plan)

### Files to Keep
- Favicons (copy to `public/favicon/`)
- Base project structure

---

## 3. GitHub Actions Configuration

### Environment Variables to Create
In the repository's **GitHub Actions Secrets & Variables**:
- `YOUTUBE_VIDEO_TOP_LEFT_ID` — Top-left YouTube webcam ID
- `YOUTUBE_VIDEO_TOP_RIGHT_ID` — Top-right YouTube webcam ID
- `YOUTUBE_VIDEO_BOTTOM_LEFT_ID` — Bottom-left YouTube webcam ID
- `YOUTUBE_VIDEO_BOTTOM_RIGHT_ID` — Bottom-right YouTube webcam ID

### Workflow `.github/workflows/deploy.yml`
**Triggers:**
- Push to `main` branch
- Manual trigger via `workflow_dispatch`

**Steps:**
1. Checkout repository
2. Setup Node.js (LTS version)
3. Install dependencies (`npm ci`)
4. Build site (`npm run build`) — environment variables will be injected into the build
5. Deploy to GitHub Pages (use `actions/deploy-pages@v2`)

**Example workflow structure:**
```yaml
name: Build & Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - run: npm ci
      - run: npm run build
        env:
          YOUTUBE_VIDEO_TOP_LEFT_ID: ${{ vars.YOUTUBE_VIDEO_TOP_LEFT_ID }}
          YOUTUBE_VIDEO_TOP_RIGHT_ID: ${{ vars.YOUTUBE_VIDEO_TOP_RIGHT_ID }}
          YOUTUBE_VIDEO_BOTTOM_LEFT_ID: ${{ vars.YOUTUBE_VIDEO_BOTTOM_LEFT_ID }}
          YOUTUBE_VIDEO_BOTTOM_RIGHT_ID: ${{ vars.YOUTUBE_VIDEO_BOTTOM_RIGHT_ID }}
      
      - uses: actions/upload-pages-artifact@v2
        with:
          path: './dist'
      
      - uses: actions/deploy-pages@v2
```

---

## 4. Astro Codebase

### 4.1 Project Configuration (`astro.config.mjs`)
```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://hrialan.github.io/',
  base: '/webcam-saint-malo/',
  output: 'static',
});
```

### 4.2 Main Layout (`src/layouts/Layout.astro`)
```astro
---
// Head & meta tags
// - Charset UTF-8
// - Responsive viewport
// - Title: "Webcam Saint-Malo"
// - Meta description
// - Favicons (use existing favicons)
// - Google Analytics (keep GA4 tag if still used)
// - PWA meta tags (mobile-web-app-capable, apple-mobile-web-app-title, etc.)

const { title = "Webcam Saint-Malo" } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Favicons, GA, meta tags -->
  </head>
  <body>
    <slot />
  </body>
</html>
```

### 4.3 Home Page (`src/pages/index.astro`)
```astro
---
import Layout from '../layouts/Layout.astro';
import WebcamGrid from '../components/WebcamGrid.astro';

const videoIds = {
  topLeft: import.meta.env.YOUTUBE_VIDEO_TOP_LEFT_ID,
  topRight: import.meta.env.YOUTUBE_VIDEO_TOP_RIGHT_ID,
  bottomLeft: import.meta.env.YOUTUBE_VIDEO_BOTTOM_LEFT_ID,
  bottomRight: import.meta.env.YOUTUBE_VIDEO_BOTTOM_RIGHT_ID,
};
---

<Layout>
  <main>
    <WebcamGrid videos={videoIds} />
  </main>
</Layout>
```

### 4.4 WebcamGrid Component (`src/components/WebcamGrid.astro`)
```astro
---
import WebcamFrame from './WebcamFrame.astro';

interface Props {
  videos: {
    topLeft: string;
    topRight: string;
    bottomLeft: string;
    bottomRight: string;
  };
}

const { videos } = Astro.props;
---

<div class="webcam-grid">
  <WebcamFrame position="top-left" videoId={videos.topLeft} />
  <WebcamFrame position="top-right" videoId={videos.topRight} />
  <WebcamFrame position="bottom-left" videoId={videos.bottomLeft} />
  <WebcamFrame position="bottom-right" videoId={videos.bottomRight} />
</div>

<style>
  .webcam-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 10px;
    width: 100%;
    height: 100vh;
    padding: 10px;
    background-color: #000;
  }

  @media (max-width: 768px) {
    .webcam-grid {
      grid-template-columns: 1fr;
      grid-template-rows: auto auto auto auto;
      height: auto;
    }
  }
</style>
```

### 4.5 WebcamFrame Component (`src/components/WebcamFrame.astro`)
```astro
---
interface Props {
  position: string;
  videoId: string;
}

const { videoId } = Astro.props;
---

<div class="webcam-frame">
  {videoId && (
    <iframe
      width="100%"
      height="100%"
      src={`https://www.youtube.com/embed/${videoId}?autoplay=1&loop=1&playlist=${videoId}`}
      title="Webcam"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
    ></iframe>
  )}
  {!videoId && (
    <div class="error">Video not available</div>
  )}
</div>

<style>
  .webcam-frame {
    width: 100%;
    height: 100%;
    border: 2px solid #333;
    border-radius: 4px;
    overflow: hidden;
    background-color: #1a1a1a;
  }

  iframe {
    display: block;
  }

  .error {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    color: #999;
    font-size: 14px;
  }
</style>
```

### 4.6 Global Styles (`src/styles/global.css`)
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  background-color: #000;
  color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow: hidden;
}

main {
  width: 100%;
  height: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  html, body {
    overflow: auto;
  }
}
```

---

## 5. Package.json & Dependencies

### Minimal Dependencies
```json
{
  "name": "webcam-saint-malo",
  "version": "3.0.0",
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "devDependencies": {
    "astro": "^4.x.x"
  }
}
```

---

## 6. Documentation

### Update README.md
- Describe new architecture (Astro)
- Explain local setup (clone, `npm install`, `npm run dev`)
- Guide for updating YouTube IDs:
  - Via GitHub Actions Variables (production)
  - Create `.env.local` file in development: `YOUTUBE_VIDEO_TOP_LEFT_ID=xxxxx`
- Build & preview locally
- GitHub Actions workflow information
- Remove references to Meteoblue, Vite, v2/

### GitHub Actions Documentation
- Add screenshot/guide for configuring 4 variables in GitHub Actions
- Explain automatic vs manual trigger workflow

---

## 7. Performance & Accessibility Optimizations

### Performance
- ✅ Astro generates static HTML → zero unnecessary JS at runtime
- ✅ Optimized images via `astro/image` if needed
- ✅ Inline & minified CSS by default
- ✅ No heavy frameworks at runtime

### Accessibility
- ✅ `alt` or `title` on iframes
- ✅ Correct viewport meta tag
- ✅ Sufficient contrast (black background/white text)
- ✅ Focus management if interactive controls needed
- ✅ ARIA labels if necessary

### Lighthouse Target Scores
- Performance: 95+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 95+

---

## 8. Step-by-Step Execution Plan

### Phase 1: Initialization (1h)
1. [ ] Create minimal Astro structure
2. [ ] Configure `astro.config.mjs`
3. [ ] Create Layout, pages, basic components
4. [ ] Setup global styles & responsive design

### Phase 2: Variable Integration (30min)
1. [ ] Configure `import.meta.env` to read GitHub Actions variables
2. [ ] Pass YouTube IDs to components
3. [ ] Test locally with `.env.local`

### Phase 3: GitHub Actions (30min)
1. [ ] Create `.github/workflows/deploy.yml`
2. [ ] Configure 4 GitHub Actions variables
3. [ ] Test workflow locally or on test branch

### Phase 4: Cleanup & Documentation (30min)
1. [ ] Remove `v2/`, obsolete assets, `MIGRATION.md`
2. [ ] Update `README.md`
3. [ ] Add GitHub Actions documentation
4. [ ] Clean up unnecessary dependencies

### Phase 5: Testing & Validation (1h)
1. [ ] Build locally and verify output
2. [ ] Test responsiveness (desktop, tablet, mobile, TV)
3. [ ] Verify YouTube videos display correctly
4. [ ] Lighthouse audit
5. [ ] Test GitHub Actions workflow by pushing to main

### Phase 6: Deployment (15min)
1. [ ] Final commit
2. [ ] Push to main
3. [ ] Verify deployment via GitHub Pages
4. [ ] Test live URL

---

## 9. Important Rules

### Commits & Code
- ✅ No "Claude" as author in commits (Claude Code instructions)
- ✅ Clear messages, e.g: "Refactor: Migrate to Astro static site generator"
- ✅ One commit per logical step

### Files to Ignore
- `node_modules/`
- `.env.local` (development variables)
- `.astro/` (build cache)
- `dist/` (generated files)

### Pre-Deployment Testing
- Verify all 4 video frames display
- Test responsive design on mobile/tablet/TV
- Verify environment variables are properly injected
- Check performance (Lighthouse)

---

## 10. Summary of Changes

| Aspect | Before | After |
|--------|--------|-------|
| Framework | Vite + Vanilla JS | Astro (static) |
| Build | Client-side | Static HTML generation |
| Deploy | GitHub Pages (manual) | GitHub Actions (auto) |
| Webcam Config | `v2/src/config.js` | GitHub Actions Variables |
| Meteoblue | ✅ Present | ❌ Removed |
| Codebase | `v2/` folder | Root with `src/` Astro |
| Performance | Good | Excellent (static) |
| Bundle Size | ~50KB JS | ~5KB (styles only) |

---

## Additional Notes

- **Rollback**: If something doesn't work, previous commits are available via git
- **Future Support**: Astro is very active with good community support
- **Extensibility**: If dynamic content needs to be added later, Astro adapts well
- **Testing**: E2E tests (Playwright) can be added to the workflow if needed in the future

---

**Ready to start the migration!**
