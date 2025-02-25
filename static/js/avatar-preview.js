// static/js/avatar-preview.js

// Функция для создания стилизованных сообщений об ошибках
function showMessage(message, isError = false) {
    // Создаем элемент сообщения
    const messageElement = document.createElement('div');
    messageElement.className = `message-box ${isError ? 'error' : 'success'}`;
    messageElement.innerText = message;

    // Добавляем стили
    messageElement.style.padding = '10px';
    messageElement.style.marginTop = '10px';
    messageElement.style.borderRadius = '5px';
    messageElement.style.backgroundColor = isError ? 'rgba(220, 38, 38, 0.2)' : 'rgba(34, 197, 94, 0.2)';
    messageElement.style.color = isError ? '#f87171' : '#86efac';

    // Удаляем предыдущие сообщения
    const prevMessages = document.querySelectorAll('.message-box');
    prevMessages.forEach(msg => msg.remove());

    // Добавляем сообщение на страницу
    const avatarInput = document.getElementById('id_avatar');
    avatarInput.parentElement.appendChild(messageElement);

    // Удаляем сообщение через 5 секунд
    setTimeout(() => {
        messageElement.classList.add('fade-out');
        setTimeout(() => messageElement.remove(), 500);
    }, 5000);
}

// Общая функция для создания элементов предпросмотра
function createPreviewElements() {
    const previewContainer = document.createElement('div');
    previewContainer.className = 'avatar-preview-container hidden';

    const previewImage = document.createElement('img');
    previewImage.className = 'avatar-preview-image';

    const removeButton = document.createElement('button');
    removeButton.className = 'avatar-remove-button';
    removeButton.textContent = 'Удалить';

    previewContainer.append(previewImage, removeButton);
    return {previewContainer, previewImage, removeButton};
}

// Валидация файла
function validateFile(file) {
    if (!file) return false;

    if (!file.type.startsWith('image/')) {
        showMessage('Пожалуйста, выберите изображение', true);
        return false;
    }
    if (file.size > 5 * 1024 * 1024) {
        showMessage('Размер файла не должен превышать 5MB', true);
        return false;
    }
    return true;
}

// Функция для предпросмотра аватара
document.addEventListener('DOMContentLoaded', function() {
    const avatarInput = document.getElementById('id_avatar');
    if (!avatarInput) return;

    const {previewContainer, previewImage, removeButton} = createPreviewElements();
    avatarInput.parentElement.appendChild(previewContainer);

    // Создаем кастомную кнопку
    const customUploadButton = document.createElement('button');
    customUploadButton.type = 'button';
    customUploadButton.className = 'neon-button';
    customUploadButton.textContent = 'Выбрать фото';
    avatarInput.parentElement.insertBefore(customUploadButton, avatarInput);

    // Обработчик изменения файла
    avatarInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!validateFile(file)) {
            avatarInput.value = '';
            return;
        }

        // Показываем предпросмотр
        const reader = new FileReader();
        reader.onload = function(event) {
            previewImage.src = event.target.result;
            previewContainer.classList.remove('hidden');
            showMessage('Аватар готов к загрузке. Нажмите "Сохранить изменения" для применения.');
        };
        reader.readAsDataURL(file);
    });

    // Обработчик удаления
    removeButton.addEventListener('click', function() {
        avatarInput.value = '';
        previewContainer.classList.add('hidden');
        previewImage.src = '';
    });

    // Обработчик клика по кастомной кнопке
    customUploadButton.addEventListener('click', () => avatarInput.click());

    // Если аватар уже есть, показываем его в предпросмотре
    const existingAvatar = document.querySelector('.mb-4 .avatar-preview-image');
    if (existingAvatar) {
        const currentSrc = existingAvatar.src;
        if (currentSrc) {
            previewImage.src = currentSrc;
            previewContainer.classList.remove('hidden');
        }
    }
});