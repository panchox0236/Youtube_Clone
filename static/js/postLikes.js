document.addEventListener('DOMContentLoaded', function () {
    const likeButton = document.getElementById('like-post');
    const dislikeButton = document.getElementById('dislike-post');

    likeButton.addEventListener('click', function () {
        handleLikeDislike('like');
    });

    dislikeButton.addEventListener('click', function () {
        handleLikeDislike('dislike');
    });

    function handleLikeDislike(action) {
        const postId = window.location.pathname.split('/')[2];  // Obtener el ID del post desde la URL
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/post/${postId}/like/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({ [action]: true })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('post-likes').textContent = data.likes;
            document.getElementById('post-dislikes').textContent = data.dislikes;
        })
        .catch(error => console.error('Error:', error));
    }
});
