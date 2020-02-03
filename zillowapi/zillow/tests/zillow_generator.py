"""Generates random test data."""

from decimal import Decimal
from io import StringIO

from django.db.models.fields import DateField, DecimalField
from faker import Faker

from ..models import Zillow

fake = Faker()

HEADERS = [
    'area_unit', 'bathrooms', 'bedrooms', 'home_size', 'home_type',
    'last_sold_date', 'last_sold_price', 'link', 'price', 'property_size',
    'rent_price', 'rentzestimate_amount', 'rentzestimate_last_updated',
    'tax_value', 'tax_year', 'year_built', 'zestimate_amount',
    'zestimate_last_updated', 'zillow_id', 'address', 'city', 'state',
    'zipcode'
]
COERCE_TO_INT = ['tax_year', 'year_built', 'zillow_id', 'zipcode']
TWOPLACES = Decimal(10)**-2


def generate_test_data():
  """Creates a database entry, and returns the new Zillow ID.

  :returns: A tuple: zillow_id, the csv row as a list of elements.
  """
  headers = ','.join(HEADERS) + '\n'
  elements, row = csv_row()
  virtual_file = StringIO(headers + row)
  Zillow.objects.import_csv(virtual_file)

  return elements[18], row


def csv_row():
  """Creates a CSV file row, using generated values.

  :returns:  A tuple of a list of elements, and a string containing the csv row
  """

  row = list()
  row.append("SqFt")
  row.append(fake.pyfloat(left_digits=2, right_digits=1, positive=True))
  row.append(fake.pyfloat(left_digits=2, right_digits=1, positive=True))
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.first_name_male())
  row.append(fake.date(pattern='%m/%d/%Y', end_datetime=None))
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.first_name_male())
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.date(pattern='%m/%d/%Y', end_datetime=None))
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.year())
  row.append(fake.year())
  row.append(fake.pyfloat(left_digits=8, right_digits=2, positive=True))
  row.append(fake.date(pattern='%m/%d/%Y', end_datetime=None))
  row.append(fake.postcode())
  row.append(fake.street_address())
  row.append(fake.city())
  row.append(fake.state())
  row.append(fake.postcode())

  return row, ','.join([str(element) for element in row])


def check_csv_row(row, model_instance):
  """Checks a CSV row, and a model instance and tests they are equal"""

  for i, element in enumerate(row):
    if Zillow._meta.get_field(HEADERS[i]).__class__ == DecimalField:
      assert getattr(model_instance, HEADERS[i]).quantize(
          TWOPLACES) == Decimal(element).quantize(TWOPLACES)
    elif Zillow._meta.get_field(HEADERS[i]).__class__ == DateField:
      assert getattr(model_instance,
                     HEADERS[i]).strftime("%m-%d-%Y") == str(element).replace(
                         '/', '-')
    elif HEADERS[i] in COERCE_TO_INT:
      assert getattr(model_instance, HEADERS[i]) == int(element)
    else:
      assert getattr(model_instance, HEADERS[i]) == element
