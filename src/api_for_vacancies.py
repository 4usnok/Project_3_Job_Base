import logging

import psycopg2
import requests


class WorkingWithVacancies:
    __slots__ = (
        "input_employer",
        "num",
        "result_employer",
        "res_vac",
        "res_employ",
        "result_vac",
    )

    def __init__(self, num, input_employer):
        """Конструктор"""
        self.input_employer = input_employer
        self.num = num
        self.result_employer = None
        self.res_vac = None
        self.res_employ = None
        self.result_vac = None

        # Настройка логирования
        path_to_log = "../logs/api_log.log"
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

    def data_employers_api(self):
        """Метод api для получения данных о работодателях с сайта hh.ru"""

        url = "https://api.hh.ru/employers"
        # Запрос к api компаний
        try:
            response_employer = requests.get(
                url,
                params={
                    "text": self.input_employer,  # Название компании
                    "per_page": self.num,  # Ограничение на кол-во результатов
                },
                timeout=120,
            )
            self.result_employer = response_employer.json()
            if not isinstance(self.result_employer, dict):
                raise ValueError("Некорректный формат данных от API")
            self.result_employer = response_employer.json()
            return self.result_employer
        except requests.exceptions.HTTPError as e:
            logging.error(f"Ошибка API: {e}")
            self.result_employer = None

    def __data_employers_api(self):
        """Приватный метод работы с API"""
        return self.data_employers_api

    def load_for_vac(self):
        """Метод работы с api-данными перед загрузкой содержимого таблицы vacancies в БД"""
        if (
            self.result_employer is None
        ):  # Проверка на обновлённую переменную - self.result_employer
            self.data_employers_api()
        if self.result_employer["found"] >= self.num:
            for item_employ in self.result_employer["items"]:  # Данные о компаниях
                response_vac = requests.get(item_employ["vacancies_url"])
                self.result_vac = response_vac.json()
                for vac_name in self.result_vac.get("items", None):
                    salary = vac_name.get("salary_range", 0)
                    if salary is not None:
                        salary = vac_name.get("salary_range", 0)
                        id_employers = item_employ["id"]
                        name_vac = vac_name.get("name", None)
                        salary_from = salary.get("from")
                        salary_to = salary.get("to")
                        currency = salary.get("currency")
                        self.__load_for_vac(
                            id_employers, name_vac, salary_from, salary_to, currency
                        )

    def __load_for_vac(self, id_employers, name_vac, salary_from, salary_to, currency):
        """Приватный метод загрузки данных таблицы vacancies в БД"""
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="data_base",
                user="postgres",
                password="10121331",
            )
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                    (id_employers, name_vac, salary_from, salary_to, currency),
                )
                cur.execute("SELECT * FROM employers")
                cur.execute(
                    "ALTER TABLE vacancies ADD CONSTRAINT unique_vacancy UNIQUE (vacancies_id, vac_name);"
                )
                conn.commit()  # сохранение
        except Exception as err:
            logging.error({err}, exc_info=True)
        finally:
            if conn:
                conn.close()
