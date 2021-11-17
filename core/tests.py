from django.contrib.auth.models import User
from django.test import TestCase

from core.models import UserProfile


class TestUserProfile(TestCase):
    def setUp(self):
        pass

    def test_auto_create_user_profile(self):
        test_purpose = 'Test purpose'
        test_affiliation = 'Test affiliation'

        user = User.objects.create(username='test@example.com', password='password123', email='test@example.com',
                            first_name='Firstname', last_name='Lastname')

        user.profile.purpose = test_purpose
        user.profile.affiliation = test_affiliation
        user.profile.save()

        profile = UserProfile.objects.get(user=user)

        self.assertEqual(profile, user.profile)
        self.assertEqual(profile.purpose, test_purpose)
        self.assertEqual(profile.affiliation, test_affiliation)
