import logging

import psycopg2

import requests

class ApiWork:
    __slots__ = (
        'input_employer',
        'num',
        'result_employer',
        'res_vac',
        'res_employ',
        'result_vac',
        'conn'
    )

    def __init__(self, num, input_employer):
        """Конструктор"""
        self.input_employer = input_employer
        self.num = num
        self.result_employer = None
        self.res_vac = None
        self.res_employ = None
        self.result_vac = None
        self.conn = psycopg2.connect(
            host='localhost',
            database='data_base',
            user='postgres',
            password='10121331')

        # Настройка логирования
        logging.basicConfig(level=logging.INFO, filename="../py_log.log", filemode="w")
        logging.debug("A DEBUG Message")
        logging.info("An INFO")
        logging.warning("A WARNING")
        logging.error("An ERROR")
        logging.critical("A message of CRITICAL severity")

    def data_employers_api(self):
        """Метод api для получения данных о работодателях с сайта hh.ru"""

        url = f"https://api.hh.ru/employers"
        # Запрос к api компаний
        try:
            response_employer = requests.get(
                url,
                params=
                {
                    "text": self.input_employer, # Название компании
                    "per_page": self.num # Ограничение на кол-во результатов
                },
                timeout=60,

            )
            response_employer.raise_for_status()  # Проверяем статус здесь!

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
            if self.result_employer is None:  # Проверка на обновлённую переменную - self.result_employer
                self.data_employers_api()
            if self.result_employer.get('found', 0) >= self.num:
                for item_employ in self.result_employer.get('items', 0):
                    self.__load_for_employ(item_employ) # Передаём в приватный метод
        except Exception as error:
            logging.critical(f"Критическая ошибка в load_for_employ: {str(error)}")

    def __load_for_employ(self, item_res: dict):
        """Приватный метод загрузки содержимого таблицы employers в БД"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO employers VALUES (%s, %s, %s, %s)",
                    (item_res.get('id', 0), item_res.get('name', 0), item_res.get('vacancies_url', 0),
                     item_res['open_vacancies'])
                )
                self.conn.commit() # сохранение
        except Exception as err:
            logging.error({err},exc_info=True)

    def load_for_vac(self):
        """Метод загрузки содержимого таблицы vacancies в БД"""
        if self.result_employer is None:  # Проверка на обновлённую переменную - self.result_employer
            self.data_employers_api()
        try:
            if self.result_employer['found'] >= self.num:
                for item_employ in self.result_employer['items']:
                    response_vac = requests.get(item_employ['vacancies_url'])
                    self.result_vac = response_vac.json()
                    for item_vac in self.result_vac['items']:
                        if item_vac["salary_range"] is not None:
                            salary_from = item_vac.get('salary_range', 0).get('from') if item_vac.get('salary_range').get('from') else 0
                            salary_to = item_vac.get('salary_range', 0).get('to') if item_vac.get('salary_range').get('to') else 0
                            currency = item_vac.get('salary_range', 0).get('currency') if item_vac.get('salary_range').get('currency') else 0
                            self.__load_for_vac(item_vac, salary_from, salary_to, currency) # Передаём, как параметры приватного метода
        except KeyError as err:
            logging.error({err}, exc_info=True)

    def __load_for_vac(self, item_vac, salary_from, salary_to, currency):
        """Приватный метод загрузки данных таблицы vacancies в БД"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                        (item_vac['id'], item_vac['name'], salary_from, salary_to, currency
                        )
                    )
            self.conn.commit() # сохранение
        except Exception as err:
            logging.error({err},exc_info=True)
        finally:
            self.conn.close() # закрытие соединения
