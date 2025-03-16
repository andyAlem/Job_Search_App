# Проект 2. Поиск вакансий

## Программа получает вакансии с платформы hh.ru при помощи API, сохраняет их в файл json


Структура проекта
- Абстрактный класс для работы с API сервиса с вакансиями
- Класс для работы с вакансиями
- Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл
- Получение данных из файла по указанным критериям и удаления информации о вакансиях
- Функция для взаимодействия с пользователем
- Описанный функционал покрыт тестами

### Зависимости:
[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.32.3"
requests-mock = "^1.12.1"

[tool.poetry.dev-dependencies]

[tool.poetry.group.lint.dependencies]
flake8 = "^7.1.2"
mypy = "^1.15.0"
black = "^25.1.0"
isort = "^6.0.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
pytest-cov = "^6.0.0"
requests-mock = "^1.11.0"

https://drive.google.com/file/d/1BVRjq02dCHADlg5a7BZXETGe0Pu9e-ob/view?usp=sharing
https://drive.google.com/file/d/1JFM9V2eMNvnbn9JpyrJAOZ6Je3VPR9z6/view?usp=sharing
