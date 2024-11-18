import unittest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from src.decision_tree import get_api_request, get_tree_node, get_user
from src.faq import get_faq_suggestions
from src.main import create_app
from enum import Enum


class TestGetNodeEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()

    def setUp(self):
        self.client_data = {
            'path': '0/1',
            'user_id': '12345'
        }

    def test_get_node_success(self):
        response = self.client.get('/chatbot/getnode', data=json.dumps(self.client_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)
        self.assertIn('field', response.json)

    def test_get_non_existing_node(self):
        data = {
            'path': '-1',
            'user_id': '12345'
        }
        response = self.client.get('/chatbot/getnode', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    def test_get_bad_request_node(self):
        data = {'user_id': '12345'}
        response = self.client.get('/chatbot/getnode', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    @patch('requests.post')
    def test_get_api_request_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': '123',
            'name': 'John Doe',
            'phone': '555-1234',
            'email': 'john@example.com'
        }
        mock_post.return_value = mock_response

        json_data = {"userId": "12345"}
        url_path = "/incidents/mobile/create_user"
        result = get_api_request(json_data, url_path)

        expected_response = "\nUsuario creado: \nID: 123 \nNombre: John Doe \nTelefono: 555-1234 \nEmail: john@example.com", 200
        self.assertEqual(result, expected_response)

    @patch('requests.post')
    def test_get_api_request_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        json_data = {"userId": "12345"}
        url_path = "/incidents/mobile/create_user"
        result, sc = get_api_request(json_data, url_path)

        self.assertEqual(sc, 500)

    @patch('requests.post')
    def test_get_api_request_no_env_var(self, mock_post):
        with patch('os.getenv', return_value=None):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'id': '123',
                'name': 'John Doe',
                'phone': '555-1234',
                'email': 'john@example.com'
            }
            mock_post.return_value = mock_response

            json_data = {"userId": "12345"}
            url_path = "/incidents/mobile/create_user"
            result = get_api_request(json_data, url_path)

            expected_response = "\nUsuario creado: \nID: 123 \nNombre: John Doe \nTelefono: 555-1234 \nEmail: john@example.com", 200
            self.assertEqual(result, expected_response)

    @patch('requests.post')
    def test_get_api_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Network error")

        json_data = {"userId": "12345"}
        url_path = "/incidents/mobile/create_user"
        result, sc = get_api_request(json_data, url_path)

        self.assertEqual(sc, 500)

    @patch('requests.get')
    def test_get_user_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': '123',
            'name': 'John Doe',
            'phone': '555-1234',
            'email': 'john@example.com',
            'company': 'Example Corp'
        }
        mock_get.return_value = mock_response

        json_data = {"userId": "12345"}
        url_base = "http://localhost:5003"
        result, status = get_user(json_data, url_base)

        self.assertEqual(status, 200)
        self.assertEqual(result['id'], '123')
        self.assertEqual(result['name'], 'John Doe')

    @patch('requests.get')
    def test_get_user_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        json_data = {"userId": "12345"}
        url_base = "http://localhost:5003"
        result, status = get_user(json_data, url_base)

        self.assertEqual(status, 404)
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()