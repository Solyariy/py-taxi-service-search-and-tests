from django.test import TestCase

from taxi.models import Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Country"
        )
        self.assertEqual(str(manufacturer), "Name Country")
