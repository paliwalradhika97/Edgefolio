from django.test import TestCase
from django.test import Client
import json

class FundTestCase(TestCase):
    fixtures = ["funds.json"]
  
    def test_endpoint(self):
        client = Client()
        response = client.get('/api/fund/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response["data"]), 6)
    
    def test_endpoint_filter(self):
        client = Client()
        response = client.get('/api/fund/?strategy=Arbitrage')#
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response["data"]), 2)
    
    def test_endpoint_file_upload(self):
        client = Client()
        with open('static/sample_fund_data.csv') as fp:
            response = client.post('/api/fund/', {'file_uploaded': fp})
            self.assertEqual(response.status_code, 201)
        
    def test_endpoint_file_error(self):
        client = Client()
        with open('static/sample_fund_data_error.csv') as fp:
            response = client.post('/api/fund/', {'file_uploaded': fp})
            json_response = json.loads(response.content)
            self.assertEqual(response.status_code, 400)            
            self.assertEqual(json_response["errors"]["file_error"]["row_num"], "4")
          


        