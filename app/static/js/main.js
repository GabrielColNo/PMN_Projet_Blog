document.addEventListener('DOMContentLoaded', () => {
  const actions = document.getElementById('article-actions');
  const likeBtn = document.getElementById('like-btn');
  const dislikeBtn = document.getElementById('dislike-btn');
  const likeCountEl = document.getElementById('like-count');
  const dislikeCountEl = document.getElementById('dislike-count');
  const commentForm = document.getElementById('comment-form');
  const commentsList = document.getElementById('comments-list');
  const commentError = document.getElementById('comment-error');

  if (actions && likeBtn && dislikeBtn && likeCountEl && dislikeCountEl) {
    const likeUrl = actions.dataset.likeUrl;
    const dislikeUrl = actions.dataset.dislikeUrl;

    likeBtn.addEventListener('click', async () => {
      try {
        const res = await fetch(likeUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        });
        if (!res.ok) return;
        const data = await res.json();
        if (typeof data.likes !== 'undefined') {
          likeCountEl.textContent = data.likes;
        }
      } catch (err) {
        console.error('Error liking article', err);
      }
    });

    dislikeBtn.addEventListener('click', async () => {
      try {
        const res = await fetch(dislikeUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        });
        if (!res.ok) return;
        const data = await res.json();
        if (typeof data.dislikes !== 'undefined') {
          dislikeCountEl.textContent = data.dislikes;
        }
      } catch (err) {
        console.error('Error disliking article', err);
      }
    });
  }

  if (commentForm && commentsList) {
    const commentsUrl = actions ? actions.dataset.commentsUrl : null;
    if (!commentsUrl) return;

    commentForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (commentError) {
        commentError.hidden = true;
        commentError.textContent = '';
      }

      const authorInput = document.getElementById('author_name');
      const bodyInput = document.getElementById('body');

      const payload = {
        author_name: authorInput ? authorInput.value : '',
        body: bodyInput ? bodyInput.value : ''
      };

      try {
        const res = await fetch(commentsUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
          if (commentError) {
            commentError.textContent = data && data.error ? data.error : 'Error adding comment';
            commentError.hidden = false;
          }
          return;
        }

        // Clear inputs
        if (authorInput) authorInput.value = '';
        if (bodyInput) bodyInput.value = '';

        // Remove "no comments" placeholder if present
        const empty = commentsList.querySelector('.comment-empty');
        if (empty) {
          empty.remove();
        }

        // Append new comment
        const li = document.createElement('li');
        li.className = 'comment-item';
        const authorName = data.author_name || 'Anonymous';
        const createdAt = data.created_at || '';

        li.innerHTML = `
          <p class="comment-meta">
            <strong>${authorName}</strong>
            ${createdAt ? ' • ' + createdAt : ''}
          </p>
          <p class="comment-body"></p>
        `;

        const bodyP = li.querySelector('.comment-body');
        if (bodyP) {
          bodyP.textContent = data.body || '';
        }

        commentsList.appendChild(li);
      } catch (err) {
        console.error('Error posting comment', err);
        if (commentError) {
          commentError.textContent = 'Network error while adding comment';
          commentError.hidden = false;
        }
      }
    });
  }
});
