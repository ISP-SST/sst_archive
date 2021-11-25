import datetime

from django.contrib.auth.models import Group, User

from data_access.models import enqueue_swedish_user_registration_request, SwedishUserValidationRequest, \
    ValidationResult
from observations.models import Instrument, DataCube
from django.test import TestCase


class TestSwedishUserFlow(TestCase):
    def setUp(self):
        self.maxDiff = None
        Instrument.objects.bulk_create(
            [Instrument(name='CHROMIS', description=''), Instrument(name='CRISP', description='')])
        self.data_cube = DataCube.objects.create(oid='test_oid', filename='test_file.fits', path='/path/to/test_file.fits',
                                size=1000000000, instrument=Instrument.objects.get(name='CHROMIS'))
        self.swedish_group = Group.objects.create(name='Swedish User')

        self.test_user = User.objects.create(username='test_user', email='test@example.com')

    def test_swedish_user_approve(self):
        current_time = datetime.datetime.now()

        enqueue_swedish_user_registration_request(self.test_user)

        self.assertFalse(self.test_user.groups.filter(pk=self.swedish_group.id).exists())

        validation_request = SwedishUserValidationRequest.objects.get(user=self.test_user)

        self.assertEqual(validation_request.validation_date, None)
        self.assertEqual(validation_request.validation_result, ValidationResult.NOT_PROCESSED)

        current_time = datetime.datetime.now()

        validation_request.validation_result = ValidationResult.APPROVED
        validation_request.save()

        self.assertGreaterEqual(validation_request.validation_date, current_time)
        self.assertEqual(validation_request.validation_result, ValidationResult.APPROVED)

        self.assertTrue(self.test_user.groups.filter(pk=self.swedish_group.id).exists())

    def test_swedish_user_reject(self):
        current_time = datetime.datetime.now()

        enqueue_swedish_user_registration_request(self.test_user)

        self.assertFalse(self.test_user.groups.filter(pk=self.swedish_group.id).exists())

        validation_request = SwedishUserValidationRequest.objects.get(user=self.test_user)

        self.assertEqual(validation_request.validation_date, None)
        self.assertEqual(validation_request.validation_result, ValidationResult.NOT_PROCESSED)

        current_time = datetime.datetime.now()

        validation_request.validation_result = ValidationResult.REJECTED
        validation_request.save()

        self.assertGreaterEqual(validation_request.validation_date, current_time)
        self.assertEqual(validation_request.validation_result, ValidationResult.REJECTED)

        self.assertFalse(self.test_user.groups.filter(pk=self.swedish_group.id).exists())
