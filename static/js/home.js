// static/js/home.js
document.addEventListener("DOMContentLoaded", function() {
    // Обновленные селекторы, соответствующие base.html
    const mobileSearchForm = document.getElementById("mobileSearchForm");
    const mobileSearchInput = document.getElementById("mobileSearchInput");

    if (mobileSearchForm && mobileSearchInput) {
        // Здесь логика для обработки мобильного поиска
        // Например, можно добавить функционал открытия/закрытия поля поиска
        const burgerBtn = document.getElementById('burger-btn');
        
        if (burgerBtn) {
            burgerBtn.addEventListener("click", function() {
                // Фокусировка на поле поиска после открытия мобильного меню
                setTimeout(() => {
                    if (document.getElementById('mobile-menu').classList.contains('open')) {
                        mobileSearchInput.focus();
                    }
                }, 300);
            });
        }
        
        // Предотвращаем отправку пустой формы поиска
        mobileSearchForm.addEventListener("submit", function(e) {
            if (!mobileSearchInput.value.trim()) {
                e.preventDefault();
            }
        });
    }
});