from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from django.contrib.auth.hashers import make_password

class LoginTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username='testuser', password=make_password('testpassword'))

    def test_valid_login(self):
        # Simulate a POST request to the login view with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        # Check if the response redirects to the expected URL
        self.assertRedirects(response, reverse('index'))

        # Check if the user is logged in by checking the session
        self.assertEqual(self.client.session['user_id'], self.user.id)

    def test_invalid_username_valid_password(self):
        # Simulate a POST request to the login view with an invalid username and valid password
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'testpassword'})

        # Check if the response renders the login template
        self.assertTemplateUsed(response, 'login.html')

        # Check if the error message is present in the response context
        self.assertIn('Invalid username or password.', response.context['error_message'])

        # Check if the user is not logged in (session should not have 'user_id')
        self.assertNotIn('user_id', self.client.session)
        error_message_start = '<p class="error-message">'
        error_message_end = '</p>'
        start_index = response.content.decode('utf-8').find(error_message_start)
        end_index = response.content.decode('utf-8').find(error_message_end, start_index + len(error_message_start))
        error_message = response.content.decode('utf-8')[start_index + len(error_message_start):end_index]
        print(error_message)

    def test_valid_username_invalid_password(self):
        # Simulate a POST request to the login view with a valid username and invalid password
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'invalidpassword'})

        # Check if the response renders the login template
        self.assertTemplateUsed(response, 'login.html')

        # Check if the error message is present in the response context
        self.assertIn('Invalid username or password.', response.context['error_message'])

        # Check if the user is not logged in (session should not have 'user_id')
        self.assertNotIn('user_id', self.client.session)
        error_message_start = '<p class="error-message">'
        error_message_end = '</p>'
        start_index = response.content.decode('utf-8').find(error_message_start)
        end_index = response.content.decode('utf-8').find(error_message_end, start_index + len(error_message_start))
        error_message = response.content.decode('utf-8')[start_index + len(error_message_start):end_index]
        print(error_message)


