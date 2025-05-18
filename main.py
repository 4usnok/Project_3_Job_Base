import logging

import psycopg2
from src.api_for_employers import WorkingWithEmployers
from src.api_for_vacancies import WorkingWithVacancies
from src.work_bd import DBManager


def main():
    """Управляющая функция"""
    # Настройка логирования
    path_to_log = 'logs/main_log.log'
    logging.basicConfig(filename=path_to_log, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")

    # `input_field` - это поле ввода для названия компании, информация о которой, добавляется в БД.
    input_field = "остин"
    # При отсутствии, либо названии, которое раньше было использовано, у нас происходит падения программы
    # Чтобы этого избежать, мы обрабатываем исключения
    try:
        if input_field != "":
            obj_cl_e = WorkingWithEmployers(10, input_field)
            obj_cl_v = WorkingWithVacancies(10, input_field)
            obj_cl_e.load_for_employ()
            obj_cl_v.load_for_vac()
        else:
            pass
    except psycopg2.Error:
        # Воспользуемся библиотекой logging, чтобы не перегружать информацией консоль
        logging.exception("Ошибка")

    print(
        "Здравствуйте!"
        "\nДанная программа, предоставляет пользователю информацию о компаниях и их вакансиях с hh.ru.\n"
        "Здесь доступны такие операции, как:\n"
        "1. Просмотр списка информации об всех доступных компаниях и их вакансиях;\n"
        "2. Просмотр списка средней зарплаты по вакансиям;\n"
        "3. Просмотр списка вакансий, у которых зарплата выше средней;\n"
        "4. Просмотра списка всех вакансий, по ключевому слову в названии, переданное пользователем;\n"
        "\nДля того, чтобы выбрать одну из операций, просто введите номер операции в предназначенном для этого поле.\n"
    )
    # Создадим экземпляр класса и вызовем его
    class_db = DBManager()
    input_db = input("Введите номер операции: ")
    # Ветвления необходимы для целостной работы программы в главном модуле
    if input_db == "1":
        return class_db.get_all_vacancies()
    elif input_db == "2":
        return f"Средняя зарплата: {class_db.get_avg_salary()}"
    elif input_db == "3":
        return class_db.get_vacancies_with_higher_salary()
    elif input_db == "4":
        return class_db.get_vacancies_with_keyword()

if __name__ == '__main__':
    print(main())