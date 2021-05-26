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


def add_bet_from_submission(request):
    print("Hello, form is submitted!")
    template_name = 'add_bets.html'
    return render(request, template_name)


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
    template_name = 'update_bets.html'
    fields = '__all__'

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    context = {
            'form': form
        }
    return render(request, 'name.html', context)