import logging

import psycopg2

from src.api_for_employers import WorkingWithEmployers
from src.api_for_vacancies import WorkingWithVacancies
from src.work_db import DBManager


def point_of_contact():
    """Управляющая функция"""
    # Настройка логирования
    path_to_log = "logs/main_log.log"
    logging.basicConfig(
        filename=path_to_log,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    )
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")

    # `input_field` - это поле ввода для названия компании, информация о которой, добавляется в БД.
    input_field = "Остин"
    # При отсутствии, либо названии, которое раньше было использовано, у нас происходит падения программы
    # Чтобы этого избежать, мы обрабатываем исключения.
    # Создадим блок для создания таблиц с вакансиями и компаниями
    try:
        if input_field != "":
            obj_cl_for_create_e = WorkingWithEmployers(10, input_field)
            obj_cl_for_create_v = WorkingWithVacancies(10, input_field)
            obj_cl_for_create_e.create_table_for_employers()
            obj_cl_for_create_v.create_table_for_vacancies()
        else:
            pass
    except psycopg2.Error:
        # Воспользуемся библиотекой logging, чтобы не перегружать информацией консоль
        logging.exception("Ошибка")

    # Создадим блок для загрузки данных в таблицы
    try:
        obj_for_load_e = WorkingWithEmployers(10, input_field)
        obj_for_load_v = WorkingWithVacancies(10, input_field)
        obj_for_load_e.load_for_employ()
        obj_for_load_v.load_for_vac()
    except psycopg2.Error:
        # Воспользуемся библиотекой logging, чтобы не перегружать информацией консоль
        logging.exception("Ошибка")
    print(
        "Здесь доступны такие операции, как:\n"
        "1. Просмотр информации об всех доступных компаниях и их вакансиях;\n"
        "2. Просмотр всех вакансий указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию;\n"
        "3. Просмотр общей средней зарплаты по вакансиям;\n"
        "4. Просмотр всех вакансий, у которых средняя зарплата выше средней по всем вакансиям;\n"
        "5. Просмотр всех вакансий, в названии которых содержатся переданные в метод слова, например python;\n"
        "\nДля того, чтобы выбрать одну из операций, просто введите номер операции в предназначенном для этого поле.\n"
    )
    # Создадим экземпляр класса и вызовем его
    class_db = DBManager()
    input_db = input("Введите номер операции: ")
    # Ветвления необходимы для целостной работы программы в главном модуле
    if input_db == "1":
        return class_db.get_companies_and_vacancies_count()
    if input_db == "2":
        return class_db.get_all_vacancies()
    elif input_db == "3":
        return class_db.get_avg_salary()
    elif input_db == "4":
        return class_db.get_vacancies_with_higher_salary()
    elif input_db == "5":
        return class_db.get_vacancies_with_keyword()


if __name__ == "__main__":
    print(
        "Здравствуйте! Данная программа, предоставляет пользователю информацию о компаниях и их вакансиях с hh.ru.\n"
    )
    start_input = input("Начать работу программы (нет/да): \n").lower()
    while start_input == "да":
        print(point_of_contact())
        while True:
            req_input = input("Повторить работу программы (нет/да): \n").lower()
            if req_input == "да":
                print(point_of_contact())
            elif req_input == "нет":
                print("Работа программы завершена.")
                exit()
            else:
                print("Ошибка: введите 'да' или 'нет'.")
