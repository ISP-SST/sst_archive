import datetime

from allauth.account.models import EmailConfirmation
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import Client
from django.urls import reverse

from core.models import UserProfile


@override_settings(
    ACCOUNT_DEFAULT_HTTP_PROTOCOL="https",
    ACCOUNT_EMAIL_VERIFICATION="mandatory",
    ACCOUNT_AUTHENTICATION_METHOD="email",
    ACCOUNT_EMAIL_SUBJECT_PREFIX=None,
    ACCOUNT_EMAIL_CONFIRMATION_HMAC=False,
    LOGIN_REDIRECT_URL="/accounts/profile/",
    ACCOUNT_SIGNUP_REDIRECT_URL="/accounts/welcome/",
    ACCOUNT_ADAPTER="core.account.EmailEnforcingAccountAdapter",
    ACCOUNT_FORMS={
        'signup': 'core.account.ExtendedSignupForm',
        'login': 'core.account.EmailVerificationEnforcingLoginForm'
    },
    ACCOUNT_USERNAME_REQUIRED=False,
    ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN=0,
    EMAIL_VERIFICATION_EXPIRATION_PERIOD=datetime.timedelta(weeks=1),
    EMAIL_VERIFICATION_CHECK_PERIOD=datetime.timedelta(seconds=0),
)
class TestAccountEmailReVerification(TestCase):
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

    def test_signup_with_extended_fields(self):
        c = Client()

        username = 'john@example.com'
        email = 'john@example.com'
        password = 'johndoe123'
        purpose = 'No particular purpose'
        affiliation = 'Unseen University'
        first_name = 'John'
        last_name = 'Doe'

        # Signup
        resp = c.post(
            reverse("account_signup"),
            {
                "username": username,
                "email": email,
                "password1": password,
                "password2": password,
                "first_name": first_name,
                "last_name": last_name,
                "affiliation": affiliation,
                "purpose": purpose
            },
            follow=True,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertGreater(mail.outbox[0].body.find("https://"), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(
            resp,
            "account/verification_sent.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION,
        )

        # Verify, and attempt to login.
        confirmation = EmailConfirmation.objects.filter(
            email_address__user__username=username
        )[:1].get()

        resp = c.get(reverse("account_confirm_email", args=[confirmation.key]))

        self.assertTemplateUsed(
            resp, "account/email_confirm.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION
        )

        c.post(reverse("account_confirm_email", args=[confirmation.key]))

        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

        user = get_user_model().objects.get(username=username)

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

        self.assertEqual(user.profile.purpose, purpose)
        self.assertEqual(user.profile.affiliation, affiliation)

        now = datetime.datetime.now()

        self.assertGreaterEqual(user.profile.email_verification_date, now - datetime.timedelta(hours=1))

    def test_email_verification_timeout_logged_out(self):
        c = Client()

        username = 'john@example.com'
        email = 'john@example.com'
        password = 'johndoe123'
        purpose = 'No particular purpose'
        affiliation = 'Unseen University'
        first_name = 'John'
        last_name = 'Doe'

        # Signup
        resp = c.post(
            reverse("account_signup"),
            {
                "username": username,
                "email": email,
                "password1": password,
                "password2": password,
                "first_name": first_name,
                "last_name": last_name,
                "affiliation": affiliation,
                "purpose": purpose
            },
            follow=True,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertGreater(mail.outbox[0].body.find("https://"), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(
            resp,
            "account/verification_sent.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION,
        )

        # Verify, and attempt to login.
        confirmation = EmailConfirmation.objects.filter(
            email_address__user__username=username
        )[:1].get()

        resp = c.get(reverse("account_confirm_email", args=[confirmation.key]))

        self.assertTemplateUsed(
            resp, "account/email_confirm.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION
        )

        c.post(reverse("account_confirm_email", args=[confirmation.key]))

        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

        resp = c.get(reverse('account_logout'))
        resp = c.post(reverse('account_logout'))

        user = get_user_model().objects.get(username=username)
        now = datetime.datetime.now()

        self.assertGreaterEqual(user.profile.email_verification_date, now - datetime.timedelta(hours=1))

        # Place the verification date two weeks in the past.
        user.profile.email_verification_date = now - datetime.timedelta(weeks=2)
        user.profile.save()

        # Try to log in and see that the attempt fails and requires re-verification.
        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )

        self.assertRedirects(resp, "/accounts/confirm-email/")

        # Expect one more verification email.
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, [email])
        self.assertGreater(mail.outbox[1].body.find("https://"), 0)

        # Simulate email verification and login again.
        confirmation = EmailConfirmation.objects.filter(
            email_address__user__username=username
        )[:1].get()

        resp = c.get(reverse("account_confirm_email", args=[confirmation.key]))

        self.assertTemplateUsed(
            resp, "account/email_confirm.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION
        )

        c.post(reverse("account_confirm_email", args=[confirmation.key]))

        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

    def test_email_verification_timeout_logged_in(self):
        c = Client()

        username = 'john@example.com'
        email = 'john@example.com'
        password = 'johndoe123'
        purpose = 'No particular purpose'
        affiliation = 'Unseen University'
        first_name = 'John'
        last_name = 'Doe'

        # Signup
        resp = c.post(
            reverse("account_signup"),
            {
                "username": username,
                "email": email,
                "password1": password,
                "password2": password,
                "first_name": first_name,
                "last_name": last_name,
                "affiliation": affiliation,
                "purpose": purpose
            },
            follow=True,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertGreater(mail.outbox[0].body.find("https://"), 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(
            resp,
            "account/verification_sent.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION,
        )

        # Verify, and attempt to login.
        confirmation = EmailConfirmation.objects.filter(
            email_address__user__username=username
        )[:1].get()

        resp = c.get(reverse("account_confirm_email", args=[confirmation.key]))

        self.assertTemplateUsed(
            resp, "account/email_confirm.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION
        )

        c.post(reverse("account_confirm_email", args=[confirmation.key]))

        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

        user = get_user_model().objects.get(username=username)
        now = datetime.datetime.now()

        self.assertGreaterEqual(user.profile.email_verification_date, now - datetime.timedelta(hours=1))

        # Place the verification date two weeks in the past.
        user.profile.email_verification_date = now - datetime.timedelta(weeks=2)
        user.profile.save()

        # Try to access the landing page. This should re-trigger the email verification phase.
        resp = c.get('/')
        self.assertRedirects(resp, reverse('account_email_verification_sent'))

        # Expect one more verification email.
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, [email])
        self.assertGreater(mail.outbox[1].body.find("https://"), 0)

        # Simulate email verification and login again.
        confirmation = EmailConfirmation.objects.filter(
            email_address__user__username=username
        )[:1].get()

        resp = c.get(reverse("account_confirm_email", args=[confirmation.key]))

        self.assertTemplateUsed(
            resp, "account/email_confirm.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION
        )

        c.post(reverse("account_confirm_email", args=[confirmation.key]))

        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

    def test_email_reverification_disabled(self):
        c = Client()

        username = 'john@example.com'
        email = 'john@example.com'
        password = 'johndoe123'
        purpose = 'No particular purpose'
        affiliation = 'Unseen University'
        first_name = 'John'
        last_name = 'Doe'

        # Signup
        resp = c.post(
            reverse("account_signup"),
            {
                "username": username,
                "email": email,
                "password1": password,
                "password2": password,
                "first_name": first_name,
                "last_name": last_name,
                "affiliation": affiliation,
                "purpose": purpose
            },
            follow=True,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertGreater(mail.outbox[0].body.find("https://"), 0)
        self.assertTemplateUsed(
            resp,
            "account/verification_sent.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION,
        )

        # Verify, and attempt to login.
        confirmation = EmailConfirmation.objects.filter(
            email_address__user__username=username
        )[:1].get()

        resp = c.get(reverse("account_confirm_email", args=[confirmation.key]))

        self.assertTemplateUsed(
            resp, "account/email_confirm.%s" % settings.ACCOUNT_TEMPLATE_EXTENSION
        )

        c.post(reverse("account_confirm_email", args=[confirmation.key]))

        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

        user = get_user_model().objects.get(username=username)
        now = datetime.datetime.now()

        self.assertGreaterEqual(user.profile.email_verification_date, now - datetime.timedelta(hours=1))

        # Place the verification date two weeks in the past.
        user.profile.email_verification_date = now - datetime.timedelta(weeks=2)
        user.profile.email_reverification_disabled = True
        user.profile.save()

        # Try to access the landing page. This should pass and we shouldn't be forced to re-verify the
        # the email address.
        resp = c.get('/')

        self.assertEqual(resp.status_code, 200)

        # Log out and check that we're not prompted with a re-verification request this time either.
        resp = c.get(reverse('account_logout'))
        resp = c.post(reverse('account_logout'))

        # Try to log in and see that the attempt fails and requires re-verification.
        resp = c.post(
            reverse("account_login"),
            {"login": email, "password": password},
        )

        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )
