from django.test import TestCase, SimpleTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from blog.views import (
    PostListView,
    UserPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    about,
)
from blog.models import Blog
import datetime
import pytz
from users.forms import UserRegisterForm


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


class TestUrls(SimpleTestCase):
    def test_home_resolves(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_user_posts_resolves(self):
        url = reverse("user-posts", args=["testuser"])
        self.assertEqual(resolve(url).func.view_class, UserPostListView)

    def test_user_posts_detail_resolves(self):
        url = reverse("post-detail", args=[1])
        self.assertEqual(resolve(url).func.view_class, PostDetailView)

    def test_user_posts_create_resolves(self):
        url = reverse("post-create")
        self.assertEqual(resolve(url).func.view_class, PostCreateView)

    def test_user_posts_update_resolves(self):
        url = reverse("post-update", args=[1])
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)

    def test_user_posts_delete_resolves(self):
        url = reverse("post-delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, PostDeleteView)

    def test_about_resolves(self):
        url = reverse("about")
        self.assertEqual(resolve(url).func, about)


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="password"
        )
        self.client = Client()
        self.home_url = reverse("home")
        self.post_list_url = reverse("user-posts", args=["testuser"])
        self.post_detail = reverse("post-detail", args=[1])
        self.post1 = Blog.objects.create(
            title="SOME TITLE",
            body="SOME TEXT",
            date=datetime.datetime(2021, 12, 7, 20, 8, 7, 127325, tzinfo=pytz.UTC),
            author=self.user,
        )

    def test_blog_home_GET(self):

        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_blog_about_GET(self):

        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/about.html")

    def test_user_post_list_view_GET(self):

        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/user_posts.html")
