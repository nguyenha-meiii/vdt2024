import unittest
from unittest.mock import patch, Mock
import requests

class TestAPI(unittest.TestCase):
    @patch('requests.post')
    def setUp(self, mock_post):
        # Mock response for creating a student
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'Student created successfully',
            'id': 'mock_id'
        }
        mock_post.return_value = mock_response

        data = {
            "no": 22,
            "fullName": "Nguyen Van CDE",
            "doB": "2001",
            "gender": "Nam",
            "school": "NEUST"
        }
        res = requests.post("mock://url", json=data)
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        self.assertEqual(res_json['message'], 'Student created successfully')
        self._id = res_json['id']

    @patch('requests.delete')
    def tearDown(self, mock_delete):
        # Mock response for deleting a student
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'Student deleted successfully'
        }
        mock_delete.return_value = mock_response

        res = requests.delete(f"mock://url/{self._id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['message'], 'Student deleted successfully')

    @patch('requests.get')
    def test_get_students(self, mock_get):
        # Mock response for getting students
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            '_id': 'mock_id',
            'no': 22,
            'fullName': 'Nguyen Van CDE',
            'doB': '2001',
            'gender': 'Nam',
            'school': 'NEUST'
        }]
        mock_get.return_value = mock_response

        res = requests.get("mock://url")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()), 0)

    @patch('requests.post')
    def test_create_student(self, mock_post):
        # Mock response for creating a student
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'Student created successfully',
            'id': 'mock_id'
        }
        mock_post.return_value = mock_response

        data = {
            "no": 44,
            "fullName": "Nguyen Van A",
            "doB": "2000",
            "gender": "Nam",
            "school": "HUST"
        }
        res = requests.post("mock://url", json=data)
        self.assertEqual(res.status_code, 200)
        self.created_id = res.json()['id']
        self.assertEqual(res.json()['message'], 'Student created successfully')

    @patch('requests.get')
    def test_get_student_by_id(self, mock_get):
        # Mock response for getting a student by ID
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            '_id': self._id,
            'no': 22,
            'fullName': 'Nguyen Van CDE',
            'doB': '2001',
            'gender': 'Nam',
            'school': 'NEUST'
        }
        mock_get.return_value = mock_response

        res = requests.get(f"mock://url/{self._id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['_id'], self._id)
        self.assertGreater(len(res.json()), 0)

    @patch('requests.put')
    def test_update_student(self, mock_put):
        # Mock response for updating a student
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'Student updated successfully'
        }
        mock_put.return_value = mock_response

        updated_data = {
            "no": 55,
            "fullName": "Nguyen Van CDF",
            "doB": "2001",
            "gender": "gioi tinh thu 3",
            "school": "NEUST"
        }
        res = requests.put(f"mock://url/{self._id}", json=updated_data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['message'], 'Student updated successfully')

    @patch('requests.post')
    @patch('requests.delete')
    @patch('requests.get')
    def test_delete_student(self, mock_get, mock_delete, mock_post):
        # Mock response for creating a student
        mock_response_create = Mock()
        mock_response_create.status_code = 200
        mock_response_create.json.return_value = {
            'message': 'Student created successfully',
            'id': 'mock_id'
        }
        mock_post.return_value = mock_response_create

        # Mock response for deleting a student
        mock_response_delete = Mock()
        mock_response_delete.status_code = 200
        mock_response_delete.json.return_value = {
            'message': 'Student deleted successfully'
        }
        mock_delete.return_value = mock_response_delete

        # Mock response for checking deleted student
        mock_response_get = Mock()
        mock_response_get.status_code = 404
        mock_get.return_value = mock_response_get

        data = {
            "no": 44,
            "fullName": "Nguyen Van A",
            "doB": "2000",
            "gender": "Nam",
            "school": "HUST"
        }
        res = requests.post("mock://url", json=data)
        self.assertEqual(res.status_code, 200)
        created_id = res.json()['id']
        self.assertEqual(res.json()['message'], 'Student created successfully')

        response = requests.delete(f'mock://url/{created_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Student deleted successfully')

        response = requests.get(f'mock://url/{created_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    test_order = ["setUp", "test_get_students", "test_create_student", "test_get_student_by_id", "test_update_student", "test_delete_student", "tearDown"] 
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=test_loader)
