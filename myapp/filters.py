import django_filters
from .models import *


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = CleanPredictions
        fields = {
            'league_name_id',
            'match_label',
            'user_full_name'
        }

