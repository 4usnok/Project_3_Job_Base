import psycopg2

import requests

class ApiWork:
    __slots__ = (
        'input_host',
        'num',
        'result_employer',
        'res_vac',
        'res_employ',
        'result_vac'

    )

    def __init__(self, num, host):
        """Конструктор"""
        self.input_host = host
        self.num = num
        self.result_employer = None
        self.res_vac = None
        self.res_employ = None
        self.result_vac = None


    def data_employers_api(self):
        """Метод api для получения данных о работодателях с сайта hh.ru"""
        # api компаний
        input_employer = input('Введите название компании: ')
        url = f"https://api.{self.input_host}/employers?text={input_employer}"
        # Запрос к api компаний
        response_employer = requests.get(
            url,
            params={"employer_id": 88687},
            timeout=120
        )
        self.result_employer = response_employer.json()

    def load_in_employ(self):
        """Метод подготовки для загрузки в базы данных"""
        if self.result_employer is None:  # Проверка на обновлённую переменную - self.result_employer
            self.data_employers_api()
        if self.result_employer['found'] >= self.num:
            for item_employ in self.result_employer['items']:
                item_res = item_employ
                with psycopg2.connect(
                        host='localhost',
                        database='data_base',
                        user='postgres',
                        password='10121331'
                ) as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO employers VALUES (%s, %s, %s, %s)",
                            (item_res['id'], item_res['name'], item_res['vacancies_url'],
                             item_res['open_vacancies'])
                        )
#
    def work_for_vac(self):
        """Метод отвечает непосредственно за работу с колонками таблиц: vacancies, employers"""
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
                        with psycopg2.connect(
                        host='localhost',
                        database='data_base',
                        user='postgres',
                        password='10121331'
                        ) as conn:
                            with conn.cursor() as cur:
                                cur.execute(
                                    "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)",
                                    (item_vac['id'], item_vac['name'], salary_from, salary_to, currency
                                    )
                                )

class_obj = ApiWork(10, 'hh.ru')
class_obj.load_in_employ()
class_obj.work_for_vac()


# Запросы для sql

# SELECT *
# FROM vacancies
#
# ALTER TABLE vacancies ADD COLUMN vacancies_id int;
# ALTER TABLE vacancies ADD COLUMN vacancies_name varchar(100);
# ALTER TABLE vacancies ADD COLUMN salary_from int;
# ALTER TABLE vacancies ADD COLUMN salary_to int;
# ALTER TABLE vacancies ADD COLUMN currency varchar(10);
#
# ALTER TABLE vacancies DROP COLUMN vacancies_id;
# ALTER TABLE vacancies DROP COLUMN vacancies_name;
# ALTER TABLE vacancies DROP COLUMN salary_from;
# ALTER TABLE vacancies DROP COLUMN salary_to;
# ALTER TABLE vacancies DROP COLUMN currency;

# SELECT *
# FROM employers

# ALTER TABLE employers DROP COLUMN employers_id;
# ALTER TABLE employers DROP COLUMN employers_name;
# ALTER TABLE employers DROP COLUMN employers_vacancies_url;
# ALTER TABLE employers DROP COLUMN employers_open_vacancies;



# ALTER TABLE vacancies RENAME salary TO salary_from;
# ALTER TABLE vacancies ADD COLUMN salary_to int;
# ALTER TABLE vacancies ADD COLUMN currency varchar;