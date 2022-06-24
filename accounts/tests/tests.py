from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts.forms import CustomSignupForm
from programOfficeAid.views import HomeView


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            first_name='will',
            last_name='smith',
            email='will@iiu.edu.pk',
            password='testpass123'
        )
        self.assertEqual(user.first_name, 'will')
        self.assertEqual(user.last_name, 'smith')
        self.assertEqual(user.email, 'will@iiu.edu.pk')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            first_name='super',
            last_name='admin',
            email='superadmin@iiu.edu.pk',
            password='testpass123'
        )
        self.assertEqual(admin_user.first_name, 'super')
        self.assertEqual(admin_user.last_name, 'admin')
        self.assertEqual(admin_user.email, 'superadmin@iiu.edu.pk')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Program Office Aid')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):  # new
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomeView.as_view().__name__
        )


class SignupPageTests(TestCase):
    first_name = 'user'
    last_name = 'name'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Register your account')
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):  # new
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomSignupForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_form2(self):
        new_user = get_user_model().objects.create_user(
            self.first_name, self.last_name, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                         [0].first_name, self.first_name)
        self.assertEqual(get_user_model().objects.all()
                         [0].email, self.email)
