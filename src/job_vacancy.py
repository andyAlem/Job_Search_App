from typing import Dict, List


class JobVacancy:
    """Класс для представления вакансии с атрибутами, такими как название, ссылка, зарплата, описание,
    а также методы для сравнения вакансий по зарплате и валидации данных."""

    __slots__ = ["name", "url", "min_salary", "max_salary", "description"]

    def __init__(
        self, name: str, url: str, min_salary: int = None, max_salary: int = None, description: str = None
    ) -> None:
        self.name = name
        self.url = url
        self.min_salary = min_salary if min_salary is not None else 0
        self.max_salary = max_salary if max_salary is not None else 0
        self.description = description or "Описание не указано"

        self._validate_data()

    def _validate_data(self) -> None:
        """Приватный метод для валидации данных вакансии."""
        if not self.name or not self.url:
            raise ValueError("Название вакансии и URL обязательны.")
        if self.min_salary < 0 or self.max_salary < 0:
            raise ValueError("Зарплата не может быть меньше 0.")
        if self.min_salary > self.max_salary:
            raise ValueError("Минимальная зарплата не может быть больше максимальной.")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта JobVacancy."""
        return f"Вакансия: {self.name}, Зарплата: {self.min_salary}-{self.max_salary}, URL: {self.url}"

    def __lt__(self, other: "JobVacancy") -> bool:
        """Сравнение вакансий по средней зарплате (меньше)."""
        return (self.min_salary + self.max_salary) / 2 < (other.min_salary + other.max_salary) / 2

    def __gt__(self, other: "JobVacancy") -> bool:
        """Сравнение вакансий по средней зарплате (больше)."""
        return (self.min_salary + self.max_salary) / 2 > (other.min_salary + other.max_salary) / 2

    @staticmethod
    def create_from_api_data(api_data: List[Dict]) -> List["JobVacancy"]:
        """Создает список объектов JobVacancy из данных, полученных от API."""
        vacancies = []
        for job_data in api_data:
            name = job_data.get("name", "Название не указано")
            url = job_data.get("apply_alternate_url", "")  # Например, можно взять альтернативный URL отклика

            salary_data = job_data.get("salary") or {}

            min_salary = salary_data.get("from")
            max_salary = salary_data.get("to")

            min_salary = min_salary if min_salary is not None else 0
            max_salary = max_salary if max_salary is not None else 0

            if min_salary > max_salary:
                min_salary, max_salary = max_salary, min_salary

            department = job_data.get("department")
            description = department.get("name", "Описание не указано") if department else "Описание не указано"

            vacancy = JobVacancy(
                name=name, url=url, min_salary=min_salary, max_salary=max_salary, description=description
            )
            vacancies.append(vacancy)
        return vacancies

    def convert_to_dict(self) -> Dict:
        """Преобразует экземпляр класса JobVacancy в словарь."""
        return {
            "name": self.name,
            "url": self.url,
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "description": self.description,
        }
