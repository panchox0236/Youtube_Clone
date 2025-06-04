document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggle-info-btn');
    const videoDetails = document.getElementById('video-details');

    toggleBtn.addEventListener('click', function () {
        if (videoDetails.style.display === 'none') {
            videoDetails.style.display = 'block';
            toggleBtn.textContent = 'Hide Details';
        } else {
            videoDetails.style.display = 'none'; 
            toggleBtn.textContent = 'Show Details'; 
        }
    });
});
