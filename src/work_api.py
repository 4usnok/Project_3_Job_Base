import psycopg2

import requests


class ApiWork:
    __slots__ = (
        'input_employer',
        'input_host',
        'num',
        'result_employer',
    )

    def __init__(self, num, host):
        """Конструктор"""
        self.input_employer = input('Введите название компании: ')
        self.input_host = host
        self.num = num
        self.result_employer = None

    def data_employers_api(self):
        """Метод api для получения данных о работодателях с сайта hh.ru"""
        # api компаний
        url = f"https://api.{self.input_host}/employers?text={self.input_employer}"
        # Запрос к api компаний
        response_employer = requests.get(url)
        self.result_employer = response_employer.json()
        return self.result_employer

    def load_in_db(self):
        """Метод для загрузки в базы данных"""
        if self.result_employer is None:  # Проверка на обновлённую переменную - self.result_employer
            self.data_employers_api()
        if self.result_employer['found'] >= self.num:
            for item_employ in self.result_employer['items']:
                response_vac = requests.get(item_employ['vacancies_url'])
                result_vac = response_vac.json()
                for item_vac in result_vac['items']:
                    if item_vac["salary_range"] is not None:
                        salary_from = item_vac.get('salary_range', 0).get('from') if item_vac.get('salary_range').get('from') else 0
                        salary_to = item_vac.get('salary_range', 0).get('to') if item_vac.get('salary_range').get('to') else 0
                        currency = item_vac.get('salary_range', 0).get('currency') if item_vac.get('salary_range').get('currency') else 0
                        with psycopg2.connect(
                        host='localhost',
                        database='data_vacancies',
                        user='postgres',
                        password='10121331'
                    ) as conn:
                            with conn.cursor() as cur:
                                cur.execute(
                                    "INSERT INTO employers VALUES (%s, %s, %s)",
                                    (item_employ['id'], item_employ['name'], item_employ['vacancies_url'])
                                )
                                cur.execute(
                                    "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                                    (item_vac['id'], item_vac['name'], salary_from, salary_to, currency)
                                )

class_obj = ApiWork(10, 'hh.ru')
class_obj.load_in_db()

# Запросы для sql
# SELECT *
# FROM vacancies
#
# ALTER TABLE vacancies ADD COLUMN vacancies_id int;
# ALTER TABLE vacancies ADD COLUMN vac_name varchar(100);
# ALTER TABLE vacancies ADD COLUMN salary_from int;
# ALTER TABLE vacancies ADD COLUMN salary_to int;
# ALTER TABLE vacancies ADD COLUMN currency varchar(10);
#
#
# ALTER TABLE vacancies DROP COLUMN vacancies_id;
# ALTER TABLE vacancies DROP COLUMN vac_name;
# ALTER TABLE vacancies DROP COLUMN salary_from;
# ALTER TABLE vacancies DROP COLUMN salary_to;
# ALTER TABLE vacancies DROP COLUMN currency;
#
# ALTER TABLE vacancies RENAME salary TO salary_from;
# ALTER TABLE vacancies ADD COLUMN salary_to int;
# ALTER TABLE vacancies ADD COLUMN currency varchar;