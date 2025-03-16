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
// Обработка кнопки "Показать все комментарии"
const showAllCommentsButton = document.getElementById('show-all-comments');
if (showAllCommentsButton) {
    showAllCommentsButton.addEventListener('click', function() {
        const newsId = this.dataset.newsId;

        // Показываем загрузку и блокируем кнопку
        this.textContent = window.translations?.loading || 'Loading...';
        this.disabled = true;

        // Получаем языковой префикс из текущего URL
        const langPrefix = getCurrentLanguagePrefix();

        // Формируем URL с учетом сортировки
        const sortBy = document.querySelector('.comment-sort-btn.active')?.dataset.sort || 'newest';

        // Загружаем все комментарии
        fetch(`${langPrefix}/news/${newsId}/comments/?show_all=true&sort_by=${sortBy}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(window.translations?.request_error || 'Network error: ' + response.status);
            }
            return response.text();
        })
        .then(html => {
            console.log('Comments loaded successfully');

            // Создаем временный элемент для парсинга HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Находим элементы для обновления
            const newCommentsSection = doc.querySelector('.comments-section');
            const currentCommentsSection = document.querySelector('.comments-section');

            if (currentCommentsSection && newCommentsSection) {
                currentCommentsSection.innerHTML = newCommentsSection.innerHTML;

                // Повторно инициализируем обработчики событий для новых элементов
                initializeEventHandlers();
            } else {
                console.error('Could not find comments section to update');
            }
        })
        .catch(error => {
            console.error('Error loading comments:', error);

            // Восстанавливаем кнопку
            this.textContent = window.translations?.show_all_comments || 'Show all comments';
            this.disabled = false;

            // Показываем уведомление об ошибке
            if (typeof showNotification === 'function') {
                showNotification(window.translations?.error_loading_comments || 'Error loading comments', 'error');
            } else {
                alert(window.translations?.error_loading_comments || 'Error loading comments: ' + error.message);
            }
        });
    });
}
    // Валидация формы комментария
    const commentForms = document.querySelectorAll('.comment-form');

    commentForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const contentField = this.querySelector('textarea[name="content"]');

            if (contentField.value.trim() === '') {
                event.preventDefault();
                // Используем общую функцию уведомлений, если она доступна
                if (typeof showNotification === 'function') {
                    showNotification(window.translations?.empty_comment || 'Comment text cannot be empty', 'error');
                } else {
                    alert(window.translations?.empty_comment || 'Comment text cannot be empty');
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

        console.log('Reaction button clicked:', commentId, reactionType);

        // Получаем CSRF-токен
        const csrftoken = getCookie('csrftoken');

        // Получаем языковой префикс из текущего URL
        const langPrefix = getCurrentLanguagePrefix();

        // Формируем полный URL с учетом языкового префикса
        const url = `${langPrefix}/comments/${commentId}/reaction/`;
        console.log('Sending request to URL:', url);

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

            console.log('Sorting by:', sortBy, 'URL:', url.toString());

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
                    throw new Error(window.translations?.request_error || 'Network error: ' + response.status);
                }
                return response.text();
            })
            .then(html => {
                console.log('Received HTML for sorting');

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
                    console.error('Could not find comments list to update');
                }
            })
            .catch(error => {
                console.error('Error during sorting:', error);
                if (typeof showNotification === 'function') {
                    showNotification(window.translations?.error_loading_comments || 'Error loading comments', 'error');
                } else {
                    alert(window.translations?.error_loading_comments || 'Error loading comments: ' + error.message);
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