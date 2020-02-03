import datetime
import math
from decimal import Decimal

import numpy as np
import pandas as pd
from django.db import models

AREA_TYPES = (
    ('SqFt', 'SqFt'),
    ('SqMeters', 'SqMeters'),
)

HOME_TYPES = (
    ('Apartment', 'Apartment'),
    ('Duplex', 'Duplex'),
    ('Condominium', 'Condominium'),
    ('MultiFamily2To4', 'MultiFamily2To4'),
    ('SingleFamily', 'SingleFamily'),
    ('VacantResidentialLand', 'VacantResidentialLand'),
)

YEARS = [
    (year, year) for year in range(datetime.datetime.now().year + 2, 1900, -1)
]
DEFAULT_YEAR = datetime.datetime.now().year
TWOPLACES = Decimal(10)**-2


class ZillowManager(models.Manager):

  convert_to_date = [
      'last_sold_date', 'rentzestimate_last_updated', 'zestimate_last_updated'
  ]
  convert_to_currency = ['price']

  def _nan(self, price):
    if isinstance(price, str):
      return price
    if math.isnan(price):
      return 0
    else:
      return price

  def _currency(self, price):
    """Converts a currency column into standard Decimal format.

    :param price: A string or numeric value to concert.
    :returns: The original value, if the input is numeric, or the converted
              value if the input was a string.
    """
    if not isinstance(price, str):
      return price
    price = price.replace("$", "")
    if "M" in price:
      price = price.upper().replace("M", "")
      price = Decimal(price) * Decimal(1000000.0)
    elif "K" in price:
      price = price.upper().replace("K", "")
      price = Decimal(price) * Decimal(1000.0)
    return Decimal(price).quantize(TWOPLACES)

  def import_csv(self, fname):
    """Imports a CSV file into the database.

    :param fname: A string containing the filename to import.
    """

    df = pd.read_csv(fname)

    for field in df.columns:
      if field in self.__class__.convert_to_date:
        df[field] = df[field].astype('datetime64[s]')
        df[field] = df[field].astype(object).where(df[field].notnull(), None)
      elif field in self.__class__.convert_to_currency:
        df[field] = df[field].apply(lambda value: self._nan(value))
        df[field] = df[field].apply(lambda value: self._currency(value))
      else:
        if df[field].dtype == np.float64:
          df[field] = df[field].fillna(0)

    Zillow.objects.bulk_create(
        Zillow(**vals) for vals in df.to_dict('records'))


class Zillow(models.Model):
  """A Location from Zillow, the Zillow_id is the primary key."""
  area_unit = models.CharField(max_length=255, choices=AREA_TYPES)
  bathrooms = models.DecimalField(max_digits=4, decimal_places=1)
  bedrooms = models.DecimalField(max_digits=4, decimal_places=1)
  home_size = models.DecimalField(max_digits=10, decimal_places=2)
  home_type = models.CharField(max_length=255, choices=HOME_TYPES)
  last_sold_date = models.DateField(null=True)
  last_sold_price = models.DecimalField(max_digits=10, decimal_places=2)
  link = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  property_size = models.DecimalField(max_digits=10, decimal_places=2)
  rent_price = models.DecimalField(max_digits=10, decimal_places=2)
  rentzestimate_amount = models.DecimalField(max_digits=10, decimal_places=2)
  rentzestimate_last_updated = models.DateField(null=True)
  tax_value = models.DecimalField(max_digits=10, decimal_places=2)
  tax_year = models.IntegerField(default=DEFAULT_YEAR, choices=YEARS)
  year_built = models.IntegerField(choices=YEARS)
  zestimate_amount = models.DecimalField(max_digits=10, decimal_places=2)
  zestimate_last_updated = models.DateField(null=True)
  zillow_id = models.IntegerField(unique=True)
  address = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  state = models.CharField(max_length=255)
  zipcode = models.IntegerField()

  objects = ZillowManager()
