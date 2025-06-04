document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.getElementById('commentForm');
    const commentText = document.getElementById('comment-text');

    commentForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const comment = commentText.value.trim();
        if (!comment) {
            alert("Please write a comment.");
            return;
        }

        fetch(window.location.href + 'comment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                'comment': comment
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const commentsSection = document.getElementById('comments-section');
                const newComment = `
                    <div class="comment mb-3">
                        <strong>${data.user}:</strong> ${data.comment}
                        <p><small>Just now</small></p>
                    </div>
                `;
                commentsSection.insertAdjacentHTML('beforeend', newComment);

                commentText.value = '';
            } else {
                alert('There was an error adding your comment. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong.');
        });
    });
});
