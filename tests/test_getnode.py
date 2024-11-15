import unittest
import json
from flask import Flask
from unittest.mock import patch, MagicMock
from src.decision_tree import get_api_request, get_tree_node
from src.faq import get_faq_suggestions
from src.main import create_app

class TestGetNodeEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()

    def setUp(self):
        self.client_data = {
            'path': '0/1',
            'user_id': ''
        }

    def test_get_node_success(self):
        response = self.client.get('/chatbot/getnode', data=json.dumps(self.client_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_non_existing_node(self):
        data = {
            'path': '-1',
            'user_id': ''
        }
        response = self.client.get('/chatbot/getnode', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_bad_request_node(self):
        data = {
            'user_id': ''
        }
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
        
        expected_response = "\nUsuario creado: \nID: 123 \nNombre: John Doe \nTelefono: 555-1234 \nEmail: john@example.com"
        self.assertEqual(result, expected_response)

    @patch('requests.post')
    def test_get_api_request_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        json_data = {"userId": "12345"}
        url_path = "/incidents/mobile/create_user"
        result = get_api_request(json_data, url_path)
        
        self.assertEqual(result, "Error en la respuesta: 500, Internal Server Error")

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

            expected_response = "\nUsuario creado: \nID: 123 \nNombre: John Doe \nTelefono: 555-1234 \nEmail: john@example.com"
            self.assertEqual(result, expected_response)

    @patch('requests.post')
    def test_get_api_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Network error")
        
        json_data = {"userId": "12345"}
        url_path = "/incidents/mobile/create_user"
        result = get_api_request(json_data, url_path)
        
        self.assertEqual(result, "Error en solicitud a http://localhost:5000/incidents/mobile/create_user, mensaje: Network error")

if __name__ == '__main__':
    unittest.main()