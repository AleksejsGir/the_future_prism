// static/js/favorites.js
document.addEventListener('DOMContentLoaded', function() {
  console.log('Favorites script loaded');

  const favoriteBtn = document.getElementById('favorite-btn');

  if (favoriteBtn) {
    console.log('Found favorite button with ID:', favoriteBtn.dataset.newsId);
    console.log('Button initial state:', favoriteBtn.classList.contains('favorite-active') ? 'Active (in favorites)' : 'Inactive (not in favorites)');

    favoriteBtn.addEventListener('click', function(e) {
      e.preventDefault(); // Предотвращаем переход по ссылке, если кнопка внутри <a>
      console.log('Favorite button clicked!');

      const newsId = this.dataset.newsId;
      const csrfToken = getCookie('csrftoken');

      console.log('Sending request for news ID:', newsId);

      // Исправляем URL - удаляем префикс 'users/'
      fetch(`/api/v1/users/favorites/toggle/${newsId}/`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
        }
      })
      .then(response => {
        console.log('Response status:', response.status);
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data);

        if(data.success) {
          // Обновляем внешний вид кнопки
          if(data.is_favorite) {
            console.log('Adding to favorites');
            favoriteBtn.classList.add('favorite-active');
            favoriteBtn.querySelector('.favorite-icon').textContent = '★';
            favoriteBtn.querySelector('.favorite-text').textContent = 'В избранном';
          } else {
            console.log('Removing from favorites');
            favoriteBtn.classList.remove('favorite-active');
            favoriteBtn.querySelector('.favorite-icon').textContent = '☆';
            favoriteBtn.querySelector('.favorite-text').textContent = 'В избранное';
          }

          // Показываем сообщение
          showNotification(data.message);
        } else {
          console.error('Error in response:', data);
          showNotification('Произошла ошибка. Попробуйте еще раз.', 'error');
        }
      })
      .catch(error => {
        console.error('AJAX error:', error);
        showNotification('Произошла ошибка при обработке запроса', 'error');
      });
    });
  } else {
    console.warn('Favorite button not found on page!');
  }

  // Функция для получения CSRF-токена из куки
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Функция для показа уведомлений
  function showNotification(message, type = 'success') {
    console.log('Showing notification:', message, 'Type:', type);
    const notification = document.createElement('div');
    notification.className = `fixed top-5 right-5 p-3 rounded-lg ${type === 'success' ? 'bg-green-500/80' : 'bg-red-500/80'} text-white z-50`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Удаляем уведомление через 3 секунды
    setTimeout(() => {
      notification.classList.add('fade-out');
      setTimeout(() => {
        notification.remove();
      }, 500);
    }, 3000);
  }
});