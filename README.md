# Diploma-Project
Учебный репозиторий - Дипломный проект по автоматизации тестирования сайта Читай - город

## Содержание 
-  [Стек](#Стек)
-  [Структура проекта](#Структура проекта)
-  [Установка](#Установка)
-  [Запуск тестов](#Запуск тестов )
-  [Формирование отчета](#Формирование отчета)

## Стек 
 - **Python**
 - **Selenium**
 - **pytest**
 - **requests**
 - **allure**

## Структура проекта 
📁 Diploma-Project/

    📁 data/                   # Тестовые данные
       search_queries.py
    📁 pages/                  # Page Object Model
       __init__.py
       catalog_page.py
       cart_page.py
    📁 tests/                  # UI тесты
       __init__.py
       test_ui.py 
    📁 test_API/               # API тесты
       __init__.py
       tests_book_api.py
     📁 allure-results/         # Allure отчеты
    📄 conftest.py             # Фикстуры pytest
    📄 pytest.ini              # Настройки pytest
    📄 requirements.txt        # Зависимости 
    📄 config.py               # Настройки (URL, токены)
    📄 .gitignore
    📄 README.md

## Установка 
 - Склонировать репозиторий 'git clone https://github.com/SvetlanaZavada/Diploma-Project.git'
 - Создать и активировать виртуальное окружеие
 - Установить библиотеки 'pip install -r requirements.txt'

## Запуск тестов 
Запуск ui тестов  pytest -m ui -v
Запуск api тестов pytest -m api -v 
Запуск всех тестов  pytest -v

## Формирование отчета 
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
  
Ссылка на финальный проект https://svetlana84.yonote.ru/share/bbed7b1c-a514-441d-b872-5756e99e7203