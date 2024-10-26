import unittest
import json
from flask import Flask
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
        response = self.client.get('/api/getnode', data=json.dumps(self.client_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_non_existing_node(self):
        self.data ={
            'path': '-1',
            'user_id': ''
        }
        response = self.client.get('/api/getnode', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_bad_request_node(self):
        self.data ={
            'user_id': ''
        }
        response = self.client.get('/api/getnode', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()