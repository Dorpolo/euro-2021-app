from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse


def user_data(request):
    context = {
        "first_name": "Anjaneyulu",
        "last_name": "Batta",
        "address": "Hyderabad, India"
    }
    template_name = "user_template.html"
    return render(request, template_name, context)




