// script.js
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('video-container');
    
    videoConfig.videos.forEach(videoId => {
        const videoWrapper = document.createElement('div');
        videoWrapper.className = 'video-wrapper';
        
        videoWrapper.innerHTML = `
            <iframe class="video-iframe" 
                src="https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&controls=0&modestbranding=1&rel=0" 
                allow="autoplay; encrypted-media" 
                allowfullscreen>
            </iframe>
        `;
        
        container.appendChild(videoWrapper);
    });

    // Mise à jour dynamique du copyright
    document.querySelector('.copyright').textContent = 
        `© ${new Date().getFullYear()} - Hugo R.`;
});
