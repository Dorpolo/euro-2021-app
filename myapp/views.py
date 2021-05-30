from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from pipelines.read_data import EuroApi
from pipelines.data_prep import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from .models import Game, League, LeagueUser, Post
from .forms import BetForm, LeagueForm, UserForm, PostForm
from data.teams import team_game_map
import json


class HomeView(TemplateView):
    template_name = "home.html"
    get_api_data = EuroApi()

    def get(self, request):
        if request.user.is_authenticated:
            league_name_id = extract_user_league_name_id(request.user.id)
            league_users = LeagueUser.objects.filter(league_name_id=league_name_id)
        else:
            league_users = None
        context = {
            'league_users': league_users,
            'fixtures': self.get_api_data.main(),
            'teams': self.get_api_data.get_unique_teams(),
        }
        return render(request, self.template_name, context)


def bet_index(request):
    form = BetForm()
    template_name = 'add_bets.html'
    context = {
        'form': form,
        'fixtures': EuroApi().main()
    }
    return render(request, template_name, context)


class AddBetsView(TemplateView):
    template_name = "add_bets.html"

    def get(self, request):
        form = BetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BetForm(request.POST)
        if form.is_valid():
            obj = Game(
                    user_name=request.user,
                    gid_8222_0=form.cleaned_data['gid_8222_0'],
                    gid_8222_1=form.cleaned_data['gid_8222_1'],
                    gid_8198_0=form.cleaned_data['gid_8198_0'],
                    gid_8198_1=form.cleaned_data['gid_8198_1'],
                    gid_8206_0=form.cleaned_data['gid_8206_0'],
                    gid_8206_1=form.cleaned_data['gid_8206_1'],
                    gid_8207_0=form.cleaned_data['gid_8207_0'],
                    gid_8207_1=form.cleaned_data['gid_8207_1'],
                    gid_8213_0=form.cleaned_data['gid_8213_0'],
                    gid_8213_1=form.cleaned_data['gid_8213_1'],
                    gid_8214_0=form.cleaned_data['gid_8214_0'],
                    gid_8214_1=form.cleaned_data['gid_8214_1'],
                    gid_8199_0=form.cleaned_data['gid_8199_0'],
                    gid_8199_1=form.cleaned_data['gid_8199_1'],
                    gid_8200_0=form.cleaned_data['gid_8200_0'],
                    gid_8200_1=form.cleaned_data['gid_8200_1'],
                    gid_8205_0=form.cleaned_data['gid_8205_0'],
                    gid_8205_1=form.cleaned_data['gid_8205_1'],
                    gid_8208_0=form.cleaned_data['gid_8208_0'],
                    gid_8208_1=form.cleaned_data['gid_8208_1'],
                    gid_8216_0=form.cleaned_data['gid_8216_0'],
                    gid_8216_1=form.cleaned_data['gid_8216_1'],
                    gid_8217_0=form.cleaned_data['gid_8217_0'],
                    gid_8217_1=form.cleaned_data['gid_8217_1'],
                    gid_19950_0=form.cleaned_data['gid_19950_0'],
                    gid_19950_1=form.cleaned_data['gid_19950_1'],
                    gid_8202_0=form.cleaned_data['gid_8202_0'],
                    gid_8202_1=form.cleaned_data['gid_8202_1'],
                    gid_19953_0=form.cleaned_data['gid_19953_0'],
                    gid_19953_1=form.cleaned_data['gid_19953_1'],
                    gid_8209_0=form.cleaned_data['gid_8209_0'],
                    gid_8209_1=form.cleaned_data['gid_8209_1'],
                    gid_19957_0=form.cleaned_data['gid_19957_0'],
                    gid_19957_1=form.cleaned_data['gid_19957_1'],
                    gid_8215_0=form.cleaned_data['gid_8215_0'],
                    gid_8215_1=form.cleaned_data['gid_8215_1'],
                    gid_8201_0=form.cleaned_data['gid_8201_0'],
                    gid_8201_1=form.cleaned_data['gid_8201_1'],
                    gid_19951_0=form.cleaned_data['gid_19951_0'],
                    gid_19951_1=form.cleaned_data['gid_19951_1'],
                    gid_8210_0=form.cleaned_data['gid_8210_0'],
                    gid_8210_1=form.cleaned_data['gid_8210_1'],
                    gid_19955_0=form.cleaned_data['gid_19955_0'],
                    gid_19955_1=form.cleaned_data['gid_19955_1'],
                    gid_19958_0=form.cleaned_data['gid_19958_0'],
                    gid_19958_1=form.cleaned_data['gid_19958_1'],
                    gid_8218_0=form.cleaned_data['gid_8218_0'],
                    gid_8218_1=form.cleaned_data['gid_8218_1'],
                    gid_19952_0=form.cleaned_data['gid_19952_0'],
                    gid_19952_1=form.cleaned_data['gid_19952_1'],
                    gid_8203_0=form.cleaned_data['gid_8203_0'],
                    gid_8203_1=form.cleaned_data['gid_8203_1'],
                    gid_19954_0=form.cleaned_data['gid_19954_0'],
                    gid_19954_1=form.cleaned_data['gid_19954_1'],
                    gid_8212_0=form.cleaned_data['gid_8212_0'],
                    gid_8212_1=form.cleaned_data['gid_8212_1'],
                    gid_19959_0=form.cleaned_data['gid_19959_0'],
                    gid_19959_1=form.cleaned_data['gid_19959_1'],
                    gid_8219_0=form.cleaned_data['gid_8219_0'],
                    gid_8219_1=form.cleaned_data['gid_8219_1'],
                    gid_19949_0=form.cleaned_data['gid_19949_0'],
                    gid_19949_1=form.cleaned_data['gid_19949_1'],
                    gid_8204_0=form.cleaned_data['gid_8204_0'],
                    gid_8204_1=form.cleaned_data['gid_8204_1'],
                    gid_19956_0=form.cleaned_data['gid_19956_0'],
                    gid_19956_1=form.cleaned_data['gid_19956_1'],
                    gid_8211_0=form.cleaned_data['gid_8211_0'],
                    gid_8211_1=form.cleaned_data['gid_8211_1'],
                    gid_19960_0=form.cleaned_data['gid_19960_0'],
                    gid_19960_1=form.cleaned_data['gid_19960_1'],
                    gid_8220_0=form.cleaned_data['gid_8220_0'],
                    gid_8220_1=form.cleaned_data['gid_8220_1'],)
            obj.save()
            try:
                league_user_email = [get_league_user_email(request.user.id)]
                if league_user_email[0] != 'dorpolo@gmail.com':
                    league_user_email.append('dorpolo@gmail.com')
                email_data = prepare_bet_submission_email(request, form)
                send_mail(
                     subject=email_data[0],
                     message=email_data[1],
                     from_email='dorpolo@gmail.com',
                     to_email=[league_user_email],
                     fail_silently=False
                )
            except Exception as exc:
                print(exc)
            return redirect('home')
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class CreateLeagueView(CreateView):
    model = League
    form_class = LeagueForm
    template_name = 'add_league.html'


class UpdateBetView(UpdateView):
    model = Game
    form_class = BetForm
    template_name = 'update_bets.html'


class CreateUserView(CreateView):
    template_name = "add_user.html"

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            obj = LeagueUser(
                    user_name=request.user,
                    league_name=form.cleaned_data['league_name'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],)
            obj.save()
            email_data = prepare_league_user_email(request, form)
            try:
               send_mail(
                     subject=email_data[0],
                     message=email_data[1],
                     from_email='dorpolo@gmail.com',
                     to_email=['dorpolo@gmail.com'],
                     fail_silently=False)
            except Exception as exc:
                print(exc)
            return redirect('home')
        else:
            form = UserForm()
            print("Not Valid!")
            print(form.errors)

        return render(request, self.template_name, {'form': form})


class TestView(TemplateView):
    template_name = "test.html"

    def get(self, request):
        form = PostForm()
        get_api_data = ['Dor', 'Polo']
        return render(request, self.template_name, {'form': form, 'data': get_api_data})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            print(text)
            form = PostForm()
            obj1 = Post(text='Hello World', author=request.user)
            obj1.save()
            return redirect('home')
        else:
            print("Not Valid!")
            print(form.errors)

        return render(request, self.template_name, {'form': form})
