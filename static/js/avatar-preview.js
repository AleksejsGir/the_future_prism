// // static/js/avatar-preview.js
// document.addEventListener('DOMContentLoaded', function() {
//     const avatarInput = document.getElementById('id_avatar');
//     if (!avatarInput) return;
//
//     const {previewContainer, previewImage, removeButton} = createPreviewElements();
//     avatarInput.parentElement.appendChild(previewContainer);
//
//     // Создаем кастомную кнопку с использованием переводов
//     const customUploadButton = document.createElement('button');
//     customUploadButton.type = 'button';
//     customUploadButton.className = 'neon-button';
//     customUploadButton.textContent = window.translations.select_photo || 'Выбрать фото'; // Используем перевод
//     avatarInput.parentElement.insertBefore(customUploadButton, avatarInput);
//
//     // Обработчик изменения файла
//     avatarInput.addEventListener('change', function(e) {
//         const file = e.target.files[0];
//         if (!validateFile(file)) {
//             avatarInput.value = '';
//             return;
//         }
//
//         // Показываем предпросмотр
//         const reader = new FileReader();
//         reader.onload = function(event) {
//             previewImage.src = event.target.result;
//             previewContainer.classList.remove('hidden');
//             // Используем общую функцию showNotification и переводы
//             if (typeof showNotification === 'function') {
//                 showNotification(window.translations.avatar_ready || 'Аватар готов к загрузке', 'success', {
//                     parent: avatarInput.parentElement,
//                     fixed: false
//                 });
//             }
//         };
//         reader.readAsDataURL(file);
//     });
//
//     // Обработчик удаления с использованием переводов
//     removeButton.addEventListener('click', function() {
//         avatarInput.value = '';
//         previewContainer.classList.add('hidden');
//         previewImage.src = '';
//     });
//
//     // Обработчик клика по кастомной кнопке
//     customUploadButton.addEventListener('click', () => avatarInput.click());
//
//     // Если аватар уже есть, показываем его в предпросмотре
//     const existingAvatar = document.querySelector('.mb-4 .avatar-preview-image');
//     if (existingAvatar) {
//         const currentSrc = existingAvatar.src;
//         if (currentSrc) {
//             previewImage.src = currentSrc;
//             previewContainer.classList.remove('hidden');
//         }
//     }
// });
//
// // Общая функция для создания элементов предпросмотра
// function createPreviewElements() {
//     const previewContainer = document.querySelector('.avatar-preview-container');
//     if (previewContainer) {
//         return {
//             previewContainer,
//             previewImage: previewContainer.querySelector('img'),
//             removeButton: previewContainer.querySelector('button')
//         };
//     } else {
//         const previewContainer = document.createElement('div');
//         previewContainer.className = 'avatar-preview-container hidden';
//
//         const previewImage = document.createElement('img');
//         previewImage.className = 'avatar-preview-image';
//
//         const removeButton = document.createElement('button');
//         removeButton.className = 'avatar-remove-button';
//         removeButton.textContent = window.translations.delete || 'Удалить'; // Используем перевод
//
//         previewContainer.append(previewImage, removeButton);
//         return {previewContainer, previewImage, removeButton};
//     }
// }
//
// // Валидация файла с использованием переводов
// function validateFile(file) {
//     if (!file) return false;
//
//     if (!file.type.startsWith('image/')) {
//         // Используем общую функцию showNotification из utils.js если доступна
//         if (typeof showNotification === 'function') {
//             showNotification(window.translations.file_not_image || 'Пожалуйста, выберите изображение', 'error');
//         } else {
//             alert(window.translations.file_not_image || 'Пожалуйста, выберите изображение');
//         }
//         return false;
//     }
//
//     if (file.size > 5 * 1024 * 1024) {
//         if (typeof showNotification === 'function') {
//             showNotification(window.translations.file_too_large || 'Размер файла не должен превышать 5MB', 'error');
//         } else {
//             alert(window.translations.file_too_large || 'Размер файла не должен превышать 5MB');
//         }
//         return false;
//     }
//     return true;
// }