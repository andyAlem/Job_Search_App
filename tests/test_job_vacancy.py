import pytest

from src.job_vacancy import JobVacancy


def test_job_vacancy_creation_valid():
    """Тест на создание вакансии с корректными данными."""
    vacancy = JobVacancy(
        name="Python Developer",
        url="http://primer.com",
        min_salary=100000,
        max_salary=150000,
        description="Разработка на Python",
    )

    assert vacancy.name == "Python Developer"
    assert vacancy.url == "http://primer.com"
    assert vacancy.min_salary == 100000
    assert vacancy.max_salary == 150000
    assert vacancy.description == "Разработка на Python"


def test_job_vacancy_creation_invalid_salary():
    """Тест на создание вакансии с некорректными данными (min_salary > max_salary)."""
    with pytest.raises(ValueError, match="Минимальная зарплата не может быть больше максимальной."):
        JobVacancy(name="Python Developer", url="http://primer.com", min_salary=200000, max_salary=150000)


def test_job_vacancy_creation_missing_name_or_url():
    """Тест на создание вакансии без обязательных полей (name или url)."""
    with pytest.raises(ValueError, match="Название вакансии и URL обязательны."):
        JobVacancy(name="", url="http://primer.com", min_salary=100000, max_salary=150000)


def test_job_vacancy_comparison():
    """Тест на сравнение вакансий по средней зарплате."""
    vacancy_1 = JobVacancy(name="Python Developer", url="http://primer.com", min_salary=100000, max_salary=150000)
    vacancy_2 = JobVacancy(name="Java Developer", url="http://primer.com", min_salary=120000, max_salary=180000)

    assert vacancy_1 < vacancy_2


def test_job_vacancy_convert_to_dict():
    """Тест на конвертацию вакансии в словарь."""
    vacancy = JobVacancy(name="Python Developer", url="http://primer.com", min_salary=100000, max_salary=150000)
    vacancy_dict = vacancy.convert_to_dict()

    assert vacancy_dict == {
        "name": "Python Developer",
        "url": "http://primer.com",
        "min_salary": 100000,
        "max_salary": 150000,
        "description": "Описание не указано",
    }


def test_job_vacancy_create_from_api_data():
    """Тест на создание вакансий из данных API."""
    api_data = [
        {
            "name": "Python Developer",
            "apply_alternate_url": "http://primer.com",
            "salary": {"from": 100000, "to": 150000},
            "department": {"name": "Разработка на Python"},
        },
        {
            "name": "Java Developer",
            "apply_alternate_url": "http://primer.com",
            "salary": {"from": 120000, "to": 180000},
            "department": {"name": "Разработка на Java"},
        },
    ]

    vacancies = JobVacancy.create_from_api_data(api_data)

    assert len(vacancies) == 2
    assert vacancies[0].name == "Python Developer"
    assert vacancies[1].name == "Java Developer"
    assert vacancies[0].description == "Разработка на Python"
    assert vacancies[1].description == "Разработка на Java"
