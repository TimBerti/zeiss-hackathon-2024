import unittest
import requests

class TestAPI(unittest.TestCase):
    test_data = [[0, 1, 0, 0, 1, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]
    def setUp(self):
        self.base_url = "http://0.0.0.0:5000"

    def test_get(self):
        response = requests.get(f"{self.base_url}/statusmask")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_post(self):
        for data in self.test_data:
            response = requests.post(f"{self.base_url}/statusmask", json={"data": data})
            self.assertIn(response.status_code, [200, 201])
            self.assertEqual(response.json()['status'], 'success')

    def test_update(self):
        for data in self.test_data:
            requests.post(f"{self.base_url}/statusmask", json={"data": data})
            response = requests.get(f"{self.base_url}/statusmask")
            self.assertEqual(response.json()['data'], data)

if __name__ == '__main__':
    unittest.main()
