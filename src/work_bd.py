import logging

import psycopg2
from tabulate import tabulate


class DBManager:

    __slots__ = ('conn', 'cur')

    def __init__(self):
        """Конструктор"""
        self.conn = psycopg2.connect(
            host="localhost", database="data_base", user="postgres", password="10121331"
        )
        self.cur = self.conn.cursor()

        # Настройка логирования
        logging.basicConfig(
            filename="../logs/main_log.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        )
        logging.debug("A DEBUG Message")
        logging.info("An INFO")
        logging.warning("A WARNING")
        logging.error("An ERROR")
        logging.critical("A message of CRITICAL severity")

    def get_companies_and_vacancies_count(self):
        """Метод может получать, список всех компаний из таблицы employers,
        так и количество вакансий из таблицы vacancies."""
        try:
            self.cur.execute(
                "SELECT employers.employers_name, employers.employers_item, vacancies.vac_name "
                "FROM employers "
                "JOIN vacancies "
                "ON vacancies.vacancies_id=employers.employers_id;"
            )
            # Получаем данные
            rows = self.cur.fetchall()
            headers = [
                desc[0] for desc in self.cur.description
            ]  # Получаем названия колонок
        finally:
            self.cur.close()
            self.conn.close()

        # Выводим таблицу
        print("\nТаблица со всеми компаниями и количеством вакансий:")
        print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))

    def get_all_vacancies(self):
        """
        Получает список всех вакансий:
        с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        try:
            self.cur.execute(
                "SELECT "
                "employers.employers_name, "
                "vacancies.vac_name, "
                "vacancies.salary_from, "
                "vacancies.salary_to, "
                "vacancies.currency, "
                "employers.employers_vacancies_url "
                "FROM employers "
                "INNER JOIN vacancies "
                "ON vacancies.vacancies_id=employers.employers_id;"
            )

            # Получаем данные
            rows = self.cur.fetchall()
            headers = [
                desc[0] for desc in self.cur.description
            ]  # Получаем названия колонок

            # Выводим таблицу
            print("\nСписок вакансий:")
            print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))
        finally:
            self.cur.close()
            self.conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        try:
            all_overage = (
                "AVG((salary_from + salary_to) / 2)"  # Находим общую среднюю зарплату
            )
            self.cur.execute(f"SELECT {all_overage} " "FROM vacancies;")

            # Получаем данные
            rows = self.cur.fetchall()
            headers = [
                desc[0] for desc in self.cur.description
            ]  # Получаем названия колонок

            # Выводим таблицу
            print("\nСредние зарплаты по вакансиям:")
            print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))
        finally:
            self.cur.close()
            self.conn.close()

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых средняя зарплата выше средней по всем вакансиям."""
        try:
            all_overage = (
                "AVG((salary_from + salary_to) / 2)"  # Находим общую среднюю зарплату
            )
            overall_average = "(salary_from + salary_to) / 2"  # Находим среднюю зарплату к каждой вакансии
            self.cur.execute(
                f"SELECT vac_name AS vacancies_name, {overall_average} AS average_salary "
                "FROM vacancies "
                f"WHERE {overall_average} > ("
                f"SELECT {all_overage} "
                f"FROM vacancies );"
            )

            # Получаем данные
            rows = self.cur.fetchall()
            headers = [
                desc[0] for desc in self.cur.description
            ]  # Получаем названия колонок

            # Выводим таблицу
            print("\nВакансии с зарплатой выше средней:")
            print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))
        finally:
            self.cur.close()
            self.conn.close()

    def get_vacancies_with_keyword(self):
        """Метод получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python."""
        try:
            keyword = input(
                "Ключевое слово: "
            )  # При запуске программы, будет служить поиском по названию вакансий
            self.cur.execute(
                "SELECT vac_name, salary_from, salary_to, currency "
                "FROM vacancies "
                f"WHERE vac_name LIKE '{keyword}%';"
            )

            # Получаем данные
            rows = self.cur.fetchall()
            headers = [
                desc[0] for desc in self.cur.description
            ]  # Получаем названия колонок

            # Выводим таблицу
            print(
                "\nВакансии, в названии которых содержатся переданные в метод слова, например python:"
            )
            print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))
        finally:
            self.cur.close()
            self.conn.close()
