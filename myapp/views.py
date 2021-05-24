from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from pipelines.read_data import EuroApi
from data.teams import teams


def user_data(request):
    context = {
        'fixtures': EuroApi().main(),
        'logos': [item['logo'] for item in teams.values()]
    }
    template_name = "user_template.html"
    return render(request, template_name, context)




