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
    
    // Extract article ID from URL
    const articleId = likeUrl.match(/\/articles\/(\d+)\//)?.[1];
    
    // Check if user has already voted
    let hasLiked = localStorage.getItem(`article_${articleId}_liked`) === 'true';
    let hasDisliked = localStorage.getItem(`article_${articleId}_disliked`) === 'true';
    
    // Update button states
    function updateButtonStates() {
      if (hasLiked) {
        likeBtn.style.opacity = '1';
        likeBtn.style.transform = 'scale(1.1)';
        dislikeBtn.style.opacity = '0.5';
      } else if (hasDisliked) {
        dislikeBtn.style.opacity = '1';
        dislikeBtn.style.transform = 'scale(1.1)';
        likeBtn.style.opacity = '0.5';
      } else {
        likeBtn.style.opacity = '1';
        likeBtn.style.transform = 'scale(1)';
        dislikeBtn.style.opacity = '1';
        dislikeBtn.style.transform = 'scale(1)';
      }
    }
    
    // Set initial button states
    updateButtonStates();

    likeBtn.addEventListener('click', async () => {
      try {
        // If already liked, unlike it
        if (hasLiked) {
          // Remove the like
          const res = await fetch(likeUrl.replace('/like', '/unlike'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (!res.ok) return;
          const data = await res.json();
          if (typeof data.likes !== 'undefined') {
            likeCountEl.textContent = data.likes;
            hasLiked = false;
            localStorage.removeItem(`article_${articleId}_liked`);
            updateButtonStates();
          }
        } else {
          // If disliked, remove dislike first
          if (hasDisliked) {
            await fetch(dislikeUrl.replace('/dislike', '/undislike'), {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({})
            });
            const dislikeRes = await fetch(dislikeUrl.replace('/dislike', '/undislike'), {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({})
            });
            if (dislikeRes.ok) {
              const dislikeData = await dislikeRes.json();
              if (typeof dislikeData.dislikes !== 'undefined') {
                dislikeCountEl.textContent = dislikeData.dislikes;
              }
            }
            hasDisliked = false;
            localStorage.removeItem(`article_${articleId}_disliked`);
          }
          
          // Add like
          const res = await fetch(likeUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (!res.ok) return;
          const data = await res.json();
          if (typeof data.likes !== 'undefined') {
            likeCountEl.textContent = data.likes;
            hasLiked = true;
            localStorage.setItem(`article_${articleId}_liked`, 'true');
            updateButtonStates();
          }
        }
      } catch (err) {
        console.error('Error liking article', err);
      }
    });

    dislikeBtn.addEventListener('click', async () => {
      try {
        // If already disliked, undislike it
        if (hasDisliked) {
          // Remove the dislike
          const res = await fetch(dislikeUrl.replace('/dislike', '/undislike'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (!res.ok) return;
          const data = await res.json();
          if (typeof data.dislikes !== 'undefined') {
            dislikeCountEl.textContent = data.dislikes;
            hasDisliked = false;
            localStorage.removeItem(`article_${articleId}_disliked`);
            updateButtonStates();
          }
        } else {
          // If liked, remove like first
          if (hasLiked) {
            const likeRes = await fetch(likeUrl.replace('/like', '/unlike'), {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({})
            });
            if (likeRes.ok) {
              const likeData = await likeRes.json();
              if (typeof likeData.likes !== 'undefined') {
                likeCountEl.textContent = likeData.likes;
              }
            }
            hasLiked = false;
            localStorage.removeItem(`article_${articleId}_liked`);
          }
          
          // Add dislike
          const res = await fetch(dislikeUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (!res.ok) return;
          const data = await res.json();
          if (typeof data.dislikes !== 'undefined') {
            dislikeCountEl.textContent = data.dislikes;
            hasDisliked = true;
            localStorage.setItem(`article_${articleId}_disliked`, 'true');
            updateButtonStates();
          }
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

// Share functionality
function shareOnTwitter() {
  const url = encodeURIComponent(window.location.href);
  const title = encodeURIComponent(document.querySelector('.article-title')?.textContent || 'Check out this article');
  window.open(`https://twitter.com/intent/tweet?url=${url}&text=${title}`, '_blank', 'width=600,height=400');
}

function shareOnFacebook() {
  const url = encodeURIComponent(window.location.href);
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank', 'width=600,height=400');
}

function shareOnLinkedIn() {
  const url = encodeURIComponent(window.location.href);
  window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank', 'width=600,height=400');
}

function copyLink() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    // Afficher le retour
    const btn = event.target.closest('.share-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span>✓</span> Copié !';
    btn.style.backgroundColor = '#3d5a3d';
    btn.style.color = 'white';
    setTimeout(() => {
      btn.innerHTML = originalText;
      btn.style.backgroundColor = '';
      btn.style.color = '';
    }, 2000);
  }).catch(err => {
    alert('Erreur lors de la copie du lien');
  });
}
