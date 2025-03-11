// apps/news/static/news/js/favorites.js

/**
 * Скрипт для управления функциональностью избранных новостей
 * Версия: 1.0.0
 * Автор: The Future Prism Team
 */
document.addEventListener('DOMContentLoaded', function() {
  // Журналирование загрузки скрипта
  console.log('Favorites script loaded successfully');

  // Получаем кнопку избранного
  const favoriteBtn = document.getElementById('favorite-btn');

  // Проверяем наличие кнопки на странице
  if (!favoriteBtn) {
    console.warn('Favorite button not found. Skipping initialization.');
    return;
  }

  // Журналирование начального состояния кнопки
  const newsId = favoriteBtn.dataset.newsId;
  console.log('Initial favorite button state:', {
    newsId: newsId,
    isFavorite: favoriteBtn.classList.contains('favorite-active')
  });

  // Обработчик клика по кнопке избранного
  favoriteBtn.addEventListener('click', function(event) {
    // Предотвращаем стандартное поведение ссылки
    event.preventDefault();

    // Отключаем кнопку во время запроса для предотвращения множественных кликов
    this.disabled = true;

    // Получаем идентификатор новости и CSRF-токен
    const newsId = this.dataset.newsId;
    const csrfToken = getCookie('csrftoken');

    // Журналирование отправляемого запроса
    console.log('Sending favorite toggle request', { newsId, csrfTokenPresent: !!csrfToken });

    // Выполняем запрос на сервер
    fetch(`/news/favorites/toggle/${newsId}/`, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      // Расширенная обработка ответа
      if (!response.ok) {
        switch(response.status) {
          case 404: throw new Error('Новость не найдена');
          case 403: throw new Error('Требуется авторизация');
          case 500: throw new Error('Внутренняя ошибка сервера');
          default: throw new Error('Неизвестная ошибка при обработке запроса');
        }
      }
      return response.json();
    })
    .then(data => {
      // Проверяем успешность операции
      if (!data.success) {
        throw new Error(data.message || 'Не удалось обновить избранное');
      }

      // Обновляем внешний вид кнопки
      updateFavoriteButtonState(favoriteBtn, data.is_favorite);

      // Показываем уведомление
      showNotification(data.message, 'success');
    })
    .catch(error => {
      // Обработка ошибок
      console.error('Favorite toggle error:', error);
      showNotification(error.message, 'error');
    })
    .finally(() => {
      // Возвращаем кнопку в активное состояние
      this.disabled = false;
    });
  });

  /**
   * Обновляет визуальное состояние кнопки избранного
   * @param {HTMLElement} button - Кнопка избранного
   * @param {boolean} isFavorite - Состояние избранного
   */
  function updateFavoriteButtonState(button, isFavorite) {
    const iconElement = button.querySelector('.favorite-icon');
    const textElement = button.querySelector('.favorite-text');

    if (isFavorite) {
      button.classList.add('favorite-active');
      iconElement.textContent = '★';
      textElement.textContent = window.translations?.in_favorites || 'В избранном';
    } else {
      button.classList.remove('favorite-active');
      iconElement.textContent = '☆';
      textElement.textContent = window.translations?.add_to_favorites || 'В избранное';
    }
  }

  /**
   * Получает значение cookie
   * @param {string} name - Имя cookie
   * @returns {string|null} Значение cookie
   */
  function getCookie(name) {
    const cookieMatch = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
    return cookieMatch ? decodeURIComponent(cookieMatch[2]) : null;
  }

  /**
   * Показывает уведомление с использованием глобальной функции или fallback
   * @param {string} message - Текст сообщения
   * @param {string} type - Тип сообщения (success/error)
   */
  function showNotification(message, type = 'success') {
    if (typeof window.showNotification === 'function') {
      window.showNotification(message, type);
    } else {
      // Fallback - локальное уведомление
      const notification = document.createElement('div');
      notification.className = `fixed top-5 right-5 p-3 rounded-lg ${
        type === 'success' ? 'bg-green-500/80' : 'bg-red-500/80'
      } text-white z-50`;
      notification.textContent = message;
      document.body.appendChild(notification);

      setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
      }, 3000);
    }
  }
});