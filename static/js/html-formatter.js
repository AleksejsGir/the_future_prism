// static/js/html-formatter.js
/**
 * Функции для форматирования HTML-контента
 */

/**
 * Исправляет HTML-сущности в тексте, превращая их в соответствующие символы
 * @param {string} html - Текст, содержащий HTML-сущности
 * @returns {string} - Форматированный текст
 */
function fixHtmlEntities(html) {
    if (!html) return '';

    return html
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&nbsp;/g, ' ');
}

/**
 * Находит и преобразует все элементы с указанным классом на странице
 * @param {string} selector - CSS-селектор элементов для обработки
 */
function formatHtmlContent(selector) {
    document.addEventListener('DOMContentLoaded', function() {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.innerHTML = fixHtmlEntities(element.innerHTML);
        });
    });
}

// Экспортируем для возможности использования как модуля
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = {
        fixHtmlEntities,
        formatHtmlContent
    };
}