from django.test import TestCase
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='testuser', password='password')

    def tearDown(self):
        self.user.delete()

    def test_add_blog_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/admin/blog/blog/add/', {'title': 'TEST TITLE', 'body': 'SOME BODY', 'date_0': '2021-12-06', 'date_1': '12:13:04', 'initial-date_0': '2021-12-06', 'initial-date_1': '12:13:04', 'author': 'testuser', '_save': 'SAVE'})
        self.assertEqual(response.status_code, 200)
        print(response.content)
        # response = self.client.get('/')
        # print(response)
        # self.assertTrue('TEST TITLE' in str(response.content))