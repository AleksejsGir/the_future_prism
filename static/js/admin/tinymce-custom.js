// Дополнительные настройки для TinyMCE

document.addEventListener('DOMContentLoaded', function() {
    // Функция для перемещения TinyMCE редактора левее
    function adjustTinyMCEPosition() {
        // Ждем инициализации TinyMCE
        setTimeout(function() {
            const tinyFrames = document.querySelectorAll('.tox-tinymce');
            if (tinyFrames.length > 0) {
                tinyFrames.forEach(frame => {
                    frame.style.marginLeft = '-200px';
                    frame.style.width = '90%';
                    frame.style.maxWidth = '1200px';
                });
            }
        }, 500);
    }

    // Вызываем функцию при загрузке страницы
    adjustTinyMCEPosition();

    // Вызываем функцию при изменении размера окна
    window.addEventListener('resize', adjustTinyMCEPosition);
});