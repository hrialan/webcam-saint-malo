# Webcam Saint-Malo v2

Application moderne pour afficher 4 webcams/widgets en live sur une grille 2x2.

🔗 **[Voir le site en ligne](https://hrialan.github.io/webcam-saint-malo/)**

## Fonctionnalités

- **3 webcams YouTube en direct** (Saint-Malo + autres locations)
- **Widget météo Meteoblue** avec détection automatique de localisation
- **Fond sombre optimisé** pour mettre en valeur les vidéos
- **Plein écran** - maximise l'affichage, parfait pour TV/écran
- **Responsive** - adapté mobile et desktop
- **Performance optimisée** avec Vite

## Structure

```
├── v2/              # Code source de développement
│   ├── src/
│   │   ├── config.js    # Configuration des vidéos
│   │   ├── main.js      # Code JavaScript
│   │   └── style.css    # Styles
│   ├── index.html
│   └── package.json
├── assets/          # Assets buildés (générés)
└── index.html       # Page principale (générée)
```

## Développement

```bash
cd v2
npm install
npm run dev
```

## Modifier les vidéos

Éditez `v2/src/config.js`:

```javascript
export const videoConfig = {
  videos: [
    'VIDEO_ID_1',  // Vidéo 1
    'VIDEO_ID_2',  // Vidéo 2
    'VIDEO_ID_3',  // Vidéo 3
    { type: 'iframe', url: 'IFRAME_URL' }  // Widget iframe
  ]
};
```

## Build et déploiement

```bash
cd v2
npm run build
cp -r dist/* ..
git add . && git commit -m "Update site" && git push
```

GitHub Pages publiera automatiquement les changements.

## Technologies

- Vite
- Vanilla JavaScript
- CSS Grid
- YouTube Embed API
- Meteoblue Widget API

---

© 2025 - Hugo R.
