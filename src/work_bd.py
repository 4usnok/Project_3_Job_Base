import requests

import psycopg2

class DBManager:

    __slots__ = (
        'rows',
        'elem_employers',
        'list_from_vac',
        'list_avg',
        'union_list',
        'res_avg_list',
        'res_work_meth',
        'list_for_high_salaries',
        'list_for_name_and_averager',
        'list_keyword'
    )

    def __init__(self):
        """Конструктор"""
        self.rows = None
        self.elem_employers = None
        self.list_from_vac = None
        self.list_avg = None
        self.union_list = None
        self.res_avg_list = None
        self.res_work_meth = None
        self.list_for_high_salaries = None
        self.list_for_name_and_averager = None
        self.list_keyword = None

    def get_companies_and_vacancies_count(self):
        """Метод может получать, как список всех компаний из таблицы employers,
        так и количество вакансий из таблицы vacancies."""
        conn = psycopg2.connect(
                host='localhost',
                database='data_base',
                user='postgres',
                password='10121331'
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM employers")

        self.rows = cur.fetchall()

        cur.close()
        conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий:
        с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.union_list = []
        if self.rows is None:
            self.get_companies_and_vacancies_count()
        for row in self.rows:
            company_vacancies = []
            response_for_vacancies_url = requests.get(
                row[2],
                params={"employer_id": 88687},
                timeout=120
            )
            list_for_all_vac = response_for_vacancies_url.json()
            for el_for_list_vac in list_for_all_vac.get('items', None):
                company_vacancies.append({
                        "name_vacancies": el_for_list_vac.get("name", 0),
                        "salary": el_for_list_vac.get("salary", 0),
                        "url_vacancies": el_for_list_vac.get("alternate_url", 0)
                }
                )
            self.union_list.append({
                "employers_name": row[1],
                "data_vacancies": company_vacancies
            })
        return self.union_list

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        if self.union_list is None:
            self.get_all_vacancies()
        self.res_avg_list = []
        self.list_for_name_and_averager = []
        for elem_list in self.union_list: # раскрытие всего списка с данными
            if elem_list.get('data_vacancies', 0):
                for elem_data_vacancies in elem_list.get("data_vacancies", 0): # раскрытие списка с данными вакансий
                    list_avg_salary = []
                    if elem_data_vacancies.get("salary", 0) is not None:
                        name_vacancies = elem_data_vacancies.get("name_vacancies", None)
                        salary_from = elem_data_vacancies.get("salary").get("from", {}) or 0
                        salary_to = elem_data_vacancies.get("salary").get("to", {}) or 0
                        list_avg_salary.append(salary_from)
                        list_avg_salary.append(salary_to)
                        res_avg_op = sum(list_avg_salary) / len(list_avg_salary)
                        self.res_avg_list.append(res_avg_op)
                        self.list_for_name_and_averager.append({
                            "avg": res_avg_op,
                            "name": name_vacancies})
        self.res_work_meth = sum(self.res_avg_list) / len(self.res_avg_list)
        return self.res_work_meth

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        if self.res_work_meth is None and self.res_avg_list is None:
            self.get_avg_salary()
        self.list_for_high_salaries = []
        for elem_res_avg in self.res_avg_list:
            if elem_res_avg > self.res_work_meth:
                self.list_for_high_salaries.append(elem_res_avg)
        return self.list_for_high_salaries

    def get_vacancies_with_keyword(self):
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        input_keyword = input("Введите ключевое слово: ")
        self.list_keyword = []
        if self.union_list is None:
            self.get_all_vacancies()
        for word in self.union_list:
            for vac in word.get("data_vacancies"):
                if input_keyword.lower() in vac.get("name_vacancies", None).lower():
                    self.list_keyword.append(word)
        return self.list_keyword
