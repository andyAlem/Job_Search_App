from io import StringIO # https://www.askpython.com/python/string/stringio-in-python3
from unittest import mock

from src.API_hh import HHJobPlatform
from src.file_storage import JSONVacancyStorage
from src.main import print_vacancies, user_interaction


def test_print_vacancies(mock_vacancies):
    """Тест функции вывода вакансий."""
    with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        print_vacancies(mock_vacancies)
        output = mock_stdout.getvalue()
        assert "Найдено вакансий: 2" in output
        assert "Вакансия #1" in output
        assert "Python Developer" in output
        assert "Вакансия #2" in output
        assert "Java Developer" in output


@mock.patch.object(HHJobPlatform, "connect", return_value=True)
@mock.patch.object(
    HHJobPlatform,
    "get_vacancies",
    return_value=[
        {
            "name": "Python Developer",
            "apply_alternate_url": "https://primer.com",
            "salary": {"from": 100000, "to": 150000},
            "department": {"name": "Django Developer"},
        },
        {
            "name": "Java Developer",
            "apply_alternate_url": "https://primer.com",
            "salary": {"from": 120000, "to": 180000},
            "department": {"name": "Java Developer"},
        },
    ],
)
@mock.patch("builtins.input", side_effect=["Python", "5", "Django", "да"])
@mock.patch.object(JSONVacancyStorage, "add_vacancies", return_value=None)
def test_user_interaction(mock_input, mock_get_vacancies, mock_connect, mock_save_vacancies):
    """Тест функции взаимодействия с пользователем."""

    with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        user_interaction()
        output = mock_stdout.getvalue()

        assert "Найдено вакансий:" in output
        assert "Топ 5 вакансий по зарплате:" in output
        assert "Найдено 1 вакансий с ключевым словом 'Django':" in output
        assert "Результаты сохранены в файл vacancies.json." in output
        assert "Спасибо за использование программы!" in output


@mock.patch.object(HHJobPlatform, "connect", return_value=True)
@mock.patch.object(HHJobPlatform, "get_vacancies", return_value=[])
@mock.patch("builtins.input", side_effect=["Python", "5", "Django", "да"])
@mock.patch.object(JSONVacancyStorage, "add_vacancies", return_value=None)
def test_no_vacancies_found(mock_input, mock_get_vacancies, mock_connect, mock_save_vacancies):
    """Тест, когда вакансии не найдены по запросу."""

    with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        user_interaction()
        output = mock_stdout.getvalue()

        assert "По вашему запросу вакансий не найдено." in output


@mock.patch.object(HHJobPlatform, "connect", return_value=True)
@mock.patch.object(
    HHJobPlatform,
    "get_vacancies",
    return_value=[
        {
            "name": "Python Developer",
            "apply_alternate_url": "https://primer.com",
            "salary": {"from": 100000, "to": 150000},
            "department": {"name": "Django Developer"},
        }
    ],
)
@mock.patch("builtins.input", side_effect=["", "5", "Django", "да"])
@mock.patch.object(JSONVacancyStorage, "add_vacancies", return_value=None)
def test_empty_search_query(mock_input, mock_get_vacancies, mock_connect, mock_save_vacancies):
    """Тест, когда поисковый запрос пустой."""

    with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        user_interaction()
        output = mock_stdout.getvalue()

        assert "Поисковый запрос не может быть пустым." in output


@mock.patch.object(HHJobPlatform, "connect", return_value=False)
def test_failed_api_connection(mock_connect):
    """Тест, когда не удается подключиться к API."""

    with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        user_interaction()
        output = mock_stdout.getvalue()

        assert "Не удалось подключиться к API hh.ru." in output
