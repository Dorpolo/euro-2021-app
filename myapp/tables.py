import django_tables2 as tables
from .models import LeagueMember


class PredictionTable(tables.Table):
    class Meta:
        model = LeagueMember
        template_name = "django_tables2/bootstrap.html"
        fields = ("user_name_id", "first_name", "last_name", "league_name_id")
