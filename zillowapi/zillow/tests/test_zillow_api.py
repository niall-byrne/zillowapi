import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Zillow
from ..serializers import ZillowDetailSerializer
from .zillow_generator import generate_test_data

ZILLOW_URL = reverse("zillow:zillow-list")


def detail_url(zillow_id):
  """Return recipe detail URL"""
  return reverse("zillow:zillow-detail", args=[zillow_id])


class UnauthenticatedZillowAPI(TestCase):
  """"Test Unauthenticated API Access"""

  def setUp(self) -> None:
    self.client = APIClient()

  def test_create_zillow_entry(self):
    """Test creating recipe."""
    payload = {
        "zillow_id": 19883200,
        "area_unit": "SqFt",
        "bathrooms": 6.0,
        "bedrooms": 5.0,
        "home_size": 6180.00,
        "home_type": "SingleFamily",
        "last_sold_date": "2016-06-09",
        "last_sold_price": 2790000.00,
        "link": "some link",
        "price": 2790000.00,
        "property_size": 44648.00,
        "rent_price": 0.00,
        "rentzestimate_amount": 11936.00,
        "rentzestimate_last_updated": "2018-08-07",
        "tax_value": 2845800.00,
        "tax_year": 2017,
        "year_built": 1990,
        "zestimate_amount": 3417658.00,
        "zestimate_last_updated": "2018-08-07",
        "address": "24975 Eldorado Meadow Rd",
        "city": "Hidden Hills",
        "state": "CA",
        "zipcode": 91302
    }
    res = self.client.post(ZILLOW_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    zillow = Zillow.objects.get(id=res.data["id"])
    for key in payload.keys():
      if key in [
          'last_sold_date', 'rentzestimate_last_updated',
          'zestimate_last_updated'
      ]:
        self.assertEqual(
            datetime.datetime.strptime(payload[key], "%Y-%m-%d").date(),
            getattr(zillow, key))
      else:
        self.assertEqual(payload[key], getattr(zillow, key))
    zillow.delete()

  def test_retrieve_zillow_list(self):
    zillow_id1, row1 = generate_test_data()
    zillow_id2, row2 = generate_test_data()
    zillow1 = Zillow.objects.get(zillow_id=zillow_id1)
    zillow2 = Zillow.objects.get(zillow_id=zillow_id2)

    res = self.client.get(ZILLOW_URL)

    serializer1 = ZillowDetailSerializer(zillow1)
    serializer2 = ZillowDetailSerializer(zillow2)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn(serializer1.data, res.data['results'])
    self.assertIn(serializer2.data, res.data['results'])

    zillow1.delete()
    zillow2.delete()

  def test_retrieve_zillow_detail(self):
    zillow_id1, row1 = generate_test_data()
    zillow_id2, row2 = generate_test_data()
    zillow1 = Zillow.objects.get(zillow_id=zillow_id1)
    zillow2 = Zillow.objects.get(zillow_id=zillow_id2)

    res = self.client.get(detail_url(zillow1.id))

    serializer1 = ZillowDetailSerializer(zillow1)
    serializer2 = ZillowDetailSerializer(zillow2)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(serializer1.data, res.data)
    self.assertNotEqual(serializer2.data, res.data)

    zillow1.delete()
    zillow2.delete()

  def test_retrieve_zillow_list_filter_by_id(self):
    zillow_id1, row1 = generate_test_data()
    zillow_id2, row2 = generate_test_data()
    zillow_id3, row3 = generate_test_data()
    zillow1 = Zillow.objects.get(zillow_id=zillow_id1)
    zillow2 = Zillow.objects.get(zillow_id=zillow_id2)
    zillow3 = Zillow.objects.get(zillow_id=zillow_id3)

    res = self.client.get(ZILLOW_URL,
                          {"zillow_ids": f"{zillow_id1},{zillow_id2}"})

    serializer1 = ZillowDetailSerializer(zillow1)
    serializer2 = ZillowDetailSerializer(zillow2)
    serializer3 = ZillowDetailSerializer(zillow3)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn(serializer1.data, res.data['results'])
    self.assertIn(serializer2.data, res.data['results'])
    self.assertNotIn(serializer3.data, res.data['results'])

    zillow1.delete()
    zillow2.delete()
    zillow3.delete()

  def test_retrieve_zillow_list_filter_by_city(self):
    zillow_id1, row1 = generate_test_data()
    zillow_id2, row2 = generate_test_data()
    zillow_id3, row3 = generate_test_data()
    zillow1 = Zillow.objects.get(zillow_id=zillow_id1)
    zillow2 = Zillow.objects.get(zillow_id=zillow_id2)
    zillow3 = Zillow.objects.get(zillow_id=zillow_id3)

    zillow1.city = "Toronto"
    zillow1.save()
    zillow2.city = "Montreal"
    zillow2.save()
    zillow3.city = "Vancouver"
    zillow3.save()

    res = self.client.get(ZILLOW_URL, {"cities": "Toronto,Montreal"})

    serializer1 = ZillowDetailSerializer(zillow1)
    serializer2 = ZillowDetailSerializer(zillow2)
    serializer3 = ZillowDetailSerializer(zillow3)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn(serializer1.data, res.data['results'])
    self.assertIn(serializer2.data, res.data['results'])
    self.assertNotIn(serializer3.data, res.data['results'])

    zillow1.delete()
    zillow2.delete()
    zillow3.delete()

  def test_retrieve_zillow_list_filter_by_state(self):
    zillow_id1, row1 = generate_test_data()
    zillow_id2, row2 = generate_test_data()
    zillow_id3, row3 = generate_test_data()
    zillow1 = Zillow.objects.get(zillow_id=zillow_id1)
    zillow2 = Zillow.objects.get(zillow_id=zillow_id2)
    zillow3 = Zillow.objects.get(zillow_id=zillow_id3)

    zillow1.state = "ON"
    zillow1.save()
    zillow2.state = "BC"
    zillow2.save()
    zillow3.state = "CA"
    zillow3.save()

    res = self.client.get(ZILLOW_URL, {"states": "ON,BC"})

    serializer1 = ZillowDetailSerializer(zillow1)
    serializer2 = ZillowDetailSerializer(zillow2)
    serializer3 = ZillowDetailSerializer(zillow3)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn(serializer1.data, res.data['results'])
    self.assertIn(serializer2.data, res.data['results'])
    self.assertNotIn(serializer3.data, res.data['results'])

    zillow1.delete()
    zillow2.delete()
    zillow3.delete()
