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
      console.log('CSRF Token:', csrfToken ? 'Found' : 'Not found');

      // Используем обычный URL маршрут вместо API (исправление)
      fetch(`/favorites/toggle/${newsId}/`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Response data:', data);

        if(data.success) {
          // Обновляем внешний вид кнопки с использованием переводов
          if(data.is_favorite) {
            console.log('Adding to favorites');
            favoriteBtn.classList.add('favorite-active');
            favoriteBtn.querySelector('.favorite-icon').textContent = '★';
            favoriteBtn.querySelector('.favorite-text').textContent = window.translations?.in_favorites || 'В избранном';
          } else {
            console.log('Removing from favorites');
            favoriteBtn.classList.remove('favorite-active');
            favoriteBtn.querySelector('.favorite-icon').textContent = '☆';
            favoriteBtn.querySelector('.favorite-text').textContent = window.translations?.add_to_favorites || 'В избранное';
          }

          // Используем общую функцию для уведомлений
          if (typeof showNotification === 'function') {
            showNotification(data.message);
          } else {
            // Запасной вариант, если общая функция недоступна
            showLocalNotification(data.message);
          }
        } else {
          console.error('Error in response:', data);

          if (typeof showNotification === 'function') {
            showNotification(window.translations?.error_occurred || 'Произошла ошибка. Попробуйте еще раз.', 'error');
          } else {
            showLocalNotification(window.translations?.error_occurred || 'Произошла ошибка. Попробуйте еще раз.', 'error');
          }
        }
      })
      .catch(error => {
        console.error('AJAX error:', error);

        if (typeof showNotification === 'function') {
            showNotification(window.translations?.request_error || 'Произошла ошибка при обработке запроса', 'error');
        } else {
            showLocalNotification(window.translations?.request_error || 'Произошла ошибка при обработке запроса', 'error');
        }
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

  // Локальная функция для показа уведомлений (запасной вариант)
  function showLocalNotification(message, type = 'success') {
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