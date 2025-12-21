/**
 * Configuration des vidéos YouTube
 *
 * Pour modifier les vidéos affichées, remplacez simplement les IDs YouTube ci-dessous.
 * Un ID YouTube est la partie après "watch?v=" dans l'URL.
 *
 * Exemple: https://www.youtube.com/watch?v=80s06q41pMo
 * L'ID est: 80s06q41pMo
 */

/**
 * Générateur d'URL Meteoblue
 * @param {Object} location - Configuration de localisation
 * @returns {string} - URL complète du widget Meteoblue
 *
 * Pour trouver les paramètres d'une ville:
 * 1. Aller sur https://www.meteoblue.com
 * 2. Chercher votre ville
 * 3. L'URL sera: https://www.meteoblue.com/en/weather/week/{slug}_{country}_{id}
 * 4. Extraire le slug, country et id
 */
function generateMeteoblueUrl({ slug, country = 'france', id, apiKeys = null }) {
  // Encode les underscores si nécessaire dans le slug
  const encodedSlug = slug.replace(/_/g, '%20');
  const baseUrl = `https://www.meteoblue.com/en/weather/widget/meteogram/${encodedSlug}_${country}_${id}`;

  const params = new URLSearchParams({
    geoloc: 'fixed',
    temperature_units: 'CELSIUS',
    windspeed_units: 'KILOMETER_PER_HOUR',
    precipitation_units: 'MILLIMETER',
    forecast_days: '4',
    layout: 'bright',
    autowidth: 'auto'
  });

  // Ajout des clés API si fournies (pour certaines villes premium)
  if (apiKeys) {
    params.append('user_key', apiKeys.user_key);
    params.append('embed_key', apiKeys.embed_key);
    if (apiKeys.sig) {
      params.append('sig', apiKeys.sig);
    }
  }

  return `${baseUrl}?${params.toString()}`;
}

export const videoConfig = {
  videos: [
    '80s06q41pMo',  // Vidéo 1 (en haut à gauche)
    'p6nAlz4_bdI',  // Vidéo 2 (en haut à droite)
    'OzYp4NRZlwQ',  // Vidéo 3 (en bas à gauche) - Webcam Paris
    {
      type: 'iframe',
      url: 'https://www.meteoblue.com/en/weather/widget/meteogram/?geoloc=detect&temperature_units=CELSIUS&windspeed_units=KNOT&precipitation_units=MILLIMETER&forecast_days=5&layout=bright&autowidth=auto&user_key=16e89a11dcb472a8&embed_key=00cb4a74d2ee217d&sig=d4b3fff7c135ac78b617afc38c8881819c8123b47e0e1c407ebc565ab6f8d80a'
    }
  ]
};
