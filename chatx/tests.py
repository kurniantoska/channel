from django.test import TestCase
from django.test import Client


class ChatxTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_chatx_works(self):
        response = self.client.get('/chat/')
        self.assertEqual(200, response.status_code)
        
    def test_view_roomname_chatx(self):
        response = self.client.get('/chat/skater')
        print(response)
