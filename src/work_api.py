import psycopg2

import requests

class ApiWork:
    __slots__ = (
        'input_host',
        'num',
        'result_employer',
        'res_vac',
        'res_employ',
        'result_vac',
        'conn'
    )

    def __init__(self, num):
        """Конструктор"""
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


    def data_employers_api(self):
        """Метод api для получения данных о работодателях с сайта hh.ru"""
        # api компаний
        input_employer = input('Введите название компании для добавления: ')
        url = f"https://api.hh.ru/employers?text={input_employer}"
        # Запрос к api компаний
        response_employer = requests.get(
            url,
            params={"employer_id": 88687},
            timeout=120
        )
        self.result_employer = response_employer.json()
        return self.result_employer


    def load_for_employ(self):
        """Метод для загрузки содержимого таблицы employers в БД"""
        if self.result_employer is None:  # Проверка на обновлённую переменную - self.result_employer
            self.data_employers_api()
        if self.result_employer.get('found', 0) >= self.num:
            for item_employ in self.result_employer.get('items', 0):
                item_res = item_employ
                with self.conn as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO employers VALUES (%s, %s, %s, %s)",
                            (item_res.get('id', 0), item_res.get('name', 0), item_res.get('vacancies_url', 0),
                             item_res['open_vacancies'])
                        )

        self.conn.commit() # сохранение

    def load_for_vac(self):
        """Метод для загрузки содержимого таблицы vacancies в БД"""
        if self.result_employer is None:  # Проверка на обновлённую переменную - self.result_employer
            self.data_employers_api()
        if self.result_employer['found'] >= self.num:
            for item_employ in self.result_employer['items']:
                response_vac = requests.get(item_employ['vacancies_url'])
                self.result_vac = response_vac.json()
                for item_vac in self.result_vac['items']:
                    if item_vac["salary_range"] is not None:
                        salary_from = item_vac.get('salary_range', 0).get('from') if item_vac.get('salary_range').get('from') else 0
                        salary_to = item_vac.get('salary_range', 0).get('to') if item_vac.get('salary_range').get('to') else 0
                        currency = item_vac.get('salary_range', 0).get('currency') if item_vac.get('salary_range').get('currency') else 0
                        with self.conn as conn:
                            with conn.cursor() as cur:
                                cur.execute(
                                    "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                                    (item_vac['id'], item_vac['name'], salary_from, salary_to, currency
                                    )
                                )
        self.conn.commit() # сохранение
        self.conn.close() # закрытие

