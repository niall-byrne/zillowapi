from rest_framework import viewsets

from .models import Zillow
from .serializers import ZillowDetailSerializer


class ZillowView(viewsets.ModelViewSet):
  serializer_class = ZillowDetailSerializer
  queryset = Zillow.objects.all()
  authentication_classes = ()
  permission_classes = ()

  def _params_to_ints(self, qs):
    """Convert a list of strings IDs to a list of integers

    :param qs: The query string value to convert.
    :returns: A list of converted integers
    """
    values = []
    for str_id in qs.split(","):
      values.append(int(str_id))
    return values

  def get_queryset(self):
    """Returns the selected query objects, or all by default.
    You may filter by:
        - zillow_ids
        - cities
        - states

    :returns: The filtered query set of Zillow objects.
    """
    zillow_ids = self.request.query_params.get("zillow_ids")
    cities = self.request.query_params.get("cities")
    states = self.request.query_params.get("states")
    queryset = self.queryset
    if zillow_ids:
      selection = self._params_to_ints(zillow_ids)
      queryset = queryset.filter(zillow_id__in=selection)
    # If I had more time, I'd normalize the data on save to be all lowercase
    # And avoid this regex
    if cities:
      selection = cities.split(',')
      regex = r'(' + '|'.join(selection) + ')'
      queryset = queryset.filter(city__iregex=regex)
    if states:
      selection = states.split(',')
      regex = r'(' + '|'.join(selection) + ')'
      queryset = queryset.filter(state__iregex=regex)

    return queryset.order_by("id")

  def perform_create(self, serializer):
    """Creates a new Zillow instance in the database.

    :param serializer:  The django serializer object to use.
    """
    serializer.save()
