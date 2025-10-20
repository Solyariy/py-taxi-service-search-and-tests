from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

DRIVER_LIST_VIEW_URL = reverse("taxi:driver-list")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.client.force_login(self.admin)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="test1",
            email="test2",
            password="test3",
            license_number="test4"
        )
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(drivers),
            list(response.context.get("driver_list"))
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )
