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

// Универсальный обработчик файлов
function handleFileInput(inputElement, previewCallback) {
    const {previewContainer, previewImage, removeButton} = createPreviewElements();
    
    inputElement.parentElement.appendChild(previewContainer);
    
    inputElement.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!validateFile(file)) return;
        
        previewCallback(file, previewImage);
        previewContainer.classList.remove('hidden');
    });

    removeButton.addEventListener('click', () => {
        inputElement.value = '';
        previewContainer.classList.add('hidden');
    });
}

// Валидация файла
function validateFile(file) {
    if (!file?.type?.startsWith('image/')) {
        alert('Пожалуйста, выберите изображение');
        return false;
    }
    if (file.size > 5 * 1024 * 1024) {
        alert('Размер файла не должен превышать 5MB');
        return false;
    }
    return true;
}

// Функция для предпросмотра аватара
document.addEventListener('DOMContentLoaded', function() {
    const avatarInput = document.getElementById('id_avatar');
    if (!avatarInput) return;

    // Создаем кастомную кнопку
    const customUploadButton = document.createElement('button');
    customUploadButton.type = 'button';
    customUploadButton.className = 'neon-button';
    customUploadButton.textContent = 'Выбрать фото';
    avatarInput.parentElement.insertBefore(customUploadButton, avatarInput);

    // Инициализируем обработчик
    handleFileInput(avatarInput, (file, previewImage) => {
        const reader = new FileReader();
        reader.onload = (e) => previewImage.src = e.target.result;
        reader.readAsDataURL(file);
    });

    // Обработчик клика по кастомной кнопке
    customUploadButton.addEventListener('click', () => avatarInput.click());
});