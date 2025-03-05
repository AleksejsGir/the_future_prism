// static/js/admin/custom-tabs.js

// Кастомная реализация переключения вкладок без jQuery UI
document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom tabs script loaded!');

    // Запускаем инициализацию вкладок с небольшой задержкой
    setTimeout(initCustomTabs, 500);

    function initCustomTabs() {
        console.log('Initializing custom tabs...');

        // Основная логика для инициализации глобальных вкладок перевода
        detectAndInitializeTabs();

        // Добавляем подсказку о переводах в верхнюю часть формы
        addTranslationGuidance();
    }

    function addTranslationGuidance() {
        const form = document.querySelector('form');
        if (!form) return;

        // Если уже есть панель с информацией, не добавляем снова
        if (document.querySelector('.translation-info-panel')) return;

        // Создаем панель с информацией о переводах
        const infoPanel = document.createElement('div');
        infoPanel.className = 'translation-info-panel';
        infoPanel.innerHTML = `
            <h3 style="margin-top:0;">Управление переводами</h3>
            <p>🇷🇺 <strong>Русский</strong> - основной язык (заполните в первую очередь)</p>
            <p>🇬🇧 <strong>English</strong> - дополнительный язык</p>
            <p>Используйте вкладки ниже для переключения между языками.</p>
        `;

        // Создаем панель переключения языков
        const tabNav = document.createElement('div');
        tabNav.className = 'global-language-tabs';

        // Создаем кнопки для каждого языка
        ['ru', 'en'].forEach((lang, index) => {
            const button = document.createElement('button');
            button.setAttribute('data-lang', lang);
            button.setAttribute('type', 'button');
            button.className = 'global-tab-button';
            button.textContent = lang === 'ru' ? 'Русский' : 'English';

            // Добавляем флаги к кнопкам
            const flag = document.createElement('span');
            flag.textContent = lang === 'ru' ? ' 🇷🇺' : ' 🇬🇧';
            button.appendChild(flag);

            // Делаем первую вкладку активной
            if (index === 0) {
                button.classList.add('active');
            }

            // Обработчик клика для переключения вкладок
            button.addEventListener('click', function() {
                // Деактивируем все кнопки
                tabNav.querySelectorAll('.global-tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });

                // Активируем текущую кнопку
                this.classList.add('active');

                // Показываем соответствующие поля
                switchLanguageFields(this.getAttribute('data-lang'));
            });

            tabNav.appendChild(button);
        });

        // Вставляем элементы в форму
        form.insertBefore(infoPanel, form.firstChild);
        form.insertBefore(tabNav, form.firstChild);

        // Показываем поля русского языка по умолчанию
        switchLanguageFields('ru');
    }

    function detectAndInitializeTabs() {
        // Ищем все поля с _ru и _en суффиксами
        const ruFields = document.querySelectorAll('[id$="_ru"], [name$="_ru"]');
        const enFields = document.querySelectorAll('[id$="_en"], [name$="_en"]');

        if (ruFields.length === 0 && enFields.length === 0) {
            console.log('No translation fields found');
            return;
        }

        console.log(`Found ${ruFields.length} Russian fields and ${enFields.length} English fields`);

        // Добавляем визуальные индикаторы языка для всех полей
        addLanguageIndicators();
    }

    function addLanguageIndicators() {
        // Находим все метки полей
        const labels = document.querySelectorAll('label');

        labels.forEach(label => {
            const forAttr = label.getAttribute('for');
            if (!forAttr) return;

            // Проверяем, относится ли метка к переводимому полю
            if (forAttr.endsWith('_ru')) {
                if (!label.querySelector('.lang-indicator')) {
                    const indicator = document.createElement('span');
                    indicator.className = 'lang-indicator';
                    indicator.textContent = ' 🇷🇺';
                    indicator.title = 'Русский язык';
                    label.appendChild(indicator);
                }
            } else if (forAttr.endsWith('_en')) {
                if (!label.querySelector('.lang-indicator')) {
                    const indicator = document.createElement('span');
                    indicator.className = 'lang-indicator';
                    indicator.textContent = ' 🇬🇧';
                    indicator.title = 'English';
                    label.appendChild(indicator);
                }
            }
        });
    }

    function switchLanguageFields(lang) {
        console.log(`Switching to language: ${lang}`);

        // Проходим по всем строкам формы
        const formRows = document.querySelectorAll('.form-row, .field-box, .tabular fieldset');

        formRows.forEach(row => {
            // Ищем поля ввода с языковыми суффиксами
            const ruElements = row.querySelectorAll('[id$="_ru"], [name$="_ru"]');
            const enElements = row.querySelectorAll('[id$="_en"], [name$="_en"]');

            // Если нашли переводимые поля
            if (ruElements.length > 0 || enElements.length > 0) {
                // Управляем видимостью полей
                ruElements.forEach(elem => {
                    const container = getFieldContainer(elem);
                    if (container) {
                        container.style.display = lang === 'ru' ? '' : 'none';
                    }
                });

                enElements.forEach(elem => {
                    const container = getFieldContainer(elem);
                    if (container) {
                        container.style.display = lang === 'en' ? '' : 'none';
                    }
                });

                // Если поле использует TinyMCE
                updateTinyMCEVisibility(ruElements, enElements, lang);
            }
        });
    }

    function getFieldContainer(element) {
        // Ищем ближайший контейнер поля
        let container = element.closest('.form-row') ||
                        element.closest('.field-box') ||
                        element.closest('.form-group');

        if (!container) {
            // Если контейнер не найден, ищем родительский элемент
            container = element.parentElement;
            // Поднимаемся до тех пор, пока не найдем достаточно большой контейнер
            while (container && container.tagName !== 'BODY' &&
                   !container.classList.contains('field-box') &&
                   !container.classList.contains('form-row')) {
                container = container.parentElement;
            }
        }

        return container;
    }

    function updateTinyMCEVisibility(ruElements, enElements, lang) {
        if (!window.tinymce) return;

        // Обрабатываем редакторы TinyMCE для русского языка
        ruElements.forEach(elem => {
            if (!elem.id) return;
            const editor = window.tinymce.get(elem.id);
            if (editor) {
                const editorContainer = editor.getContainer();
                if (editorContainer) {
                    editorContainer.style.display = lang === 'ru' ? '' : 'none';
                }
            }
        });

        // Обрабатываем редакторы TinyMCE для английского языка
        enElements.forEach(elem => {
            if (!elem.id) return;
            const editor = window.tinymce.get(elem.id);
            if (editor) {
                const editorContainer = editor.getContainer();
                if (editorContainer) {
                    editorContainer.style.display = lang === 'en' ? '' : 'none';
                }
            }
        });
    }
});