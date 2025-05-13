import psycopg2

import requests


class ApiWork:
    __slots__ = ('input_employer', 'input_host', 'only_with_vacancies', 'text', 'input_open_vac')

    def __init__(self):
        """Конструктор"""
        self.input_employer = input('Введите название компании: ')
        self.input_host = 'hh.ru'

    def data_employers(self):
        """Метод api для получения данных о работодателях с сайта hh.ru"""
        # api компаний
        url = f"https://api.{self.input_host}/employers?text={self.input_employer}"
        # Запрос к api компаний
        response_employer = requests.get(url)
        result_employer = response_employer.json()
        if result_employer['found'] >= 10:
            for i in result_employer['items']:
                response_vac = requests.get(i['vacancies_url'])
                result_vac = response_vac.json()
                for k in result_vac['items']:
                    if k["salary_range"] is not None:
                        salary_from = k.get('salary_range', 0).get('from') if k.get('salary_range').get('from') else 0
                        salary_to = k.get('salary_range', 0).get('to') if k.get('salary_range').get('to') else 0
                        currency = k.get('salary_range', 0).get('currency') if k.get('salary_range').get('currency') else 0
                        with psycopg2.connect(
                        host='localhost',
                        database='data_vacancies',
                        user='postgres',
                        password='10121331'
                    ) as conn:
                            with conn.cursor() as cur:
                                cur.execute("INSERT INTO employers VALUES (%s, %s, %s)",
                                            (i['id'], i['name'], i['vacancies_url']))
                                cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                                            (k['id'], k['name'], salary_from, salary_to, currency))

class_obj = ApiWork()
class_obj.data_employers()

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