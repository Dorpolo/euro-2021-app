from django.shortcuts import render, redirect
from django.core.mail import send_mail
from pipelines.data_prep import *
from django.views.generic import CreateView, UpdateView, TemplateView
from .forms import *
from .models import *
from data.teams import team_game_map
from data.knockout import KNOCK_OUT_LOGOS
from django.urls import reverse
from .filters import *
from django.shortcuts import render
from django.conf import settings
import environ
import os

env = environ.Env(SECRET_KEY=str, )
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))
SECRET_KEY = env('DJANGO_SECRET_KEY')


class HomeView(TemplateView):
    template_name = "home.html"
    GetAPIData = GetMatchData()

    def get(self, request):
        if request.user.is_authenticated:
            UserPred = UserPredictionBase(request.user.id)
            home_page_context = self.GetAPIData.game_router()
            onboarding = BaseViewUserControl(request.user.id).onboarding()
            league_data_output = UserPred.get_league_members()
            if league_data_output is not None:
                context = {
                    'league_members': league_data_output,
                    'prev_match_logos': home_page_context['prev']['logo'],
                    'next_match_logos': home_page_context['next']['logo'],
                    'league_signup': onboarding['league'],
                    'committed_a_bet': onboarding['bet'],
                    'image_uploaded': onboarding['image'],
                    'committed_a_bet_16': onboarding['bet_top_16'],
                    'committed_a_bet_8': onboarding['bet_top_8'],
                    'committed_a_bet_4': onboarding['bet_top_4'],
                    'committed_a_bet_2': onboarding['bet_top_2'],
                    'bet_id': UserPred.user_game_bet_id('group'),
                    'bet_id_knockout': UserPred.user_game_bet_id('top_16'),
                    'games_started': home_page_context['started_games'],
                    'is_cup_user': UserPred.is_cup_user(),
                    'show_results': False
                }
                if onboarding['bet']:
                    presented_data = UserPred.home_screen_match_relevant_data(home_page_context)
                    context['user_game_points'] = presented_data[2]
                    context['next_match'] = presented_data[1]
                    context['prev_match'] = presented_data[0]
                    context['league_member_points'] = UserPred.league_member_points()
                    context['league_memberships'] = UserPred.get_league_members_data()
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name, {'data': None})
        else:
            return render(request, self.template_name, {'data': None})


class CupView(TemplateView):
    template_name = "the_cup.html"
    GetAPIData = GetMatchData()

    def get(self, request):
        if request.user.is_authenticated:
            UserPred = UserPredictionBase(request.user.id)
            league_data_output = UserPred.get_league_members()
            onboarding = BaseViewUserControl(request.user.id).onboarding()
            qualification_1_data = UserPred.league_member_points_cup('qualification_1')
            relevant_key = [item for item in qualification_1_data.keys()
                            if 'Conference' in item or 'Beta Coffee' in item][0]
            qualification_1 = qualification_1_data[relevant_key]
            qualification_1_df = pd.DataFrame(qualification_1[0:15])
            qualification_1_images_df = pd.DataFrame(league_data_output[relevant_key])
            images_qualification_1 = list(
                pd.merge(qualification_1_df, qualification_1_images_df, on=[0], how='inner')['1_y'])
            qualification_1_losers_df = pd.DataFrame(qualification_1[1:])
            qualification_2_nick_names = list(qualification_1_losers_df[0])
            qualification_2_data = {key: [item for item in val if item[0] in qualification_2_nick_names]
                                    for key, val in UserPred.league_member_points_cup('qualification_2').items()
                                    if key in relevant_key}
            qualification_2 = qualification_2_data[relevant_key]
            qualification_2_df = pd.DataFrame(qualification_2)
            images_qualification_2 = list(
                pd.merge(qualification_2_df, qualification_1_images_df, on=[0], how='inner')['1_y'])

            if league_data_output is not None:
                match_router = self.GetAPIData.game_router()
                context = {
                    'is_cup_user': UserPred.is_cup_user(),
                    'qualification_1_points': qualification_1_data,
                    'qualification_1_images': images_qualification_1,
                    'qualification_2_points': qualification_2_data,
                    'qualification_2_images': images_qualification_2,
                    'top_16_points': UserPred.league_member_points_cup('1/8 Final'),
                    'top_8_points': UserPred.league_member_points_cup('1/4 Final'),
                    'top_4_points': UserPred.league_member_points_cup('1/2 Final'),
                    'top_2_points': UserPred.league_member_points_cup('Final'),
                    'league_members': league_data_output,
                    'prev_match_logos': match_router['prev']['logo'],
                    'next_match_logos': match_router['next']['logo'],
                    'league_signup': onboarding['league'],
                    'committed_a_bet': onboarding['bet'],
                    'image_uploaded': onboarding['image'],
                    'committed_a_bet_16': onboarding['bet_top_16'],
                    'committed_a_bet_8': onboarding['bet_top_8'],
                    'committed_a_bet_4': onboarding['bet_top_4'],
                    'committed_a_bet_2': onboarding['bet_top_2'],
                    'bet_id': UserPred.user_game_bet_id('group'),
                    'league_member_points': UserPred.league_member_points(),
                    'league_memberships': UserPred.get_league_members_data(),
                }
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name, {'data': None})
        else:
            return render(request, self.template_name, {'data': None})


class TermsView(TemplateView):
    template_name = "terms.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class BaseView(TemplateView):
    template_name = "base.html"

    def get(self, request):
        onboarding = BaseViewUserControl(request.user.id).onboarding()
        UserPred = UserPredictionBase(request.user.id)
        context = {
            'league_signup': onboarding['league'],
            'committed_a_bet': onboarding['bet'],
            'committed_a_bet_16': onboarding['bet_top_16'],
            'committed_a_bet_8': onboarding['bet_top_8'],
            'committed_a_bet_4': onboarding['bet_top_4'],
            'committed_a_bet_2': onboarding['bet_top_2'],
            'is_cup_user': UserPred.is_cup_user(),
        }
        return render(request, self.template_name, context)


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
                top_assist_3=form.cleaned_data['top_assist_3'], )
            obj.save()
            try:
                league_user_email = [LeagueMember.objects.filter(user_name_id=request.user.id)[0].email]
                if league_user_email[0] != env('EMAIL_HOST_USER'):
                    league_user_email.append(env('EMAIL_HOST_USER'))
                email_data = MailTemplate().group_stage_bet_submission(request, form)
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


class AddBetsTop16View(TemplateView):
    template_name = "add_bets_top_16.html"

    def get(self, request):
        form = BetFormTop16()
        context = {
            'form': form,
            'logos': KNOCK_OUT_LOGOS['1/8 Final']
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BetFormTop16(request.POST)
        if form.is_valid():
            obj = GameTop16(
                user_name=form.cleaned_data['user_name'],
                gid_a0_0=form.cleaned_data['gid_a0_0'],
                gid_a0_1=form.cleaned_data['gid_a0_1'],
                gid_a0_w=form.cleaned_data['gid_a0_w'],
                # gid_a0_alt=form.cleaned_data['gid_a0_alt'],
                gid_a1_0=form.cleaned_data['gid_a1_0'],
                gid_a1_1=form.cleaned_data['gid_a1_1'],
                gid_a1_w=form.cleaned_data['gid_a1_w'],
                # gid_a1_alt=form.cleaned_data['gid_a1_alt'],
                gid_a2_0=form.cleaned_data['gid_a2_0'],
                gid_a2_1=form.cleaned_data['gid_a2_1'],
                gid_a2_w=form.cleaned_data['gid_a2_w'],
                # gid_a2_alt=form.cleaned_data['gid_a2_alt'],
                gid_a3_0=form.cleaned_data['gid_a3_0'],
                gid_a3_1=form.cleaned_data['gid_a3_1'],
                gid_a3_w=form.cleaned_data['gid_a3_w'],
                # gid_a3_alt=form.cleaned_data['gid_a3_alt'],
                gid_a4_0=form.cleaned_data['gid_a4_0'],
                gid_a4_1=form.cleaned_data['gid_a4_1'],
                gid_a4_w=form.cleaned_data['gid_a4_w'],
                # gid_a4_alt=form.cleaned_data['gid_a4_alt'],
                gid_a5_0=form.cleaned_data['gid_a5_0'],
                gid_a5_1=form.cleaned_data['gid_a5_1'],
                gid_a5_w=form.cleaned_data['gid_a5_w'],
                # gid_a5_alt=form.cleaned_data['gid_a5_alt'],
                gid_a6_0=form.cleaned_data['gid_a6_0'],
                gid_a6_1=form.cleaned_data['gid_a6_1'],
                gid_a6_w=form.cleaned_data['gid_a6_w'],
                # gid_a6_alt=form.cleaned_data['gid_a6_alt'],
                gid_a7_0=form.cleaned_data['gid_a7_0'],
                gid_a7_1=form.cleaned_data['gid_a7_1'],
                gid_a7_w=form.cleaned_data['gid_a7_w'],
                # gid_a7_alt=form.cleaned_data['gid_a7_alt'],
            )
            obj.save()
            try:
                league_user_email = [LeagueMember.objects.filter(user_name_id=request.user.id)[0].email]
                if league_user_email[0] != env('EMAIL_HOST_USER'):
                    league_user_email.append(env('EMAIL_HOST_USER'))
                email_data = MailTemplate().knockout_bet_submission(request, form, stage='1/16 Final')
                print(email_data)
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


class AddBetsTop8View(TemplateView):
    template_name = "add_bets_top_8.html"

    def get(self, request):
        form = BetFormTop8()
        context = {
            'form': form,
            'logos': KNOCK_OUT_LOGOS_BETA['1/4 Final']
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BetFormTop8(request.POST)
        if form.is_valid():
            obj = GameTop8(
                user_name=form.cleaned_data['user_name'],
                gid_a0_0=form.cleaned_data['gid_a0_0'],
                gid_a0_1=form.cleaned_data['gid_a0_1'],
                gid_a0_w=form.cleaned_data['gid_a0_w'],
                # gid_a0_alt=form.cleaned_data['gid_a0_alt'],
                gid_a1_0=form.cleaned_data['gid_a1_0'],
                gid_a1_1=form.cleaned_data['gid_a1_1'],
                gid_a1_w=form.cleaned_data['gid_a1_w'],
                # gid_a1_alt=form.cleaned_data['gid_a1_alt'],
                gid_a2_0=form.cleaned_data['gid_a2_0'],
                gid_a2_1=form.cleaned_data['gid_a2_1'],
                gid_a2_w=form.cleaned_data['gid_a2_w'],
                # gid_a2_alt=form.cleaned_data['gid_a2_alt'],
                gid_a3_0=form.cleaned_data['gid_a3_0'],
                gid_a3_1=form.cleaned_data['gid_a3_1'],
                gid_a3_w=form.cleaned_data['gid_a3_w'],
                # gid_a3_alt=form.cleaned_data['gid_a3_alt'],
            )
            obj.save()
            try:
                league_user_email = [LeagueMember.objects.filter(user_name_id=request.user.id)[0].email]
                if league_user_email[0] != env('EMAIL_HOST_USER'):
                    league_user_email.append(env('EMAIL_HOST_USER'))
                email_data = MailTemplate().knockout_bet_submission(request, form, '1/8 Final')
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


class AddBetsTop4View(TemplateView):
    template_name = "add_bets_top_4.html"

    def get(self, request):
        form = BetFormTop4()
        context = {
            'form': form,
            'logos': KNOCK_OUT_LOGOS_BETA['1/2 Final']
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BetFormTop4(request.POST)
        if form.is_valid():
            obj = GameTop4(
                user_name=form.cleaned_data['user_name'],
                gid_a0_0=form.cleaned_data['gid_a0_0'],
                gid_a0_1=form.cleaned_data['gid_a0_1'],
                gid_a0_w=form.cleaned_data['gid_a0_w'],
                # gid_a0_alt=form.cleaned_data['gid_a0_alt'],
                gid_a1_0=form.cleaned_data['gid_a1_0'],
                gid_a1_1=form.cleaned_data['gid_a1_1'],
                gid_a1_w=form.cleaned_data['gid_a1_w'],
                # gid_a1_alt=form.cleaned_data['gid_a1_alt'],
            )
            obj.save()
            try:
                league_user_email = [LeagueMember.objects.filter(user_name_id=request.user.id)[0].email]
                if league_user_email[0] != env('EMAIL_HOST_USER'):
                    league_user_email.append(env('EMAIL_HOST_USER'))
                email_data = MailTemplate().knockout_bet_submission(request, form, '1/2 Final')
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


class AddBetsTop2View(TemplateView):
    template_name = "add_bets_top_2.html"

    def get(self, request):
        form = BetFormTop2()
        context = {
            'form': form,
            'logos': KNOCK_OUT_LOGOS_BETA['Final']
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BetFormTop2(request.POST)
        if form.is_valid():
            obj = GameTop2(
                user_name=form.cleaned_data['user_name'],
                gid_a0_0=form.cleaned_data['gid_a0_0'],
                gid_a0_1=form.cleaned_data['gid_a0_1'],
                gid_a0_w=form.cleaned_data['gid_a0_w'],
                # gid_a0_alt=form.cleaned_data['gid_a0_alt'],
            )
            obj.save()
            try:
                league_user_email = [LeagueMember.objects.filter(user_name_id=request.user.id)[0].email]
                if league_user_email[0] != env('EMAIL_HOST_USER'):
                    league_user_email.append(env('EMAIL_HOST_USER'))
                email_data = MailTemplate().knockout_bet_submission(request, form, 'Final')
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


class CupBracket(TemplateView):
    template_name = 'cup_bracket.html'

    def get(self, request):
        context = {'data': None}
        return render(request, self.template_name, context)


class UpdateBetViewThirdRound(UpdateView):
    model = Game
    form_class = BetFormUpdate3Round
    template_name = 'update_bets_third_round.html'


class UpdateBetViewTop16(UpdateView):
    model = GameTop16
    form_class = BetFormTop16
    template_name = 'update_bets_top_16.html'



class UpdateBetViewTop8(UpdateView):
    model = GameTop8
    form_class = BetFormTop8
    template_name = 'update_bets_top_8.html'


class UpdateBetViewTop4(UpdateView):
    model = GameTop4
    form_class = BetFormTop4
    template_name = 'update_bets_top_4.html'


class UpdateBetViewTop2(UpdateView):
    model = GameTop2
    form_class = BetFormTop2
    template_name = 'update_bets_top_2.html'


class UpdateLeagueMember(UpdateView):
    model = LeagueMember
    form_class = LeagueMemberForm
    template_name = 'update_league_member.html'


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
            league_user_email = LeagueMember.objects.filter(user_name_id=request.user.id)[0].email
            email_data = MailTemplate().user_joined_a_league(request, form)
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


class AllPredictionsView(TemplateView):
    template_name = "score_predictions.html"

    def get(self, request):
        if request.user.is_authenticated:
            UserPrediction = UserPredictionBase(request.user.id)
            get_league_data = UserPrediction.present_predictions()
            league_data_output = get_league_data[0]
            league_table_output = UserPrediction.league_member_points()
        else:
            league_data_output = None
        onboarding = BaseViewUserControl(request.user.id).onboarding()
        context = {
            'league_members': league_data_output,
            'league_signup': onboarding['league'],
            'committed_a_bet': onboarding['bet'],
            'image_uploaded': onboarding['image'],
            'committed_a_bet_16': onboarding['bet_top_16'],
            'committed_a_bet_8': onboarding['bet_top_8'],
            'committed_a_bet_4': onboarding['bet_top_4'],
            'committed_a_bet_2': onboarding['bet_top_2'],
            'league_member_points': league_table_output
        }
        return render(request, self.template_name, context)


class MyPredictionsView(TemplateView):
    template_name = "my_predictions.html"

    def get(self, request):
        if request.user.is_authenticated:
            UserPred = UserPredictionBase(request.user.id)
            get_my_predictions = UserPred.present_my_predictions()
            get_my_players = UserPred.get_top_players_my_predictions()
        else:
            get_my_predictions = None
        context = {
            'my_predictions': get_my_predictions[0],
            'my_players': get_my_players
        }
        return render(request, self.template_name, context)


class LeagueTableView(TemplateView):
    template_name = "league_table.html"

    def get(self, request):
        if request.user.is_authenticated:
            class_init = UserPredictionBase(request.user.id)
            get_league_data = class_init.present_predictions()
            league_data_output = get_league_data[0]
            league_table_output = class_init.league_member_points()
        else:
            league_data_output = None
        onboarding = BaseViewUserControl(request.user.id).onboarding()
        context = {
            'league_members': league_data_output,
            'league_signup': onboarding['league'],
            'committed_a_bet': onboarding['bet'],
            'image_uploaded': onboarding['image'],
            'committed_a_bet_16': onboarding['bet_top_16'],
            'committed_a_bet_8': onboarding['bet_top_8'],
            'committed_a_bet_4': onboarding['bet_top_4'],
            'committed_a_bet_2': onboarding['bet_top_2'],
            'league_member_points': league_table_output
        }
        return render(request, self.template_name, context)


class LiveGameView:
    def next(request):
        is_next = True
        match_router = GetMatchData().game_router()
        match = match_router['next']['data'] if is_next else match_router['prev']['data']
        status = match['match_status']
        onboarding = BaseViewUserControl(request.user.id).onboarding()
        if onboarding['bet']:
            LiveOutput = TopPlayerStats(request.user.id).live_game_plot(match_label=match['match_label'])
        else:
            LiveOutput = [None, None]
        context = {
            'title': match['match_label'],
            'real_score': f"{match['home_team_score']}-{match['away_team_score']}",
            'status': 'Fixture' if status == '0' else 'Started' if status == '-1' else 'Finished',
            'plots': LiveOutput[0],
            'logos': match_router['next']['logo'] if is_next else match_router['prev']['logo'],
            'entitled_users': LiveOutput[1],
            'committed_a_bet': onboarding['bet'],
        }
        template_name = f"stats_live_game_{'next' if is_next else 'prev'}.html"
        return render(request, template_name, context)

    def prev(request):
        is_next = False
        match_router = GetMatchData().game_router()
        match = match_router['next']['data'] if is_next else match_router['prev']['data']
        status = match['match_status']
        onboarding = BaseViewUserControl(request.user.id).onboarding()
        if onboarding['bet']:
            LiveOutput = TopPlayerStats(request.user.id).live_game_plot(match_label=match['match_label'])
        context = {
            'title': match['match_label'],
            'real_score': f"{match['home_team_score']}-{match['away_team_score']}",
            'status': 'Fixture' if status == '0' else 'Started' if status == '-1' else 'Finished',
            'plots': LiveOutput[0],
            'logos': match_router['next']['logo'] if is_next else match_router['prev']['logo'],
            'entitled_users': LiveOutput[1],
            'committed_a_bet': onboarding['bet'],
        }
        template_name = f"stats_live_game_{'next' if is_next else 'prev'}.html"
        return render(request, template_name, context)


class GameStatsView:
    def next(request):
        is_next = True
        match_router = GetMatchData().game_router()
        match = match_router['next']['data'] if is_next else match_router['prev']['data']
        status = match['match_status']
        Plot = GameStats(request.user.id, match['match_label'])
        viz = Plot.match_prediction_outputs()
        context = {
            'plot_next_match': viz,
            'title': match['match_label'],
            'real_score': f"{match['home_team_score']}-{match['away_team_score']}",
            'logos': match_router['next']['logo'] if is_next else match_router['prev']['logo'],
            'status': 'Fixture' if status == '0' else 'Started' if status == '-1' else 'Finished',
        }
        template = 'stats_next_game.html' if is_next else 'stats_prev_game.html'
        return render(request, template, context)

    def prev(request):
        is_next = False
        match_router = GetMatchData().game_router()
        match = match_router['next']['data'] if is_next else match_router['prev']['data']
        status = match['match_status']
        Plot = GameStats(request.user.id, match.match_label[0])
        viz = Plot.match_prediction_outputs()
        context = {
            'plot_next_match': viz,
            'title': match['match_label'],
            'real_score': f"{match['home_team_score']}-{match['away_team_score']}",
            'logos': match_router['next']['logo'] if is_next else match_router['prev']['logo'],
            'status': 'Fixture' if status == '0' else 'Started' if status == '-1' else 'Finished',
        }
        template = 'stats_next_game.html' if is_next else 'stats_prev_game.html'
        return render(request, template, context)


def plot_top_players(request):
    DataClass = TopPlayerStats(request.user.id)
    top_players_real = {key: val[0:10] for key, val in
                        DataClass.top_players_real()[0].items()}
    started_games = DataClass.started_games()
    predicted_plots = DataClass.top_players_pred_plot()
    context = {
        'top_players': top_players_real,
        'games_started': started_games,
        'plots': predicted_plots
    }
    return render(request, "stats_top_players.html", context)
