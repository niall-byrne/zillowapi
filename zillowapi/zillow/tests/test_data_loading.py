from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from ..management import commands


class CommandTests(TestCase):

  @patch(commands.__name__ + '.load_csv.Zillow.objects.import_csv')
  def test_data_loading(self, m_import):
    """Test waiting for db when db is available."""

    capture = StringIO()

    args = ['somefile']
    options = {'stdout': capture}
    call_command("load_csv", *args, **options)
    self.assertEqual(m_import.call_count, 1)
    m_import.assert_called_once_with(args[0])
