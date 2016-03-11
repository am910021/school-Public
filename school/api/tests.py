  # 测试 REST Api
    # test_api.py
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from db.models import Demo

class FirstTest(TestCase):

    def setUp(self):
        print('setup done.')
        
    def test_list(self):
        url = "/api/2000/2/30-35-25-36"
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
        #data = json.loads(response.content)
        #self.assertEquals(len(data), 1)