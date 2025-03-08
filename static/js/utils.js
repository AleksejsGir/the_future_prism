// static/js/utils.js
/**
 * Утилитарные функции для использования во всем проекте
 */

/**
 * Показывает уведомление пользователю
 * @param {string} message - Текст сообщения
 * @param {string} type - Тип сообщения ('success', 'error', 'info', 'warning')
 * @param {Object} options - Дополнительные параметры
 * @param {HTMLElement} options.parent - Родительский элемент (если null, добавляется к body)
 * @param {number} options.duration - Длительность отображения в мс (0 - без автоскрытия)
 * @param {boolean} options.fixed - Фиксированное позиционирование (по умолчанию: true)
 */
function showNotification(message, type = 'success', options = {}) {
    // Настройки по умолчанию
    const defaultOptions = {
        parent: null,
        duration: 3000,
        fixed: true,
    };

    // Объединяем настройки по умолчанию с переданными параметрами
    const settings = {...defaultOptions, ...options};

    // Создаем элемент уведомления
    const notification = document.createElement('div');

    // Базовые стили
    let className = 'p-3 rounded-lg z-50 ';

    // Добавляем стили в зависимости от типа сообщения
    switch(type) {
        case 'success':
            className += 'bg-green-500/80 text-white';
            break;
        case 'error':
            className += 'bg-red-500/80 text-white';
            break;
        case 'warning':
            className += 'bg-yellow-500/80 text-white';
            break;
        case 'info':
            className += 'bg-blue-500/80 text-white';
            break;
        default:
            className += 'bg-gray-700/80 text-white';
    }

    // Позиционирование
    if (settings.fixed) {
        notification.className = `fixed top-5 right-5 ${className}`;
    } else {
        notification.className = className;
    }

    notification.textContent = message;

    // Добавляем к родительскому элементу или к body
    const parent = settings.parent || document.body;
    parent.appendChild(notification);

    // Добавляем класс для анимации появления
    notification.classList.add('fade-in');

    // Автоматическое скрытие уведомления
    if (settings.duration > 0) {
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, settings.duration);
    } else {
        // Если duration = 0, добавляем кнопку закрытия
        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.className = 'ml-3 text-white hover:text-gray-200';
        closeButton.addEventListener('click', () => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 500);
        });
        notification.appendChild(closeButton);
    }

    return notification;
}

// Экспортируем для возможности использования как модуля
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = {
        showNotification
    };
}