import unittest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from src.decision_tree import get_tree_node, get_api_request, get_user, parse_request_response
from src.faq import get_faq_suggestions
from src.main import create_app
import os


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

    @patch('src.faq.get_faq_suggestions')
    def test_get_faq_suggestions(self, mock_faq):
        # Mock FAQ response
        mock_faq.return_value = "No se encontraron sugerencias relacionadas con 'internet', 'red', 'email', 'telefono' o 'celular'."

        json_data = {"question": "problema técnico"}
        result = get_faq_suggestions(json_data["question"])

        # Now checking the actual response format, which is likely a different string.
        self.assertIn("No se encontraron sugerencias relacionadas", result)

    @patch('src.decision_tree.find_full_path')
    def test_get_tree_node(self, mock_find_full_path):
        # Test the flow through get_tree_node function
        mock_node = MagicMock()
        mock_node.get_attr.return_value = "Test message"
        mock_node.is_leaf = True
        mock_find_full_path.return_value = mock_node

        json_data = {"userId": "12345"}
        result = get_tree_node('1', json_data)

        self.assertIn('message', result)
        self.assertEqual(result['message'], "Test message")
        self.assertTrue(result['is_leaf'])

    def test_get_invalid_tree_node(self):
        # Test case where 'invalid_path' doesn't exist in the tree
        json_data = {"userId": "12345"}  # Sample request data
        
        # Now testing with an invalid path
        result = get_tree_node('0/3/3', json_data)

        # We expect the error message when the path is invalid
        self.assertTrue(result['error'])  # Check that there's an error
        self.assertEqual(result['message'], 'Selección inválida, por favor intente nuevamente')  # Check the error message
        self.assertIsNone(result['field'])

    def test_parse_request_response_with_user_email(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 123,
            "description": "Test incident",
            "userEmail": "user@example.com"
        }
        mock_response.status_code = 200
        
        # Call the function
        result, status_code = parse_request_response(mock_response, "http://example.com")
        
        # Assertions
        self.assertEqual(result, "\nID: 123 \nDescripcion: Test incident \nCorreo del usuario: user@example.com")
        self.assertEqual(status_code, 200)

    def test_parse_request_response_with_type_and_solved(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 123,
            "description": "Test incident",
            "type": "Technical",
            "solved": True,
            "response": "Issue resolved"
        }
        mock_response.status_code = 200
        
        # Call the function
        result, status_code = parse_request_response(mock_response, "http://example.com")
        
        # Assertions
        self.assertEqual(result, "\nID: 123 \nDescripcion: Test incident \nTipo: Technical, \nResuelto: True \nRespuesta: Issue resolved")
        self.assertEqual(status_code, 200)

    def test_parse_request_response_with_user_details(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "John Doe",
            "phone": "+1234567890",
            "email": "john.doe@example.com"
        }
        mock_response.status_code = 200
        
        # Call the function
        result, status_code = parse_request_response(mock_response, "http://example.com")
        
        # Assertions
        self.assertEqual(result, "\nUsuario creado: \nID: 1 \nNombre: John Doe \nTelefono: +1234567890 \nEmail: john.doe@example.com")
        self.assertEqual(status_code, 200)

    def test_parse_request_response_with_unexpected_format(self):
        # Mock response with unexpected format
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "unexpected_key": "value"
        }
        mock_response.status_code = 400
        
        # Call the function
        result, status_code = parse_request_response(mock_response, "http://example.com")
        
        # Assertions
        self.assertEqual(result, "Error: Unexpected response format from http://example.com")
        self.assertEqual(status_code, 400)

    def test_parse_request_response_with_missing_fields(self):
        # Mock response with missing fields
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 123,
            "description": "Test incident"
        }
        mock_response.status_code = 200
        
        # Call the function
        result, status_code = parse_request_response(mock_response, "http://example.com")
        
        # Assertions
        self.assertEqual(result, "Error: Unexpected response format from http://example.com")
        self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()