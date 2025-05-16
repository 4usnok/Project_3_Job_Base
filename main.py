from src.work_api import ApiWork
from src.work_bd import DBManager


def main():
    """Управляющая функция"""
    print(
        "Здравствуйте!\nДанная программа"
        ", позволяет пользователю получать информацию "
        "с сайта hh.ru о данных вакансий той или иной компании.\n"
        "\nШаг 1."
        "\nНа этом шаге, пользователь может загрузить в БД данные об интересующей его компании и её вакансиях."
    )
    input_add = input("Добавить новую компанию(да/нет): ")
    if input_add.lower() == "да".lower():
        obj_class = ApiWork(10)
        obj_class.load_for_employ()
        obj_class.load_for_vac()
    elif input_add.lower() == "нет".lower():
        pass

    print(
        "\nШаг 2.\n"
          "На этом шаге, пользователь достаёт данные о вакансиях, ему доступны такие операции с базой данных, как:\n"
          "1. Просмотр списка всех вакансий;\n"
          "2. Просмотр списка средней зарплаты по вакансиям;\n"
          "3. Просмотр списка вакансий, у которых зарплата выше средней;\n"
          "4. Просмотра списка всех вакансий, по ключевому слову в названии, переданное пользователем;\n"
          "Для того, чтобы выбрать одну из операций, просто введите номер операции в предназначенном для этого поле.\n"
    )
    class_db = DBManager()
    input_db = input("Введите номер операции: ")
    if input_db == "1":
        return class_db.get_all_vacancies()
    elif input_db == "2":
        return f"Средняя зарплата: {class_db.get_avg_salary()}"
    elif input_db == "3":
        return class_db.get_vacancies_with_higher_salary()
    elif input_db == "4":
        return class_db.get_vacancies_with_keyword()

print(main())