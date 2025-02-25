// static/js/search.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput'); // Получаем поле ввода
    const searchForm = document.getElementById('searchForm'); // Получаем форму

    if (searchInput && searchForm) {
        // Отправка формы только по Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !searchInput.value.trim()) {
                e.preventDefault();
            }
        });

        // Предотвращаем отправку пустой формы
        searchForm.addEventListener('submit', function(e) {
            if (!searchInput.value.trim()) {
                e.preventDefault();
            }
        });
    }
});