// static/js/admin/translation-tabs.js

// Функция для улучшения интерфейса вкладок перевода
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, находимся ли мы на странице с вкладками перевода
    if (document.querySelector('.ui-tabs')) {
        // Ждем загрузки jQuery UI и TinyMCE
        setTimeout(function() {
            // Функция проверки статуса заполнения перевода
            function checkTranslationStatus() {
                const tabPanels = document.querySelectorAll('.ui-tabs-panel');
                tabPanels.forEach(function(panel) {
                    // Проверяем наличие элементов ввода в панели
                    let inputs = panel.querySelectorAll('input[type="text"], textarea');
                    let isEmpty = true;
                    let isComplete = true;

                    inputs.forEach(function(input) {
                        // Если это TinyMCE
                        if (input.id && input.id.indexOf('id_content_') !== -1 && window.tinymce) {
                            const editor = window.tinymce.get(input.id);
                            if (editor) {
                                const content = editor.getContent();
                                if (content && content.trim() !== '') {
                                    isEmpty = false;
                                } else {
                                    isComplete = false;
                                }
                            }
                        } else if (input.classList.contains('vTextField') || input.tagName === 'TEXTAREA') {
                            // Обычное поле ввода
                            if (input.value && input.value.trim() !== '') {
                                isEmpty = false;
                            } else {
                                isComplete = false;
                            }
                        }
                    });

                    // Определяем состояние заполнения вкладки
                    panel.classList.remove('empty-translation', 'partial-translation', 'complete-translation');
                    if (isEmpty) {
                        panel.classList.add('empty-translation');
                    } else if (!isComplete) {
                        panel.classList.add('partial-translation');
                    } else {
                        panel.classList.add('complete-translation');
                    }

                    // Находим связанную вкладку
                    const tabId = panel.id;
                    const tabSelector = `a[href="#${tabId}"]`;
                    const tab = document.querySelector(tabSelector);

                    if (tab && tab.parentNode) {
                        // Удаляем предыдущие индикаторы, если они есть
                        const existingIndicator = tab.querySelector('.translation-status-indicator');
                        if (existingIndicator) {
                            existingIndicator.remove();
                        }

                        // Добавляем индикатор заполненности к вкладке
                        const indicator = document.createElement('span');
                        indicator.className = 'translation-status-indicator';
                        indicator.style.marginLeft = '4px';

                        if (isEmpty) {
                            tab.parentNode.title = 'Перевод не заполнен';
                            indicator.innerHTML = '✗';
                            indicator.style.color = 'red';
                        } else if (!isComplete) {
                            tab.parentNode.title = 'Перевод заполнен частично';
                            indicator.innerHTML = '⚠';
                            indicator.style.color = 'orange';
                        } else {
                            tab.parentNode.title = 'Перевод заполнен';
                            indicator.innerHTML = '✓';
                            indicator.style.color = 'green';
                        }

                        tab.appendChild(indicator);
                    }
                });
            }

            // Запускаем проверку статуса при загрузке
            checkTranslationStatus();

            // Добавляем обработчики событий к TinyMCE редакторам (если они есть)
            if (window.tinymce) {
                window.tinymce.editors.forEach(function(editor) {
                    editor.on('change', function() {
                        setTimeout(checkTranslationStatus, 100);
                    });
                });
            }

            // Добавляем обработчики событий к обычным полям ввода
            const inputs = document.querySelectorAll('.ui-tabs-panel input, .ui-tabs-panel textarea');
            inputs.forEach(function(input) {
                input.addEventListener('input', function() {
                    setTimeout(checkTranslationStatus, 100);
                });
            });

        }, 1200); // Увеличиваем задержку для уверенности, что TinyMCE полностью загрузился
    }
});