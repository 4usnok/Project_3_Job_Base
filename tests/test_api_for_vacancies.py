import logging
import unittest
from unittest.mock import MagicMock, patch

import requests
from src.api_for_vacancies import \
    WorkingWithVacancies  # замените на имя вашего модуля


class TestWorkingWithVacancies(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения."""
        self.test_employer = "Яндекс"
        self.test_num = 5
        self.instance = WorkingWithVacancies(self.test_num, self.test_employer)

    def test_init(self):
        """Тест инициализации класса."""
        self.assertEqual(self.instance.input_employer, self.test_employer)
        self.assertEqual(self.instance.num, self.test_num)
        self.assertIsNone(self.instance.result_employer)

    @patch("requests.get")
    def test_data_employers_api_success(self, mock_get):
        """Тест успешного запроса к API работодателей."""
        # Настраиваем мок для requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "found": 10,
            "items": [
                {"id": "123", "name": "Яндекс", "vacancies_url": "http://example.com"}
            ],
        }
        mock_get.return_value = mock_response

        result = self.instance.data_employers_api()
        self.assertIsNotNone(result)
        self.assertEqual(result["found"], 10)
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_data_employers_api_failure(self, mock_get):
        """Тест обработки ошибки API."""
        mock_get.side_effect = requests.exceptions.HTTPError("API недоступен")
        result = self.instance.data_employers_api()
        self.assertIsNone(result)

    @patch("requests.get")
    @patch("psycopg2.connect")
    def test_load_for_vac(self, mock_db, mock_get):
        # Мок для API работодателей
        mock_employer = MagicMock()
        mock_employer.json.return_value = {
            "found": 5,
            "items": [
                {"id": "123", "vacancies_url": "http://example.com", "name": "Яндекс"}
            ],
        }

        # Мок для API вакансий
        mock_vacancy = MagicMock()
        mock_vacancy.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                }
            ]
        }

        mock_get.side_effect = [mock_employer, mock_vacancy]

        # Мок для БД
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn

        # Тестируем
        self.instance.load_for_vac()

        # Проверяем вызовы
        self.assertEqual(mock_get.call_count, 2)
        mock_db.assert_called_once()

    def tearDown(self):
        """Очистка после тестов."""
        logging.shutdown()


if __name__ == "__main__":
    unittest.main()
