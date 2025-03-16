import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from src.job_vacancy import JobVacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с файлами, который позволит сохранять вакансии, читать их и удалять."""

    @abstractmethod
    def add_vacancies(self, vacancies: List[JobVacancy]):
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict):
        pass

    @abstractmethod
    def delete_vacancies(self, criteria: Dict):
        pass


class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_path: str = None) -> None:
        """Инициализация хранилища вакансий с указанием пути к JSON-файлу."""
        default_path = Path("/home/andrej/Poetry_homework/Job_Search_App/data/vacancies.json")
        self.__file_path = Path(file_path) if file_path else default_path

        self.__file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.__file_path.exists():
            self._save_data([])

    def _load_data(self) -> List[Dict]:
        """Приватный метод для безопасной загрузки данных из JSON-файла."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except (FileNotFoundError, json.JSONDecodeError):
            print("Ошибка: JSON-файл поврежден или отсутствует. Создаем новый файл.")
            self._save_data([])
            return []

    def _save_data(self, data: List[Dict]) -> None:
        """Приватный метод для сохранения данных в JSON-файл."""
        try:
            with open(self.__file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных в файл: {e}")

    def add_vacancies(self, vacancies: List[JobVacancy]) -> None:
        """Добавляет список вакансий в JSON-файл, избегая дублирования."""
        data = self._load_data()
        for vacancy in vacancies:
            vacancy_dict = vacancy.convert_to_dict()
            if vacancy_dict not in data:
                data.append(vacancy_dict)
        self._save_data(data)

    def get_vacancies(self, criteria: Dict) -> List[Dict]:
        """Возвращает список вакансий, соответствующих заданным критериям."""
        data = self._load_data()
        result = []

        for item in data:
            match = True
            for key, value in criteria.items():
                if key in ["min_salary", "max_salary"] and isinstance(value, tuple):
                    if not (value[0] <= item.get(key, 0) <= value[1]):
                        match = False
                elif isinstance(value, str) and value.lower() not in str(item.get(key, "")).lower():
                    match = False
                elif item.get(key) != value:
                    match = False
            if match:
                result.append(item)

        return result

    def delete_vacancies(self, criteria: Dict) -> None:
        """Удаляет вакансии, соответствующие заданным критериям, из JSON-файла."""
        data = self._load_data()
        data = [item for item in data if not all(item.get(key) == value for key, value in criteria.items())]
        self._save_data(data)
