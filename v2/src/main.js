import './style.css';
import { videoConfig } from './config.js';

const STORAGE_KEY = 'video4-selection';

/**
 * Crée un élément de wrapper pour une vidéo YouTube
 * @param {string} videoId - L'ID de la vidéo YouTube
 * @returns {HTMLElement} - L'élément wrapper avec l'iframe
 */
function createVideoElement(videoId) {
  const wrapper = document.createElement('div');
  wrapper.className = 'video-wrapper';

  const iframe = document.createElement('iframe');
  iframe.className = 'video-iframe';
  iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&controls=0&modestbranding=1&rel=0&loop=1&playlist=${videoId}`;
  iframe.allow = 'autoplay; encrypted-media';
  iframe.allowFullscreen = true;
  iframe.loading = 'lazy';

  wrapper.appendChild(iframe);
  return wrapper;
}

/**
 * Crée un élément iframe générique
 * @param {string} url - L'URL de l'iframe
 * @returns {HTMLElement} - L'élément wrapper avec l'iframe
 */
function createIframeElement(url) {
  const wrapper = document.createElement('div');
  wrapper.className = 'video-wrapper iframe-wrapper';

  const iframe = document.createElement('iframe');
  iframe.className = 'video-iframe';
  iframe.src = url;
  iframe.loading = 'lazy';
  iframe.setAttribute('frameborder', '0');
  iframe.setAttribute('scrolling', 'NO');
  iframe.setAttribute('allowtransparency', 'true');
  iframe.setAttribute('sandbox', 'allow-same-origin allow-scripts allow-popups allow-popups-to-escape-sandbox');

  wrapper.appendChild(iframe);

  // Attribution Meteoblue (obligatoire)
  if (url.includes('meteoblue.com')) {
    const attribution = document.createElement('div');
    attribution.className = 'meteoblue-attribution';
    const link = document.createElement('a');
    link.href = 'https://www.meteoblue.com/en/weather/week/index';
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = 'meteoblue';
    attribution.appendChild(link);
    wrapper.appendChild(attribution);
  }

  return wrapper;
}

/**
 * Crée l'élément sélecteur pour la vidéo 4
 * @param {Function} onChange - Callback appelé lors du changement
 * @returns {HTMLElement} - L'élément sélecteur
 */
function createSelector(onChange) {
  const selector = document.createElement('div');
  selector.className = 'video-selector';

  videoConfig.video4Options.forEach(option => {
    const button = document.createElement('button');
    button.className = 'selector-button';
    button.textContent = option.label;
    button.dataset.optionId = option.id;
    button.addEventListener('click', () => onChange(option));
    selector.appendChild(button);
  });

  return selector;
}

/**
 * Récupère la sélection sauvegardée ou la première option par défaut
 * @returns {Object} - L'option sélectionnée
 */
function getSavedSelection() {
  const savedId = localStorage.getItem(STORAGE_KEY);
  return videoConfig.video4Options.find(opt => opt.id === savedId) || videoConfig.video4Options[0];
}

/**
 * Sauvegarde la sélection dans localStorage
 * @param {string} optionId - L'ID de l'option sélectionnée
 */
function saveSelection(optionId) {
  localStorage.setItem(STORAGE_KEY, optionId);
}

/**
 * Initialise l'application
 */
function initApp() {
  const app = document.querySelector('#app');

  // Création de la grille de vidéos
  const videoGrid = document.createElement('div');
  videoGrid.className = 'video-grid';

  // Ajout des 3 premières vidéos fixes
  videoConfig.videos.forEach(video => {
    let videoElement;

    // Si c'est un objet (iframe), sinon c'est un ID YouTube
    if (typeof video === 'object') {
      videoElement = createIframeElement(video.url);
    } else {
      videoElement = createVideoElement(video);
    }

    videoGrid.appendChild(videoElement);
  });

  // Ajout de la vidéo 4 avec sélecteur
  const video4Container = document.createElement('div');
  video4Container.className = 'video-wrapper-container';

  // Récupération de la sélection sauvegardée
  const currentSelection = getSavedSelection();

  // Création de l'élément vidéo initial
  let currentVideoElement = createIframeElement(currentSelection.url);
  video4Container.appendChild(currentVideoElement);

  // Fonction pour changer la vidéo
  const changeVideo = (option) => {
    // Suppression de l'ancienne vidéo
    const oldVideo = video4Container.querySelector('.video-wrapper');
    if (oldVideo) {
      oldVideo.remove();
    }

    // Création de la nouvelle vidéo
    currentVideoElement = createIframeElement(option.url);
    video4Container.insertBefore(currentVideoElement, video4Container.querySelector('.video-selector'));

    // Sauvegarde de la sélection
    saveSelection(option.id);

    // Mise à jour des boutons actifs
    updateActiveButton(option.id);
  };

  // Création du sélecteur
  const selector = createSelector(changeVideo);
  video4Container.appendChild(selector);

  // Fonction pour mettre à jour le bouton actif
  const updateActiveButton = (activeId) => {
    selector.querySelectorAll('.selector-button').forEach(btn => {
      if (btn.dataset.optionId === activeId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  };

  // Initialisation du bouton actif
  updateActiveButton(currentSelection.id);

  videoGrid.appendChild(video4Container);

  // Création du footer
  const footer = document.createElement('footer');
  footer.className = 'copyright';
  footer.textContent = `© ${new Date().getFullYear()} - Hugo R.`;

  // Ajout des éléments au DOM
  app.appendChild(videoGrid);
  app.appendChild(footer);
}

// Démarrage de l'application quand le DOM est prêt
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
