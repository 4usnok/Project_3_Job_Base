import logging
import unittest
from unittest.mock import patch

from src.work_db import DBManager


class TestDBManager(unittest.TestCase):
    def setUp(self):
        # Очищаем handlers логгера перед каждым тестом
        logging.root.handlers = []
        self.db_manager = DBManager()

    def tearDown(self):
        # Закрываем соединение после каждого теста
        if hasattr(self.db_manager, "conn"):
            self.db_manager.conn.close()

    @patch("builtins.print")
    @patch.object(DBManager, "cur")
    def test_get_companies_and_vacancies_count(self, mock_cursor, mock_print):
        """Тестируем метод get_companies_and_vacancies_count"""
        # Настраиваем моки
        mock_cursor.description = [
            ("employers_name",),
            ("employers_item",),
            ("employers_vacancies_url",),
        ]
        mock_cursor.fetchall.return_value = [
            ("Company1", "Item1", "Vacancy1"),
            ("Company2", "Item2", "Vacancy2"),
        ]

        # Вызываем метод
        self.db_manager.get_companies_and_vacancies_count()

        # Проверяем вызовы
        mock_cursor.execute.assert_called_once_with(
            "SELECT employers.employers_name, employers.employers_item, employers.employers_vacancies_url "
            "FROM employers "
            "JOIN vacancies "
            "ON vacancies.vacancies_id=employers.employers_id;"
        )
        mock_print.assert_called()

    @patch("builtins.print")
    @patch.object(DBManager, "cur")
    def test_get_all_vacancies(self, mock_cursor, mock_print):
        """Тестируем метод get_all_vacancies"""
        # Настраиваем моки
        mock_cursor.description = [
            ("employers_name",),
            ("vac_name",),
            ("salary_from",),
            ("salary_to",),
            ("currency",),
            ("vacancies_url",),
        ]
        mock_cursor.fetchall.return_value = [
            ("Company1", "Vacancy1", 100000, 150000, "RUR", "http://example.com")
        ]

        # Вызываем метод
        self.db_manager.get_all_vacancies()

        # Проверяем вызовы
        mock_cursor.execute.assert_called_once_with(
            "SELECT "
            "employers.employers_name, "
            "vacancies.vac_name, "
            "vacancies.salary_from, "
            "vacancies.salary_to, "
            "vacancies.currency, "
            "vacancies.vacancies_url "
            "FROM employers "
            "INNER JOIN vacancies "
            "ON vacancies.vacancies_id=employers.employers_id;"
        )
        mock_print.assert_called()

    @patch("builtins.print")
    @patch.object(DBManager, "cur")
    def test_get_vacancies_with_higher_salary(self, mock_cursor, mock_print):
        """Тестируем метод get_vacancies_with_higher_salary"""
        # Настраиваем моки
        mock_cursor.description = [("vacancies_name",), ("average_salary",)]
        mock_cursor.fetchall.return_value = [("Vacancy1", 130000.0)]

        # Вызываем метод
        self.db_manager.get_vacancies_with_higher_salary()

        # Проверяем вызовы
        expected_query = (
            "SELECT vac_name AS vacancies_name, (salary_from + salary_to) / 2 AS average_salary "
            "FROM vacancies "
            "WHERE (salary_from + salary_to) / 2 > ("
            "SELECT AVG((salary_from + salary_to) / 2) "
            "FROM vacancies );"
        )
        mock_cursor.execute.assert_called_once_with(expected_query)
        mock_print.assert_called()

    @patch("builtins.input", return_value="python")
    @patch("builtins.print")
    @patch.object(DBManager, "cur")
    def test_get_vacancies_with_keyword(self, mock_cursor, mock_print, mock_input):
        """Тестируем метод get_vacancies_with_keyword"""
        # Настраиваем моки
        mock_cursor.description = [
            ("vac_name",),
            ("salary_from",),
            ("salary_to",),
            ("currency",),
        ]
        mock_cursor.fetchall.return_value = [
            ("Python Developer", 100000, 150000, "RUR")
        ]

        # Вызываем метод
        self.db_manager.get_vacancies_with_keyword()

        # Проверяем вызовы
        mock_cursor.execute.assert_called_once_with(
            "SELECT vac_name, salary_from, salary_to, currency "
            "FROM vacancies "
            "WHERE vac_name LIKE 'python%';"
        )
        mock_print.assert_called()


if __name__ == "__main__":
    unittest.main()
