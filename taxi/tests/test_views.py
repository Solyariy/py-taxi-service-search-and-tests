from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm


DRIVER_LIST_VIEW_URL = reverse("taxi:driver-list")
CAR_LIST_VIEW_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_VIEW_URL = reverse("taxi:manufacturer-list")


class PrivateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer_id=manufacturer.id
        )
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="test_license"
        )
        car.drivers.add(driver)

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
        qs = response.context.get("driver_list")
        self.assertTrue(qs.exists())
        self.assertQuerySetEqual(
            drivers,
            qs,
            ordered=False
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_retrieve_manufacturers(self):
        car = Manufacturer.objects.get(pk=1)
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        qs = response.context.get("manufacturer_list")
        self.assertTrue(qs.exists())
        self.assertQuerySetEqual(
            manufacturers,
            qs,
            ordered=False
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_retrieve_cars(self):
        car = Car.objects.get(pk=1)
        response = self.client.get(CAR_LIST_VIEW_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        qs = response.context.get("car_list")
        self.assertTrue(qs.exists())
        self.assertQuerySetEqual(
            cars,
            qs,
            ordered=False
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )
