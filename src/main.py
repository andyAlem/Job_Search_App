from typing import List

from src.API_hh import HHJobPlatform
from src.file_storage import JSONVacancyStorage
from src.job_vacancy import JobVacancy


def print_vacancies(vacancies: List[JobVacancy]) -> None:
    """Выводит информацию о вакансиях."""
    if not vacancies:
        print("Вакансии не найдены.")
        return

    print(f"Найдено вакансий: {len(vacancies)}")
    for i, vacancy in enumerate(vacancies, start=1):
        print(f"\nВакансия #{i}")
        print(vacancy)
        print("-" * 40)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""
    hh_api = HHJobPlatform()

    if not hh_api.connect():
        print("Не удалось подключиться к API hh.ru.")
        return

    search_query = input("Введите поисковый запрос: ")
    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    platform_data = hh_api.get_vacancies(search_query, per_page=100)  # до 100 вакансий
    vacancies = JobVacancy.create_from_api_data(platform_data)

    if not vacancies:
        print("По вашему запросу вакансий не найдено.")
        return

    try:
        top_n = int(input("Введите количество вакансий для вывода: "))
    except ValueError:
        print("Некорректное значение. Будет выведено 10 вакансий.")
        top_n = 10

    sorted_vacancies = sorted(vacancies, reverse=True)[:top_n]

    print(f"\nТоп {top_n} вакансий по зарплате:")
    print_vacancies(sorted_vacancies)

    keyword = input("\nВведите ключевое слово для поиска в описании (например, 'Django'): ")
    if keyword:
        filtered_vacancies = [v for v in vacancies if keyword.lower() in v.description.lower()]
        if filtered_vacancies:
            print(f"\nНайдено {len(filtered_vacancies)} вакансий с ключевым словом '{keyword}':")
            print_vacancies(filtered_vacancies)
        else:
            print(f"Вакансий с ключевым словом '{keyword}' не найдено.")

    save_option = input("\nХотите сохранить результаты в файл? (да/нет): ").lower()
    if save_option == "да":
        storage = JSONVacancyStorage()
        storage.add_vacancies(vacancies)
        print("Результаты сохранены в файл vacancies.json.")

    print("\nСпасибо за использование программы!")


if __name__ == "__main__":
    user_interaction()
