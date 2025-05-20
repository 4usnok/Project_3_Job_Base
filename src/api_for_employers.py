import logging

import psycopg2
import requests


class WorkingWithEmployers:
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
                timeout=60,
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

    def load_for_employ(self):
        """Метод загрузки содержимого таблицы employers в БД"""
        try:
            if (
                self.result_employer is None
            ):  # Проверка на обновлённую переменную - self.result_employer
                self.data_employers_api()
            if self.result_employer.get("found", 0) >= self.num:
                for item_employ in self.result_employer.get("items", 0):
                    self.__load_for_employ(item_employ)  # Передаём в приватный метод
        except Exception as error:
            logging.critical(f"Критическая ошибка в load_for_employ: {str(error)}")

    def __load_for_employ(self, item_res: dict):
        """Приватный метод загрузки содержимого таблицы employers в БД"""
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
                    "INSERT INTO employers VALUES (%s, %s, %s, %s)",
                    (
                        item_res.get("id", 0),
                        item_res.get("name", 0),
                        item_res.get("vacancies_url", 0),
                        item_res["open_vacancies"],
                    ),
                )
            cur.execute("SELECT * FROM employers")
            conn.commit()  # сохранение
        except Exception as err:
            logging.error({err}, exc_info=True)
