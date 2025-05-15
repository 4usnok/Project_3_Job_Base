import json

import requests

import psycopg2

from src.work_api import ApiWork

class DBManager:

    __slots__ = (
        'rows',
        'elem_employers',
        'list_from_vac',
        'list_avg',
        'union_list',
        'res_work_meth'
    )

    def __init__(self):
        """Конструктор"""
        self.rows = None
        self.elem_employers = None
        self.list_from_vac = None
        self.list_avg = None
        self.union_list = None
        self.res_work_meth = None

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
            for el_for_list_vac in list_for_all_vac['items']:
                company_vacancies.append({
                        "name_vacancies": el_for_list_vac["name"],
                        "salary": el_for_list_vac["salary"],
                        "url_vacancies": el_for_list_vac["alternate_url"]
                }
                )
            self.union_list.append({
                "employers_name": row[1],
                "data_vacancies": company_vacancies
            })

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        if self.union_list is None:
            self.get_all_vacancies()
        res_avg_list = []
        for elem_list in self.union_list: # раскрытие всего списка с данными
            if elem_list.get('data_vacancies', 0):
                for elem_data_vacancies in elem_list.get("data_vacancies", 0): # раскрытие списка с данными вакансий
                    list_avg_salary = []
                    if elem_data_vacancies.get("salary", 0) is not None:
                        salary_from = elem_data_vacancies.get("salary").get("from", {}) or 0
                        salary_to = elem_data_vacancies.get("salary").get("to", {}) or 0
                        list_avg_salary.append(salary_from)
                        list_avg_salary.append(salary_to)
                        res_avg_op = sum(list_avg_salary) / len(list_avg_salary)
                        res_avg_list.append(res_avg_op)
        self.res_work_meth = sum(res_avg_list) / len(res_avg_list)
        print(self.res_work_meth)

    # def get_vacancies_with_higher_salary(self):
    #     """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
    #     if self.res_work_meth is None:
    #         self.get_avg_salary()
    #     pass


    def get_vacancies_with_keyword(self):
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass

if __name__ == "__main__":
    obj_class = DBManager()
    obj_class.get_avg_salary()

        # for k in result_employer['items']:
        #     url_vac = (k['vacancies_url'])
        #     response_vac = requests.get(url_vac)
        #     result_vac = response_vac.json()
        #     for j in result_vac['items']:
        #         count = 0
        #         name = j.get("name")
        #         url = j.get("alternate_url")
        #         if j["salary_range"] is not None:
        #             salary_from = j.get("salary_range", 0).get("from") if j.get("salary_range").get("from") else 0
        #             salary_to = j.get("salary_range", 0).get("to") if j.get("salary_range").get("to") else 0
        #             if salary_from != 0:
        #                 count += 1
        #             if salary_to != 0:
        #                 count += 1
        #             list_vac.append(
        #                 {
        #                 "name": name,
        #                 "salary": j.get("salary_range", 0),
        #                 "salary_average": (salary_from + salary_to) / count,
        #                 "url": url
        #                 }
        #             )
        #
        #     with open('../data/vacancies.json', 'w', encoding='utf-8') as f:
        #         json.dump(list_vac, f, ensure_ascii=False, indent=4)