// apps/comments/static/comments/js/comments.js
document.addEventListener('DOMContentLoaded', function() {
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
});