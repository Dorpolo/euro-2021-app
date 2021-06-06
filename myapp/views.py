from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from pipelines.data_prep import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from .forms import *
from .models import *
from data.teams import team_game_map
from django.urls import reverse
from django_tables2 import SingleTableView
from .tables import PredictionTable
from .filters import OrderFilter
from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.conf import settings
import environ
import os

env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))
SECRET_KEY = env('DJANGO_SECRET_KEY')


class HomeView(TemplateView):
    template_name = "home.html"
    get_api_data = EuroApi()

    def get(self, request):
        if request.user.is_authenticated:
            league_data_output = get_league_member_data(request.user.id)
        else:
            league_data_output = None
        onboarding = user_onboarding(request.user.id)
        bet_id = user_game_bet_id(request.user.id)
        context = {
            'league_members': league_data_output,
            'fixtures': self.get_api_data.main(),
            'teams': self.get_api_data.get_unique_teams(),
            'league_signup': onboarding['league'],
            'committed_a_bet': onboarding['bet'],
            'image_uploaded': onboarding['image'],
            'bet_id': bet_id
        }
        return render(request, self.template_name, context)


class TermsView(TemplateView):
    template_name = "terms.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class BaseView(TemplateView):
    template_name = "base.html"

    def get(self, request):
        onboarding = user_onboarding(request.user.id)
        context = {
            'league_signup': onboarding['league'],
            'committed_a_bet': onboarding['bet']
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
                    user_name=form.cleaned_data['user_name'],
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
                    gid_8220_1=form.cleaned_data['gid_8220_1'],
                    top_scorer_1=form.cleaned_data['top_scorer_1'],
                    top_scorer_2=form.cleaned_data['top_scorer_2'],
                    top_scorer_3=form.cleaned_data['top_scorer_3'],
                    top_assist_1=form.cleaned_data['top_assist_1'],
                    top_assist_2=form.cleaned_data['top_assist_2'],
                    top_assist_3=form.cleaned_data['top_assist_3'],)
            obj.save()
            try:
                league_user_email = [get_league_user_email(request.user.id)]
                if league_user_email[0] != env('EMAIL_HOST_USER'):
                    league_user_email.append(env('EMAIL_HOST_USER'))
                email_data = prepare_bet_submission_email(request, form)
                send_mail(
                     email_data['subject'],
                     email_data['message'],
                     env('EMAIL_HOST_USER'),
                     league_user_email,
                     fail_silently=False
                    )
                print(f"Email has been sent successfully to {', '.join(league_user_email)}")
            except Exception as exc:
                print(exc)
            return redirect('home')
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class UpdateBetView(UpdateView):
    model = Game
    form_class = BetForm
    template_name = 'update_bets.html'


class CreateLeagueMemberView(CreateView):
    template_name = "add_league_member.html"

    def get(self, request):
        form = LeagueMemberForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LeagueMemberForm(request.POST)
        if form.is_valid():
            obj = LeagueMember(
                    user_name=request.user,
                    league_name=form.cleaned_data['league_name'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    nick_name=form.cleaned_data['nick_name'],
                    email=form.cleaned_data['email'],
                )
            obj.save()
            league_user_email = get_league_user_email(request.user.id)
            email_data = prepare_league_user_email(request, form)
            recipient_list = [league_user_email, env('EMAIL_HOST_USER')]
            try:
               send_mail(
                 email_data['subject'],
                 email_data['message'],
                 env('EMAIL_HOST_USER'),
                 recipient_list,
                 fail_silently=False
                )
               print(f"Email has been sent successfully to {', '.join(recipient_list)}")
            except Exception as exc:
                print(exc)
            return redirect('home')
        else:
            form = LeagueMemberForm()
            print(form.errors)
        return render(request, self.template_name, {'form': form})


def predictions(request, pk):
    data = LeagueMember.objects.filter(user_name_id=pk)
    league = data[0].league_name_id
    bets = CleanPredictions.objects.filter(league_name_id=league)
    myFilter = OrderFilter(request.GET, queryset=bets)
    bets = myFilter.qs
    context = {
        'bets': bets,
        'myFilter': myFilter
    }
    return render(request, 'score_predictions.html', context)


def index(request):
    returns = np.random.normal(0.01, 0.2, 100)
    price = 100 * np.exp(returns.cumsum())
    time = np.arange(100)
    layout = go.Layout(
        title="Historic Prices",
        plot_bgcolor="#FFF",  # Sets background color to white
        xaxis=dict(
            title="time",
            linecolor="#BCCCDC",  # Sets color of X-axis line
            showgrid=False  # Removes X-axis grid lines
        ),
        yaxis=dict(
            title="price",
            linecolor="#BCCCDC",  # Sets color of Y-axis line
            showgrid=False,  # Removes Y-axis grid lines
        )
    )
    fig = go.Figure(
        data=go.Scatter(x=time, y=price),
        layout=layout
    )
    plt_div = plot(fig, output_type='div', include_plotlyjs=False)
    context = {'plot_div': plt_div}
    return render(request, "stats.html", context)


class UpdateBetView(UpdateView):
    model = Game
    form_class = BetForm
    template_name = 'update_bets.html'


class UserImageView(CreateView):
    model = UserImage
    form_class = UserImageForm
    template_name = 'add_user_image.html'


class CreateLeagueView(CreateView):
    model = League
    form_class = LeagueForm
    template_name = 'add_league.html'

