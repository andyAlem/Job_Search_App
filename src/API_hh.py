import requests

from src.abstract_class import JobPlatformAPI


class HHJobPlatform(JobPlatformAPI):
    def __init__(self, base_url="https://api.hh.ru/vacancies") -> None:
        self.base_url = base_url

    def connect(self) -> bool:
        """Метод проверяющий доступность API"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return False

    def get_vacancies(self, search_query: str, per_page: int = 20):
        """Получаем вакансии с платформы hh.ru по заданному запросу и количеству на страницу."""
        params = {"text": search_query, "per_page": per_page}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return []
