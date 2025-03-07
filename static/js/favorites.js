// static/js/favorites.js
document.addEventListener('DOMContentLoaded', function() {
  const favoriteBtn = document.getElementById('favorite-btn');

  if (favoriteBtn) {
    favoriteBtn.addEventListener('click', function() {
      const newsId = this.dataset.newsId;
      const csrfToken = getCookie('csrftoken');

      // Отправляем AJAX запрос
      fetch(`/users/favorites/toggle/${newsId}/`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken,
        }
      })
      .then(response => response.json())
      .then(data => {
        if(data.success) {
          // Обновляем внешний вид кнопки
          if(data.is_favorite) {
            favoriteBtn.classList.add('favorite-active');
            favoriteBtn.querySelector('.favorite-icon').textContent = '★';
            favoriteBtn.querySelector('.favorite-text').textContent = 'В избранном';
          } else {
            favoriteBtn.classList.remove('favorite-active');
            favoriteBtn.querySelector('.favorite-icon').textContent = '☆';
            favoriteBtn.querySelector('.favorite-text').textContent = 'В избранное';
          }

          // Показываем сообщение
          showNotification(data.message);
        } else {
          showNotification('Произошла ошибка. Попробуйте еще раз.', 'error');
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при обработке запроса', 'error');
      });
    });
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