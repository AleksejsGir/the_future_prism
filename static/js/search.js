// static/js/search.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');

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