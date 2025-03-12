// apps/comments/static/comments/js/comments.js
document.addEventListener('DOMContentLoaded', function() {
    initializeEventHandlers();
});

// Выносим всю логику обработчиков событий в отдельную функцию
function initializeEventHandlers() {
    // Переключение формы ответа на комментарий
    const replyButtons = document.querySelectorAll('.reply-button');

    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            const replyForm = document.getElementById(`reply-form-${commentId}`);

            // Скрываем все открытые формы ответа
            document.querySelectorAll('.reply-form').forEach(form => {
                if (form !== replyForm) {
                    form.classList.add('hidden');
                }
            });

            // Переключаем видимость текущей формы
            replyForm.classList.toggle('hidden');

            // Если форма видима, устанавливаем фокус на поле ввода
            if (!replyForm.classList.contains('hidden')) {
                replyForm.querySelector('textarea').focus();
            }
        });
    });

    // Валидация формы комментария
    const commentForms = document.querySelectorAll('.comment-form');

    commentForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const contentField = this.querySelector('textarea[name="content"]');

            if (contentField.value.trim() === '') {
                event.preventDefault();
                // Используем общую функцию уведомлений, если она доступна
                if (typeof showNotification === 'function') {
                    showNotification('Текст комментария не может быть пустым', 'error');
                } else {
                    alert('Текст комментария не может быть пустым');
                }
                contentField.focus();
            }
        });
    });

    // Обработка лайков/дизлайков
    const reactionButtons = document.querySelectorAll('.reaction-btn');


reactionButtons.forEach(button => {
    button.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        const reactionType = this.dataset.reactionType;

        console.log('Нажата кнопка реакции:', commentId, reactionType);

        // Получаем CSRF-токен
        const csrftoken = getCookie('csrftoken');

        // Получаем языковой префикс из текущего URL
        const langPrefix = getCurrentLanguagePrefix();

        // Формируем полный URL с учетом языкового префикса
        const url = `${langPrefix}/comments/${commentId}/reaction/`;
        console.log('Отправка запроса на URL:', url);

        // Отправляем стандартный POST-запрос вместо AJAX для отладки
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = url;
        form.style.display = 'none';

        // Добавляем CSRF-токен
        const csrfField = document.createElement('input');
        csrfField.type = 'hidden';
        csrfField.name = 'csrfmiddlewaretoken';
        csrfField.value = csrftoken;
        form.appendChild(csrfField);

        // Добавляем тип реакции
        const reactionField = document.createElement('input');
        reactionField.type = 'hidden';
        reactionField.name = 'reaction_type';
        reactionField.value = reactionType;
        form.appendChild(reactionField);

        // Добавляем форму в DOM и отправляем
        document.body.appendChild(form);
        form.submit();
    });
});

// Добавим новую функцию для получения языкового префикса
function getCurrentLanguagePrefix() {
    // Получаем текущий URL
    const path = window.location.pathname;

    // Проверяем на наличие языкового префикса в формате /xx/
    const match = path.match(/^\/([a-z]{2})\//);

    // Если есть языковой префикс, возвращаем его с косой чертой впереди и сзади
    if (match) {
        return '/' + match[1];
    }

    // Иначе возвращаем пустой префикс
    return '';
}

    // Обработка сортировки без перезагрузки страницы через AJAX
    const sortButtons = document.querySelectorAll('.comment-sort-btn');

    sortButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const sortBy = this.dataset.sort;
            // Используем текущий URL и только меняем параметр sort_by
            const url = new URL(window.location.href);
            url.searchParams.set('sort_by', sortBy);

            console.log('Сортировка по:', sortBy, 'URL:', url.toString());

            // Визуально активируем кнопку сортировки
            sortButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Обновляем URL без перезагрузки страницы
            history.pushState({}, '', url.toString());

            // Загружаем комментарии с новой сортировкой
            fetch(`/news/${getCurrentNewsId()}/comments/?sort_by=${sortBy}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети: ' + response.status);
                }
                return response.text();
            })
            .then(html => {
                console.log('Получен HTML для сортировки');

                // Создаем временный элемент для парсинга HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');

                // Находим новый список комментариев
                const newCommentsList = doc.querySelector('.comments-list');

                // Заменяем текущий список комментариев
                const currentCommentsList = document.querySelector('.comments-list');
                if (currentCommentsList && newCommentsList) {
                    currentCommentsList.innerHTML = newCommentsList.innerHTML;

                    // Повторно инициализируем обработчики событий
                    initializeEventHandlers();
                } else {
                    console.error('Не удалось найти список комментариев для обновления');
                }
            })
            .catch(error => {
                console.error('Ошибка при сортировке:', error);
                if (typeof showNotification === 'function') {
                    showNotification('Произошла ошибка при загрузке комментариев', 'error');
                } else {
                    alert('Произошла ошибка при загрузке комментариев: ' + error.message);
                }
            });
        });
    });
}

// Функция для получения CSRF-токена из cookie
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

// Функция для получения ID текущей новости из URL
function getCurrentNewsId() {
    // Предполагаем, что URL имеет формат /news/{id}/
    const pathParts = window.location.pathname.split('/');
    // Находим ID новости (обычно это третий элемент после /news/)
    let newsId = null;
    for (let i = 0; i < pathParts.length; i++) {
        if (pathParts[i] === 'news' && i + 1 < pathParts.length) {
            newsId = pathParts[i + 1];
            break;
        }
    }
    return newsId || 0; // Возвращаем 0, если не удалось найти ID
}