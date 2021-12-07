from django.test import TestCase
from django.contrib.auth.models import User


class AdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="password"
        )

    def tearDown(self):
        self.user.delete()

    def test_add_blog_post(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            "/admin/blog/blog/add/",
            {
                "title": "TEST TITLE",
                "body": "SOME BODY",
                "date_0": "2021-12-07",
                "date_1": "11:08:04",
                "initial-date_0": "2021-12-07",
                "initial-date_1": "11:08:04",
                "author": self.user.id,
                "_save": "SAVE",
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/")
        self.assertTrue("TEST TITLE" in str(response.content))
