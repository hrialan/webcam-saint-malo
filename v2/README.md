# Webcam Saint-Malo v2

Application moderne pour afficher 4 webcams YouTube en live sur une grille 2x2.

## Fonctionnalités

- **4 vidéos en grille 2x2** avec fond sombre pour mettre en valeur les webcams
- **Configuration ultra-simple** dans un seul fichier
- **Optimisé pour TV/écran** - plein écran, pas de menus
- **Build statique** pour hébergement sur GitHub Pages
- **Responsive** - adapté mobile et desktop
- **Performance optimisée** avec Vite

## Développement local

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le site sera accessible sur `http://localhost:5173`

## Configuration des vidéos

Pour modifier les vidéos affichées, éditez simplement le fichier `src/config.js`:

```javascript
export const videoConfig = {
  videos: [
    'VIDEO_ID_1',  // Vidéo en haut à gauche
    'VIDEO_ID_2',  // Vidéo en haut à droite
    'VIDEO_ID_3',  // Vidéo en bas à gauche
    'VIDEO_ID_4'   // Vidéo en bas à droite
  ]
};
```

Pour trouver l'ID d'une vidéo YouTube:
- URL: `https://www.youtube.com/watch?v=80s06q41pMo`
- ID: `80s06q41pMo`

## Build pour production

```bash
# Créer le build optimisé
npm run build

# Prévisualiser le build en local
npm run preview
```

Les fichiers seront générés dans le dossier `dist/`.

## Déploiement sur GitHub Pages

1. Modifier le `base` dans `vite.config.js` avec le nom de votre repo:
   ```javascript
   base: '/votre-nom-de-repo/',
   ```

2. Builder le projet:
   ```bash
   npm run build
   ```

3. Déployer le contenu du dossier `dist/` sur GitHub Pages

## Technologies utilisées

- **Vite** - Build tool ultra-rapide
- **Vanilla JavaScript** - Aucune dépendance
- **CSS Grid** - Layout moderne et responsive
- **YouTube Embed API** - Intégration des vidéos

## License

MIT - Hugo R.
