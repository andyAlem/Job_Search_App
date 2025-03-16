import tempfile

import pytest

from src.API_hh import HHJobPlatform
from src.file_storage import JSONVacancyStorage
from src.job_vacancy import JobVacancy


@pytest.fixture
def hh_api():
    """Создаем HHJobPlatform."""
    return HHJobPlatform()


@pytest.fixture
def vacancy_storage():
    """Фикстура для создания экземпляра JSONVacancyStorage с временным файлом."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Создаем путь к файлу внутри временной директории
        file_path = f"{temp_dir}/vacancies.json"
        yield JSONVacancyStorage(file_path=file_path)


@pytest.fixture
def mock_vacancies():
    """Фикстура для создания списка вакансий."""
    return [
        JobVacancy(
            name="Python Developer",
            url="https://primer.com",
            min_salary=100000,
            max_salary=150000,
            description="Django, Python",
        ),
        JobVacancy(
            name="Java Developer",
            url="https://primer.com",
            min_salary=120000,
            max_salary=180000,
            description="Spring, Java",
        ),
    ]
