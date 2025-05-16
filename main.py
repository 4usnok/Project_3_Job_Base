from src.work_api import ApiWork
from src.work_bd import DBManager


def main():
    """Управляющая функция"""
    print(
        "Здравствуйте! Данная "
        ", позволяет пользователю получать информацию "
        "с сайта hh.ru о данных вакансий той или иной компании.\n"
        "\nШаг 1."
        "\nНа этом шаге, пользователь производит загрузку данных о компаниях "
        "в БД из которой в дальнейшем сможет доставать информацию."
    )
    class_api = ApiWork(10)
    class_api.load_for_employ()
    class_api.load_for_vac()


    print(
        "\nШаг 2.\n"
          "На этом шаге, пользователь достаёт данные о вакансиях, ему доступны такие операции с базой данных, как:\n"
          "1. Список всех вакансий;\n"
          "2. Средняя зарплата по вакансиям;\n"
          "3. Список вакансий, у которых зарплата выше средней;\n"
          "4. Список всех вакансий, по ключевому слову в названии, переданное пользователем;\n"
          "Для того, чтобы выбрать одну из операций, просто введите номер операции ниже в предназначенном для этого поле.\n"
    )
    class_db = DBManager()
    input_db = input("Введите число: ")
    if input_db == "1":
        return class_db.get_all_vacancies()
    elif input_db == "2":
        return f"Средняя зарплата: {class_db.get_avg_salary()}"
    elif input_db == "3":
        return class_db.get_vacancies_with_higher_salary()
    elif input_db == "4":
        return class_db.get_vacancies_with_keyword()

print(main())