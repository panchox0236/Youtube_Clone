document.addEventListener('DOMContentLoaded', function () {
    const likeButton = document.getElementById('like-video');
    const dislikeButton = document.getElementById('dislike-video');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (likeButton) {
        likeButton.addEventListener('click', function () {
            sendLikeDislikeRequest('like');
        });
    }

    if (dislikeButton) {
        dislikeButton.addEventListener('click', function () {
            sendLikeDislikeRequest('dislike');
        });
    }

    function sendLikeDislikeRequest(action) {
        const videoId = window.location.pathname.split('/')[3];
        const url = `/drunk/watch_video/${videoId}/like_dislike/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({ 'action': action })
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            document.getElementById('video-likes').textContent = data.likes;
            document.getElementById('video-dislikes').textContent = data.dislikes;
        })
        .catch(error => console.error('Error:', error));
    }
});
