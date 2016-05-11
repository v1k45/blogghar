from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import UserProfile


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', email='test_user@email.com',
            password='test_password')
        profile = UserProfile(user=self.user)
        profile.save()

    def test_view_profile_is_accessible(self):
        target = reverse('authapp:profile', args=[self.user.username])
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authapp/user_profile.html')
        self.assertEqual(response.context['profile'], self.user.profile)
