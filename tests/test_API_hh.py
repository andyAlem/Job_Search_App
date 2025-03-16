import requests_mock


def test_connect_success(hh_api):
    """Тест успешного подключения к API."""
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", status_code=200)
        assert hh_api.connect() is True


def test_connect_failure(hh_api):
    """Тест неудачного подключения к API."""
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", status_code=500)
        assert hh_api.connect() is False


def test_get_vacancies_success(hh_api):
    """Тест успешного получения вакансий."""
    mock_data = {
        "items": [
            {"id": "1", "name": "Python Developer", "salary": {"from": 100000, "to": 150000}},
            {"id": "2", "name": "Java Developer", "salary": {"from": 120000, "to": 180000}},
        ]
    }
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", json=mock_data, status_code=200)
        vacancies = hh_api.get_vacancies("Python", per_page=20)
        assert len(vacancies) == 2
        assert vacancies[0]["name"] == "Python Developer"
        assert vacancies[1]["name"] == "Java Developer"


def test_get_vacancies_failure(hh_api):
    """Тест неудачного получения вакансий."""
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", status_code=500)
        vacancies = hh_api.get_vacancies("Python", per_page=20)
        assert len(vacancies) == 0


def test_get_vacancies_empty_response(hh_api):
    """Тест получения пустого ответа от API."""
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", json={"items": []}, status_code=200)
        vacancies = hh_api.get_vacancies("Python", per_page=20)
        assert len(vacancies) == 0


def test_get_vacancies_invalid_json(hh_api):
    """Тест получения некорректного JSON-ответа."""
    with requests_mock.Mocker() as m:
        m.get("https://api.hh.ru/vacancies", text="invalid json", status_code=200)
        vacancies = hh_api.get_vacancies("Python", per_page=20)
        assert len(vacancies) == 0
