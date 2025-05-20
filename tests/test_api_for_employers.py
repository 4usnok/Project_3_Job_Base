import unittest
from unittest.mock import MagicMock, patch

import psycopg2
import requests
from src.api_for_employers import WorkingWithEmployers


class TestWorkingWithEmployers(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения"""
        self.employer = WorkingWithEmployers(num=5, input_employer="Тинькофф")

    @patch("requests.get")
    def test_data_employers_api_success(self, mock_get):
        """Тестирование успешного запроса к API работодателей"""
        # Настраиваем mock
        mock_response = MagicMock()
        expected_result = {
            "items": [
                {
                    "id": "12345",
                    "name": "Тинькофф",
                    "vacancies_url": "https://api.hh.ru/vacancies?employer_id=12345",
                    "open_vacancies": 10,
                }
            ],
            "found": 1,
        }
        mock_response.json.return_value = expected_result
        mock_get.return_value = mock_response

        # Вызываем метод
        result = self.employer.data_employers_api()

        # Проверяем результаты
        self.assertEqual(result, expected_result)
        self.assertEqual(self.employer.result_employer, expected_result)
        mock_get.assert_called_once_with(
            "https://api.hh.ru/employers",
            params={"text": "Тинькофф", "per_page": 5},
            timeout=60,
        )

    @patch("requests.get")
    def test_data_employers_api_failure(self, mock_get):
        """Тестирование ошибки при запросе к API"""
        mock_get.side_effect = requests.exceptions.HTTPError("API недоступен")

        result = self.employer.data_employers_api()

        self.assertIsNone(result)
        self.assertIsNone(self.employer.result_employer)

    @patch.object(WorkingWithEmployers, "data_employers_api")
    @patch("psycopg2.connect")
    def test_load_for_employ_db_error(self, mock_connect, mock_data_api):
        """Тестирование обработки ошибки БД"""
        mock_data_api.return_value = {
            "items": [
                {
                    "id": "12345",
                    "name": "Тинькофф",
                    "vacancies_url": "https://example.com",
                    "open_vacancies": 10,
                }
            ],
            "found": 1,
        }

        mock_connect.side_effect = psycopg2.Error("DB error")

        # Проверяем, что исключение обрабатывается
        self.employer.load_for_employ()

    @patch.object(WorkingWithEmployers, "data_employers_api")
    def test_load_for_employ_no_data(self, mock_data_api):
        """Тестирование случая, когда нет данных от API"""
        mock_data_api.return_value = {"items": [], "found": 0}

        # Проверяем, что метод не падает
        self.employer.load_for_employ()

    def test_private_methods(self):
        """Тестирование доступности приватных методов"""
        # Проверяем, что приватные методы действительно приватные
        with self.assertRaises(AttributeError):
            self.employer.__data_employers_api()

        with self.assertRaises(AttributeError):
            self.employer.__load_for_employ({})


if __name__ == "__main__":
    unittest.main()
