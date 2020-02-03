from decimal import Decimal
from io import StringIO

from django.test import TestCase

from ..models import Zillow
from .zillow_generator import HEADERS, check_csv_row, csv_row


class TestZillowManager(TestCase):

  def setUp(self):
    self.headers = ','.join(HEADERS) + '\n'

  def test_currency_k(self):
    row = "EasyToFind,,,,,,,,$739K,,,,,,,,,,,,"
    virtual_file = StringIO(self.headers + row)
    Zillow.objects.import_csv(virtual_file)

    q = Zillow.objects.get(area_unit="EasyToFind")
    self.assertEqual(q.price, Decimal(739000))

    q.delete()

  def test_currency_m(self):
    row = "EasyToFind,,,,,,,,$1.5M,,,,,,,,,,,,"
    virtual_file = StringIO(self.headers + row)
    Zillow.objects.import_csv(virtual_file)

    q = Zillow.objects.get(area_unit="EasyToFind")
    self.assertEqual(q.price, Decimal(1500000))

    q.delete()

  def test_currency_blank(self):
    row = "EasyToFind,,,,,,,,,,,,,,,,,,,,"
    virtual_file = StringIO(self.headers + row)
    Zillow.objects.import_csv(virtual_file)

    q = Zillow.objects.get(area_unit="EasyToFind")
    self.assertEqual(q.price, Decimal(0))

    q.delete()

  def test_currency_normal(self):
    row = "EasyToFind,,,,,,,,$1500000,,,,,,,,,,,,"
    virtual_file = StringIO(self.headers + row)
    Zillow.objects.import_csv(virtual_file)

    q = Zillow.objects.get(area_unit="EasyToFind")
    self.assertEqual(q.price, Decimal(1500000))

    q.delete()

  def test_currency_forgive_input_error(self):
    row = "EasyToFind,,,,,,,,1.5,,,,,,,,,,,,"
    virtual_file = StringIO(self.headers + row)
    Zillow.objects.import_csv(virtual_file)

    q = Zillow.objects.get(area_unit="EasyToFind")
    self.assertEqual(q.price, Decimal(1.50))

    q.delete()

  def test_load_manufactured_random_row_without_error(self):

    elements, row = csv_row()
    virtual_file = StringIO(self.headers + row)
    Zillow.objects.import_csv(virtual_file)

    q = Zillow.objects.get(area_unit="SqFt")
    check_csv_row(elements, q)
    q.delete()
