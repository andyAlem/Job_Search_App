from typing import List, Dict
from src.API_hh import HHJobPlatform

def print_vacancies(vacancies: List[Dict]) -> None:
    """Выводит информацию о вакансиях."""
    if not vacancies:
        print("Вакансии не найдены.")
        return

    print(f"Найдено вакансий: {len(vacancies)}")
    for i, vacancy in enumerate(vacancies, start=1):
        print(f"\nВакансия #{i}")
        print(f"Название: {vacancy.get('name', 'Не указано')}")
        print(f"Ссылка: {vacancy.get('alternate_url', 'Не указана')}")
        salary = vacancy.get('salary')
        if salary:
            salary_from = salary.get('from', 'Не указано')
            salary_to = salary.get('to', 'Не указано')
            currency = salary.get('currency', '')
            print(f"Зарплата: от {salary_from} до {salary_to} {currency}")
        else:
            print("Зарплата: Не указана")
        print("-" * 40)

def main() -> None:
    hh_api = HHJobPlatform()

    if not hh_api.connect():
        print("Не удалось подключиться к API hh.ru.")
        return

    # ищем по питону "Python"
    search_query = "Python"
    vacancies = hh_api.get_vacancies(search_query, per_page=20)

    print_vacancies(vacancies)

if __name__ == "__main__":
    main()