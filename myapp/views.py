from django.shortcuts import render
from django.http import HttpResponse
from pipelines.read_data import EuroApi
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Game, League, LeagueUser
from .forms import BetForm, LeagueForm, UserForm


def user_data(request):
    context = {
        'fixtures': EuroApi().main()
    }
    template_name = "user_template.html"
    return render(request, template_name, context)


def index(request):
    form = LeagueForm()
    template_name = 'add_league.html'
    context = {
        'form': form,
        'fixtures': EuroApi().main()
    }
    return render(request, template_name, context)


def bet_index(request):
    form = BetForm()
    template_name = 'add_bets.html'
    context = {
        'form': form,
        'fixtures': EuroApi().main()
    }
    return render(request, template_name, context)


class AddBetsView(CreateView):
    model = Game
    form_class = BetForm
    template_name = 'add_bets.html'


class CreateLeagueView(CreateView):
    model = League
    form_class = LeagueForm
    template_name = 'add_league.html'


class CreateUserView(CreateView):
    model = LeagueUser
    form_class = UserForm
    template_name = 'add_user.html'


class UpdateBetView(UpdateView):
    model = Game
    form_class = BetForm
    template_name = 'update_bets.html'
