from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from pipelines.read_data import EuroApi
from data.teams import teams
from django.views.generic import ListView, DetailView, CreateView
from .models import Game
from .forms import PostForm


def user_data(request):
    context = {
        'fixtures': EuroApi().main()
    }
    template_name = "user_template.html"
    return render(request, template_name, context)


class AddPostView(CreateView):
    model = Game
    form_class = PostForm
    template_name = 'add_bets.html'


