from django.core.management.base import BaseCommand

from ...models import Zillow


class Command(BaseCommand):
  """Django command that waits for database to be available"""

  def add_arguments(self, parser):
    parser.add_argument('csv_file', nargs='+', type=str)

  def handle(self, *args, **options):
    """Handle the command"""

    fname = options['csv_file'][0]
    self.stdout.write("Loading file: %s ..." % fname)
    Zillow.objects.import_csv(fname)
    self.stdout.write(self.style.SUCCESS("Successfully Loaded Data"))
