import unittest
import json
from flask import Flask
from src.main import create_app
from unittest.mock import patch

class TestGetIncidentSolutionsEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()

    def setUp(self):
        self.client_data = {
            'incident_id': '12345',
            'user_id': 'user_1',
        }

    @patch('src.commands.solutions.GetIncidentSolutions.execute')
    def test_get_incident_solutions_success(self, mock_execute):
        mock_execute.return_value = [
            {"text": "Solution 1 for incident 12345"},
            {"text": "Solution 2 for incident 12345"}
        ]
        
        response = self.client.get('/chatbot/getsolutions', 
                                   data=json.dumps(self.client_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        solutions = json.loads(response.data)

        self.assertEqual(len(solutions), 2)
        self.assertEqual(solutions[0]['text'], "Solution 1 for incident 12345")
        self.assertEqual(solutions[1]['text'], "Solution 2 for incident 12345")

    @patch('src.commands.solutions.GetIncidentSolutions.execute')
    def test_get_incident_solutions_empty(self, mock_execute):
        mock_execute.return_value = []
        response = self.client.get('/chatbot/getsolutions', 
                                   data=json.dumps(self.client_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        solutions = json.loads(response.data)
        self.assertEqual(solutions, [])

    @patch('src.commands.solutions.GetIncidentSolutions.execute')
    def test_get_incident_solutions_error(self, mock_execute):
        mock_execute.side_effect = Exception("Some error occurred")
        
        response = self.client.get('/chatbot/getsolutions', 
                                   data=json.dumps(self.client_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()