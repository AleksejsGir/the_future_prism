// Функция для предпросмотра аватара
document.addEventListener('DOMContentLoaded', function() {
    // Находим элементы управления
    const avatarInput = document.getElementById('id_avatar');
    const previewContainer = document.createElement('div');
    const previewImage = document.createElement('img');
    const removeButton = document.createElement('button');

    // Настраиваем контейнер предпросмотра
    previewContainer.className = 'avatar-preview-container hidden';
    previewImage.className = 'avatar-preview-image';
    removeButton.className = 'avatar-remove-button';
    removeButton.textContent = 'Удалить';

    // Добавляем элементы на страницу
    if (avatarInput) {
        avatarInput.parentElement.appendChild(previewContainer);
        previewContainer.appendChild(previewImage);
        previewContainer.appendChild(removeButton);

        // Добавляем кастомную кнопку для загрузки
        const customUploadButton = document.createElement('button');
        customUploadButton.type = 'button';
        customUploadButton.className = 'neon-button';
        customUploadButton.textContent = 'Выбрать фото';
        avatarInput.parentElement.insertBefore(customUploadButton, avatarInput);

        // Обработчик клика по кастомной кнопке
        customUploadButton.addEventListener('click', () => {
            avatarInput.click();
        });

        // Обработчик изменения файла
        avatarInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Проверяем тип файла
                if (!file.type.startsWith('image/')) {
                    alert('Пожалуйста, выберите изображение');
                    avatarInput.value = '';
                    return;
                }

                // Проверяем размер файла (5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Размер файла не должен превышать 5MB');
                    avatarInput.value = '';
                    return;
                }

                // Показываем предпросмотр
                const reader = new FileReader();
                reader.onload = function(event) {
                    previewImage.src = event.target.result;
                    previewContainer.classList.remove('hidden');
                };
                reader.readAsDataURL(file);
            }
        });

        // Обработчик удаления
        removeButton.addEventListener('click', function() {
            avatarInput.value = '';
            previewContainer.classList.add('hidden');
            previewImage.src = '';
        });
    }
});