from unittest import mock

from src.job_vacancy import JobVacancy


def test_add_vacancies(vacancy_storage):
    """Тест на добавление вакансий в хранилище."""
    vacancy1 = mock.Mock(spec=JobVacancy)
    vacancy1.convert_to_dict.return_value = {"id": 1, "name": "Python Developer"}

    vacancy2 = mock.Mock(spec=JobVacancy)
    vacancy2.convert_to_dict.return_value = {"id": 2, "name": "Java Developer"}

    with mock.patch.object(vacancy_storage, "_load_data", return_value=[]), mock.patch.object(
        vacancy_storage, "_save_data"
    ) as mock_save:
        vacancy_storage.add_vacancies([vacancy1, vacancy2])

        mock_save.assert_called_once_with([{"id": 1, "name": "Python Developer"}, {"id": 2, "name": "Java Developer"}])


def test_get_vacancies(vacancy_storage):
    """Тест на получение вакансий по критериям."""
    mock_data = [
        {"id": 1, "name": "Python Developer", "min_salary": 100000, "max_salary": 150000},
        {"id": 2, "name": "Java Developer", "min_salary": 120000, "max_salary": 180000},
    ]

    with mock.patch.object(vacancy_storage, "_load_data", return_value=mock_data):

        criteria = {"min_salary": (100000, 180000)}
        result = vacancy_storage.get_vacancies(criteria)

        assert len(result) == 2
        assert result[0]["name"] == "Python Developer"
        assert result[1]["name"] == "Java Developer"


def test_delete_vacancies(vacancy_storage):
    """Тест на удаление вакансий по критериям."""
    mock_data = [
        {"id": 1, "name": "Python Developer", "min_salary": 100000, "max_salary": 150000},
        {"id": 2, "name": "Java Developer", "min_salary": 120000, "max_salary": 180000},
    ]

    with mock.patch.object(vacancy_storage, "_load_data", return_value=mock_data), mock.patch.object(
        vacancy_storage, "_save_data"
    ) as mock_save:
        criteria = {"name": "Java Developer"}
        vacancy_storage.delete_vacancies(criteria)

        mock_save.assert_called_once_with(
            [{"id": 1, "name": "Python Developer", "min_salary": 100000, "max_salary": 150000}]
        )


def test_load_data_file_not_found(vacancy_storage):
    """Тест на обработку ошибки при отсутствии файла."""

    with mock.patch("builtins.open", side_effect=FileNotFoundError):
        with mock.patch.object(vacancy_storage, "_save_data") as mock_save:
            data = vacancy_storage._load_data()
            mock_save.assert_called_once_with([])


def test_load_data_invalid_json(vacancy_storage):
    """Тест на обработку ошибки при поврежденном JSON-файле."""
    with mock.patch("builtins.open", mock.mock_open(read_data="invalid json")), mock.patch.object(
        vacancy_storage, "_save_data"
    ) as mock_save:
        data = vacancy_storage._load_data()
        mock_save.assert_called_once_with([])
