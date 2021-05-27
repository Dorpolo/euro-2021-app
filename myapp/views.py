from django.shortcuts import render
from django.http import HttpResponse
from pipelines.read_data import EuroApi
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from .models import Game, League, LeagueUser
from .forms import BetForm, LeagueForm, UserForm


class HomeView(TemplateView):
    template_name = "home.html"
    get_api_data = EuroApi()

    def get(self, request):
        league_users = LeagueUser.objects.all()
        context = {
            'league_users': league_users,
            'fixtures': self.get_api_data.main(),
            'teams': self.get_api_data.get_unique_teams()
        }
        return render(request, self.template_name, context)

# def user_data(request):
#     init = EuroApi()
#     context = {
#         'fixtures': init.main(),
#         'teams': init.get_unique_teams(),
#         'league_users': LeagueUser.objects.all()
#     }
#     template_name = 'home.html'
#     return render(request, template_name, context)


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
