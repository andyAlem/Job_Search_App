from abc import ABC, abstractmethod


class JobPlatformAPI(ABC):
    @abstractmethod
    def connect(self):
        """Метод для подключения к API платформам для сбора вакансий."""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, page: int = 1):
        """Метод для получения списка вакансий по поисковому запросу."""
        pass
